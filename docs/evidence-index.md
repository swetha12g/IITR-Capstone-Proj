# Evidence index

Raw installation/build/test output is retained under ignored `reports/private/`. Public records contain sanitized status, counts, identifiers, timestamps, and checksums only. No credentials, personal contact details, or raw findings belong here.

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
