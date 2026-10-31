#!/usr/bin/env python3
"""Validate scanner execution and apply exact, reviewed, expiring risk exceptions."""
import argparse
from collections import Counter
from datetime import datetime, date
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


class InvalidReport(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise InvalidReport(code)


def read_json(path):
    return json.loads(path.read_text(), parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))


def identifier(value):
    require(isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z0-9_.:/@+~-]{1,250}", value)), "invalid-identifier")
    return value


def source_path(value, base=ROOT):
    require(isinstance(value, str) and value and ".." not in Path(value).parts
            and not any(c in value for c in "\r\n\x00"), "invalid-source-path")
    if Path(value).is_absolute():
        require(Path(value).is_relative_to(base), "source-path-outside-scan-root")
        value = str(Path(value).relative_to(base))
    # Never publish a contact-like path, even if a historical filename contains it.
    require(not re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", value), "contact-in-source-path")
    return value.removeprefix("./")


def normalize(stage, report, policy, base=ROOT):
    findings = []
    if stage == "sast":
        require(isinstance(report, dict) and isinstance(report.get("version"), str)
                and isinstance(report.get("results"), list) and isinstance(report.get("errors"), list), "invalid-sast-schema")
        require(not report["errors"], "sast-coverage-error")
        require(isinstance(report.get("paths", {}).get("scanned"), list) and report["paths"]["scanned"], "sast-no-scanned-files")
        for item in report["results"]:
            severity = item["extra"]["severity"]
            require(severity in policy["semgrep_severities"], "unmapped-sast-severity")
            line = item["start"]["line"]
            require(type(line) is int and line > 0, "invalid-source-line")
            findings.append({"stage": stage, "rule": identifier(item["check_id"]),
                             "path": source_path(item["path"], base), "line": line,
                             "severity": policy["semgrep_severities"][severity]})
    elif stage == "sca":
        require(isinstance(report, dict) and report.get("SchemaVersion") == 2
                and isinstance(report.get("Results"), list) and report["Results"], "invalid-sca-schema")
        require(any(r.get("Type") == "npm" for r in report["Results"]), "sca-no-npm-analysis")
        for result in report["Results"]:
            for item in result.get("Vulnerabilities") or []:
                severity = item["Severity"]
                require(severity in {"UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL"}, "unmapped-sca-severity")
                findings.append({"stage": stage, "rule": identifier(item["VulnerabilityID"]),
                                 "path": source_path(result["Target"]),
                                 "component": identifier(item["PkgName"]),
                                 "version": identifier(item["InstalledVersion"]), "severity": severity})
    elif stage in {"secrets-history", "secrets-tree"}:
        require(isinstance(report, list), "invalid-secrets-schema")
        for item in report:
            line = item["StartLine"]
            require(type(line) is int and line > 0, "invalid-source-line")
            finding = {"stage": stage, "rule": identifier(item["RuleID"]),
                       "path": source_path(item["File"], base), "line": line,
                       "severity": policy["secrets_severity"]}
            if stage == "secrets-history":
                commit = item["Commit"]
                require(isinstance(commit, str) and re.fullmatch(r"[a-f0-9]{40,64}", commit), "invalid-history-commit")
                finding["commit"] = commit
            findings.append(finding)
    else:
        raise InvalidReport("stage-not-implemented")
    unique = {}
    for finding in findings:
        # Severity can change with DB/rule updates without changing finding identity.
        identity = {k: v for k, v in finding.items() if k != "severity"}
        fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        finding["fingerprint"] = fingerprint
        if stage != "secrets-history":
            source = (base / finding["path"]).resolve()
            require(source.is_relative_to(base.resolve()) and source.is_file(), "finding-source-unavailable-or-unsafe")
            finding["content_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        unique[fingerprint] = finding
    return sorted(unique.values(), key=lambda f: f["fingerprint"])


def evaluate(manifest_path, policy_path, profile="day3", as_of=None, allow_fixture=False):
    today = as_of or datetime.now(ZoneInfo("Asia/Kolkata")).date()
    errors, findings = [], []
    result = {"schema_version": 1, "profile": profile, "evaluated_on": today.isoformat(),
              "passed": False, "operational_errors": errors, "findings": findings}
    try:
        policy = read_json(policy_path)
        require(policy.get("schema_version") == 1 and profile in policy["profiles"], "invalid-gate-policy")
        require(bool(re.fullmatch(r"[a-f0-9]{40}", policy["baseline_commit"])), "invalid-baseline-commit")
        stages = policy["profiles"][profile]
        require(isinstance(stages, list) and stages and len(stages) == len(set(stages)), "invalid-required-stages")
        exception_path = (policy_path.parent / policy["exceptions_file"]).resolve()
        require(exception_path.is_relative_to(policy_path.parent.resolve()), "exception-path-escape")
        exceptions = read_json(exception_path)
        require(exceptions.get("schema_version") == 1 and isinstance(exceptions.get("exceptions"), list), "invalid-exception-schema")
        approved = {}
        for item in exceptions["exceptions"]:
            require(isinstance(item, dict) and bool(re.fullmatch(r"[a-f0-9]{64}", item.get("fingerprint", ""))), "invalid-exception-fingerprint")
            require(item["fingerprint"] not in approved, "duplicate-exception")
            require(item.get("baseline_commit") == policy["baseline_commit"], "exception-baseline-mismatch")
            require(item.get("owner_role") == policy["exception_owner_role"] and item.get("review_status") == "approved"
                    and isinstance(item.get("reason"), str) and len(item["reason"]) >= 10, "exception-not-reviewed")
            require(date.fromisoformat(item["expires_on"]) > today, "expired-exception")
            require(item.get("stage") in stages and isinstance(item.get("identity"), dict), "invalid-exception-identity")
            require(hashlib.sha256(json.dumps(item["identity"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
                    == item["fingerprint"], "exception-fingerprint-identity-mismatch")
            approved[item["fingerprint"]] = item
        manifest = read_json(manifest_path)
        require(manifest.get("schema_version") == 1 and isinstance(manifest.get("stages"), list), "invalid-manifest-schema")
        scope = manifest.get("scope")
        require(scope == "application" or (scope == "synthetic-fixture" and allow_fixture), "non-application-scan")
        result["scope"] = scope
        require(manifest.get("dependency_scope") == "production-and-development" or "sca" not in stages, "development-dependency-coverage-unconfirmed")
        require(manifest.get("full_history") is True or "secrets-history" not in stages, "shallow-history")
        observed = {}
        for entry in manifest["stages"]:
            require(isinstance(entry, dict) and isinstance(entry.get("stage"), str), "invalid-stage-manifest")
            require(entry["stage"] not in observed, "duplicate-stage")
            observed[entry["stage"]] = entry
        for stage in stages:
            try:
                require(stage in observed, "mandatory-stage-missing")
                entry = observed[stage]
                require(entry.get("execution") in {"clean", "findings"}, "scanner-execution-failed-or-skipped")
                code = entry.get("exit_code")
                allowed_codes = {0, 1} if stage == "sast" else {0, 20}
                require(type(code) is int and code in allowed_codes, "scanner-execution-exit-code")
                require(entry["execution"] == ("clean" if code == 0 else "findings"), "execution-exit-mismatch")
                path = (manifest_path.parent / entry["report"]).resolve()
                require(path.is_relative_to(manifest_path.parent.resolve()), "report-path-escape")
                require(path.is_file(), "report-missing")
                require(hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], "report-hash-mismatch")
                base = manifest_path.parent / "working-tree" if stage == "secrets-tree" else (
                    Path(manifest["source_root"]) if scope == "synthetic-fixture" else ROOT / "app/juice-shop" if stage == "sca" else ROOT)
                found = normalize(stage, read_json(path), policy, base)
                require(bool(found) == (code != 0), "findings-exit-mismatch")
                findings.extend(found)
            except (InvalidReport, KeyError, TypeError, ValueError, OSError) as error:
                errors.append({"stage": stage, "code": str(error) if isinstance(error, InvalidReport) else "invalid-or-unreadable-report"})
        for finding in findings:
            item = approved.get(finding["fingerprint"])
            if item:
                identity = {k: v for k, v in finding.items() if k not in {"severity", "fingerprint", "content_sha256"}}
                require(item["identity"] == identity and item["stage"] == finding["stage"], "exception-identity-mismatch")
                require(item.get("accepted_severity") == finding["severity"], "exception-severity-changed")
                if finding["stage"] != "secrets-history" and item.get("baseline_file_sha256") != finding.get("content_sha256"):
                    item = None
                    finding["exception_status"] = "source-or-lock-content-changed"
            finding["disposition"] = "accepted-baseline-risk" if item else (
                "blocking" if finding["severity"] in policy["blocking_severities"] else "visible-nonblocking")
        result["baseline_commit"] = policy["baseline_commit"]
        result["severity_counts"] = dict(Counter(f["severity"] for f in findings))
        result["blocking_count"] = sum(f["disposition"] == "blocking" for f in findings)
        result["accepted_risk_count"] = sum(f["disposition"] == "accepted-baseline-risk" for f in findings)
        result["passed"] = not errors and result["blocking_count"] == 0
    except (InvalidReport, KeyError, TypeError, ValueError, OSError) as error:
        errors.append({"stage": "policy-or-manifest", "code": str(error) if isinstance(error, InvalidReport) else "invalid-policy-or-manifest"})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--policy", type=Path, default=Path("policies/gates.json"))
    parser.add_argument("--profile", default="day3", choices=["day3", "full"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate(args.manifest.resolve(), args.policy.resolve(), args.profile)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "findings"}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
