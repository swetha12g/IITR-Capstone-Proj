#!/usr/bin/env python3
"""Run the fail-closed gate contract tests and write a sanitized result."""
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import unittest

root = Path(__file__).resolve().parents[1]
private = root / "reports/private/day3"
private.mkdir(parents=True, exist_ok=True)
stream = io.StringIO()
suite = unittest.defaultTestLoader.discover(str(root / "tests/day3"))
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
(private / "gate-tests.log").write_text(stream.getvalue())
summary = {"observed_at_utc": datetime.now(timezone.utc).isoformat(), "tests": result.testsRun,
           "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
           "passed": result.wasSuccessful(), "scope": "synthetic fail-closed contracts; not an application detection metric"}
public = root / "reports/sanitized/day3"
public.mkdir(parents=True, exist_ok=True)
(public / "gate-tests.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
raise SystemExit(0 if summary["passed"] else 1)
