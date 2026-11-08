"""The public Compute Inbox is a task board, never an automatic executor."""
import json
from pathlib import Path
import tempfile
import unittest

from logical_cloud.compute_agent import tasks, locate, run_approved
from logical_cloud.inbox_fabric import ProtocolError

SENDER = "device:fire-console-0123456789ab"


def task(task_id="compute-request-20261108"):
    return {"schema_version":1,"id":task_id,"from":SENDER,
            "to":"agent:compute","kind":"request","project":"compute",
            "text":"Write a short verification file", "refs":[]}


class ComputeAgentTest(unittest.TestCase):
    def test_only_addressed_tasks_are_read(self):
        valid=task()
        invalid=dict(task("other-request-20261108"),to="agent:another")
        plain=dict(task("someone-else-20261108"),kind="message")
        self.assertEqual(tasks([valid,invalid,plain]),[valid])
        self.assertEqual(locate([valid],"compute-request-20261108"),valid)
        self.assertIsNone(locate([valid],"no-task"))

    def test_unapproved_request_never_launches_codex(self):
        with tempfile.TemporaryDirectory() as dir:
            marker=Path(dir)/"executed.txt"
            fake=Path(dir)/"codex-stub"
            fake.write_text("#!/usr/bin/env python3\n"
                "from pathlib import Path\n"
                "Path('executed.txt').write_text('executed')\n"
                "print('{\"type\":\"item.completed\",\"item\":{\"type\":\"agent_message\",\"text\":\"done\"}}')\n")
            fake.chmod(0o700)
            with self.assertRaises(ProtocolError):
                run_approved(task(),"wrong-task",dir,str(fake))
            self.assertFalse(marker.exists())
            output=run_approved(task(),task()["id"],dir,str(fake))
            self.assertEqual(output["exit_code"],0)
            self.assertEqual(output["summary"],"done")
            self.assertFalse(output["post_to_inbox"])
            self.assertEqual(marker.read_text(),"executed")


if __name__=="__main__":
    unittest.main()
