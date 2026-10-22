# Reproducing the study pipeline

Use a separate full-history clone of the reviewed integration commit on Linux x86_64 with Python 3.10, Bash, curl, Git and a reachable Docker daemon. Allow outbound access to the pinned distributions, package registries, base images and vulnerability database. The script installs tools within the project; it does not install system packages or change host kernel/network settings.

```bash
bash scripts/reproduce.sh
```

The script bootstraps pinned Node/Python tooling, installs verified scanners, runs the application offline profile and control tests, rebuilds the allowlisted image, executes all six scanner stages, runs the owned temporary Kubernetes lab and passive ZAP, normalizes the findings and regenerates the mock triage/dashboard. The nine external-service availability tests are excluded explicitly. Application defects and scanner/cluster failures are not suppressed.

Each run creates a unique kind cluster and a private kubeconfig. Finalization deletes only that cluster and verifies no owned node container remains. Check `reports/sanitized/reproduction/run.json` and private reproduction logs. Failed setup is a failed reproduction, even when security findings are deferred. The original study cluster is separate.

No external AI credential, live API call, purchase or top-up is part of reproduction. Public evidence contains only sanitized counts, identities and hashes; raw scans, full SBOMs and alias maps remain ignored. Historical before/after image comparison is separate from the current fresh-run receipts. Database updates may change vulnerability counts without changing source.

For report generation, create a separate environment with `locks/report-requirements.txt`, then run `python scripts/generate-report.py` and render every page with Poppler. PDF tooling is not needed to run the security pipeline.

## Verified fresh-directory run

Commit `6ef16a09d9c60ab5b78136f3430590fcefba8d7a`, run `20261022T152803854522Z`: PASS_WITH_DEFERRED_RISKS, zero operational errors and verified temporary-cluster removal. The full pipeline commands took 268.94 seconds, including all six fresh application stages (154.47 seconds). Bootstrap/download/setup time is additional. This used a new full-history directory and project-local tool environments on the same Docker host with standard caches; it is not a fresh-machine result. The later isolated DAST header fixture at `bc5a054` was verified separately and is included in the latest reproduction script. [Bound evidence](../reports/sanitized/reproduction/run.json).
