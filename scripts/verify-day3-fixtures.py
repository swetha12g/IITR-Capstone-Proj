#!/usr/bin/env python3
"""Prove scanner and gate behavior with isolated, non-executed synthetic inputs."""
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import random
import shutil
import string
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


scans = module("scans", "run-scans.py")
gate = module("gate", "gate.py")


def git(repo, *args):
    return subprocess.check_output(["git", "-c", "user.name=Synthetic fixture", "-c",
                                    "user.email=fixture@example.invalid", "-C", str(repo), *args], stderr=subprocess.DEVNULL)


def lock(repo, version):
    (repo / "package.json").write_text(json.dumps({"name": "isolated-scanner-fixture", "version": "0.0.0", "dependencies": {"lodash": version}}))
    (repo / "package-lock.json").write_text(json.dumps({"name": "isolated-scanner-fixture", "version": "0.0.0", "lockfileVersion": 3,
        "requires": True, "packages": {"": {"name": "isolated-scanner-fixture", "version": "0.0.0", "dependencies": {"lodash": version}},
        "node_modules/lodash": {"version": version, "resolved": "https://registry.npmjs.org/lodash/-/lodash-" + version + ".tgz"}}}))


BAD = """import {exec} from 'node:child_process'
db.query(`SELECT name FROM demo WHERE name = '${input}'`)
eval(input)
exec(input)
crypto.createHash('md5')
https.request({rejectUnauthorized: false})
jwt.decode(input)
"""
FIXED = """import {execFile} from 'node:child_process'
db.query('SELECT name FROM demo WHERE name = ?', {replacements: [input]})
JSON.parse(input)
execFile('/usr/bin/printf', ['%s', input])
crypto.createHash('sha256')
https.request({rejectUnauthorized: true})
jwt.verify(input, publicKey)
"""


def run_case(root, repo, label):
    private = root / label
    private.mkdir()
    env = scans.tool_environment(private)
    # A dedicated fixture snapshot avoids reading project/private credential files.
    for name in ["source.ts", "package.json", "package-lock.json", "canary.txt"]:
        target = private / "working-tree" / name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(repo / name, target)
    manifest = {"schema_version": 1, "scope": "synthetic-fixture", "source_root": str(repo), "full_history": True,
                "dependency_scope": "production-and-development", "stages": []}
    for stage, command, code in scans.commands(private, repo, repo, fixture=True):
        manifest["stages"].append(scans.collect(stage, command, private / (stage + ".json"), private, env, code))
    path = private / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    result = gate.evaluate(path, root / "fixture-gates.json", allow_fixture=True)
    (private / "gate.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    root = ROOT / "reports/private/day3" / ("fixtures-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    repo = root / "application"
    repo.mkdir(parents=True)
    policy = json.loads((ROOT / "policies/gates.json").read_text())
    policy["exceptions_file"] = "fixture-exceptions.json"
    (root / "fixture-gates.json").write_text(json.dumps(policy))
    (root / "fixture-exceptions.json").write_text(json.dumps({"schema_version": 1, "exceptions": []}))
    git(repo, "init", "--quiet")
    fixed_version = "4.18.1"
    (repo / "source.ts").write_text(FIXED)
    (repo / "canary.txt").write_text("No credential material.\n")
    lock(repo, fixed_version)
    git(repo, "add", ".")
    git(repo, "commit", "--quiet", "-m", "Synthetic clean fixture")
    # Generated only in ignored private fixtures; never valid or tested against a service.
    canary = "gh" + "p_" + "".join(random.Random(481516).choices(string.ascii_letters + string.digits, k=36))
    (repo / "source.ts").write_text(BAD)
    (repo / "canary.txt").write_text('github_token = "' + canary + '"\n')
    lock(repo, "4.17.20")
    bad = run_case(root, repo, "bad")
    rules = {f["rule"].split(".")[-1] for f in bad["findings"] if f["stage"] == "sast"}
    expected_rules = {"pf-sql-template-query", "pf-eval-input", "pf-shell-command", "pf-weak-md5", "pf-tls-validation-disabled", "pf-jwt-decode"}
    assert not bad["passed"] and not bad["operational_errors"]
    assert rules == expected_rules, "Every authored source rule must detect its bad pattern"
    assert any(f["stage"] == "sca" and f["rule"] == "CVE-2021-23337" for f in bad["findings"])
    assert any(f["stage"] == "secrets-tree" and f["rule"] == "github-pat" for f in bad["findings"])
    assert canary not in json.dumps(bad), "Synthetic match leaked into safe gate output"
    (repo / "source.ts").write_text(FIXED)
    (repo / "canary.txt").write_text("Synthetic canary removed.\n")
    lock(repo, fixed_version)
    fixed = run_case(root, repo, "fixed")
    assert fixed["passed"] and not fixed["findings"] and not fixed["operational_errors"]
    # Removing a historical secret is not equivalent to removing it from Git history.
    (repo / "canary.txt").write_text('github_token = "' + canary + '"\n')
    git(repo, "add", ".")
    git(repo, "commit", "--quiet", "-m", "Synthetic historical canary")
    (repo / "canary.txt").write_text("Synthetic canary removed.\n")
    git(repo, "add", ".")
    git(repo, "commit", "--quiet", "-m", "Synthetic working-tree repair")
    history = run_case(root, repo, "history-persists")
    assert not history["passed"] and not history["operational_errors"]
    assert any(f["stage"] == "secrets-history" for f in history["findings"])
    assert not any(f["stage"] == "secrets-tree" for f in history["findings"])
    assert canary not in json.dumps(history)
    public = ROOT / "reports/sanitized/day3"
    public.mkdir(parents=True, exist_ok=True)
    summary = {"observed_at_utc": datetime.now(timezone.utc).isoformat(), "scope": "isolated synthetic fixtures only; no source executed or real credential used",
               "bad": {"gate_passed": False, "all_six_source_rules_detected": True, "advisory_detected": "CVE-2021-23337", "secret_rule_detected": "github-pat"},
               "fixed": {"gate_passed": True, "findings": 0, "lodash_version": fixed_version},
               "history_persists_after_working_tree_fix": True, "synthetic_canary_absent_from_safe_outputs": True,
               "advisory_reference": "https://github.com/advisories/GHSA-35jh-r3h4-6jhm",
               "fixture_exception_approval": "none required or used; clean history in bad/fixed pair, separate history-retention probe remains blocked"}
    (public / "fixture-evidence.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
