# Reproducing the study pipeline

Use a separate full-history clone of the reviewed integration commit on Linux x86_64 with Python 3.10, Bash, curl, Git and a reachable Docker daemon. Allow outbound access to the pinned distributions, package registries, base images and vulnerability database. The script installs tools within the project; it does not install system packages or change host kernel/network settings.

```bash
bash scripts/reproduce.sh
```

The script bootstraps pinned Node/Python tooling, installs verified scanners, runs the application offline profile and control tests, rebuilds the allowlisted image, executes all six scanner stages, runs the owned temporary Kubernetes lab and passive ZAP, normalizes the findings and regenerates the mock triage/dashboard. The nine external-service availability tests are excluded explicitly. Application defects and scanner/cluster failures are not suppressed.

Each run creates a unique kind cluster and a private kubeconfig. Finalization deletes only that cluster and verifies no owned node container remains. Check `reports/sanitized/reproduction/run.json` and private reproduction logs. Failed setup is a failed reproduction, even when security findings are deferred. The original study cluster is separate.

No external AI credential, live API call, purchase or top-up is part of reproduction. Public evidence contains only sanitized counts, identities and hashes; raw scans, full SBOMs and alias maps remain ignored. Historical before/after image comparison is separate from the current fresh-run receipts. Database updates may change vulnerability counts without changing source.

For report generation, create a separate environment with `locks/report-requirements.txt`, then run `python scripts/generate-report.py` and render every page with Poppler. PDF tooling is not needed to run the security pipeline.

## Verified fresh-directory runs

The latest full run at commit `1e0115c14c85fd28332d85151b7ec560b8837c91`, run `20261022T155913232877Z`, passed with deferred risks and zero operational errors. The full pipeline commands took 286.23 seconds, including a freshly executed 156.59-second application sequence; bootstrap/download/setup time is additional. All scanner stages, different-UID write probes, bad/fixed DAST fixtures, workload checks, mock triage and dashboard completed. Cleanup verified removal of the uniquely owned temporary cluster. [Bound receipt](../reports/sanitized/reproduction/run.json).

This uses a new full-history directory and tool environments on the same Docker host with standard caches; it is not a fresh-machine result. Earlier Python activation could remove the repository's Kubernetes-tool PATH entry and fall back to the same pinned user-local versions. The later clean-PATH run below verifies the correction. Initial package-index unavailability was retained privately; retry succeeded with unchanged hash-pinned distributions. Later code separates cold image acquisition from the short permission probe and increases SAST's bounded per-rule/file time. Final hosted verification passes with those corrections.

The earlier full run at `6ef16a0` passed in 268.94 seconds and is retained under [historical reproduction evidence](../reports/sanitized/reproduction/history/6ef16a0/run.json). No live API calls, purchases, billing changes or original-cluster changes occurred in either run.

## Verified clean-PATH run

At `bef666437f60416fed4d5bceed675c2a6d8513af`, `env PATH=/usr/bin:/bin /bin/bash scripts/reproduce.sh` passed from the existing project directory. Node, kind and kubectl resolve within this repository after environment activation. This is a portability check on the same host, not a third fresh-directory or fresh-machine claim.

Run `20261022T171521035420Z` completed the full pipeline in 252.36 seconds, without build/test reuse; application steps total 158.45 seconds (the enclosing application command took 158.72 seconds). All six scanner stages, 62 current contracts, different-UID and bad/fixed DAST fixtures, mock triage and dashboard passed; temporary-cluster cleanup was verified. [Receipt](../reports/sanitized/reproduction/clean-path-run.json), [aggregate](../reports/sanitized/pipeline/aggregate.json). Setup/download/cluster-creation time is additional.

Its dashboard has 371 observations / 234 underlying issues; the historical fresh-directory results have 372 / 235. A medium passive alert-instance variation explains the difference; no fix is inferred. Final [hosted run 39821125926](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39821125926) also passed all eight jobs at the same code revision, with downloaded artifact integrity and aggregate recomputation verified.

## Critical-remediation variant — current local proof

The subsequent repair changes application source/root dependencies and enforces a zero-critical gate. Run `20261022T181348556832Z` passed all stages with zero critical findings and cleanup in an owned temporary cluster. It used the existing directory and explicitly reused a fresh six-step application check (143.51 seconds) and rebuilt image; scans/runtime took 93.19 seconds separately. The source tree is hash-bound despite being uncommitted. The owned original study deployment was then updated and verified against the same image. [Complete repair receipt](../reports/sanitized/critical-remediation/verification.json).

The earlier fresh-directory/clean-PATH results above predate these fixes. New hosted CI and a fresh checkout of a published remediation revision are not yet claimed. The current frontend lock and original exact source approvals are unchanged; the root lock is intentionally updated. No live API call or purchase is required by reproduction.
