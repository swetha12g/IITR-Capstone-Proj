#!/usr/bin/env python3
"""Collect all Day 3 scanner reports; findings and operational failure stay distinct."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / ".tools/day3"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tool_environment(private):
    env = os.environ.copy()
    home = private / "tool-home"
    home.mkdir(parents=True, exist_ok=True)
    env.update({"HOME": str(home), "DOCKER_CONFIG": str(home / ".docker"),
                "SEMGREP_SETTINGS_FILE": str(home / "semgrep-settings.yml"),
                "SEMGREP_SEND_METRICS": "off", "SEMGREP_ENABLE_VERSION_CHECK": "0",
                "SEMGREP_APP_TOKEN": "", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_NOSYSTEM": "1"})
    for key in ["TRIVY_USERNAME", "TRIVY_PASSWORD", "TRIVY_TOKEN", "GITLEAKS_CONFIG", "GITLEAKS_CONFIG_TOML"]:
        env.pop(key, None)
    return env


def snapshot(destination):
    names = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
    copied = []
    for name in sorted(set(filter(None, names))):
        source = ROOT / name
        if not source.exists():
            continue
        if source.is_symlink() or not source.resolve().is_relative_to(ROOT):
            raise ValueError("unsafe working-tree link")
        if not source.is_file():
            continue
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        copied.append(name)
    if not copied:
        raise ValueError("empty working-tree snapshot")
    return copied


def collect(stage, command, report, private, env, finding_code, timeout=900):
    started = datetime.now(timezone.utc).isoformat()
    before = time.monotonic()
    log = private / (stage + ".log")
    code = 127
    try:
        with log.open("wb") as output:
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                code = 124
    except OSError:
        code = 127
    entry = {"stage": stage, "command": command, "started_at_utc": started,
             "finished_at_utc": datetime.now(timezone.utc).isoformat(),
             "duration_seconds": round(time.monotonic() - before, 2), "exit_code": code,
             "execution": "clean" if code == 0 else "findings" if code == finding_code else "error",
             "report": str(report.relative_to(private)),
             "sha256": digest(report) if report.is_file() else None,
             "log_sha256": digest(log) if log.is_file() else None}
    print(json.dumps({k: entry[k] for k in ["stage", "exit_code", "execution", "duration_seconds"]}), flush=True)
    return entry


def commands(private, target, history_repo, fixture=False):
    semgrep = [str(TOOLS / "semgrep/bin/semgrep"), "scan", "--config", str(ROOT / "policies/semgrep/source.yml"),
               "--metrics=off", "--disable-version-check", "--disable-nosem", "--no-git-ignore",
               "--project-root", str(target if fixture else ROOT),
               "--error", "--strict", "--jobs", "2", "--json-output", str(private / "sast.json")]
    for name in ["node_modules", "build", "dist", "coverage", ".angular"]:
        semgrep += ["--exclude", "**/" + name + "/**"]
    semgrep.append(str(target))
    trivy = [str(TOOLS / "trivy"), "fs", "--scanners", "vuln", "--exit-code", "20", "--format", "json",
             "--output", str(private / "sca.json"), "--cache-dir", str(TOOLS / "trivy-cache"),
             "--ignorefile", os.devnull, "--list-all-pkgs", "--timeout", "15m"]
    for name in ["node_modules", "build", "dist", "coverage", ".angular"]:
        trivy += ["--skip-dirs", "**/" + name]
    trivy.append(str(target))
    common = ["--config", str(ROOT / "policies/gitleaks.toml"), "--redact=100", "--exit-code", "20",
              "--ignore-gitleaks-allow", "--gitleaks-ignore-path", str(private / "no-ignore-file"),
              "--report-format", "json", "--no-banner"]
    history = [str(TOOLS / "gitleaks"), "git", str(history_repo), "--log-opts=--all", *common,
               "--report-path", str(private / "secrets-history.json")]
    tree = [str(TOOLS / "gitleaks"), "dir", str(private / "working-tree"), *common,
            "--report-path", str(private / "secrets-tree.json")]
    return [("sast", semgrep, 1), ("sca", trivy, 20), ("secrets-history", history, 20), ("secrets-tree", tree, 20)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    private = (args.output_dir or ROOT / "reports/private/day3" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")).resolve()
    private.mkdir(parents=True, exist_ok=False)
    env = tool_environment(private)
    lock_inputs = {}
    for source, destination in [(ROOT / "locks/juice-shop/package-lock.json", ROOT / "app/juice-shop/package-lock.json"),
                                (ROOT / "locks/juice-shop/frontend-package-lock.json", ROOT / "app/juice-shop/frontend/package-lock.json")]:
        if destination.exists() and digest(destination) != digest(source):
            raise RuntimeError("Application lock differs from the recorded baseline; existing local file preserved")
        if not destination.exists():
            shutil.copyfile(source, destination)
        lock_inputs[str(source.relative_to(ROOT))] = digest(source)
    shallow = subprocess.check_output(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, env=env, text=True).strip() == "true"
    manifest = {"schema_version": 1, "scope": "application", "run_id": private.name,
                "started_at_utc": datetime.now(timezone.utc).isoformat(),
                "target_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "full_history": not shallow, "lock_inputs": lock_inputs, "stages": []}
    path = private / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    for stage, command, finding_code in commands(private, ROOT / "app/juice-shop", ROOT):
        if stage == "secrets-tree":
            try:
                manifest["working_tree_files"] = len(snapshot(private / "working-tree"))
            except (ValueError, OSError):
                manifest["stages"].append({"stage": stage, "execution": "error", "exit_code": 125})
                continue
        entry = collect(stage, command, private / (stage + ".json"), private, env, finding_code)
        manifest["stages"].append(entry)
        path.write_text(json.dumps(manifest, indent=2) + "\n")
    manifest["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    # This summary deliberately excludes commands, raw logs, source, and matches.
    safe = {k: manifest[k] for k in ["schema_version", "scope", "run_id", "target_commit", "full_history", "started_at_utc", "finished_at_utc"]}
    safe["stages"] = [{k: s.get(k) for k in ["stage", "execution", "exit_code", "duration_seconds", "sha256", "log_sha256"]} for s in manifest["stages"]]
    safe["lock_inputs"] = lock_inputs
    public = ROOT / "reports/sanitized/day3"
    public.mkdir(parents=True, exist_ok=True)
    (public / "scan-execution.json").write_text(json.dumps(safe, indent=2) + "\n")
    (ROOT / "reports/private/day3/latest-manifest.txt").write_text(str(path) + "\n")
    print("Raw manifest retained privately; gate evaluation is a separate command.")
    return 0 if all(s["execution"] in {"clean", "findings"} for s in manifest["stages"]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
