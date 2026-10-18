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
| kind | v0.33.0; owned `pipelinefortress` cluster created and Ready |
| kubectl | v1.37.0; Kustomize v5.8.1; `~/.local/bin/kubectl` |
| Kubernetes | v1.37.0 kubelet verified in the Ready kind node; kubectl matches |
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

## Day 2 container and CI pins

- Baseline image: Linux/amd64, Node v24.22.0 verified inside the running image; original upstream distroless runtime and user 65532 retained. Image identity and pod matching are in [runtime-baseline.json](../reports/sanitized/day2/runtime-baseline.json).
- kind node: `kindest/node:v1.37.0@sha256:a1ed56cfb0e7b93589bdf97c8cd566405a265939e3620fc4f5de89adff580ae5`, from the [official release](https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0).
- CI installer downloads kind 0.33.0 and kubectl 1.37.0 from official release endpoints and checks their official SHA-256 files; the exact installer passed locally in temporary storage, with no system replacement. See [validation.json](../reports/sanitized/day2/validation.json).
- Actions are pinned to reviewed commit SHAs in [security.yml](../.github/workflows/security.yml): checkout 7.0.1, setup-node 7.0.0, setup-python 6.1.0 and upload-artifact 7.0.1; runner label `ubuntu-24.04`. The label is a supported OS release, not an immutable runner-machine snapshot.
- actionlint 1.7.12 was downloaded to temporary storage, verified against the official checksum list, and passed workflow validation.
- Original upstream Dockerfile uses mutable base tags and some ranged global tools. This baseline records the actual built image, rather than claiming byte-identical rebuilds. Digest/tool pinning and hardened image comparison are Day 4 work. Initial resolved base digests: `node:24@sha256:14078204b6bb268c107ceff6d3c43f45a888105e5c2b18b14c32b3409d93a1b0` and `gcr.io/distroless/nodejs24-debian13@sha256:9ddd3f7de61d8c62337cdcbeaceb621de5e0c955ccdc70f4c3586db74a8c278f`.

## Day 3 scanner environment — 18 October 2026

| Tool | Pin | Integrity / isolation |
|---|---|---|
| Semgrep CE | 1.181.0 | Official PyPI wheel digest matched; all 66 resolved distributions pinned with hashes in [requirements](../locks/scanners/semgrep-requirements.txt); separate Python 3.10 environment |
| Trivy | 0.76.0 | Official Linux archive checksum verified; project-local binary and DB cache |
| Gitleaks | 8.30.1 | Official Linux archive checksum verified; default rules extended without suppressions; separate full-history/tree scans |

Exact archive URLs/hashes and platform requirements are in [tools.json](../locks/scanners/tools.json). Bootstrap verification is recorded in [tools-verification.json](../reports/sanitized/day3/tools-verification.json). No scanner replaces system tools. HOME/settings/Docker config are isolated during scanner execution; no account login or Semgrep telemetry/remote rule fetch is used. Trivy's vulnerability DB is updated separately; the local [DB metadata and digest](../reports/sanitized/day3/database.json) records this run, not an immutable future DB result.

Official references: [Semgrep CLI](https://docs.semgrep.dev/cli-reference), [PyPI release](https://pypi.org/project/semgrep/1.181.0/), [Trivy release](https://github.com/aquasecurity/trivy/releases/tag/v0.76.0), [Trivy exit-code configuration](https://trivy.dev/docs/latest/configuration/others/), [Gitleaks release/CLI](https://github.com/gitleaks/gitleaks/tree/v8.30.1). Finding exits are explicit; scanner errors remain blocking.

Day 3 coverage correction: the mandatory Trivy command explicitly includes development dependencies (`--include-dev-deps`), and the gate requires that scope in the collection manifest. The initial production-only proposal remains archived and does not approve the three additional high findings. Current packet: 186 exact lab-only entries explicitly approved on 18 October, expiring 25 October 2026 at 00:00 IST. All 25 contracts and the approved source gate pass locally and in hosted run `39110505372`; no application/dependency upgrade is implied.
