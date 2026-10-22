# Evidence index

Local raw installation/build/test output is retained under ignored `reports/private/`. Hosted runner private files are discarded after the job; only sanitized records and selected failure diagnostics are published. Public records contain sanitized status, counts, identifiers, timestamps, and checksums only. No credentials, personal contact details, or raw findings belong here.

| ID | Date | Evidence | Verdict / limitation |
|---|---|---|---|
| ENV-20261016 | 16 October 2026 | [Day 1 checkpoint](day1-checkpoint.md), published closeout `a172539` / `3bea933` | Basic setup passed; build/tests deferred |
| ENV-20261017 | 17 October 2026 | [Versions](versions.md), [execution log](daily-log.md#execution-on-17-october-2026) | Environment recheck passed; no cluster |
| NODE-20261017 | 17 October 2026 | Official SHA-256 recorded in [versions.md](versions.md) | User-local Node 24.22.0 verified; system Node retained |
| PY-20261017 | 17 October 2026 | [requirements-dev.txt](../requirements-dev.txt), versions record | pip dependency check and schema positive/negative checks passed |
| SOURCE-20261017 | 17 October 2026 | [source-import.json](../reports/sanitized/source-import.json), [provenance](upstream-provenance.md) | Verified real fork, immutable commit, matching 1,466-file import and MIT license |
| APP-20261017 | 17 October 2026 | [Run manifest](../reports/sanitized/day1-20261016T183808Z.json), [test counts](../reports/sanitized/day1-test-counts.json) | All six selected steps exited 0; 2,334 tests passed, 8 skipped, 0 failed; dependency locks unchanged |
| REVIEW-20261017 | 17 October 2026 | [Content review](../reports/sanitized/day1-content-review.json) | Prepublication snapshot: private generated files excluded and all upstream tracked files visible; later staging/delivery verified separately |
| LINT-20261017 | 17 October 2026 | [Precommit lint](../reports/sanitized/day1-precommit-lint.json) | `npm run lint` passed; exit 0; 8.57 seconds |
| WHITESPACE-20261017 | 17 October 2026 | [Upstream whitespace review](../reports/sanitized/upstream-whitespace-review.json) | 190 pre-existing diagnostics retained in the exact upstream snapshot; new override passed |
| CROSSCHECK-20261017 | 17 October 2026 | [Final Day 1 cross-check](../reports/sanitized/day1-crosscheck.json) | Rechecked committed upstream blob IDs/modes, build outputs, test-log checksums, zero failures, and lint success |

Application evidence identifies its immutable upstream commit separately from the earlier project baseline `3bea933`. Source commit `425d129` and setup/evidence/18 October plan commit `9bca61f` were successfully pushed to `feature-16-kick-start`. Ahead/behind counts were verified as `0 / 0`; the working tree was clean at delivery verification. Upstream tracked bytes still match after build/tests. The manifests record their prepublication observation times; later delivery is recorded in the daily log.

## Application run details

Run ID `20261016T183808Z` uses UTC. It ran on **17 October 2026, 00:08:08–00:10:48 IST**; the UTC date in its filename is therefore 16 October. Total measured stage duration: **159.77 seconds**, excluding setup, downloads, dependency lock resolution, and documentation work.

| Stage | Exit code | Duration |
|---|---|---|
| Root `npm ci` | 0 | 102.83 s |
| Frontend `npm ci` | 0 | 4.63 s |
| Explicit production build | 0 | 10.65 s |
| Frontend finite coverage tests | 0 | 21.47 s |
| Server unit tests | 0 | 3.09 s |
| API integration tests | 0 | 17.10 s |

Frontend: 123 test files / 1,372 tests passed. Server: 419 total, 417 passed, 2 skipped. API: 551 total, 545 passed, 6 skipped. The eight upstream skips remain visible; Cypress E2E, live LLM calls, scanner stages, containers, and cluster deployment were not tested by this run.

| Sanitized artifact | SHA-256 |
|---|---|
| `source-import.json` | `d705b3310efd1a37df2e42eeb168b9df50ccc6d68b7e837aa6f0f675c0834045` |
| `day1-20261016T183808Z.json` | `081d4ec669054b2d57e0116da26f7d5eeb689d812497a9f3a654036ea751eb17` |
| `day1-test-counts.json` | `b7fa7d73fb4027335e54af66858a5a1c488ad051e599ff3d6cc4976a27ab2696` |
| `day1-content-review.json` | `efe74216fdbcd489af949c345e279b68292c1134d6e9f96492c587e1c1abd55a` |
| `day1-precommit-lint.json` | `7103e90442acd7b9011a9f1d2c12b47d153070d4c32a8ae73133ef43c8c6440a` |
| `upstream-whitespace-review.json` | `c63cf8c729ececc53da7df4f8d4b8e5e33730676248c2f7caa5fb02a1e8d6df7` |
| `day1-crosscheck.json` | `08739535f46438535d083125c2f23c844e91e61dacedf25f6fff13d7d315bfef` |

The manifest includes relative private-log references and checksums, not raw output. Keep those raw logs ignored; their presence is not authorization to publish them.

## Day 2 evidence — 17 October 2026

| ID | Evidence | Verdict / limitation |
|---|---|---|
| IMAGE-20261017 | [Image build](../reports/sanitized/day2/image-build.json) | Original upstream Dockerfile/source build exited 0 in 430.05 seconds; actual image recorded |
| KIND-20261017 | [Runtime and workload status](../reports/sanitized/day2/runtime-baseline.json) | Node/pod Ready, zero pod restarts at observation, ClusterIP service, exact running image config matched |
| RUNTIME-20261017 | [Runtime baseline](runtime-baseline.md), status/hash manifest above | Home HTTP 200; three locally confirmed behaviors; no external scan or exploitation/data extraction claim |
| VALIDATION-20261017 | [Validation](../reports/sanitized/day2/validation.json) | Official kind/kubectl checksums passed; actionlint, shell/Python syntax and Kubernetes server dry-run passed |

Evidence timestamps use UTC; observations on 16 October after 18:30 UTC belong to 17 October in Asia/Kolkata. The hosted run uses its own image and cluster and will have separate evidence identifiers; do not equate its image digest with the laptop build.

| ID | Evidence | Verdict / limitation |
|---|---|---|
| SCREENSHOT-20261017 | [Running app](../reports/sanitized/day2/juice-shop-running.png), [metadata](../reports/sanitized/day2/screenshot.json) | Isolated headless browser authorized by user; reviewed catalog screenshot, external requests blocked |
| CI-20261017 | [Run 38954124002](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38954124002), implementation `f9867e0` | Initial run superseded after deployment helper correction; build/tests passed before supersession; final CI below |

Local final verification: [local-crosscheck.json](../reports/sanitized/day2/local-crosscheck.json). Repeated runtime checks passed with the same four HTTP statuses and zero restarts; the imported application source has no changes from the Day 1 pin. Private kubeconfig/responses remain ignored.

| Local Day 2 artifact | SHA-256 |
|---|---|
| `image-build.json` | `6893213754bf3d0457974a29eda2ed9855f7e481ec4b22921634eff9f1ca623e` |
| `runtime-baseline.json` | `eb63ed807c6a06debfe8dcf9e0ab8c4daf5b0434e6722d77767e8771a826a350` |
| `validation.json` | `abe6c37c243db15e0b5ad1ddaad0dab2326459b7162a4b9af1ddae287b809378` |
| `screenshot.json` | `c4ce99cdbc104baf3313c40889d4a637cac02dc01dcae29270adcfe8027e93bb` |
| `juice-shop-running.png` | `834db620cb9fe9ee0fb6219a0b64cba80fe92302eb6b7c0e722a93ffe735c80a` |
| `local-crosscheck.json` | `d2ec57fa6a4bd7c9605558c3ef6dde3228556831f1e6d5d81782149bf412e680` |

Previous hosted verification: [run 38955433523](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38955433523) for implementation `c1d78b9`; failed during deployment, with tests/image build passed and historical cause unconfirmed. This run is not accepted; final successful verification is below. The local image-ID annotation rollout and unchanged-image second apply both passed, followed by a passing runtime recheck on the replacement pod.

## Final accepted Day 2 hosted evidence

[Run 38957969793](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38957969793) and job `117165524668` completed successfully for code `280514f`. The complete job passed, including runtime and cleanup. Downloaded artifact `12071418832` matched GitHub's SHA-256 digest before extracting only the two expected sanitized JSON records.

| Evidence | Verdict |
|---|---|
| [CI receipt](../reports/sanitized/day2/ci-receipt.json) | Actual head/run/job/stage conclusions and artifact digest; prior failed/cancelled results remain visible |
| [CI build/tests](../reports/sanitized/day2/ci/build-tests.json) | All six selected stages exited 0; locks unchanged; no new test count is inferred from hidden raw logs |
| [CI runtime](../reports/sanitized/day2/ci/runtime-baseline.json) | Node/pod Ready, exact runner image matched, four checks passed: 200/200/200/500 |
| [Earlier test-only artifact](../reports/sanitized/day2/ci-failed-run-build-tests.json) | Tests passed in a workflow that failed deployment; not a full acceptance result |

Earlier private deployment output was lost, so historical root cause remains unconfirmed. A current successful run and added failure diagnostics do not retroactively establish that cause. Local manual review confirmation predates the hosted result; no independent approval is claimed.

| Hosted evidence file | SHA-256 |
|---|---|
| `ci-receipt.json` | `06e18bc06f472c3557dfbe2f4cc3637dca943f73bc24c1c24677237d7e4cd318` |
| `ci/build-tests.json` | `7c47396352895d3d20a1fe0e435148fbda68e198ef93a5d50b5d2544622c50a0` |
| `ci/runtime-baseline.json` | `3c5ddc81ab3ef1cf377ae0e194ee5a99ae641dd4800be7bbef980f849a7f0af0` |
| `ci-failed-run-build-tests.json` | `4299ba6549e542dbe0276f904a4ad881f17bd667d51ce5b6b3433dcffbb99f93` |

## Day 3 local evidence — 18 October 2026

Actual scanner output is kept under ignored `reports/private/day3/`; public records contain only allowlisted identifiers, paths, hashes, counts and decisions. No raw matched lines, secret values, author contacts or credential files are included.

| Evidence | Verified outcome / limitation |
|---|---|
| [Tools](../reports/sanitized/day3/tools-verification.json), [pins](../locks/scanners/tools.json), [DB snapshot](../reports/sanitized/day3/database.json) | Official distribution hashes verified; 66 Python distribution hashes locked; DB timestamp/hash retained |
| [Collection](../reports/sanitized/day3/scan-execution.json) | Semgrep/Trivy/history/tree scans executed; finding codes distinct from operational errors |
| [Gate summary](../reports/sanitized/day3/gate-summary.json) | 221 visible findings, 186 explicitly approved lab risks, zero blockers/errors; production and development dependencies included |
| [Review proposals](../reports/sanitized/day3/baseline-review-proposals.json), [review packet](day3-baseline-review.md) | Exact path/rule/component/commit fingerprints and file bindings; explicitly approved until 25 October at 00:00 IST |
| [Secret provenance](../reports/sanitized/day3/secret-provenance.json) | All 24 match files equal the pinned public upstream blobs; does not establish credential safety |
| [Contract tests](../reports/sanitized/day3/gate-tests.json) | 25 passed, zero failed/skipped; synthetic contract evidence, not detection metrics |
| [Actual scanner fixtures](../reports/sanitized/day3/fixture-evidence.json) | Bad inputs blocked; repaired clean inputs passed; history retained its synthetic canary and stayed blocked |
| [Full-profile rejection](../reports/sanitized/day3/full-profile-not-ready.json) | Missing IaC/container/DAST stages block; Day 3 is not complete six-stage acceptance |

Historical pre-approval hosted verification is recorded below. The current approved-policy result follows it; no full-pipeline success or production-readiness verdict is claimed.

First production-only Day 3 hosted source job `117616578672` in [run 39107551251](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39107551251) passed installation, 24 contract tests, actual fixtures and collection. The gate then correctly failed on 183 unapproved risks, zero operational errors. [Downloaded CI gate](../reports/sanitized/day3/ci/gate-summary.json), [tests](../reports/sanitized/day3/ci/gate-tests.json), [fixtures](../reports/sanitized/day3/ci/fixture-evidence.json), [execution](../reports/sanitized/day3/ci/scan-execution.json), [tools](../reports/sanitized/day3/ci/tools-verification.json). Artifact digest matched `94cbf4f7b27904c430d575ba4c4508bbe7dd9f0af4554524f2594e5d830af5bd`; all 217 identities and content bindings matched local evidence, with no raw match/contact fields or canary. Owner baseline review was pending at that run.

Dependency scope correction: the mandatory collection now includes development dependencies, adding three high findings. Corrected local evidence has 221 distinct identities, 186 blockers and 25 passing contracts. The first production-only packet/artifact is historical; its 183 entries cannot authorize additional findings. The corrected hosted run below verified this expanded scope. The parallel baseline job in the first run completed successfully.

Corrected hosted source scope: [run 39108322664](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39108322664), source job `117618870374`, code `421f8eb`. [Gate](../reports/sanitized/day3/ci/39108322664/gate-summary.json), [25 passing contracts](../reports/sanitized/day3/ci/39108322664/gate-tests.json), [fixtures](../reports/sanitized/day3/ci/39108322664/fixture-evidence.json), [execution](../reports/sanitized/day3/ci/39108322664/scan-execution.json), [tools](../reports/sanitized/day3/ci/39108322664/tools-verification.json). Actual gate failure is 186 unapproved risks, zero operational errors. Artifact `12129287626` matched digest `16a6749e2cf91180a5b2cbccee34dde19146875949a3d302b37d95a3b7faa5e9`; all 221 identities/file hashes match local data, with no forbidden raw/contact/canary fields in published evidence/logs. Owner review was pending at that run.

## Day 3 historical technical verdict — before owner approval

[Run 39108322664](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39108322664) completed with source-gate **failure on 186 unapproved risks**, zero scanner operational errors. Its baseline application job passed. [Historical receipt](../reports/sanitized/day3/ci/39108322664/receipt.json), [baseline build/tests](../reports/sanitized/day3/ci/39108322664/baseline/build-tests.json), [baseline runtime](../reports/sanitized/day3/ci/39108322664/baseline/runtime-baseline.json). Source artifact SHA-256: `16a6749e2cf91180a5b2cbccee34dde19146875949a3d302b37d95a3b7faa5e9`; baseline artifact SHA-256: `176447fe97a142930d7fba8abeaba90675b2dda905990387dc89bb7b2b309580`. Both downloaded ZIPs were checked. At that observation no owner approval had been received and no exception was enabled; the subsequent explicit approval/current result is recorded below.

| Current Day 3 record | SHA-256 |
|---|---|
| `baseline-review-proposals-production-only.json` | `43e6506041623aa0a54bf88ee5c0be3d290a732fb5596fa2f778317a2e20632f` |
| `baseline-review-proposals.json` | `18d6c661f2bd34a671b6dfabc85a92e272927ebadc316adaa162e0d837118ff0` |
| `ci-receipt.json` | `b0ed4e9513b972a60d0eb4fd6d9c551629ecbd75a89ef47e7141d0710c2089ff` |
| `database.json` | `235dece9b402f1f9694a677e554fb2b8d47973729176e0071550ca5e5eae2a15` |
| `fixture-evidence.json` | `782cd5cab4cd3f9b3c9fcb47a6da08ec86b15b65ae3205f10894385418c1d470` |
| `full-profile-not-ready.json` | `878c88be89d670340e508e86f72cfbca4e103779573cef0934b1e47cccf155a0` |
| `gate-summary.json` | `8acc955dd26c44eedee05a70e3451024627799bd445689b25087b498bb561e67` |
| `gate-tests.json` | `b480931551facbe01011a7dd37a01b02f616357e789545f0c565194302620096` |
| `owner-review.json` | `08873d6547678cf00f6cb260c5178849b15dfa25bed88abb21ec2a4412fed713` |
| `publication-audit.json` | `734f1e4e589d173929f28f9bf220e15b2d1083ff9aa7a0ede33da516db0ae233` |
| `rollout-fix-local.json` | `eb63ed807c6a06debfe8dcf9e0ab8c4daf5b0434e6722d77767e8771a826a350` |
| `scan-execution.json` | `953d43ba3c8e5f589a65b6b9064a4d6da995521344eeb8df82c0accd42d5bf8c` |
| `secret-provenance.json` | `f6a56d1bb80dbbdcb3c8eeb9550e63fc0d7e87127c3645ed1ef04142085c3f3f` |
| `tools-verification.json` | `f53caa03494bf94cc18692f24a323da7709ef983491707b82e2a006e8e4294ad` |

[Final publication audit](../reports/sanitized/day3/publication-audit.json) rescanned the current tracked/non-ignored tree: the same 68 baseline secret-location fingerprints (69 raw report rows), zero new fingerprints. Raw output remained private. This verifies publication candidates, not owner acceptance of those existing risks.

Stage counts: 11 SAST, 74 dependency, 68 history and 68 tree identities = 221; identities that would block without approval are 8 + 42 + 68 + 68 = 186, now exactly accepted for the lab. Secret reports have 69 raw rows each; de-duplication is by exact rule/path/line/commit identity and current-file content binding. No risk fingerprint or scope changed in this count-label correction.

## Current approved-policy verification — 18 October 2026

Day 3 is complete for its defined source-scan/gate scope. The designated reviewer explicitly accepted the current 186 exact lab-only entries; [approval receipt](../reports/sanitized/day3/owner-review.json), [active policy](../policies/baseline-exceptions.json). Local and hosted gates pass with **221 visible findings / 186 accepted risks / zero blockers and operational errors**. Approval expires **25 October at 00:00 IST**; acceptance is not a fix.

[Run 39111621696](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696), code `d68686a`, passed both source and baseline jobs, 25 gate contracts, five rollout regressions, six application stages, deployment/image identity, four runtime observations and cleanup. Source ZIP SHA-256 `7e96dff369e214e2c3dd5def98413015a92d278d785a01fc70e949541d3362b7` and baseline ZIP SHA-256 `dba4c58132054b52235643f998d85dcb189eda274adbc25e869089f77b307a4a` were verified. All source identities/content bindings match local data, and both job logs/artifact metadata passed privacy checks. One terminating pod was present in the successful runtime check, verifying the readiness-race correction while live-pod/image/HTTP checks remained enforced. [Current CI receipt](../reports/sanitized/day3/ci-receipt.json).

The prior approval run's source gate passed but its post-rollout pod wait failed; [historical receipt](../reports/sanitized/day3/ci/39110505372/receipt.json), [retained diagnostics](../reports/sanitized/day3/ci/39110505372/baseline/deployment-failure.json). It is not relabeled green. The original Day 2 incident's unavailable log still prevents a historical root-cause claim. Day 4 is unstarted pending actual program acknowledgement; the user requested help and the LMS page link is needed. Full six-stage/AI/report acceptance remains open.


| Current hosted Day 3 evidence (relative to `reports/sanitized/day3/ci/39111621696/`) | SHA-256 |
|---|---|
| [baseline/build-tests.json](../reports/sanitized/day3/ci/39111621696/baseline/build-tests.json) | `97ee296dcd41adbe04c7715f3ba602ee0c09a46d3f0d5a166c1f2ea8f06fe5a9` |
| [baseline/runtime-baseline.json](../reports/sanitized/day3/ci/39111621696/baseline/runtime-baseline.json) | `ccbcdf80aac7137f43f47b2775e3541f5ad011fa1ee9e2536c19123bbf10cbc0` |
| [fixture-evidence.json](../reports/sanitized/day3/ci/39111621696/fixture-evidence.json) | `119a8503921bd6cdf97e007627585622182ebfb0d3938f300d977c9b6a80e40f` |
| [gate-summary.json](../reports/sanitized/day3/ci/39111621696/gate-summary.json) | `8acc955dd26c44eedee05a70e3451024627799bd445689b25087b498bb561e67` |
| [gate-tests.json](../reports/sanitized/day3/ci/39111621696/gate-tests.json) | `4272d3ebf77d1e4ec200f8333d0fbe589ff4488641340d33ec94ce624f4d26ee` |
| [receipt.json](../reports/sanitized/day3/ci/39111621696/receipt.json) | `b0ed4e9513b972a60d0eb4fd6d9c551629ecbd75a89ef47e7141d0710c2089ff` |
| [scan-execution.json](../reports/sanitized/day3/ci/39111621696/scan-execution.json) | `7a9000d1c4cb226fe98c1665b5d38bedfd52d03325d8f3fd1077ae873fa40e56` |
| [tools-verification.json](../reports/sanitized/day3/ci/39111621696/tools-verification.json) | `f53caa03494bf94cc18692f24a323da7709ef983491707b82e2a006e8e4294ad` |

Active exact policy SHA-256: `ec0f59810986dd92d89bdaf73c11ae9aa460f7feeb87036ea320004f60fac78c`.

## Day 4 local comparison evidence — 22 October 2026

Acknowledgement was confirmed before resumed work. Collection at repository HEAD `993f1df` binds the then-local implementation inputs by SHA-256; that HEAD alone did not contain the implementation. The study profile continues with 39 deferred findings and zero operational errors, while the historical strict security result is retained. Exact source approvals are unchanged.

| Evidence | Result | SHA-256 |
|---|---|---|
| [tools-verification.json](../reports/sanitized/day4/tools-verification.json) | Pinned isolated Checkov/Syft | `4135be334089347843ee17fef22edb270688617fd248fccd12abc7e2869d5229` |
| [policy-fixtures.json](../reports/sanitized/day4/policy-fixtures.json) | Eight actual CLI fixtures passed | `fb169aa211235fcbad7b990328d018df87cf28ab192ad6dcc745f7990685d821` |
| [image-build.json](../reports/sanitized/day4/image-build.json) | Allowlisted source-built hardened image | `ffd17a6a7eb73aec16c6b28c767fda5ff49cce4e52517b34df1746a461bc1b97` |
| [runtime-docker.json](../reports/sanitized/day4/runtime-docker.json) | Seven functional checks and runtime controls passed | `674da7ad8f63ca8189f791b89edb8f3b533ecea924b7f0e97ba87c412d6485cd` |
| [runtime-kubernetes.json](../reports/sanitized/day4/runtime-kubernetes.json) | Ready workload; exact image and seven checks passed | `0f63337a29f158b99f7df104d9d37d0c1f29fff885d7606ab704823a4e388548` |
| [deployment.json](../reports/sanitized/day4/deployment.json) | Local manifest/config identities verified | `91847e190c2ae2c17a1c7fee425aba12a4dc5274d9480033e81d06c28c1430b9` |
| [scan-execution.json](../reports/sanitized/day4/scan-execution.json) | Seven comparison stages; one frozen DB | `ba1a025bed099d0833ab033cd709f35da053762adb5694fe0ff7ef69892afa2d` |
| [gate-summary.json](../reports/sanitized/day4/gate-summary.json) | Study execution passed; 39 findings deferred | `7dfeff0a40b58e8892a69e14953883883a1b51e98ee20752ed60fa04d999394b` |
| [gate-tests.json](../reports/sanitized/day4/gate-tests.json) | 15 error/security gate contracts passed | `805e9692b39d20b927dad09caebc4abfa9a842387dc950b2bc5f6c676102b820` |

Collection run `20261022T151417042900Z`; SBOM has 2,748 CycloneDX 1.6 components. Kubernetes/Dockerfile failures fell from 17 to one; image identities from 101 to 100 with no new identities. The 38 high/critical image findings and NetworkPolicy gap remain deferred. Raw reports/SBOM stay ignored. The later fresh cluster was healthy; this does not claim recovery of historical unready system pods in the original lab.

## Current critical-remediation evidence — 22 October 2026

The later repair supersedes critical deferral. **Fresh source/image scans: 11 → 0 critical underlying issues.** The recorded local source/root-lock snapshot was modified and uncommitted at measurement time; all its stage receipts bind that project tree. Repairs are now committed/pushed as `8ac412e`, with the dynamic Actions report at `1616f14`; fresh hosted run 39842575944 passed all eight jobs with zero critical findings. Earlier hosted runs and fresh-directory datasets below predate this variant. [Current repair state](critical-remediation.md).

| Evidence | Verified scope | SHA-256 |
|---|---|---|
| [Complete critical verification](../reports/sanitized/critical-remediation/verification.json) | Zero critical source/image; 2,332 application passes / six skips; 64 current contracts | `641ef286c0c9a9a524dd7c9ef3c153a454a03f38aadb06b558e3b2fe3b5a9971` |
| [Repair privacy review](../reports/sanitized/critical-remediation/publication-review.json) | Ten unchanged upstream fixture matches; no new matched credential content | `5ccd5165ada3129395435a438688af60e23ab5bacc25f5f0173c29c8173dbb37` |
| [Original critical baseline](../reports/sanitized/critical-remediation/before.json) | Eleven original issue identities retained | `de9436418da4b48779f3c22cf0093898e508042ef9151e6a0e1623c73fff1f57` |
| [Actual old/new image probes](../reports/sanitized/critical-remediation/negative-probes.json) | Unsigned JWT and executable query accepted before, rejected after | `bef68612d1b2440f45f8618bcf4cbdc1496a50e9f00bca97100db0f7a36c8a20` |
| [Critical gate control](../reports/sanitized/critical-remediation/gate-probe.json) | Real CLI exit0 at zero, exit1 with synthetic critical; no scanner evidence modified | `49c78a3f9b81b8dd2d5d3631a6ea2ac91009c92a8c581d11b71eb73e9253e38e` |
| [Owned study deployment](../reports/sanitized/critical-remediation/deployment-owned-lab.json) | Current verified image deployed | `91847e190c2ae2c17a1c7fee425aba12a4dc5274d9480033e81d06c28c1430b9` |
| [Owned study runtime](../reports/sanitized/critical-remediation/runtime-owned-lab.json) | Seven checks and controls pass against the exact image | `0f63337a29f158b99f7df104d9d37d0c1f29fff885d7606ab704823a4e388548` |
| [Temporary cluster cleanup](../reports/sanitized/critical-remediation/run.json) | Owned cluster removed; script exit0 | `eb56831484ba3fa51f621727543461d86f1897e6fabe8933beedbac594e8c9cd` |
| [Pre-remediation PDF](../output/pdf/history/c7f25d9/PipelineFortress_Study_Report.pdf) | Original twelve-page delivery retained | `dc7bfb3621eed3fc211707f3dfaf8e80c356fcd9b00dfd8fb9a689a65f21b024` |

## Days 5–10 delivery evidence — current mutable receipts and historical snapshots

The user directed completing the study assignment with vulnerabilities deferred. This supersedes earlier security-acceptance pauses. Exact historical source approvals are unchanged; scanner errors, skipped jobs, missing reports and mixed identities remain execution failures. [Current state](project-completion.md) distinguishes implementation delivery from remaining assessment requirements.

| Evidence | Result | SHA-256 |
|---|---|---|
| [Local full pipeline](../reports/sanitized/pipeline/aggregate.json) | Current repair: all scans complete; 93.19 seconds with explicit fresh-build/test reuse; zero operational errors | `45beece21cd66f470729729938bd17bce2aaaa7feb4d84dc8a2e8f50b282d5c3` |
| [Hosted run receipt](../reports/sanitized/delivery/ci-receipt.json) | Historical before-repair baseline: eight jobs passed at bef6664 | `e14a9b0aa0c2f08c0bce0729873d62eaed5bd07c3322ecbc6862c6225d970eb7` |
| [Downloaded artifact verification](../reports/sanitized/delivery/artifact-verification.json) | Official ZIP digest, recomputed aggregate, run/revision and exact image linkage verified | `1e9ca3da0e848633463c1171c463eb476e48b92a0a475335c927334869867038` |
| [Prior full hosted pass](../reports/sanitized/delivery/historical/39818760193/artifact-verification.json) | Independent preserved success at 61b064f | `359ba82b5d4eeda817afed14eba306fe57dd4752d45d9187246a16cc45439dda` |
| [Passive ZAP](../reports/sanitized/day5/dast.json) | 121 URLs, route proof and scanner cleanup | `4a50fada231abf874580c939f3107af31acf6acb54219a7231aa989d4b811deb` |
| [DAST controls](../reports/sanitized/day5/fixture-evidence.json) | Real different-UID access probes and selected bad/fixed header detections pass | `e3321d93ea09361e7b85b8cb5c02ac4d7aad3b9c12292e731c5b8ccc9120d707` |
| [Dashboard inputs/results](../reports/sanitized/dashboard/index.json) | Current 251 observations / 180 underlying issues; post-hoc fixture metrics | `8351ffd935ffc8e00f969601fbfc8f43af5e2d650643077a9b9b87f885114945` |
| [Deferred register](../reports/sanitized/deferred-risks.json) | Current zero critical / 91 high; earlier eleven critical identities retained separately | `02066c5861f27f0835d8770b66c638ff03abbbe3e4b5cad7561c81f47178536e` |
| [Current contract proof](../reports/sanitized/day7/redaction-tests.json) | 64 tests passed; current boundary/prompt hash | `4d2a3de29e565c4d7ed2496e2672db6cc6c192c2977ec206fe4648c1d159a860` |
| [Source contract proof](../reports/sanitized/day3/gate-tests.json) | 25 fail-closed contracts passed | `2b297e22685b012374c956c4246a508ef253435ef1a1550dab7a935d0622a477` |
| [Real OpenAI failure](../reports/sanitized/day8/triage-live-error.json) | HTTP429; no successful live result or billing change | `d9f67208a0f2cd9835dc6752479627032a4d0eb478a962196f04ca0c2a61dddb` |
| [Three focused proposals](../reports/sanitized/day9/proposals.json) | Actual selected-check and runtime before/after evidence | `3530cd44eaefeecde02df661bc02eb72c78a3a9b4f71176511b9957434b989e4` |
| [Published draft PRs](../reports/sanitized/day9/pr-receipt.json) | Three green hosted workflows; one-file diffs; independent review pending | `3ed4b17b57df9f8d046283f59d853b2d1547c7bb410b6301d1aa515fe0fd55c5` |
| [Fresh-directory receipt](../reports/sanitized/reproduction/run.json) | Full 1e0115c pipeline passed; 286.23 seconds; cleanup verified | `50909e46bc99a70c93844894000373f0f86d962feaf5a82c305c89ed4952b600` |
| [Clean-PATH receipt](../reports/sanitized/reproduction/clean-path-run.json) | Full bef6664 execution; repository-local tools; cleanup verified | `eb3f8d1d01945792476423c0741360f25283f977f1d882fccc11d7df8d4e80f7` |
| [Final report](../output/pdf/PipelineFortress_Study_Report.pdf) | Current repair report: twelve pages rendered and visually inspected | `51d662b3d574a2879bd07cfa14d3867bec351335f930c8cf343ff2427690a364` |

Fresh-directory runs at 6ef16a0 and 1e0115c share host caches; they are not fresh-machine tests. The later clean-PATH run verifies the Kubernetes-tool selection correction in the existing project directory. Historical fresh datasets have 372 normalized observations / 235 issues; the current local dataset has one fewer passive medium alert instance. No fix is inferred from crawl variation. [Reproduction scope](reproduction.md).

[Hosted run 39821125926](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39821125926) and the three remediation PR workflows passed. All earlier failed runs remain historical failures. Successful live AI, independent labels/human review and oral assessment remain open; no provider retry or purchase was made. [Final validation record](../reports/sanitized/delivery/validation.json) records the historical publication checks; its original report is retained in output history. The current repair receipt identifies the updated report.

## Critical repair hosted publication — 23 October 2026 IST

[Actions Summary](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) passed on `1616f14`; source and exact-image critical counts are zero. All 2,332 selected application tests and 76 contracts passed; six application skips and nine excluded external checks remain explicit. Hosted totals are 257 cross-stage observations, including 159 high; these are not the local deduplicated register. The original local proof and checked-in PDF remain historical snapshots.

| Evidence | Verified scope | SHA-256 |
| --- | --- | --- |
| [Hosted publication verification](../reports/sanitized/critical-remediation/ci/verification.json) | Eight green jobs; archive digest, recomputed gate and run/commit/image bindings | `f18e944842db3c425e54113a257c9dccc48be2d906e7e23fece1683fbedeebbe` |
| [Published poster copy](../reports/sanitized/critical-remediation/ci/actions-summary.md) | 7,435 bytes identical to logged Actions Summary write and regeneration | `fb6f1dd2e2485b31097d2e55ca9ed2b4ea8e2f06f44123db898632cc0471694c` |
| [Hosted aggregate](../reports/sanitized/critical-remediation/ci/pipeline/aggregate.json) | Seven stage receipts; zero critical, zero operational errors | `4630822fa0cc3385a2d55a626975a5a3728f2b82cb3d3350dcb8f02221bbea4a` |

## Continuation audit packet — 23 October 2026 IST

The canonical PDF is refreshed with the accepted hosted repair and fresh b20b9b1 checkout. The original pre-hosted PDF remains in versioned history; its original verification receipt now points to those exact preserved bytes. [Full requirement audit](completion-audit.md).

| Evidence | Verified scope | SHA-256 |
| --- | --- | --- |
| [Fresh repaired reproduction](../reports/sanitized/reproduction/critical-variant/run.json) | 274.71 seconds; zero critical; complete application/scans/mock/dashboard and cleanup | `8325212c3afa46d99733ff45335c0a134c19e9d35ffd7747f95991465d2cf1c6` |
| [Refreshed report validation](../reports/sanitized/final-audit/report-validation.json) | Twelve pages rendered and visually inspected; preserved prior PDF | `45ee5c8599bad9bde7d244167ee2581f371740608960de96d962b92548e9e928` |
| [Dashboard visual/timing verification](../reports/sanitized/final-audit/dashboard-validation.json) | 1440px/390px Chrome layout; same-run feedback timing and explicit scope | `a0cece66ba8d53f7a1801c10e14aed9558d545a34d3ba81f52d7efb51e01f528` |
| [Current PR observation](../reports/sanitized/final-audit/review-observation.json) | Three separate unmerged one-file drafts; zero independent reviews | `34646f2aefc685ad596f968860d349278c80c8f7d3bece628442ba3602ec81bd` |
| [Acceptance audit](../reports/sanitized/final-audit/acceptance.json) | Current implementation proofs; external evidence explicitly unachieved | `fd8578f4f7c2b65f35370d49cb7cdc364161eb532b42c7db837dea8196ed92e7` |
| [Preserved original repair PDF](../output/pdf/history/1616f14/PipelineFortress_Study_Report.pdf) | Original bytes in accepted ten-file hosted packet | `4d3c34febab430dbbed9b897d625b7955d08edc2f195214de5e03c1f5a4ecf9d` |
