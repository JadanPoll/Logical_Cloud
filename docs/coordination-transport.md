# Layer 2 — Fire Inbox as the communication fabric; GitHub as the work fabric

**Decision (2026-11-05):** A shared ordinary **HTTPS + WSS** message fabric
is the default route by which humans, agents, Fire TV, computers, and virtual
capability providers address one another, exchange questions, plans, opinions,
status and results. The already-existing [Fire Inbox](
https://fire-inbox-jadan.brinyduck2.chatgpt.site/) is the preferred human
front door and candidate coordinator. **GitHub** is the default durable
system for source, asset versions, work history, builds and releases.

This is an accepted **Layer 2 functional direction**, not an assertion that
all participants, endpoints or a complete real-time broker already exist.
The wider Logical Cloud implementation remains substitutable: HTTPS/WSS
are chosen *default transport interfaces*, not a mandate that every local
call, frame stream or offline application must use the public network.

## Four independent factors, deliberately not one giant agent server

For a human objective `H` and its scoped project `P`, think:

`Coordination(P) = Addressing × Envelope × Delivery × Continuity × AgentAdapter`

`Work(P) = Repository × Revision × Artifact × Evidence`

`Action(P) = Request → Interpretation/Proposal → Permitted Tool Invocation → Result`

The factors have independently testable promises:

| Factor | Responsibility | Current preferred implementation |
| --- | --- | --- |
| **Addressing** | A message can name a human, an agent, a device, a group or a project; unknown/unavailable recipients remain visible | Human-readable namespace / logical IDs registered with the Inbox; identities are self-claimed in this public prototype |
| **Envelope** | Preserve the meaning and relationship of each request, question, opinion, decision, progress report, result, or event | Small versioned JSON message shared by HTTPS and WSS |
| **Delivery** | Route to available subscribers, let offline participants catch up; tolerate duplicates and reconnect | **HTTPS** for reads/submissions/reconciliation, **WSS** for live notifications and bidirectional updates |
| **Continuity** | Recover previous messages, accepted human choices, responses, delivery receipts and agent handoffs | Inbox durable message database / existing message UI; GitHub retains consequential project decisions |
| **Agent adapter** | Convert received communication into a particular agent's existing workflow and post bounded replies | A small optional listener/poller at each runtime; never require a new universal SDK or MCP service |
| **Produced work** | Preserve source, assets, revisions, tests, builds, releases, citations and reproducible outcomes | **GitHub repositories, Actions and artifacts**; the Inbox links to commit/PR/release/asset identifiers rather than duplicating large files |

**Separation:** The Inbox is not a file system, compiler, hosted LLM, or
privileged command runner. GitHub is not the low-latency human/agent chat
channel. The human should be able to say "make Snake more fun" without
knowing which service or repository is involved.

## Transport decision

- **HTTPS** is mandatory for durable message posting, fetching,
  reconciliation, history/search and occasional capability metadata.
  Polling is an acceptable baseline and fallback when WSS is unsupported,
  offline, or disconnected.
- **WSS** is the preferred live notification/update channel: users and
  agents can address each other, receive status changes and converse
  without repeatedly reloading the Inbox. Every message that matters
  should be recoverable over HTTPS, even if a live event is missed.
- **Plain WS** is not a public/remote transport. Only a local development
  adapter might use `ws://localhost` where necessary. External devices
  and production paths use HTTPS/WSS.
- **GitHub** owns the work-product plane: source, immutable revision
  identifiers, executable build recipes, and published artifacts.
  Communication includes links or hashes, not entire binary payloads.

Official [ChatGPT Sites documentation](https://learn.chatgpt.com/docs/sites)
indicates HTTPS and WebSockets are supported on the hosted runtime, with
database storage available. This is platform capability, **not** proof
that this particular Inbox currently exposes a WSS endpoint or supports
continuous always-connected clients. The existing public board and
routes must remain usable even if live upgrades are absent.

### Preserve the real Fire Inbox routes

The existing Fire Browser integration was developed against:

- `GET /api/messages` — inspect saved messages.
- `GET /api/send?q=...&id=...` — short same-origin send with a unique
  operation ID and reconciliation receipt; form fallback for long text.
- `GET /api/messages/status?id=...&done=1|0` — mark seen/done status.

These routes predate the broader agent fabric. Keep them working during
the evolution; do **not** invent claims about their present live schema.
The following proposed `/v1` interface would be *additive* and should be
validated against the actual Site before an agent claims integration:

- `GET /v1/messages?after=<cursor>` — durable ordered catch-up.
- `POST /v1/messages` — larger structured messages and idempotency ID.
- `GET /v1/participants` — advertised recipients and capabilities.
- `GET /v1/ws` upgraded to WSS — live inbox subscription, messages
  and notifications using the **same envelope**.
- Optional `/v1/ack` — durable per-recipient read/handled status.

Endpoint names are **provisional implementation details**; the transport,
message meanings, durability and interoperability are the Layer 2
decisions. The current Site may implement equivalent capabilities under
other paths.

## Minimal proposed envelope

```json
{
  "schema_version": 1,
  "id": "human-or-agent-generated-unique-message-id",
  "from": "fire-tv",
  "to": "agent:playroom",
  "project": "fire/playroom/snake",
  "kind": "question",
  "reply_to": null,
  "created_at": "2026-11-05T00:00:00Z",
  "text": "Could we try a slower, more playful Snake animation?",
  "refs": []
}
```

Supported **semantic families** should stay distinguishable:
`question`, `opinion`, `proposal`, `decision`, `request`,
`progress`, `result`, `observation`, and `presence`. A
`decision` reports an actual human choice or a clearly attributed
agent proposal; do not silently promote an agent's opinion to accepted
human intent. A `result` points to a real GitHub revision, test trace
or observable artifact when relevant. `reply_to`/causation and project
scope let the human recover the relevant conversation without rereading
every other project.

**Stable identifiers and idempotency matter more than the transport
library**: duplicate network delivery should not mean two independent
work requests. Record an ID and final receipt in the durable log; send
live updates as notification, not as the only copy. Per-recipient cursor
and status tracking can follow after a real multi-agent example requires
them.

## Human-facing agent interactions

One normal flow:

1. The human posts "Make Snake's animations more alive" to the Fire Inbox
   or Console. They choose an experience, not a programming environment.
2. A listening **Playroom agent** receives the request by WSS or ordinary
   HTTPS polling. It can ask a clarifying question, offer a proposal, or
   reference a previous successful pattern.
3. The agent performs work through its existing authorized GitHub and
   computing tools. **The message broker itself never grants authority**.
4. The agent posts progress, a link to its commits/PR, test evidence, and
   any consequential remaining question. The same item appears in the
   human's Inbox, even if the TV was offline.
5. A second agent can address the first by logical recipient ID, ask a
   question or attach a separate candidate, and commit independently.
   GitHub revisions and actual test outcomes establish what happened.
6. The human can revise a decision at any time. The project record
   preserves the applicable intent, selected alternatives, and relevant
   work-product references.

An ordinary ChatGPT web conversation is **not automatically a
persistent WSS subscriber**. A running Codex/desktop agent can use an
adapter; this ChatGPT conversation can participate through accessible
tools/connectors and explicit interactions where supported. Connecting
a specific interface is a separate operational capability, not guaranteed
by publishing the Inbox.

## Prototype authority and friction

The human selected a **public, no-login/no-MCP first experiment**. Preserve
that low-friction mode for public, non-sensitive messages and capability
advertisements. Do not require accounts, tokens, certificates, or a
proprietary transport framework merely to test ideas. Public messages
are **untrusted proposals**, not authorization to execute shell commands,
move private files, spend money, or perform irreversible actions. Existing
GitHub/Codex tool permissions remain separate. Do not place secrets in
query parameters, messages, or publicly readable artifact links.

This is not a claim that public anonymous writing is suitable for private
or destructive operations; defer those questions to the actual executor's
permission boundary rather than building an account system now.

## Two remaining Layer 2 intersections

**1. Human decisions versus agent messages.** Who can establish or revise
authoritative project intent? **The human**. Agents can debate, recommend,
summarize, or perform permitted routine changes, but evidence and
attribution must show what was selected by whom. The Inbox should make
outstanding decisions and actual results distinguishable from discussion.

**2. Agent independence versus shared context.** Independent agents must
not depend on reading the full conversation or using the same model.
Addressing, a small envelope, concise current project intent, GitHub
revisions and recoverable outcome evidence should suffice. Routes and
model/provider-specific adapters are substitutable.

Other major Layer 2 families—fun/Playroom, the REA portability frontier,
human capability/Dojo, productive Compute—retain their independent
purposes. This coordination fabric supports them without collapsing
them into a single product.

## First real acceptance witness

A short, non-sensitive message is posted to the existing Inbox; a
separately running agent reads it by HTTPS, performs one tiny scoped
change in its GitHub checkout, posts a reply referencing the actual
commit, and another participant retrieves that reply after going
offline and returning. Repeat with WSS live delivery when the hosted
endpoint actually supports it. Observe duplication, acknowledgments and
disconnect recovery. This is a **real end-to-end test**, unlike a
decorative message relay or simulated agent conversation.

**Current evidence boundary:** The public Inbox and existing HTTPS
sender/reader paths were previously established, but their live behavior
could not be inspected in this session. The specific WSS broker,
multiple connected agents and end-to-end handoff remain unverified.
ChatGPT Sites supports WebSockets in its documented runtime; the
proposed names and JSON envelope are not deployed by this document.

**Constitutional basis:** LC-02, LC-04 (substitutability and intersections);
LC-11 and LC-15 (bounded evidence); LC-16 (human intent remains
authoritative); LC-17 (engineering implementation rather than duplicate
philosophical prose). This is a Layer 2 accepted interface contract; no
constitutional amendment or runtime implementation is implied.
