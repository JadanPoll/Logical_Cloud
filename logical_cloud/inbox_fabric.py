"""Fire Inbox agent adapter: public, addressed, non-executable messages.

Works over existing text-based HTTPS routes by carrying a compact LC1 header.
There is no assumption that the hosted Site has a WSS broker yet.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4

DEFAULT_SITE = "https://fire-inbox.vercel.app/"
DEFAULT_DB = Path.home() / ".local/share/logical-cloud/inbox-agent.sqlite3"
PARTICIPANT = re.compile(r"^(human|agent|device|project):[a-z0-9][a-z0-9._/-]{0,63}$")
KINDS = {"question", "opinion", "proposal", "decision", "request", "progress", "result", "observation", "presence"}
HEADER = "[LC1 "


class ProtocolError(ValueError):
    pass


class UnknownDelivery(RuntimeError):
    """The message may be saved; reconcile before any manual retry."""
    pass


class SiteUnavailable(RuntimeError):
    pass


def validate_participant(name: str) -> str:
    if not isinstance(name, str) or not PARTICIPANT.fullmatch(name):
        raise ProtocolError("participant must be human:, agent:, device: or project: plus stable lowercase ID")
    return name


def new_message(sender: str, recipient: str, kind: str, text: str,
                *, project: str = "", reply_to: str | None = None,
                refs: list[str] | None = None, message_id: str | None = None) -> dict:
    validate_participant(sender)
    validate_participant(recipient)
    if kind not in KINDS:
        raise ProtocolError("unknown message kind")
    if not isinstance(text, str) or not text.strip() or len(text) > 850:
        raise ProtocolError("public message text must be 1-850 characters")
    if not isinstance(project, str) or len(project) > 80 or any(c in project for c in "\r\n\0"):
        raise ProtocolError("invalid project label")
    if reply_to is not None and (not isinstance(reply_to, str) or len(reply_to) > 96):
        raise ProtocolError("invalid reply_to")
    refs = refs or []
    if len(refs) > 3 or any(not isinstance(r, str) or len(r) > 180 or not
        (r.startswith("https://github.com/") or re.fullmatch(r"sha256:[0-9a-f]{64}", r)) for r in refs):
        raise ProtocolError("references must be GitHub links or immutable sha256 identifiers")
    msg = {"schema_version": 1, "id": message_id or str(uuid4()),
           "from": sender, "to": recipient, "kind": kind, "project": project,
           "reply_to": reply_to, "created_at": datetime.now(timezone.utc).isoformat(),
           "text": text.strip(), "refs": refs}
    encode_message(msg)
    return msg


def encode_message(msg: dict) -> str:
    """Human-readable text with a machine header for the existing Inbox UI."""
    if msg.get("schema_version") != 1:
        raise ProtocolError("unknown schema version")
    validate_participant(msg["from"])
    validate_participant(msg["to"])
    if msg.get("kind") not in KINDS:
        raise ProtocolError("unknown kind")
    meta = {key: msg.get(key) for key in
            ("id", "from", "to", "kind", "project", "reply_to", "created_at", "refs")}
    if not isinstance(meta["id"], str) or not re.fullmatch(r"[A-Za-z0-9._-]{8,96}", meta["id"]):
        raise ProtocolError("invalid message ID")
    body = msg.get("text", "")
    if not isinstance(body, str) or not body.strip() or len(body) > 850:
        raise ProtocolError("invalid message body")
    serialized = HEADER + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + "]\n" + body
    if len(serialized.encode("utf-8")) > 1200:
        raise ProtocolError("too long for existing short-message Inbox endpoint")
    return serialized


def decode_message(raw: str) -> dict | None:
    """Ignore ordinary Inbox posts; do not fabricate recipient or authority."""
    if not isinstance(raw, str) or not raw.startswith(HEADER):
        return None
    pos = raw.find("]\n")
    if pos < 0 or pos > 1100:
        return None
    try:
        meta = json.loads(raw[len(HEADER):pos])
        if not isinstance(meta, dict) or meta.get("schema_version", 1) != 1:
            return None
        msg = {"schema_version": 1, **meta, "text": raw[pos + 2:]}
        encode_message(msg)
        return msg
    except (TypeError, KeyError, ValueError, ProtocolError):
        return None


def decode_structured(record: dict) -> dict | None:
    """Recognize *addressed* native Vercel messages without treating legacy
    public posts or arbitrary user-supplied text as agent commands."""
    if not isinstance(record, dict) or record.get("schema_version", 1) != 1:
        return None
    try:
        sender, recipient = record["from"], record["to"]
        validate_participant(sender)
        validate_participant(recipient)
        kind, identifier = record["kind"], record["id"]
        if kind not in KINDS or not isinstance(identifier, str) or not re.fullmatch(
                r"[A-Za-z0-9._-]{8,96}", identifier):
            return None
        message = record.get("text")
        if not isinstance(message, str) or not message.strip() or len(message) > 12000:
            return None
        refs = record.get("refs") or []
        if not isinstance(refs, list) or len(refs) > 3 or any(
            not isinstance(r, str) or len(r) > 180 or not (
                r.startswith("https://github.com/") or
                re.fullmatch(r"sha256:[a-f0-9]{64}", r)) for r in refs
        ):
            return None
        reply = record.get("reply_to")
        if reply is not None and (
                not isinstance(reply, str) or len(reply) > 96):
            return None
        return {
            "schema_version": 1, "id": identifier,
            "from": sender, "to": recipient, "kind": kind,
            "project": str(record.get("project") or "")[:120],
            "reply_to": reply, "created_at": str(record.get("created_at") or ""),
            "text": message, "refs": refs,
            "from_label": str(record.get("from_label") or "")[:64]
        }
    except (KeyError, TypeError, ProtocolError):
        return None


def parse_site_list(body: bytes) -> list[dict]:
    """Known JSON shapes only; do not silently interpret arbitrary HTML."""
    try:
        data = json.loads(body)
    except (ValueError, UnicodeDecodeError) as e:
        raise ProtocolError("GET /api/messages did not return JSON; inspect the live schema") from e
    records = data if isinstance(data, list) else (
        data.get("messages", data.get("items", data.get("results"))) if isinstance(data, dict) else None)
    if not isinstance(records, list):
        raise ProtocolError("Site response lacks recognizable messages list")
    output = []
    for record in records:
        if isinstance(record, str):
            raw = record
        elif isinstance(record, dict):
            raw = next((record[k] for k in ("message", "text", "body", "content")
                        if isinstance(record.get(k), str)), None)
        else:
            raw = None
        msg = decode_message(raw) if raw is not None else None
        if msg is None and isinstance(record, dict):
            msg = decode_structured(record)
        if msg is not None:
            output.append(msg)
    return output


def validate_origin(site: str) -> str:
    parsed = urlsplit(site)
    local_http = parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
    if ((parsed.scheme != "https" and not local_http) or not parsed.hostname or
        parsed.username or parsed.password or parsed.query or parsed.fragment):
        raise ProtocolError("Site must use HTTPS, except loopback HTTP for tests")
    if parsed.path not in ("", "/"):
        raise ProtocolError("Site must be an origin, not an endpoint path")
    return site.rstrip("/") + "/"


class SiteClient:
    def __init__(self, site: str = DEFAULT_SITE, *, timeout: float = 8):
        self.site = validate_origin(site)
        self.timeout = timeout

    def _request(self, path: str) -> bytes:
        request = Request(urljoin(self.site, path),
                          headers={"Accept": "application/json", "Cache-Control": "no-store",
                                   "User-Agent": "logical-cloud-agent-fabric/0.1"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                final = urlsplit(response.geturl())
                original = urlsplit(self.site)
                if final.scheme != original.scheme or final.netloc != original.netloc:
                    raise SiteUnavailable("Site redirected off origin; no receipt accepted")
                body = response.read(512001)
                if len(body) > 512000:
                    raise ProtocolError("Inbox history exceeds 512 KB; use a smaller recipient-scoped request")
                return body
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            raise SiteUnavailable(f"Site request unverified: {type(e).__name__}") from e

    def fetch(self, recipient: str | None = None, limit: int = 50) -> list[dict]:
        if recipient is not None:
            validate_participant(recipient)
        if not 1 <= limit <= 100:
            raise ProtocolError("History limit must be 1–100")
        qs = urlencode({"limit": limit, **({"to": recipient} if recipient else {})})
        return parse_site_list(self._request("api/messages?" + qs))

    def send(self, msg: dict) -> bool:
        encoded = encode_message(msg)
        qs = urlencode({"q": encoded, "id": msg["id"]})
        if len(qs) > 5000:
            raise ProtocolError("URL exceeds short-message test limit")
        try:
            reply = json.loads(self._request("api/send?" + qs))
            if not isinstance(reply, dict):
                raise ValueError("receipt must be an object")
            nested = reply.get("message")
            nested_id = nested.get("id") if isinstance(nested, dict) else None
            success = any(reply.get(k) is True for k in ("ok", "saved", "success", "posted")) or reply.get("status") == "ok"
            if success and (str(nested_id) == msg["id"] or str(reply.get("id")) == msg["id"]):
                return True
        except (ValueError, TypeError):
            pass
        except SiteUnavailable as e:
            raise UnknownDelivery(str(e)) from e
        raise UnknownDelivery("No matching ID receipt; reconcile before retrying")


class AgentLedger:
    """Durable SQLite deduplication and no-blind-retry outbound journal."""
    def __init__(self, path: str | Path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.execute("CREATE TABLE IF NOT EXISTS outbound (id TEXT PRIMARY KEY, body TEXT NOT NULL, status TEXT NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS inbound (id TEXT PRIMARY KEY, body TEXT NOT NULL)")
        self.db.commit()

    def close(self):
        self.db.close()

    def enqueue(self, msg: dict) -> None:
        encode_message(msg)
        with self.db:
            self.db.execute("INSERT INTO outbound(id,body,status) VALUES (?,?,?)",
                            (msg["id"], json.dumps(msg), "pending"))

    def status(self, message_id: str) -> str | None:
        row = self.db.execute("SELECT status FROM outbound WHERE id=?", (message_id,)).fetchone()
        return row[0] if row else None

    def send_once(self, message_id: str, site: SiteClient) -> str:
        with self.db:
            cursor = self.db.execute(
                "UPDATE outbound SET status='attempting' WHERE id=? AND status='pending'",
                (message_id,))
            if cursor.rowcount != 1:
                raise ProtocolError("already attempted or unknown; reconcile before manual resend")
            row = self.db.execute("SELECT body FROM outbound WHERE id=?", (message_id,)).fetchone()
        try:
            confirmed = site.send(json.loads(row[0]))
        except (Exception, KeyboardInterrupt):
            with self.db:
                self.db.execute("UPDATE outbound SET status='unknown' WHERE id=?", (message_id,))
            raise
        with self.db:
            self.db.execute("UPDATE outbound SET status=? WHERE id=?",
                            ("confirmed" if confirmed else "unknown", message_id))
        return "confirmed" if confirmed else "unknown"

    def reconcile(self, messages: list[dict]) -> list[str]:
        """Confirm uncertain sends found in durable Site history, no new request."""
        seen = {m["id"]: m for m in messages}
        confirmed = []
        with self.db:
            rows = self.db.execute(
                "SELECT id,body FROM outbound WHERE status IN ('attempting','unknown')").fetchall()
            for mid, body in rows:
                if seen.get(mid) == json.loads(body):
                    self.db.execute("UPDATE outbound SET status='confirmed' WHERE id=?", (mid,))
                    confirmed.append(mid)
        return confirmed

    def collect(self, messages: list[dict], recipient: str) -> int:
        validate_participant(recipient)
        inserted = 0
        with self.db:
            for msg in messages:
                if msg.get("to") != recipient:
                    continue
                # Native task requests can exceed the legacy short LC1 body
                # bound. Their structured envelope is independently validated.
                if decode_structured(msg) is None and decode_message(
                        encode_message(msg)) is None:
                    continue
                cur = self.db.execute("INSERT OR IGNORE INTO inbound(id,body) VALUES (?,?)",
                                      (msg["id"], json.dumps(msg)))
                inserted += cur.rowcount
        return inserted

    def received(self) -> list[dict]:
        return [json.loads(row[0]) for row in
                self.db.execute("SELECT body FROM inbound ORDER BY rowid")]

    def sent(self) -> list[dict]:
        return [{"id": row[0], "status": row[1]} for row in
                self.db.execute("SELECT id,status FROM outbound ORDER BY rowid")]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Addressed Inbox messages; no credentials or code execution")
    parser.add_argument("--site", default=DEFAULT_SITE)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    sub = parser.add_subparsers(dest="command", required=True)
    send = sub.add_parser("send", help="enqueue once, submit via existing HTTPS route")
    send.add_argument("--from", dest="sender", required=True)
    send.add_argument("--to", dest="recipient", required=True)
    send.add_argument("--kind", choices=sorted(KINDS), default="question")
    send.add_argument("--project", default="")
    send.add_argument("--reply-to")
    send.add_argument("--ref", action="append", default=[])
    send.add_argument("--text", required=True)
    poll = sub.add_parser("poll", help="retrieve and deduplicate addressed messages")
    poll.add_argument("--as", dest="recipient", required=True)
    watch = sub.add_parser("listen", help="foreground HTTPS polling, no background service")
    watch.add_argument("--as", dest="recipient", required=True)
    watch.add_argument("--interval", type=float, default=10)
    sub.add_parser("status")
    sub.add_parser("reconcile", help="confirm uncertain sends from durable Inbox history; no retry")
    args = parser.parse_args(argv)
    db = AgentLedger(args.db)
    site = SiteClient(args.site)
    try:
        if args.command == "send":
            msg = new_message(args.sender, args.recipient, args.kind, args.text,
                              project=args.project, reply_to=args.reply_to, refs=args.ref)
            db.enqueue(msg)
            print(json.dumps({"id": msg["id"], "status": "queued"}))
            try:
                state = db.send_once(msg["id"], site)
                print(json.dumps({"id": msg["id"], "status": state}))
            except (UnknownDelivery, SiteUnavailable):
                print(json.dumps({"id": msg["id"], "status": "unknown",
                                  "instruction": "Check Inbox by ID before resending; never blindly retry."}))
                return 3
        elif args.command == "status":
            print(json.dumps(db.sent(), indent=2))
        elif args.command == "reconcile":
            ids = db.reconcile(site.fetch())
            print(json.dumps({"confirmed": ids, "remaining": db.sent()}, indent=2))
        else:
            validate_participant(args.recipient)
            if args.command == "listen" and args.interval < 2:
                raise ProtocolError("minimum polling interval is 2 seconds")
            while True:
                count = db.collect(site.fetch(), args.recipient)
                print(json.dumps({"new": count, "messages": db.received()}, indent=2))
                if args.command == "poll":
                    break
                time.sleep(args.interval)
    except (ProtocolError, SiteUnavailable, OSError) as e:
        print(f"inbox: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 0
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
