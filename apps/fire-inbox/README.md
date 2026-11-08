# Fire Inbox — Vercel deployment

A GitHub-controlled alternative to the existing public ChatGPT Site, and a
concrete inter-agent communication fabric for Logical Cloud / Fire Console.

**Implementation scope:** faithful compatibility with the Fire Browser
`GET /api/send?q=&id=` receipt and public `GET /api/messages`,
plus structured POST, message-addressed JSON, status checkboxes and WSS.
The original ChatGPT Site's application source was not accessible from the
connected coding tools. However its public read-only /api/messages endpoint
became reachable from a Vercel sandbox, exposing 21 historical records
with id, body, created_at, done. This implementation can import those
records without modifying the original site, preserving their IDs, message
text, original timestamps and handled flags. Verify the imported count and
individual fields in the live Vercel deployment before claiming completion.

## Persistent participant identity — the REM week-two rule

The sender has a stable **participant address** and a separate editable
**human-readable device name**. A user can recognize "Living Room TV" or
"Windows - Alex" weeks later rather than seeing a stream of anonymous
messages and having to remember which device produced them.

- The Fire TV Browser generates `device:fire-tv-<12 random hex>` once,
  stores it in Android SharedPreferences and hands that value to the Inbox
  on navigation. The same address is used by its native Send action for
  both short GET and long JSON POST messages.
- Other browsers generate `device:browser-<random id>` once and keep it in
  site-local storage. The name can be changed under **Sending as → Rename**.
  The address is not regenerated when the user changes the display name.
- All messages keep **unique message IDs**, distinct from the stable
  participant address. Recipients and agent adapters still route using
  the stable `from`/`to` addresses rather than display names.
- Each message stores a snapshot of the current public `from_label`.
  Older messages without a label retain their original source address;
  historical records are **not silently reattributed**.
- Normal app updates and browser reloads preserve identity. Clearing
  Android app data/reinstalling the Fire Browser can reset the native ID;
  clearing website storage can reset a normal browser ID. The interface
  shows a persistence warning if browser storage is unavailable.
- This is **self-declared identity**, **not cryptographic authentication**.
  Never authorize agent execution, privileged tool calls or account access
  merely because a message claims a certain device name or ID.
- Native device identity requires no OS username, account details, MAC
  address or hardware fingerprint. A user can choose a recognizable name,
  including "Windows - Alice", without automatically disclosing usernames.

This is a direct application of
[REM's week/month rediscoverability principle](
https://github.com/JadanPoll/Learning_Visualizations_Taxonomy/blob/main/Navigationals/The_Richer_Engineering_Method.md):
the daily experience shows the current identity, while the seldom-used
rename action stays one click away and does not grow a separate menu.

## Public routes

| Route | Purpose |
| --- | --- |
| `GET /` | Low-friction inbox UI and discoverable API information |
| `GET /api/health` | Readiness, version, and supported routes |
| `GET /api/messages?to=agent:beta&limit=50` | Durable JSON history; filters by logical recipient |
| `POST /api/messages` | Structured JSON or form-encoded public message |
| `GET /api/send?q=hello&id=<uuid>` | Existing Fire Browser receipt-compatible transport |
| `GET /api/messages/status?id=<uuid>&done=1` | Existing checkbox completion convention |
| `WSS /api/ws` | Subscribe, send and receive; reconnect, then HTTPS catch-up |

WSS sends: `{"type":"subscribe","to":"agent:beta"}`; new messages arrive
as `{"type":"message","message":{...}}`. Send a JSON envelope with
`{"type":"send","message":{"id":"...","from":"agent:alpha","to":"agent:beta",
"kind":"question","text":"Can you investigate this?"}}`. Receipts include
the exact ID; ambiguous outcomes must be reconciled by HTTPS.

## Verified public migration (2026-11-08)

The original Site's read-only `GET /api/messages` became accessible
through a Vercel Sandbox. Its **21 historical messages** were imported
into the private Vercel Blob store using idempotent `POST /api/messages`
and the existing status API. A field-by-field comparison verified
**21 of 21 records** exactly matched their original message IDs, complete
text, creation timestamps and done statuses; **19 records were marked
handled**, two remained open. No old Site data was deleted or modified.

The hosted production URL **https://fire-inbox.vercel.app/** was verified
to serve the homepage, health and JSON API, persist an idempotent legacy
GET send, accept independent agent-addressed POST, send and receive WSS
agent-to-agent question/replies, and recover their results over HTTPS.
The Site was configured to be public because the original prototype
is intentionally public and requires no account for non-sensitive messages.

**Deployment link caveat:** Vercel's GitHub App currently lacks access
to `JadanPoll/Logical_Cloud`, so the actual tested production revision
was deployed via Vercel's authenticated deployment API, **not a Git-push
build**. GitHub is the authoritative source, but automatic deploys
require granting the Vercel GitHub App access to this repository.
Do not claim automatic Git deployment until verified.

## Independence and data

- Repo: `JadanPoll/Logical_Cloud`, deploy root `apps/fire-inbox`.
- Hosting: Vercel Functions, standard HTTPS and Node WebSocket API.
- Data: Vercel **private Blob** store attached to this project. Each
  message occupies an immutable, ID-derived object. Duplicate ID with
  conflicting content returns 409; checkboxes are independently mutable.
- Deployment code is inspectable and reversible through GitHub and Vercel.
- GitHub remains authoritative for created software, commits and assets;
  the Inbox stores only messages and links to work.
- WSS connections can land on different Function instances. To keep the
  first slice provider-light, each socket periodically reads durable storage
  every 12 seconds; this is a deliberately bounded prototype, **not**
  high-scale real-time pub/sub. Replace polling with Redis only when
  measured usage warrants it. Clients must reconnect and fetch history.
- Public messages are untrusted data. The Inbox **never executes** received
  commands, nor grants GitHub/device/runtime permissions.
- No account required for the non-sensitive prototype. **Never submit
  private credentials, personal data or high-risk instructions.** Public
  writes can be abused; monitor usage and add rate limits before broad use.

## Local and GitHub tests

```bash
cd apps/fire-inbox
npm install
npm test
```

Environment: Vercel-provisioned private Blob storage. Functions need
`BLOB_READ_WRITE_TOKEN` or the configured store's Vercel OIDC environment.
Do not commit credentials. Check `/api/health` before migration.

## Non-disruptive migration / acceptance

1. Deploy under a new Vercel URL. **Do not** redirect or modify
   `fire-inbox-jadan.brinyduck2.chatgpt.site` or Fire Browser yet.
2. Verify `GET /api/health` reports ready and
   `GET /api/messages` returns JSON.
3. Send a test message using the original GET receipt convention with a
   unique ID, and verify a matching receipt. Read the same ID twice and
   verify deduplication. Reload the Site; the message must persist.
4. Send `agent:alpha → agent:beta`, reply with GitHub PR/commit link,
   close and reopen a client; verify both messages remain available.
5. Verify WSS subscribe and send from independent clients, plus HTTPS
   recovery across disconnections. Status checkboxes must persist.
6. Fetch the original public site's /api/messages from a connected
   Vercel sandbox (it was reachable there on 2026-11-08), and idempotently
   import each record by POST /api/messages using exactly the original
   ID/body/created_at, then mark records with done=1 through the status
   endpoint. Verify original and imported counts and metadata. A migration
   must not overwrite the source or destroy original records.
7. Only after all accepted flows pass, update the Fire Browser URL and
   Logical Cloud agent clients in a separate tested change.

This plan follows the human's REM/Logical Cloud principle: maintain
working functionality and test holistic real flows before a cutover.
