"""Design-factor contracts are separate from the performance simulator."""
import copy
import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import json
import unittest

from logical_cloud.cli import main
from logical_cloud.design_space import (
    compare_design, human_summary, load_design, resolve_design, validate_design,
)
from logical_cloud.model import ModelError

ROOT = Path(__file__).resolve().parents[1]


class DesignSpaceTest(unittest.TestCase):
    def setUp(self):
        self.world = load_design(ROOT / "examples/design_playroom_3d.json")
        self.compute = load_design(ROOT / "examples/design_compute_tv.json")

    def test_partial_world_does_not_force_unresolved_choices(self):
        plan = resolve_design(self.world, variant_id="browser_prototype")
        self.assertEqual(plan["verdict"], "incomplete")
        self.assertEqual(plan["selected"]["renderer"]["option"], "browser_webgl")
        self.assertIn("world_language", {f["id"] for f in plan["open_factors"]})
        self.assertIn("agent_workflow", {f["id"] for f in plan["open_factors"]})
        self.assertFalse(plan["conflicts"])
        self.assertIn("not proof", plan["epistemic_limit"])

    def test_contract_intersection_not_global_assumption(self):
        plan = resolve_design(self.world, variant_id="remote_fidelity")
        self.assertFalse(plan["conflicts"])
        self.assertTrue(any(x["id"] == "remote_video_presentation" and
                            x["status"] == "satisfied_as_assignment"
                            for x in plan["intersections"]))
        # Missing continuity is a research question, not a false incompatibility.
        self.assertTrue(any(x["id"] == "remote_state_continuity" and
                            x["status"] == "question"
                            for x in plan["intersections"]))
        contradicted = resolve_design(self.world, variant_id="remote_fidelity",
                                     overrides={"presentation": "local_frames"})
        self.assertEqual(contradicted["verdict"], "declared_contract_conflict")
        self.assertEqual(contradicted["conflicts"][0]["id"], "remote_video_presentation")

    def test_explicit_variants_not_unbounded_cartesian_product(self):
        cases = compare_design(self.world)
        self.assertEqual(len(cases), 3)
        self.assertEqual({c["variant"] for c in cases},
                         {"browser_prototype", "native_world", "remote_fidelity"})
        self.assertTrue(any(c["open_factors"] for c in cases))

    def test_compute_scope_and_real_work_remain_independent(self):
        current = resolve_design(self.compute, variant_id="browse_only")
        self.assertEqual(current["selected"]["dispatch"]["option"], "explore_only")
        self.assertNotIn("execution", current["selected"])
        future = resolve_design(self.compute, variant_id="agent_work")
        self.assertEqual(future["selected"]["execution"]["option"], "virtual_agent")
        self.assertEqual(future["verdict"], "candidate_unverified")
        self.assertIn("not runtime verification", human_summary(future))

    def test_invalid_assignment_is_not_forgiven(self):
        with self.assertRaises(ModelError):
            resolve_design(self.world, overrides={"renderer": "quantum"})
        with self.assertRaises(ModelError):
            resolve_design(self.world, variant_id="magic")

    def test_bad_evidence_cannot_claim_observed(self):
        invalid = copy.deepcopy(self.world)
        option = invalid["factors"][0]["options"][0]
        option["maturity"] = "observed"
        option["evidence"] = {"kind": "hypothesis"}
        with self.assertRaises(ModelError):
            validate_design(invalid)

    def test_invalid_crossfactor_reference(self):
        invalid = copy.deepcopy(self.compute)
        invalid["intersections"][0]["requires"] = {"unknown_factor": "yes"}
        with self.assertRaises(ModelError):
            validate_design(invalid)

    def test_cli_human_projection_and_machine_projection(self):
        p = str(ROOT / "examples/design_playroom_3d.json")
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(["design", p, "--variant", "remote_fidelity"])
        self.assertEqual(code, 0)
        self.assertIn("FACTOR INTERSECTIONS:", stream.getvalue())
        self.assertIn("remote_state_continuity", stream.getvalue())
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(["design", p, "--compare", "--json"])
        self.assertEqual(code, 0)
        cases = json.loads(stream.getvalue())
        self.assertEqual(len(cases), 3)

    def test_cli_targeted_variable_override_does_not_change_source(self):
        path = ROOT / "examples/design_playroom_3d.json"
        original = path.read_bytes()
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "analysis.json"
            code = main(["design", str(path), "--variant", "remote_fidelity",
                         "--set", "presentation=local_frames", "--output", str(output)])
            self.assertEqual(code, 0)
            report = json.loads(output.read_text())
            self.assertEqual(report["verdict"], "declared_contract_conflict")
        self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
