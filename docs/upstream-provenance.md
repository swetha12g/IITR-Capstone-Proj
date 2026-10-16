# Juice Shop upstream provenance

Verified: 17 October 2026.

| Item | Value |
|---|---|
| Official upstream | <https://github.com/juice-shop/juice-shop> |
| Separate GitHub fork | <https://github.com/swetha12g/juice-shop> |
| Fork evidence | GitHub repository metadata reports `fork=true`, parent `juice-shop/juice-shop` |
| Release | [v20.3.0](https://github.com/juice-shop/juice-shop/releases/tag/v20.3.0) |
| Immutable commit | `f189f521266f42c6bd05884468292000cee852ed` |
| Source directory | `app/juice-shop/` |
| Import method | Fetch the pinned commit from the fork into an external source checkout, then `git archive` that commit into the project |
| Tracked files verified | 1,466; imported contents match the pinned checkout |
| Nested Git metadata | None in the imported directory |
| License | MIT; original `LICENSE` preserved byte-for-byte |
| License SHA-256 | `fa4ca6d61009e537c953f1c0b8455dd66d69f810888546c48db8ea05f0713093` |

The project repository is an imported snapshot linked to a separate GitHub fork. It is not itself described as a GitHub fork. Public upstream copyright notices and contributor attribution remain unchanged. The pinned tree contains `LICENSE` and no separate `NOTICE` file.

Sanitized machine-readable verification: [source-import.json](../reports/sanitized/source-import.json).

## Dependency lock adaptation

The pinned release does not track application npm lockfiles and its `.gitignore` excludes `package-lock.json`. Root and frontend locks were resolved with Node v24.22.0 / npm 11.19.1 using `npm install --package-lock-only --ignore-scripts --no-audit --no-fund`. They are recorded separately under `locks/juice-shop/` so the imported tracked source remains unchanged.

The Day 1 runner copies those recorded locks into their ignored application locations before `npm ci`. It checks that the locks still match afterward. The upstream root postinstall runs a frontend `npm install` and builds the app; the runner also performs an explicit frontend `npm ci` and explicit full build to verify those stages separately and catch build failures the upstream postinstall could mask.

| Recorded lock | SHA-256 |
|---|---|
| `locks/juice-shop/package-lock.json` | `5060cfe6d994f31e4aac2c0f7eeb347675d899fd42ad7acbe12fd5c22fd19e8c` |
| `locks/juice-shop/frontend-package-lock.json` | `2cab8508e02d7ca0b74df30010cfefa1c98ce4e76708928726f80e090d931503` |

No upstream tracked files, application code, workflows, configuration, translations, or challenge definitions were changed during import/build/tests. A local `.gitignore` was added under `frontend/src/assets/private/` to retain nine public JavaScript assets already tracked by upstream but excluded by its general generated-JavaScript ignore rule. The project root also explicitly retains the public upstream `ftp/encrypt.pyc` challenge fixture. These narrow publication overrides preserve the complete pinned snapshot without broad forced staging; generated artifacts remain ignored.

This baseline import is not a hardening or remediation change. Public intentionally vulnerable challenge fixtures remain present; no scanner verdict that the application is secret-free or production-safe is claimed.
