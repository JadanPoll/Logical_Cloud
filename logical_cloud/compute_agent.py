"""Operator-gated Compute agent adapter for the public Fire Inbox.

The public Inbox is *not* an execution service. A connected operator can
inspect requests, explicitly approve one task for a dedicated Codex
workspace, review the output, and post a short reply with GitHub refs.
Nothing is executed merely because a message appears in the Inbox.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

from .inbox_fabric import (
    SiteClient, AgentLedger, DEFAULT_DB, DEFAULT_SITE, ProtocolError,
    UnknownDelivery, SiteUnavailable, new_message
)

AGENT = "agent:compute"
MAX_PROMPT = 6000


def tasks(messages):
    return [m for m in messages if m.get("to") == AGENT and
            m.get("kind") == "request" and
            isinstance(m.get("text"), str) and
            0 < len(m["text"].strip()) <= MAX_PROMPT]


def locate(messages, task_id):
    return next((m for m in tasks(messages) if m["id"] == task_id), None)


def run_approved(task, approved_id, workspace, codex="codex"):
    if approved_id != task["id"]:
        raise ProtocolError("Approval must repeat the exact visible task ID")
    path = Path(workspace).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ProtocolError("Choose a dedicated existing workspace directory")
    binary = shutil.which(codex) if "/" not in codex else codex
    if not binary:
        raise ProtocolError("Codex CLI is not installed or on PATH")
    # Same narrow sandbox principle as fire/tools/codex_executor.py.
    # Only an operator who explicitly provided the target ID and workspace
    # can start a run. Avoid host credentials, generic shell and global CWD.
    args = [binary, "--ask-for-approval", "never", "exec", "--json",
            "--sandbox", "workspace-write", "--skip-git-repo-check", task["text"]]
    try:
        outcome = subprocess.run(args, cwd=path, input="",
            capture_output=True, text=True, errors="replace", timeout=300,
            check=False)
    except subprocess.TimeoutExpired as e:
        raise ProtocolError("Codex exceeded 5-minute budget; inspect workspace before retry") from e
    last = ""
    for line in outcome.stdout.splitlines():
        try:
            event = json.loads(line)
            if event.get("type") == "item.completed":
                item = event.get("item") or {}
                if item.get("type") == "agent_message":
                    last = str(item.get("text", ""))[-3000:]
        except (ValueError, TypeError):
            continue
    return {"task":task["id"], "exit_code":outcome.returncode,
            "summary":last or "No agent text output; inspect workspace and Codex logs.",
            "post_to_inbox":False,
            "note":"Review local changes/results before deliberately sending a public reply."}


def main(argv=None):
    p=argparse.ArgumentParser(description="Operator-gated Compute agent. No public auto-execution.")
    p.add_argument("--site",default=DEFAULT_SITE)
    p.add_argument("--db",default=str(DEFAULT_DB))
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("list",help="Show human requests for agent:compute; do not run them")
    run=sub.add_parser("run",help="Run exactly one manually approved task in a dedicated Codex workspace")
    run.add_argument("--task",required=True)
    run.add_argument("--approve-task",required=True,help="Repeat exact task ID as operator authorization")
    run.add_argument("--workspace",required=True)
    run.add_argument("--codex",default="codex")
    reply=sub.add_parser("reply",help="Publish a reviewed result (NOT automatically generated code)")
    reply.add_argument("--task",required=True)
    reply.add_argument("--kind",choices=("progress","result","question"),default="result")
    reply.add_argument("--text",required=True)
    reply.add_argument("--ref",action="append",default=[])
    args=p.parse_args(argv)
    db=AgentLedger(args.db)
    try:
        site=SiteClient(args.site)
        incoming=site.fetch(recipient=AGENT, limit=50)
        open_tasks=tasks(incoming)
        db.collect(open_tasks, AGENT)
        if args.command=="list":
            for task in open_tasks[:30]:
                print(json.dumps({"id":task["id"],
                    "from":task["from"],"name":task.get("from_label",""),
                    "created_at":task.get("created_at"),
                    "request":task["text"][:700]},ensure_ascii=False))
            if not open_tasks:print("No recent requests for agent:compute.")
            return 0
        task=locate(incoming,args.task)
        if task is None:
            raise ProtocolError("Task not found in recent durable history; no work or reply performed")
        if args.command=="run":
            result=run_approved(task,args.approve_task,args.workspace,args.codex)
            print(json.dumps(result,indent=2,ensure_ascii=False))
            return 0 if result["exit_code"]==0 else 4
        response=new_message(AGENT,task["from"],args.kind,args.text,
                             project=task.get("project") or "compute",
                             reply_to=task["id"],refs=args.ref)
        db.enqueue(response)
        try:
            state=db.send_once(response["id"],site)
        except UnknownDelivery as e:
            print(json.dumps({"id":response["id"],"state":"unknown",
                "note":"Do not resend blindly. Reconcile this ID using inbox_fabric."}))
            return 3
        print(json.dumps({"id":response["id"],"state":state,
            "reply_to":task["id"],"recipient":task["from"]}))
        return 0
    except (ProtocolError, SiteUnavailable, OSError) as exc:
        print("Compute: "+str(exc),file=sys.stderr)
        return 2
    finally:
        db.close()


if __name__=="__main__":
    raise SystemExit(main())
