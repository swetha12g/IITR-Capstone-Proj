# Local environment and version record

Verified on 17 October 2026. Build/test status is recorded in [evidence-index.md](evidence-index.md).

| Component | Verified version / state |
|---|---|
| Host | Pop!_OS 22.04 LTS; Linux 6.9.3-76060903-generic; x86_64 |
| CPU / RAM / disk | Intel i7-12700H, 20 threads; 31 GiB RAM; approximately 582 GiB disk available at recheck |
| Git | 2.34.1; `feature-16-kick-start`; fetch passed |
| System Node / npm | v12.22.9 / 8.5.1; unchanged |
| Project Node / npm | v24.22.0 / 11.19.1; separate user-local installation |
| Python | 3.10.12; project `.venv` |
| pytest / jsonschema | 9.1.1 / 4.26.0; dependency and schema checks passed |
| Docker | Client/server 27.3.1; daemon reachable; no warnings |
| kind | v0.33.0; no cluster created |
| kubectl | v1.37.0; Kustomize v5.8.1; `~/.local/bin/kubectl` |
| Planned Kubernetes | v1.37.0; documentation-compatible with the installed kind/kubectl; not deployed |
| Bridge configuration | `br_netfilter` loaded; IPv4 forwarding and both bridge-filtering sysctls equal 1 |
| Juice Shop | v20.3.0, commit `f189f521266f42c6bd05884468292000cee852ed` |

## Select the project runtimes

From the project root in Bash:

```bash
source scripts/dev-env.sh
node --version
npm --version
python --version
python -m pip check
```

Node was installed under `${XDG_DATA_HOME:-$HOME/.local/share}/pipelinefortress/node-v24.22.0-linux-x64`. `scripts/dev-env.sh` selects it for the current shell and activates `.venv` when available. It does not edit shell startup files or replace system Node. Open a new unmodified shell to use the normal system PATH again. A custom Node location can be supplied through `PIPELINEFORTRESS_NODE_DIR`.

Official archive: <https://nodejs.org/dist/v24.22.0/node-v24.22.0-linux-x64.tar.xz>.

Official checksum list: <https://nodejs.org/dist/v24.22.0/SHASUMS256.txt>.

Verified Node archive SHA-256:

```text
cc2f601cee82d9a5a233302fe307abc600727035fd7d2c3a3571755989e95008
```

The selected runtime is [Node v24.22.0 LTS](https://nodejs.org/en/blog/release/v24.22.0); the [pinned Juice Shop README](https://github.com/juice-shop/juice-shop/blob/v20.3.0/README.md#nodejs-version-compatibility) marks Node 24 supported and tested. Application engines specify Node 22–26. Actual installation, production build, and selected frontend/server/API suites passed with this runtime; the eight upstream test skips are recorded in [evidence-index.md](evidence-index.md).

## Python environment recovery and pins

The host has the `venv` module but lacks `ensurepip`, so `python3 -m venv .venv` failed. A temporary PyPI `virtualenv` tool created the isolated environment without installing system packages. pytest/jsonschema were then installed inside `.venv`; `pip check`, pytest's CLI, and valid/invalid JSON Schema validation passed.

Exact compatible dependencies are recorded in [requirements-dev.txt](../requirements-dev.txt). Reinstall them into an isolated Python 3.10 environment with:

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pip check
```

Scanner environments remain separate; none were installed for this checkpoint.

## Reproduce the selected application checks

After the pinned source import and recorded locks are present:

```bash
source scripts/dev-env.sh
python scripts/run-day1-checks.py
```

The runner executes root and frontend `npm ci`, the explicit production frontend/server build, finite frontend coverage tests, server unit tests, and API integration tests. It captures exit codes and durations in sanitized manifests while retaining raw output under ignored `reports/private/day1/`.

Cypress binary download is disabled for these selected suites; Cypress E2E tests are not claimed. No live LLM key is configured or required. Bridge module loading is temporary and must be rechecked after reboot.
