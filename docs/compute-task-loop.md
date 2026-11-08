# Compute: real work from the TV, without a control-panel habit

**Human goal (REM week-two test):** Return to the TV, describe what you want,
and see the current result without remembering pairing commands, agents,
websocket routes, GitHub API syntax, or technical setup. A useful live demo
must still make sense a month later.

Two independent useful paths are now built:

| Visible action | Actual behavior | What it does **not** claim |
| --- | --- | --- |
| **Send to agents** | Save an addressed `request` for `agent:compute` in the public Fire Inbox, with a persistent sender and unique request ID; display replies linked by `reply_to` and GitHub references | No agent starts merely because a public request arrived. Unconnected agents won't reply |
| **Check project work** | Fetch current public GitHub repository, latest commit, open PRs and build history using a real, server-side read-only API; display citations/links and distinguish unavailable data | Not an LLM analysis, private-repository access or proof that an APK was tested on a TV |
| **Run paired Codex** (native Console, secondary) | Existing authenticated private HTTPS executor runs official Codex CLI in its configured workspace | Not open to anonymous Inbox messages; operator maintains host/token |

The practical Compute web surface is **https://fire-inbox.vercel.app/compute.html**,
and Fire Console's native Compute channel submits public tasks using
`ComputeInboxClient`. Its familiar native Fire TV keyboard/dictation
remains available, and existing private Codex execution is not removed.
The Inbox has a persistent identity and durable message history.

## Design boundaries / no new engine

```text
Human goal (native Compute / Compute web)
  ├─ Send public task (HTTPS JSON, exact ID receipt)
  │     → Fire Inbox storage → agent:compute recipient
  │     → reviewed connected agent or dedicated operator
  │     → response to originating device, reply_to=task ID
  │     → GitHub commit/PR/release reference
  ├─ Inspect public GitHub work (GET /api/compute/inspect?repo=owner/name)
  │     → current public GitHub metadata, bounded result, links
  └─ Use authorized Codex workspace
        → existing private paired executor, no Inbox privilege escalation
```

A public message is **untrusted task data** and must not be forwarded
automatically to a shell, Codex CLI, GitHub write operation or private
app. The Inbox is a communication bus, not an authorization system.
GitHub remains the source of produced code/artifacts. The user can use
the **Check project work** option immediately, whether any agents
are online or not.

## Connect an independently running agent

The [existing Inbox adapter](inbox-agent-bridge.md) now understands
both legacy `LC1` short messages and native JSON messages from the TV.
The new opt-in, operator-controlled adapter runs without extra Python
dependencies:

```bash
# See current tasks addressed to the Compute agent (no commands executed).
python -m logical_cloud.compute_agent list

# A separate workstation with authenticated Codex CLI can deliberately
# approve ONE reviewed task ID in a dedicated, disposable workspace.
python -m logical_cloud.compute_agent run \
  --task REQUEST_ID --approve-task REQUEST_ID \
  --workspace /path/to/dedicated/experiments

# Review the resulting local files and messages. Then send a short reply,
# ideally with a real GitHub PR/commit link as provenance.
python -m logical_cloud.compute_agent reply \
  --task REQUEST_ID --kind result \
  --text 'Reviewed the result and published the tested revision.' \
  --ref https://github.com/JadanPoll/fire/pull/21
```

The operator is responsible for connecting a real authenticated Codex
CLI and choosing an isolated workspace. An ordinary ChatGPT chat is not
an automatically running persistent agent, nor does deploying Vercel
start a host worker. This manual approval boundary protects against
public prompt injection; **there is no automatic execution of anonymous
messages**. For a no-tool task, an agent may reply directly without
running any code.

## Native TV and browser return behavior

- Native Compute's primary action is **SEND TO AGENTS**; the prompt
  and latest request ID are stored on-device, with no credentials.
- **CHECK AGENT RESPONSE** reads the Inbox; replies must match both
  request ID and recipient address. A Github reference is a direct
  **VIEW RESULT ON GITHUB** action.
- Errors preserve the draft and ID, and never silently resend after
  an uncertain response. The human can inspect the public Inbox first.
- The **OPEN CODEX** fallback remains, and paired host configuration,
  cancellation, recovery and devices are still accessible in Compute
  options. Starting a paired job reveals its job/status panel immediately.
- The web Compute surface keeps recent requests in local storage
  **and** tries to recover them from public Inbox messages, without
  introducing extra first-screen setup controls.
- If old requests exceed the most recent Inbox page, show that the
  history search is incomplete rather than claiming the request failed.
  A dedicated per-thread cursor is a future scaling task, not needed for
  this initial real-world demonstration.
- **Public privacy:** do not send private tasks, personal credentials,
  customer data or sensitive files to the public Inbox. The project
  inspection uses GitHub's public API; optional checks may be rate limited.

## Acceptance evidence / stopping point

Tests must establish the following, separately:

1. A hosted public GitHub inspection returns real current links, commit,
   PR/build facts and a time stamp; when an upstream endpoint fails,
   unavailable does not masquerade as zero.
2. Fire TV submits once and receives the exact ID receipt; it can close
   and reopen the channel and check status without re-posting.
3. An independently connected agent retrieves a JSON-native addressed
   request, with no execution side effect. Explicit approval is required
   to invoke Codex in a dedicated workspace.
4. The agent replies with `reply_to` and a real GitHub work reference;
   the originating device sees the message and can open that reference.
5. A real device has readable focus, working keyboard and appropriate
   status visibility. CI compilation alone does not prove this.
6. No new account, password, MCP server, or general purpose web-shell
   capability is invented to make the demo work.

**Stopping point:** A person can ask from the TV, recover the task,
see an actual agent reply and open the result, and independently inspect
real GitHub project work. Automatic always-on task execution requires
a *separately connected, authorized worker*; label it unconnected until
a real one is running and an actual task completes.
