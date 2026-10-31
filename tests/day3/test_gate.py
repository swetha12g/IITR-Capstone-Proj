import copy
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


gate = module("gate", "gate.py")
scans = module("scans", "run-scans.py")


class GateContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "source.ts").write_text("const initial = 1;\n")
        (self.root / "package-lock.json").write_text('{}')
        self.policy = json.loads((ROOT / "policies/gates.json").read_text())
        self.policy_path = self.root / "gates.json"
        self.policy_path.write_text(json.dumps(self.policy))
        self.exception_path = self.root / "baseline-exceptions.json"
        self.exception_path.write_text(json.dumps({"schema_version": 1, "exceptions": []}))
        self.manifest = {"schema_version": 1, "scope": "synthetic-fixture", "source_root": str(self.root),
                         "full_history": True, "dependency_scope": "production-and-development", "stages": []}
        self.manifest_path = self.root / "manifest.json"
        self.reports = {
            "sast": {"version": "1.181.0", "results": [], "errors": [], "paths": {"scanned": ["source.ts"]}},
            "sca": {"SchemaVersion": 2, "Results": [{"Target": "package-lock.json", "Type": "npm", "Vulnerabilities": []}]},
            "secrets-history": [], "secrets-tree": [],
        }
        for stage, report in self.reports.items():
            self.store(stage, report)

    def store(self, stage, report, code=0):
        path = self.root / (stage + ".json")
        path.write_text(json.dumps(report))
        entry = {"stage": stage, "report": path.name, "exit_code": code,
                 "execution": "clean" if code == 0 else "findings",
                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        self.manifest["stages"] = [e for e in self.manifest["stages"] if e["stage"] != stage] + [entry]
        return entry

    def evaluate(self, profile="day3", allow_fixture=True):
        self.manifest_path.write_text(json.dumps(self.manifest))
        return gate.evaluate(self.manifest_path, self.policy_path, profile, date(2026, 10, 18), allow_fixture)

    def add_high(self, line=1):
        report = copy.deepcopy(self.reports["sast"])
        report["results"] = [{"check_id": "pf-eval-input", "path": "source.ts", "start": {"line": line}, "extra": {"severity": "ERROR"}}]
        self.store("sast", report, 1)

    def approve(self, finding, expires="2026-10-25"):
        entry = {"fingerprint": finding["fingerprint"], "stage": finding["stage"],
                 "identity": {k: v for k, v in finding.items() if k not in {"severity", "fingerprint", "disposition", "content_sha256"}},
                 "baseline_file_sha256": finding.get("content_sha256"),
                 "accepted_severity": finding["severity"], "baseline_commit": self.policy["baseline_commit"],
                 "owner_role": "project-owner reviewer", "review_status": "approved",
                 "reason": "Synthetic exception-matcher contract test only; no actual owner approval or production exception.",
                 "expires_on": expires}
        self.exception_path.write_text(json.dumps({"schema_version": 1, "exceptions": [entry]}))
        return entry

    def test_clean_complete_fixture_passes(self):
        self.assertTrue(self.evaluate()["passed"])

    def test_fixture_cannot_count_as_application_acceptance(self):
        self.assertFalse(self.evaluate(allow_fixture=False)["passed"])

    def test_new_high_blocks(self):
        self.add_high()
        self.assertEqual(self.evaluate()["blocking_count"], 1)

    def test_exact_reviewed_exception_passes_and_risk_remains_visible(self):
        self.add_high()
        self.approve(self.evaluate()["findings"][0])
        result = self.evaluate()
        self.assertTrue(result["passed"])
        self.assertEqual(result["accepted_risk_count"], 1)
        self.assertEqual(len(result["findings"]), 1)

    def test_changed_location_is_not_excepted(self):
        self.add_high()
        self.approve(self.evaluate()["findings"][0])
        self.add_high(line=2)
        self.assertFalse(self.evaluate()["passed"])

    def test_same_location_changed_content_is_not_excepted(self):
        self.add_high()
        self.approve(self.evaluate()["findings"][0])
        (self.root / "source.ts").write_text("const changed = 2;\n")
        result = self.evaluate()
        self.assertFalse(result["passed"])
        self.assertEqual(result["blocking_count"], 1)

    def test_expired_exception_blocks_even_with_valid_reports(self):
        self.add_high()
        self.approve(self.evaluate()["findings"][0], "2026-10-18")
        self.assertFalse(self.evaluate()["passed"])

    def test_unreviewed_exception_blocks(self):
        self.add_high()
        entry = self.approve(self.evaluate()["findings"][0])
        entry["review_status"] = "pending"
        self.exception_path.write_text(json.dumps({"schema_version": 1, "exceptions": [entry]}))
        self.assertFalse(self.evaluate()["passed"])

    def test_exception_cannot_forge_identity(self):
        self.add_high()
        entry = self.approve(self.evaluate()["findings"][0])
        entry["identity"]["path"] = "another.ts"
        self.exception_path.write_text(json.dumps({"schema_version": 1, "exceptions": [entry]}))
        self.assertFalse(self.evaluate()["passed"])

    def test_severity_escalation_needs_new_review(self):
        report = copy.deepcopy(self.reports["sca"])
        report["Results"][0]["Vulnerabilities"] = [{"VulnerabilityID": "CVE-2021-23337", "PkgName": "lodash", "InstalledVersion": "4.17.20", "Severity": "HIGH"}]
        self.store("sca", report, 20)
        self.approve(self.evaluate()["findings"][0])
        report["Results"][0]["Vulnerabilities"][0]["Severity"] = "CRITICAL"
        self.store("sca", report, 20)
        self.assertFalse(self.evaluate()["passed"])

    def test_missing_report_blocks(self):
        (self.root / "sast.json").unlink()
        self.assertFalse(self.evaluate()["passed"])

    def test_malformed_json_with_matching_hash_blocks(self):
        path = self.root / "sast.json"
        path.write_text('{"invalid":')
        self.manifest["stages"][0]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertFalse(self.evaluate()["passed"])

    def test_modified_report_hash_blocks(self):
        (self.root / "sast.json").write_text('{}')
        self.assertFalse(self.evaluate()["passed"])

    def test_schema_valid_json_is_not_enough(self):
        self.store("sca", {"SchemaVersion": 2, "Results": []})
        self.assertFalse(self.evaluate()["passed"])

    def test_partial_sast_coverage_blocks(self):
        report = copy.deepcopy(self.reports["sast"])
        report["errors"] = [{"type": "Syntax error", "level": "warn"}]
        self.store("sast", report)
        self.assertFalse(self.evaluate()["passed"])

    def test_scanner_crash_blocks_despite_stale_valid_report(self):
        report = self.root / "sast.json"
        entry = scans.collect("sast", [sys.executable, "-c", "raise SystemExit(3)"], report, self.root,
                              scans.tool_environment(self.root), 1, timeout=5)
        self.manifest["stages"][0] = entry
        self.assertEqual(entry["execution"], "error")
        self.assertFalse(self.evaluate()["passed"])

    def test_scanner_timeout_blocks(self):
        report = self.root / "sast.json"
        entry = scans.collect("sast", [sys.executable, "-c", "import time; time.sleep(5)"], report, self.root,
                              scans.tool_environment(self.root), 1, timeout=0.05)
        self.manifest["stages"][0] = entry
        self.assertEqual(entry["exit_code"], 124)
        self.assertFalse(self.evaluate()["passed"])

    def test_missing_or_skipped_mandatory_stage_blocks(self):
        self.manifest["stages"].pop()
        self.assertFalse(self.evaluate()["passed"])
        self.store("secrets-tree", [])
        self.manifest["stages"][-1]["execution"] = "skipped"
        self.assertFalse(self.evaluate()["passed"])

    def test_full_pipeline_cannot_pass_before_later_stages_exist(self):
        self.assertFalse(self.evaluate("full")["passed"])

    def test_shallow_history_blocks(self):
        self.manifest["full_history"] = False
        self.assertFalse(self.evaluate()["passed"])

    def test_development_dependency_coverage_must_be_declared(self):
        self.manifest.pop("dependency_scope")
        self.assertFalse(self.evaluate()["passed"])

    def test_unknown_severity_blocks(self):
        report = copy.deepcopy(self.reports["sast"])
        report["results"] = [{"check_id": "pf-rule", "path": "source.ts", "start": {"line": 1}, "extra": {"severity": "NEW_SEVERITY"}}]
        self.store("sast", report, 1)
        self.assertFalse(self.evaluate()["passed"])

    def test_report_symlink_escape_blocks(self):
        outside = self.root.parent / (self.root.name + "-outside.json")
        outside.write_text(json.dumps(self.reports["sast"]))
        self.addCleanup(outside.unlink)
        (self.root / "sast.json").unlink()
        (self.root / "sast.json").symlink_to(outside)
        self.assertFalse(self.evaluate()["passed"])

    def test_raw_match_and_contact_fields_never_reach_gate_output(self):
        canary = "SYNTHETIC_PRIVATE_MATCH_NOT_FOR_PUBLICATION"
        report = [{"RuleID": "github-pat", "File": "fixture.txt", "StartLine": 1,
                   "Match": canary, "Secret": canary, "Author": "Synthetic fixture",
                   "Email": "fixture@example.invalid", "Commit": "a" * 40}]
        self.store("secrets-history", report, 20)
        result = self.evaluate()
        serialized = json.dumps(result)
        self.assertNotIn(canary, serialized)
        self.assertNotIn("fixture@example.invalid", serialized)
        self.assertNotIn("Synthetic fixture", serialized)
        self.assertEqual(result["blocking_count"], 1)

    def test_exception_from_another_baseline_blocks(self):
        self.add_high()
        entry = self.approve(self.evaluate()["findings"][0])
        entry["baseline_commit"] = "b" * 40
        self.exception_path.write_text(json.dumps({"schema_version": 1, "exceptions": [entry]}))
        self.assertFalse(self.evaluate()["passed"])


if __name__ == "__main__":
    unittest.main()
