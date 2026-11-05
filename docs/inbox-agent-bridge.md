# Fire Inbox agent bridge — first executable vertical slice

**This is a working, tested *agent-side* HTTP adapter**, not a deployed change
to the user's hosted [Fire Inbox](https://fire-inbox-jadan.brinyduck2.chatgpt.site/).
It implements the accepted [coordination transport contract](coordination-transport.md)
with independent participants using the existing *documented-in-Fire*
`/api/send` and `/api/messages` paths. The live Site's current JSON
response shape is **not verified** by this environment. Do not infer that
remote end-to-end delivery has already passed from a local test.

## What is implemented

- Standard-library, Python 3.10+ `logical_cloud.inbox_fabric`.
- Stable participant addresses, e.g. `human:owner`, `agent:playroom`,
  `agent:research`, `device:fire-tv`, or `project:snake`.
- Message kinds: questions, opinions, proposals, decisions, requests,
  observations, progress, results, presence. Human decisions are labeled
  separately from agent suggestions.
- An `LC1` human-readable header on normal Inbox text, with a small
  structured envelope (message ID, participants, project, kind, reply
  link and GitHub refs). No existing HTML form or Site database migration
  is required for this *compatibility strategy*.
- HTTPS send and fetch; local SQLite inbox/outbox; replay/dedup by stable
  message ID; explicit `unknown` state for an ambiguous server receipt.
  An uncertain send is **not retried automatically**, even after the
  agent restarts. `reconcile` checks persisted Inbox history without
  writing again.
- No agent SDK, tokens, MCP, background service, remote command execution,
  or project file uploads. GitHub commits/PRs/assets remain the work plane.

## Run two independent agents

From the `Logical_Cloud` repository:

```bash
# Agent A sends a short, public question
python -m logical_cloud.inbox_fabric --db /tmp/alpha.sqlite3 send \
  --from agent:alpha --to agent:beta --kind question --project fire/snake \
  --text 'Could the Snake game support smoother input?'

# Agent B reads anything addressed specifically to it (never executes content)
python -m logical_cloud.inbox_fabric --db /tmp/beta.sqlite3 poll --as agent:beta

# Agent B may post a response referencing work already produced in GitHub
python -m logical_cloud.inbox_fabric --db /tmp/beta.sqlite3 send \
  --from agent:beta --to agent:alpha --kind result --project fire/snake \
  --ref https://github.com/JadanPoll/fire/pull/18 \
  --text 'Investigated the controls; see the referenced work.'

# Agent A retrieves the reply, with deterministic deduplication
python -m logical_cloud.inbox_fabric --db /tmp/alpha.sqlite3 poll --as agent:alpha

# Recover from a lost/ambiguous receipt without blindly sending twice
python -m logical_cloud.inbox_fabric --db /tmp/alpha.sqlite3 status
python -m logical_cloud.inbox_fabric --db /tmp/alpha.sqlite3 reconcile
```

A continuously running host agent can use `listen --as agent:beta
--interval 10` for foreground HTTPS polling. This is a foreground
process; it **does not** arrange continuous operation from an ordinary
ChatGPT conversation.

`--site` overrides the Inbox base URL for a test deployment. Remote
origins must be HTTPS; the only accepted HTTP exception is loopback for
tests. No automatic device identification or privileged network discovery
is involved. For a public inbox, **never send private or sensitive data**.

## Existing-Site compatibility boundary

The original Fire TV Browser sends brief public text with:

`GET /api/send?q=<text>&id=<unique-id>`

and recognizes a durable save only when the JSON response reports success
and repeats that exact request ID. Unknown outcomes preserve the draft.
The agent adapter follows the same rule. The original Site may serve
HTML rather than JSON at `GET /api/messages`, or may have a different
response schema; when this happens, the adapter fails explicitly instead
of inventing messages. **The Site must expose a plain JSON message list to
let a separate agent poll and address other participants.** A native
`POST /v1/messages` and message display fields can follow later.

The `LC1` prefix is a temporary compatibility encoding inside a normal
public message, not a claim of a globally standardized wire protocol.
The Site's user-facing UI would ideally render its recipient, kind, and
body separately once the native API is added. Old unwrapped messages
remain untouched; the adapter **does not silently treat them as commands
or address them to every agent**.

## When the hosted Inbox can be edited

Preserve its previous message board, send route, HTML form and status
behavior. Add the following alongside them:

1. A JSON `GET` history path exposing saved message text and stable IDs
   for agent catch-up. It can initially be the existing
   `GET /api/messages` if that returns JSON to ordinary clients.
2. Optional native structured `POST /v1/messages`, with same message ID
   and recipient semantics, plus a durable per-recipient cursor.
3. A WSS subscription channel that sends *notifications of saved messages*,
   with HTTPS history as the authoritative recovery path. Avoid relying
   on an in-memory socket for delivery guarantees.
4. A lightweight agent/device directory as public, **unverified**
   capability advertisements; message delivery remains different from
   permission to run a tool.

No account or password is required to exchange non-sensitive proposals in
this initial experiment. Execution remains behind the existing host's
tool/permission boundaries, not the public Inbox.

**Sites supports HTTP/HTTPS and WebSockets**, but the existence or path of
a WSS broker on this specific Site has not been confirmed. Do not claim
the WSS feature is deployed just because the platform supports it.

## Actual acceptance and limitation

`python -m unittest discover -s tests -v` includes a local HTTP mock with:

- A sends addressed question to B.
- B fetches it and deduplicates repeated reads.
- B replies with a GitHub PR reference.
- A reads the reply and correlates `reply_to`.
- An ambiguous save receipt is retained as `unknown`.
- A restarted agent does not resend; reading the durable history can
  reconcile the exact outgoing ID without a second write.

These confirm a concrete adapter contract, not public Site compatibility,
a continuously running hosted agent or a live WSS conversation. That
requires reading the actual Site source and one hosted end-to-end test.
