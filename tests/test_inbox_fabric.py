"""Real local HTTP round-trip for two agent adapters; no remote Site required."""
import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from logical_cloud.inbox_fabric import (
    AgentLedger, SiteClient, UnknownDelivery, ProtocolError,
    new_message, encode_message, decode_message, parse_site_list, validate_origin,
)


class MemorySite:
    def __init__(self, uncertain=False):
        self.store = []
        self.uncertain = uncertain
        self.attempts = 0
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                url = urlsplit(self.path)
                if url.path == "/api/messages":
                    self.respond({"messages": outer.store})
                elif url.path == "/api/send":
                    outer.attempts += 1
                    q = parse_qs(url.query)
                    message_id = q["id"][0]
                    text = q["q"][0]
                    if not any(x["id"] == message_id for x in outer.store):
                        outer.store.append({"id": message_id, "message": text})
                    self.respond({"ok": True,
                                  "id": "wrong-id" if outer.uncertain else message_id})
                else:
                    self.send_error(404)

            def respond(self, obj):
                payload = json.dumps(obj).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.server.shutdown()
        self.thread.join(timeout=2)
        self.server.server_close()

    @property
    def url(self):
        return f"http://127.0.0.1:{self.server.server_port}/"


class InboxFabricTest(unittest.TestCase):
    def test_human_readable_agent_roundtrip(self):
        msg = new_message("agent:alpha", "agent:beta", "question",
                          "Can we change Snake's speed?", project="fire/snake")
        display = encode_message(msg)
        self.assertIn("agent:beta", display)
        self.assertIn("Snake's speed", display)
        self.assertEqual(decode_message(display), msg)
        self.assertIsNone(decode_message("Plain legacy message from TV"))
        self.assertIsNone(decode_message("[LC1 not-json]\\nfake"))

    def test_end_to_end_read_recover_and_github_reply(self):
        with MemorySite() as site, tempfile.TemporaryDirectory() as path:
            a = AgentLedger(Path(path) / "alpha.sqlite3")
            b = AgentLedger(Path(path) / "beta.sqlite3")
            try:
                client = SiteClient(site.url)
                question = new_message("agent:alpha", "agent:beta", "question",
                    "Can you investigate animation timing?", project="fire/snake")
                a.enqueue(question)
                self.assertEqual(a.send_once(question["id"], client), "confirmed")
                self.assertEqual(b.collect(client.fetch(), "agent:beta"), 1)
                self.assertEqual(b.collect(client.fetch(), "agent:beta"), 0)
                self.assertEqual(b.received()[0]["id"], question["id"])
                reply = new_message("agent:beta", "agent:alpha", "result",
                    "Experiment proposed in PR.", project="fire/snake",
                    reply_to=question["id"],
                    refs=["https://github.com/JadanPoll/fire/pull/18"])
                b.enqueue(reply)
                self.assertEqual(b.send_once(reply["id"], client), "confirmed")
                self.assertEqual(a.collect(client.fetch(), "agent:alpha"), 1)
                self.assertEqual(a.received()[0]["reply_to"], question["id"])
                self.assertEqual(len(site.store), 2)
            finally:
                a.close()
                b.close()

    def test_uncertain_receipt_never_retries_even_after_restart(self):
        with MemorySite(uncertain=True) as site, tempfile.TemporaryDirectory() as path:
            file = Path(path) / "ledger.sqlite3"
            msg = new_message("agent:first", "agent:second", "question", "A question")
            ledger = AgentLedger(file)
            ledger.enqueue(msg)
            with self.assertRaises(UnknownDelivery):
                ledger.send_once(msg["id"], SiteClient(site.url))
            self.assertEqual(ledger.status(msg["id"]), "unknown")
            ledger.close()
            reopened = AgentLedger(file)
            try:
                with self.assertRaises(ProtocolError):
                    reopened.send_once(msg["id"], SiteClient(site.url))
                self.assertEqual(site.attempts, 1)
                self.assertEqual(len(site.store), 1)
                self.assertEqual(reopened.reconcile(SiteClient(site.url).fetch()), [msg["id"]])
                self.assertEqual(reopened.status(msg["id"]), "confirmed")
                self.assertEqual(site.attempts, 1)  # reconciliation reads only
            finally:
                reopened.close()

    def test_native_compute_request_is_deliverable_without_execute_authority(self):
        long_goal = "Investigate Snake input. " * 75
        original = {
            "schema_version": 1,
            "id": "native-compute-task-20261108",
            "from": "device:fire-console-0123456789ab",
            "from_label": "Fire Console TV",
            "to": "agent:compute", "kind": "request",
            "project": "compute", "reply_to": None,
            "text": long_goal, "created_at": "2026-11-08T13:00:00Z",
            "refs": []
        }
        parsed = parse_site_list(json.dumps({"messages": [original]}).encode())
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["text"], long_goal)
        self.assertEqual(parsed[0]["from_label"], "Fire Console TV")
        with tempfile.TemporaryDirectory() as folder:
            ledger = AgentLedger(Path(folder) / "inbox.sqlite")
            try:
                self.assertEqual(ledger.collect(parsed, "agent:compute"), 1)
                self.assertEqual(ledger.collect(parsed, "agent:compute"), 0)
                self.assertEqual(ledger.received()[0]["kind"], "request")
            finally:
                ledger.close()
        bad = dict(original, to="shell:root")
        self.assertEqual(parse_site_list(json.dumps({"messages":[bad]}).encode()), [])

    def test_legacy_messages_do_not_turn_into_agent_commands(self):
        self.assertEqual(parse_site_list(
            json.dumps({"messages": [{"id": "plain", "message": "rm -rf /"}]}).encode()), [])

    def test_schema_and_sender_constraints(self):
        with self.assertRaises(ProtocolError):
            validate_origin("http://example.org/")
        with self.assertRaises(ProtocolError):
            new_message("agent:valid", "bad recipient", "question", "Hi")
        with self.assertRaises(ProtocolError):
            new_message("agent:valid", "agent:other", "question", "Hi",
                        refs=["https://unknown.example/file"])
        with self.assertRaises(ProtocolError):
            parse_site_list(b"<html>Sign in</html>")


if __name__ == "__main__":
    unittest.main()
