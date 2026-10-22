#!/usr/bin/env python3
"""Run the pinned application's Day 1 checks and retain sanitized evidence."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app/juice-shop"
STEPS = {
    "install-server": ["npm", "ci", "--no-audit", "--no-fund"],
    "install-frontend": ["npm", "--prefix", "frontend", "ci", "--no-audit", "--no-fund"],
    "build": ["npm", "run", "build"],
    "test-frontend": ["npm", "run", "test:frontend:coverage"],
    "test-server": ["npm", "run", "test:server"],
    "test-api": ["npm", "run", "test:api"],
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", nargs="+", choices=STEPS, default=list(STEPS))
    parser.add_argument("--offline", action="store_true", help="Exclude the independent internet-resource availability suite; keep all local application tests")
    args = parser.parse_args()
    node = subprocess.check_output(["node", "--version"], text=True).strip()
    npm = subprocess.check_output(["npm", "--version"], text=True).strip()
    if node != "v24.22.0" or npm != "11.19.1":
        parser.error("Run 'source scripts/dev-env.sh' to select pinned Node/npm.")
    if not (APP / "package.json").is_file():
        parser.error("Import the verified source before running checks.")

    locks = {
        ROOT / "locks/juice-shop/package-lock.json": APP / "package-lock.json",
        ROOT / "locks/juice-shop/frontend-package-lock.json": APP / "frontend/package-lock.json",
    }
    for source, destination in locks.items():
        if not source.is_file():
            parser.error("Recorded dependency lockfiles are missing.")
        shutil.copyfile(source, destination)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    private = ROOT / "reports/private/day1" / run_id
    private.mkdir(parents=True, exist_ok=False)
    sanitized = ROOT / "reports/sanitized"
    sanitized.mkdir(parents=True, exist_ok=True)
    report_path = sanitized / f"day1-{run_id}.json"
    report = {
        "run_id": run_id,
        "source_commit": "f189f521266f42c6bd05884468292000cee852ed",
        "node_version": node,
        "npm_version": npm,
        "selected_steps": args.steps,
        "steps": [],
        "status": "running",
        "profile": "offline-local" if args.offline else "upstream-finite",
        "external_availability_suite": "not-selected" if args.offline else "selected",
    }
    env = os.environ.copy()
    env.update({"CI": "true", "CYPRESS_INSTALL_BINARY": "0",
                "npm_config_audit": "false", "npm_config_fund": "false"})
    env.setdefault("NODE_OPTIONS", "--max-old-space-size=8192")
    env.setdefault("NG_BUILD_MAX_WORKERS", "2")

    def save():
        text = json.dumps(report, indent=2) + "\n"
        report_path.write_text(text)
        (sanitized / "day1-latest.json").write_text(text)

    save()
    for step in args.steps:
        command = STEPS[step]
        if args.offline and step == "test-api":
            files = sorted(str(p.relative_to(APP)) for p in (APP / "test/api").rglob("*.test.ts") if p.name != "internet-resources.test.ts")
            if not files:
                raise ValueError("No local API test files selected")
            command = ["node", "--import", "./test/api/helpers/test-env.mjs", "--import", "tsx",
                       "--test", "--test-force-exit", *files]
        log_path = private / f"{step}.log"
        started = datetime.now(timezone.utc).isoformat()
        before = time.monotonic()
        print(f"Starting {step}; output retained in ignored private evidence.", flush=True)
        with log_path.open("w") as log:
            process = subprocess.Popen(command, cwd=APP, env=env, stdout=log,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = process.wait(timeout=1800)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                code = 124
        report["steps"].append({
            "step": step, "command": command, "started_at_utc": started,
            "duration_seconds": round(time.monotonic() - before, 2),
            "exit_code": code, "log_reference": str(log_path.relative_to(ROOT)),
            "log_sha256": sha256(log_path),
        })
        save()
        print(f"Finished {step}: exit {code}.", flush=True)
        if code and step in {"install-server", "install-frontend", "build"}:
            break

    report["locks_unchanged"] = all(sha256(a) == sha256(b) for a, b in locks.items())
    passed = (len(report["steps"]) == len(args.steps)
              and all(s["exit_code"] == 0 for s in report["steps"])
              and report["locks_unchanged"])
    report["status"] = "passed" if passed else "failed"
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    save()
    print(f"Run {report['status']}; evidence: {report_path.relative_to(ROOT)}.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
