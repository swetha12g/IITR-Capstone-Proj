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
| `runtime-baseline.json` | `51242b47f795343e341071167fc52f842060326d90f054d62dd62a634416d218` |
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
| `ci-receipt.json` | `ceb3988b2289d9f7487ae8c62234bf330794216293cac53e93decf809632b51e` |
| `database.json` | `235dece9b402f1f9694a677e554fb2b8d47973729176e0071550ca5e5eae2a15` |
| `fixture-evidence.json` | `782cd5cab4cd3f9b3c9fcb47a6da08ec86b15b65ae3205f10894385418c1d470` |
| `full-profile-not-ready.json` | `878c88be89d670340e508e86f72cfbca4e103779573cef0934b1e47cccf155a0` |
| `gate-summary.json` | `8acc955dd26c44eedee05a70e3451024627799bd445689b25087b498bb561e67` |
| `gate-tests.json` | `b480931551facbe01011a7dd37a01b02f616357e789545f0c565194302620096` |
| `owner-review.json` | `08873d6547678cf00f6cb260c5178849b15dfa25bed88abb21ec2a4412fed713` |
| `publication-audit.json` | `705b3240b701fe9eb88cfc6d09615f6bed253096b80173a80ae79580f13ecc3e` |
| `rollout-fix-local.json` | `eb63ed807c6a06debfe8dcf9e0ab8c4daf5b0434e6722d77767e8771a826a350` |
| `scan-execution.json` | `7338ecf09fd882d15266bc304790c3da695e3ec96590829fd9f184e6fcd9dc02` |
| `secret-provenance.json` | `f6a56d1bb80dbbdcb3c8eeb9550e63fc0d7e87127c3645ed1ef04142085c3f3f` |
| `tools-verification.json` | `f53caa03494bf94cc18692f24a323da7709ef983491707b82e2a006e8e4294ad` |

[Final publication audit](../reports/sanitized/day3/publication-audit.json) rescanned the current tracked/non-ignored tree: the same 68 baseline secret-location fingerprints (69 raw report rows), zero new fingerprints. Raw output remained private. This verifies publication candidates, not owner acceptance of those existing risks.

Stage counts: 11 SAST, 74 dependency, 68 history and 68 tree identities = 221; blockers 8 + 42 + 68 + 68 = 186. Secret reports have 69 raw rows each; de-duplication is by exact rule/path/line/commit identity and current-file content binding. No risk fingerprint or scope changed in this count-label correction.

## Current approved-policy verification — 18 October 2026

The pending-review descriptions above are historical. The designated reviewer has now explicitly accepted the current 186 exact lab-only entries; [approval receipt](../reports/sanitized/day3/owner-review.json), [active policy](../policies/baseline-exceptions.json). Fresh local gate passes with 221 visible findings, 186 accepted risks and zero blockers/errors. Fresh hosted source verification passed in run `39110505372`, matching all 221 local identities/content bindings. [Gate](../reports/sanitized/day3/ci/39110505372/gate-summary.json), [25 contracts](../reports/sanitized/day3/ci/39110505372/gate-tests.json), [probes](../reports/sanitized/day3/ci/39110505372/fixture-evidence.json), [collection](../reports/sanitized/day3/ci/39110505372/scan-execution.json), [tools](../reports/sanitized/day3/ci/39110505372/tools-verification.json). The source artifact ZIP SHA-256 matched `85c2a6d575759246afc00576dfb2ec176755a93a80dfb8ab805d324bdc5f03f3`; source-job logs and artifact metadata passed privacy checks. The parallel baseline hit a post-rollout pod-wait race; a narrow correction passed local redeploy/runtime and awaits hosted confirmation. Historical failed-run evidence is retained. Acceptance expires 25 October at 00:00 IST and is not a fix.
