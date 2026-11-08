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
