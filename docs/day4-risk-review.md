# Day 4 residual risks — deferred for study work

Observed 22 October 2026. **The user explicitly directed deferring these findings and continuing the full study assignment.** The `study-lab` profile records findings without stopping assignment work; the separate `strict` profile retains the original security verdict. This is a lab execution decision, not remediation or production approval. Scanner failures, missing evidence and invalid reports remain execution errors. The earlier Day 3 source-exception file is preserved.

The strict Day 4 assessment identifies **39 distinct findings** with zero operational errors; the study profile carries them as deferred:

| Group | Count | Meaning / next action |
|---|---:|---|
| NetworkPolicy control, CKV2_K8S_6 | 1 | Workload has no declared policy and enforcement is unverified. Plan and test a policy-capable lab network; an untested YAML-only pass would not establish isolation |
| Container HIGH | 27 | Known vulnerable package versions remain in the exact hardened image. Review exact advisory/fixed-version records privately, then patch with behavior checks or make an explicit bounded lab risk decision |
| Container CRITICAL | 11 | Same review requirement; hardening the runtime does not remediate application dependencies |

The hardened image has 100 visible vulnerability identities in total: 11 critical, 27 high, 51 medium and 11 low. Comparison with the baseline under one frozen DB removes one unknown-severity CA-certificate advisory, adds zero new identities and retains the other 100. Do not describe the retained 38 high/critical identities as fixed or assume that source-stage acceptance covers container-stage evidence.

Exact container fingerprints, the remaining IaC identity, image IDs, DB metadata and raw-report/SBOM hashes are retained in the sanitized gate/scan manifests. Advisory/package/fix details are in an ignored local review packet under `reports/private/day4/residual-risk-review.md`; raw scanner reports and the full SBOM remain private. No signature, credential, raw source match or personal contact information is included in this record.

Next: continue Days 5–10 and keep these identities in the deferred-risk register. Address remediation after the assignment implementation, as directed. Never describe a study-profile pass as a clean security assessment. Hosted Day 4 CI and Day 5 DAST/aggregate integration have not yet run.
