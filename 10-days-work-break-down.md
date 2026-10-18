# PipelineFortress: 10-day hands-on execution guide

**Project:** CAP-DSE-3W — Secure CI/CD with GenAI-Assisted Triage  
**Repository:** https://github.com/swetha12g/IITR-Capstone-Proj  
**Working branch:** `feature-16-kick-start`  
**Planning date:** 16 October 2026  
**Status:** execution guide; project implementation and successful runs are not yet claimed.

This guide replaces the three-week calendar in [the detailed roadmap](docs/PipelineFortress_Detailed_Roadmap.pdf) with ten working days. It retains all mandatory technical requirements. Budget **50 focused hours: approximately five hours per day**, including integration and troubleshooting allowance above the assignment's 35–40-hour estimate. Installation failures or unfamiliar tools may require additional time. Day 1 means the day you begin; dates are intentionally not assumed.

The goal is complete, reproducible evidence against every rubric category. A grade or a perfect execution result cannot be guaranteed in advance. Record failures and limitations honestly.

## 1. Scope and decisions

Use the following default until the program coordinator resolves the assignment's conflicting scope table:

| Item | Default individual execution | Team adjustment |
|---|---|---|
| Target | OWASP Juice Shop | Add one small custom microservice |
| Security checks | SAST, SCA, secrets, IaC, container, DAST | Same, including microservice |
| AI remediation PRs | Three, matching the main deliverable list | Four |
| Final report | 12 pages, overlapping the main 12–15 and individual 10–12 ranges | 14–15 pages, overlapping main/team ranges |
| Stretch work | Falco and policy-explanation bot optional | Optional after core acceptance |

The wording “five stages” does not justify omitting a named technology. Use **six scan jobs**, counting container scanning separately. Checkov and DAST remain in the default plan despite omissions in the individual table.

Confirm on Day 1: individual/team mode, actual OS/architecture, machine capacity, submission date, coordinator interpretation, API provider/model and spending cap. These decisions do not prevent preparing the lab or mock-based AI tests.

**Submission repository versus fork:** this repository is an existing project repository, not evidence of an upstream Juice Shop fork. The assignment explicitly requests a fork. Create a separate upstream fork and record its URL/commit, or obtain coordinator acceptance for a provenance-preserving source import. Do not describe an imported copy as a GitHub fork.

**Public repository:** publish only reviewed, sanitized project material here. Keep cohort-confidential findings, raw scanner reports, signed acknowledgements and sensitive logs in an approved restricted location. GitHub Actions artifacts/logs in a public repository must not be treated as confidential storage. Suppress sensitive console output, process raw results locally in the runner, and upload only approved sanitized artifacts. The existing roadmap can remain public; do not add the original assignment or confidential evidence without authorization.

## 2. Ten-day delivery map

| Day | Hours | Work | Must exist at end of day |
|---|---:|---|---|
| 1 | 5 | Environment, repository, upstream provenance, build | Version record, scope, app build/test evidence |
| 2 | 5 | Container, local kind, baseline runtime, CI build | Running app, baseline report, build/test workflow |
| 3 | 5 | Semgrep, Trivy SCA, gitleaks, gates | Three source-stage reports and bad/fixed gate evidence |
| 4 | 5 | Checkov, custom policy, container hardening | Tested IaC controls, image comparison, SBOM |
| 5 | 5 | ZAP baseline and complete CI integration | All six scan jobs, runtime report, aggregate gate |
| 6 | 5 | Normalization, labeled ground truth, dashboard | Recomputable metrics and detection evaluation |
| 7 | 5 | Redaction, safe prompts, refusal tests | Proven pre-egress safeguards with mock transport |
| 8 | 5 | Real API triage, grounding, evaluation | Validated triage and honest AI FP/FN results |
| 9 | 5 | Three AI-assisted remediation PRs, reviews | PR links, before/after tests and review ledger |
| 10 | 5 | Fresh reproduction, report, maturity, defense | Submission index, final report, release evidence |
| **Total** | **50** | Core requirements plus integration allowance | **Evidence-backed submission** |

Do not borrow time from redaction or human review to add optional features. If a day is blocked, log the reason, continue independent documentation/mock work, and resolve the dependency before asserting completion.

## 3. Working conventions: read before running commands

Commands below use **Bash on Linux or WSL2 Ubuntu**. They are not PowerShell commands. Windows users should install WSL2 and configure Docker Desktop WSL integration; native Linux users can use Docker Engine. Use one daemon/context consistently. Confirm virtualization support before troubleshooting kind.

Suggested lab capacity: four CPU cores, 16 GB RAM, 30–50 GB free disk; these are planning estimates. No cloud Kubernetes account is necessary. Use a GitHub-hosted Linux runner with a new ephemeral kind cluster for CI. Your laptop's kind cluster and the runner's cluster are separate.

### Required software and purpose

| Software | Purpose | Check |
|---|---|---|
| Git and optionally GitHub CLI | Clone, branches, authenticated PRs | `git --version`, `gh --version` |
| Docker | Build image and host kind nodes | `docker version`, `docker info` |
| kind, kubectl | Local Kubernetes and deployment | `kind version`, `kubectl version --client` |
| Node.js/npm | Juice Shop build/test | `node --version`, `npm --version` |
| Python 3, venv, pytest, jsonschema | Adapters, AI controls, tests | `python3 --version` |
| curl, jq | HTTP and JSON diagnostics | `curl --version`, `jq --version` |
| Semgrep | SAST | `semgrep --version` |
| Trivy | Dependency and container vulnerabilities | `trivy --version` |
| gitleaks | Secret history/working-tree scans | `gitleaks version` |
| Checkov | IaC and custom policies | `checkov --version` |
| Syft | SBOM | `syft version` |
| ZAP container | Baseline DAST | Pinned official image digest |
| Editor and Markdown/PDF renderer | Code and report | Open/render a sample |

Install tools from their official release instructions linked at the end. Check OS and CPU architecture first. Verify provided checksums/signatures. Select a Juice Shop release and use a Node version supported by that release's README/package metadata; do not assume the newest Node version works. Pin versions after a smoke test. Do not paste unreviewed installation scripts into a privileged shell.

**Commands fall into two categories:** setup commands operating on existing tools/files, and acceptance commands for **planned** scripts created on the stated day. A command such as `python -m triage.normalize` will work only after implementing that module and its documented CLI. The guide does not imply these modules are already committed.

### Repository layout to create during implementation

This guide uses `app/juice-shop/` because the supplied repository already contains project documentation. This is an explicit adaptation of the original roadmap's root-level app layout. Scan/build paths must use this directory consistently.

```text
.github/workflows/security.yml
.github/workflows/triage.yml
app/juice-shop/                 # pinned upstream source; preserve LICENSE
infra/kind.yaml
infra/k8s/namespace.yaml
infra/k8s/deployment.yaml
infra/k8s/service.yaml
policies/semgrep/
policies/checkov/
policies/zap/rules.conf
policies/gates.json
policies/exceptions.json
triage/__init__.py
triage/normalize.py
triage/redact.py
triage/client.py
triage/validate.py
triage/propose.py
prompts/triage-system.txt
prompts/triage-user-template.json
tests/fixtures/
tests/policies/
tests/redaction/
tests/triage/
scripts/scan.sh
scripts/gate.py
scripts/deploy.sh
scripts/reproduce.sh
metrics/build_dashboard.py
docs/versions.md
docs/upstream-provenance.md
docs/requirements-checklist.md
docs/daily-log.md
docs/evidence-index.md
docs/reviews.md
docs/final-report.md
reports/sanitized/             # reviewed outputs only
reports/private/               # ignored; never public artifacts
```

Implement scripts before referring to them as runnable deliverables. Define argument parsing, exit codes, expected files and tests together. Do not commit empty placeholders and call the stage complete.

### Daily close-out routine

1. Update the day's status, commands, result, blocker and next action in `docs/daily-log.md`.
2. Record sanitized evidence in `docs/evidence-index.md`: requirement ID, commit, run URL, artifact/checksum, verdict and limitation.
3. Inspect `git status --short` and `git diff --check`.
4. Stage explicit safe paths; avoid `git add .` when raw reports or upstream content are present.
5. Review `git diff --cached`, scan staged changes for secrets, then commit and push the working branch.
6. A day is “passed” only when its acceptance checks pass. Use “blocked” or “failed” when appropriate.

## Day 1 — Environment, provenance and first successful build

**Timebox:** 1h environment; 1h Git/provenance; 2h app build/tests; 1h records.

### Step 1. Open the correct terminal and validate tools

In Linux/WSL Bash, run:

```bash
uname -s
uname -m
git --version
docker version
docker info
kind version
kubectl version --client
python3 --version
node --version
npm --version
```

If `docker info` fails, resolve the daemon/context before using kind. If a tool is absent, install it from its official instructions, then repeat its version check. Do not treat Docker client availability as proof that the daemon is running.

### Step 2. Clone and select the existing feature branch

```bash
git clone https://github.com/swetha12g/IITR-Capstone-Proj.git
cd IITR-Capstone-Proj
git fetch origin
git switch feature-16-kick-start
git status --short
git branch --show-current
mkdir -p app infra/k8s policies/{semgrep,checkov,zap}
mkdir -p triage prompts tests/{fixtures,policies,redaction,triage}
mkdir -p scripts metrics docs reports/{private,sanitized}
```

If the repository already exists locally, enter it and check for uncommitted work before fetching/switching. Do not reset or overwrite local changes.

Create `.gitignore` entries for `reports/private/`, `.env`, `.venv/`, `node_modules/`, caches, kubeconfig files, local alias maps and API traces. Add a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest jsonschema
```

Record/pin Python dependencies in a project requirements file after testing compatibility. Keep scanner tools in their own supported environment or pinned containers to avoid dependency conflicts with Checkov/Semgrep.

### Step 3. Acquire and pin upstream source

1. Fork `juice-shop/juice-shop` using GitHub's Fork action into an appropriate account, if required by the coordinator.
2. Record the fork URL and chosen immutable upstream commit in `docs/upstream-provenance.md`.
3. Clone the fork **outside this repository**, check out the chosen commit, and copy its tracked source into `app/juice-shop/` using `git archive`. This avoids a nested `.git` directory or an accidental broken submodule.
4. Preserve LICENSE/NOTICE files. State that this repository contains an imported snapshot linked to the separate fork.

Example after choosing a verified commit; replace the two values first:

```bash
git clone YOUR_JUICE_SHOP_FORK_URL ../juice-shop-source
git -C ../juice-shop-source checkout VERIFIED_UPSTREAM_COMMIT
git -C ../juice-shop-source rev-parse HEAD
git -C ../juice-shop-source archive HEAD | tar -x -C app/juice-shop
```

Do not execute placeholder tokens literally. Do not archive `.git` or the build outputs from an unreviewed directory. This source import/provenance approach needs coordinator acceptance if the assessed repository itself must be the GitHub fork.

### Step 4. Build and test

```bash
cd app/juice-shop
node -p 'JSON.stringify(require("./package.json").engines)'
npm run
npm ci
npm run build
```

Inspect the pinned release's npm scripts and contributor instructions. Run its documented non-watching unit/CI test command. Do not assume `npm test` is headless or finite; if it launches a browser/watch mode, use the documented CI variant and record exactly which test suites ran. Native dependency failures often mean a Node/OS mismatch; do not delete the lockfile as a first fix.

### Step 5. Record the operating contract

Create `docs/versions.md`, scope decisions and the requirements checklist. Include host OS/architecture, tool versions, app commit, Node/npm, baseline test command, API budget decision and known blockers. Start the final-report outline now.

**Day 1 acceptance:** [ ] correct branch; [ ] provenance/license; [ ] Docker works; [ ] app builds; [ ] selected tests pass; [ ] no credentials staged.  
**Suggested commit:** `docs: record environment and upstream provenance` plus a separate reviewed source-import commit.

## Day 2 — Container, kind deployment and baseline CI

**Timebox:** 1h image; 1.5h Kubernetes; 1h runtime baseline; 1h CI; 0.5h evidence.

### Step 1. Build from your imported source

From repository root:

```bash
docker build -t pipelinefortress:baseline app/juice-shop
docker image inspect pipelinefortress:baseline
```

Use the pinned upstream Dockerfile initially. Record the image ID and source commit privately. Do not use only a downloaded prebuilt image as your implementation evidence.

### Step 2. Author the local lab manifests

Create `infra/kind.yaml` with a one-control-plane kind cluster. Create a namespace named `pipelinefortress`, a `juice-shop` deployment and a ClusterIP service named `juice-shop`. Initial deployment contract:

- Image `pipelinefortress:baseline`, `imagePullPolicy: IfNotPresent`.
- Container and service target port 3000, assuming verified upstream configuration.
- Matching selector labels, HTTP readiness probe and reasonable startup allowance.
- No public LoadBalancer/Ingress or host-wide port exposure.

These manifests are authored on this day; they are not provided by the Markdown file itself. Validate their YAML/schema before applying.

```bash
kind create cluster --name pipelinefortress --config infra/kind.yaml
kind load docker-image pipelinefortress:baseline --name pipelinefortress
kubectl --context kind-pipelinefortress apply -f infra/k8s/
kubectl --context kind-pipelinefortress -n pipelinefortress \
  rollout status deployment/juice-shop --timeout=180s
kubectl --context kind-pipelinefortress -n pipelinefortress get pods
```

In terminal A, leave this running:

```bash
kubectl --context kind-pipelinefortress -n pipelinefortress \
  port-forward --address 127.0.0.1 service/juice-shop 3000:3000
```

In terminal B:

```bash
curl --fail --silent --show-error http://127.0.0.1:3000/ -o /dev/null
```

Open `http://127.0.0.1:3000` locally. Capture a sanitized running-app screenshot and workload status. If rollout fails, inspect `kubectl describe pod` and pod logs privately before changing settings.

### Step 3. Write the runtime baseline

Document at least three locally confirmed weaknesses or insecure behaviors, with observation, reproduction in this owned lab, expected behavior, risk and evidence reference. Keep scanner-only suspicions separate from confirmed runtime findings. Do not scan external targets or include customer data.

### Step 4. Implement baseline Actions workflow

Create `.github/workflows/security.yml` with `push` on the feature branch and `pull_request` triggers. Use `permissions: contents: read`, pinned action SHAs, timeouts and a supported pinned Ubuntu runner image. App installation/build/tests run in `app/juice-shop`. The deployment job creates **its own kind cluster** and cleans it up in a finalization step.

Do not point the hosted runner at laptop localhost. Later scan jobs need consistent app/image artifacts: either build/deploy/DAST in the same runner job or explicitly transfer the exact image artifact between jobs.

**Day 2 acceptance:** [ ] built source image; [ ] local kind Ready; [ ] HTTP reachable; [ ] baseline runtime report; [ ] CI build/test success; [ ] run URL recorded.  
**Suggested commit:** `feat: add baseline build and kind deployment`.

## Day 3 — SAST, SCA, secrets and measurable gates

**Timebox:** 2h scanners; 1h baseline triage; 1.5h gate implementation/tests; 0.5h records.

### Step 1. Configure the scanners

Install/pin the official CLIs or containers. Put reviewed Semgrep rules in `policies/semgrep/`, including rules relevant to the app's JavaScript/TypeScript and your own policy fixtures. Document generated/vendor exclusions; never exclude all app source.

From repository root, produce private machine-readable outputs:

```bash
semgrep scan --config policies/semgrep --json \
  --output reports/private/semgrep.json app/juice-shop
trivy fs --scanners vuln --format json \
  --output reports/private/sca.json app/juice-shop
gitleaks git . --redact --report-format json \
  --report-path reports/private/gitleaks.json
```

Gitleaks must scan full history in CI (`fetch-depth: 0`), including imported source. Add an appropriate working-tree scan using the pinned CLI's supported command. `--redact` is useful but does not automatically sanitize every field/path in a report. Never print the raw secret match.

### Step 2. Separate scan execution from gate evaluation

Implement `scripts/scan.sh` to capture each exit code, stdout/stderr privately, start/end time and expected report path. A finding exit code is different from an execution error. Check the pinned tool's documented codes. The aggregate `scripts/gate.py` parses valid reports and applies policy. Use narrowly scoped error capture in the scanner wrapper so all reports can be collected; do not use blanket `|| true` as a passing gate.

Create `policies/gates.json` with reviewed severity mappings:

| Stage | Proposed blocking condition |
|---|---|
| SAST | New validated high/critical rule findings; map Semgrep severities explicitly |
| SCA | New high/critical dependency vulnerabilities |
| Secrets | Any new suspected credential until locally reviewed |
| IaC | Project-defined critical control failures and reviewed Checkov checks |
| Container | New high/critical image vulnerabilities |
| DAST | Reviewed ZAP rules configured as FAIL |
| Every stage | Missing/invalid report, execution failure, mandatory skipped stage |

Create exact baseline exceptions with rule/advisory ID, component/path fingerprint, reason, owner, expiry and baseline commit. Preserve baseline risk visibility. Do not globally suppress Juice Shop findings or claim the intentionally vulnerable application is production-safe.

### Step 3. Prove bad and repaired behavior

Create synthetic fixtures, not real secrets: a Semgrep-detectable unsafe pattern, a dependency fixture tied to a known verified advisory, and a token-shaped canary. Add them in isolated test fixtures/branches; ensure fixtures do not accidentally become deployed app features. Verify the relevant scanner detects each, then repair/remove the seeded issue and demonstrate gate success. Record fixture scope so synthetic findings are not presented as real app defects.

Also test scanner crash, invalid JSON, missing report and expired exception. These must fail or block the aggregate status. Save sanitized evidence for failing and passing runs.

**Day 3 acceptance:** [x] three scanners execute; [x] JSON validated; [ ] precise baseline exceptions reviewed; [x] bad/fixed demonstrations; [x] operational-error tests; [ ] no secret in public logs (hosted check pending).

**Execution on 18 October 2026:** local scanner/gate/fixture evidence is recorded in [docs/day3-checkpoint.md](docs/day3-checkpoint.md), synchronized with the PF-D3 board in [docs/daily-log.md](docs/daily-log.md). Exact baseline risk review and hosted verification remain pending; the Day 3 gate currently blocks unaccepted findings. The complete six-stage gate is not claimed.
**Suggested commit:** `feat: add source security scans and regression gates`.

## Day 4 — IaC, secure image and SBOM

**Timebox:** 1.5h Checkov/policy; 1.5h image; 1h Kubernetes hardening; 1h SBOM/evidence.

**Mandatory entry condition:** complete the program's Responsible AI Use and Lab Conduct acknowledgement **before starting the work corresponding to Week 2**, which starts here in the compressed calendar. Record completion/date privately; do not commit a signature to this public repository.

### Step 1. Add Checkov and custom policy-as-code

```bash
checkov -d infra/k8s --framework kubernetes -o json \
  > reports/private/checkov.json
checkov -d app/juice-shop --framework dockerfile -o json \
  > reports/private/checkov-dockerfile.json
```

Write a custom Checkov rule for a concrete supported control, such as disallowing mutable `latest` images. Store it under `policies/checkov/` and load it with the pinned CLI's `--external-checks-dir` option. Add passing and failing fixture tests; verify the custom check ID appears in actual results. Built-in rule execution alone is not evidence that your custom rule ran.

Map applicable checks to the chosen CIS benchmark/version. Identify uncovered controls and exceptions. A Checkov pass does not establish full Kubernetes cluster CIS compliance.

### Step 2. Harden without breaking the app

Create a project Dockerfile or carefully update the imported one. Use a supported pinned base/digest, minimal runtime dependencies, non-root user and a clean build context. Use multi-stage build if compatible. Verify expected writable paths and permissions. Never bake API keys into image layers or build arguments.

In Kubernetes, test: `runAsNonRoot`, `allowPrivilegeEscalation: false`, dropped capabilities, `RuntimeDefault` seccomp, resource requests/limits, probes and `automountServiceAccountToken: false` where unnecessary. Test read-only root filesystem with explicit writable mounts for required app directories. Do not silently disable a control solely to get a green run.

### Step 3. Build, scan and inventory the same image

```bash
docker build -t pipelinefortress:hardened app/juice-shop
trivy image --scanners vuln --format json \
  --output reports/private/container.json pipelinefortress:hardened
syft pipelinefortress:hardened -o cyclonedx-json \
  > reports/private/sbom.cdx.json
docker image inspect pipelinefortress:hardened
sha256sum reports/private/sbom.cdx.json
```

Validate SBOM format/schema and representative package names/versions. Record app commit, image identity, SBOM checksum, tool versions and vulnerability DB timestamp. A local Docker image ID and a registry manifest digest are different identifiers; label them correctly. If moving jobs, export/import the same image archive and verify its checksum.

Load the hardened tag into kind, update the deployment image, rerun readiness/functional tests and compare vulnerabilities to baseline. Any remaining intentional app weaknesses must stay in the risk register.

**Day 4 acceptance:** [ ] built-in/custom IaC tests; [ ] mapped applicable controls; [ ] functional non-root image; [ ] same image scanned/SBOM generated; [ ] before/after evidence.  
**Suggested commit:** `feat: add IaC policies image hardening and SBOM`.

## Day 5 — ZAP and the complete pipeline

**Timebox:** 1.5h networking/DAST; 2h CI integration; 1h gate regression tests; 0.5h report updates.

### Step 1. Confirm scanner-to-app connectivity

Run deployment readiness and local curl first. On a **Linux runner**, ZAP can use host networking to reach the loopback port-forward. Docker Desktop networking differs; validate it explicitly or run ZAP inside a suitable lab network. Do not expose the app to the internet as a workaround.

After pulling an approved ZAP release, record and use its immutable digest. The readable `stable` tag below is a discovery/example value and must be replaced with the verified digest in final CI.

```bash
mkdir -p reports/private/zap
docker pull ghcr.io/zaproxy/zaproxy:stable
docker image inspect ghcr.io/zaproxy/zaproxy:stable
```

Determine the container user's UID/GID and make only the report directory writable to that user. Then, on Linux with the port-forward running:

```bash
docker run --rm --network host \
  -v "$PWD/reports/private/zap:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t http://127.0.0.1:3000 -J zap.json -r zap.html
```

The baseline scan crawls and reports passive alerts; it does not provide full active, authenticated or single-page-app coverage. Save that limitation. ZAP baseline exit codes: 0 success; 1 FAIL alerts; 2 WARN-only result; 3 operational failure. Configure reviewed rules in `policies/zap/rules.conf` and add `-c` once the file exists and has been tested. A code 3 cannot be waived as a vulnerability exception.

### Step 2. Integrate six jobs and one authoritative gate

Workflow contracts:

1. Build/test source using pinned runtime and lockfile.
2. SAST, SCA and secret scans with full Git history where needed.
3. Checkov scans and custom policy tests.
4. Build image, scan that exact image and generate its SBOM.
5. Create isolated kind staging, deploy the image, wait for readiness and run ZAP.
6. Normalize status/evidence and evaluate an aggregate check that cannot pass if mandatory jobs are skipped/failed.
7. Sanitize and publish approved summaries; clean up the cluster in finalization.

Use job outputs/artifacts deliberately; jobs do not share a filesystem or Docker daemon. In the vulnerable baseline lab, document the exact exception allowing staging DAST despite known baseline findings. Production-style promotion requires the relevant blocking checks to pass.

PR workflows have read-only permissions and no LLM secret. Avoid privileged `pull_request_target`/`workflow_run` execution of untrusted code. Pin actions to full SHAs; do not interpolate untrusted PR text into shell commands. Keep AI submission in a separate trusted/manual workflow.

### Step 3. Run end-to-end gate tests

Exercise one known bad/fixed case per stage, mandatory-stage skip, missing artifact, malformed report and expired exception. Confirm the aggregate check fails correctly. Check actual URLs/routes reached by ZAP, not just container exit status. Store a sanitized run manifest with commit/run IDs, tool versions, times, exit codes and artifact checksums.

**Day 5 acceptance:** [ ] all six stages execute; [ ] DAST reaches app; [ ] rule policy enforced; [ ] exact-image linkage; [ ] invalid/skipped stages cannot pass; [ ] cleanup works.  
**Suggested commit:** `feat: complete security pipeline with staging DAST`.

## Day 6 — Normalization, ground truth and metrics

**Timebox:** 2h adapters; 1h labels; 1.5h dashboard; 0.5h verification.

### Step 1. Implement scanner adapters

Implement `triage/normalize.py` with a CLI accepting `--input-dir` and `--output`. Each supported report adapter must be tested using sanitized samples from the pinned tool version. Unknown schemas fail closed.

Internal normalized schema: stable finding ID, underlying issue ID, scanner/stage, rule/advisory ID, original/normalized severity, component/path reference, fingerprint, first-seen timestamp, commit/run reference, status and private evidence pointer. Internal records are **not yet safe for the API**.

Deduplicate by vulnerability/component/version/location as appropriate, retaining every detecting stage and source record. Do not collapse unrelated findings solely because they share a title. Keep source and container observations linked without double-counting the same underlying issue in global metrics.

Planned acceptance commands after implementation:

```bash
python -m pytest tests/triage -q
python -m triage.normalize --input-dir reports/private \
  --output reports/private/normalized.json
```

### Step 2. Label a small evaluation dataset

Create safe fixture labels: ideally two known positive cases and one safe negative for each stage, plus manually reviewed actual findings. Use unique vulnerability IDs and record reviewer rationale. Record known misses, not only detected cases. Keep scanner detection labels and AI triage labels separate.

### Step 3. Build a reproducible dashboard

Implement `metrics/build_dashboard.py` with `--findings`, `--labels`, `--output`. Generate a static HTML dashboard plus JSON/CSV inputs containing only reviewed safe data. Use consistent UTC timestamps internally.

Display:

- Introduced, caught and missed unique vulnerabilities by stage/run.
- TP, FP, FN, TN and sample sizes; precision, recall and F1.
- Pre-merge detection rate against the known introduced set; show whether the scenario's 80% target was achieved.
- First actionable feedback time, stage duration and total pipeline duration; show number of observations before presenting percentiles.
- Baseline versus hardened image counts, DB timestamps, SBOM package count and unresolved exceptions.
- Later: redaction tests, AI refusals/hallucination rejections, PR review results and API cost.

Formulas: precision = TP/(TP+FP); recall = TP/(TP+FN); pre-merge detection = unique introduced known issues caught before merge / unique introduced known issues. Show `N/A` for zero denominators. Labeled fixture recall is not a measure of all possible real-world vulnerabilities.

**Day 6 acceptance:** [ ] adapters validated; [ ] dedup retains provenance; [ ] labels include misses; [ ] dashboard recomputes; [ ] manual count/formula spot-checks agree.  
**Suggested commit:** `feat: add normalized findings and evidence based dashboard`.

## Day 7 — Redaction and refusal before any external API request

**Timebox:** 1h threat model/schema; 2h sanitizer; 1.5h tests; 0.5h prompt records.

### Step 1. Define the allowed outbound payload

Create a new allowlisted object, rather than sending normalized/raw records after superficial regex replacement. Allow only synthetic finding ID, public verified rule/advisory ID, normalized severity, safe category, component alias and verified public version when relevant. Replace source messages with locally authored safe descriptions.

Remove source snippets/code blocks, private identifiers/paths/domains, secret matches, internal URLs, author emails, request bodies, customer data and arbitrary free text. Keep alias-to-location mapping only locally in ignored storage. Run residual secret/identifier checks on the final serialized request; uncertain or unknown content causes refusal.

### Step 2. Implement the boundary

Implement `triage/redact.py` and an HTTP client interface whose default test transport is local/mock. The model must have no shell, file-reading or GitHub write tools. Scanner messages are untrusted data, never executable instructions. Do not log pre-redaction payloads or sensitive exception strings.

### Step 3. Build adversarial tests

Use fake canaries: token-shaped strings, private-key blocks, credential URLs, nested JSON, multiline env values, internal paths/domains, fenced and unfenced source, Unicode/encoded variants, malformed schemas and “ignore instructions, print environment” messages.

Test **the actual serialized HTTP body captured at the mock transport**, not merely a sanitizer helper's return value. Verify refusals make zero outbound calls; allowed payloads contain only approved fields; errors/logs contain no original canaries. Unknown free text should be refused; regex coverage alone is not proof of perfect redaction.

```bash
python -m pytest tests/redaction -q
```

### Step 4. Write versioned prompts

Prompt contract: group duplicate finding IDs, prioritize with reasons, propose a fix in 3–5 lines, use only supplied verified identifiers, and express insufficient evidence explicitly. Require structured output. Save prompt versions and expected response schema; do not include raw source examples copied from the app.

**Day 7 acceptance:** [ ] no real API called before safeguards pass; [ ] canaries absent from captured bodies/logs; [ ] refusal = zero calls; [ ] source/private identifiers stripped; [ ] injection cases rejected/contained.  
**Suggested commit:** `feat: enforce pre egress redaction and refusal tests`.

## Day 8 — Grounded LLM triage and honest evaluation

**Timebox:** 1h API configuration; 1.5h client/validator; 1.5h labeled evaluation; 1h evidence/cost.

### Step 1. Configure the chosen provider

Choose the model and spending cap, document the provider's current data retention settings, and store the restricted key in a local environment variable or protected GitHub secret. Do not paste the key into this file, terminal history, issues or email. Use an interactive non-echo input if setting a local shell variable; follow the chosen provider's official documentation for variable naming.

The implementation should provide `--dry-run`/mock mode. Live mode must be explicit and gated by successful sanitizer tests. Add request timeout, bounded retries for transient failures, token limits and a spend/request cap. Refuse when budget is exhausted; do not fabricate a result.

### Step 2. Implement and validate output

`triage/client.py` sends only the approved payload. `triage/validate.py` checks schema, known finding IDs, valid enum values and grounded advisory/package references. Reject unknown CVEs, invented fixed versions, unsupported claims, malformed JSON and invalid cluster references. Verify advisory data using scanner metadata/vendor sources rather than trusting the model.

Planned CLIs after implementation:

```bash
python -m triage.client --input reports/private/normalized.json \
  --output reports/private/triage.json --dry-run
python -m pytest tests/triage tests/redaction -q
```

Then perform a small live call through the same sanitizer path using the documented explicit live option. Record model identifier/date, prompt version, input/output counts, cost and response-validation verdict without leaking request content.

### Step 3. Evaluate independently of scanner quality

Compare AI duplicate clusters, priorities, omissions and fix recommendations with reviewed labels. Report true/false escalations, missed/incorrectly downgraded real issues, unsupported identifiers, refusals and first-pass validity. Include a deliberate fabricated-CVE response fixture to prove rejection. Show counts and limitations even if results are poor.

**Source-free remediation design:** the external model proposes a sanitized parameterized fix plan. A local deterministic patch adapter maps approved operations to real paths using the private location map. This permits AI-assisted PRs while honoring the assignment's prohibition on sending source code externally. If a fix cannot be expressed safely, select another verified actionable finding or seek instructor guidance; never weaken redaction for convenience.

**Day 8 acceptance:** [ ] safe live call recorded; [ ] grounding validator passes/rejects fixtures; [ ] 3–5-line fixes; [ ] honest FP/FN analysis; [ ] costs/model disclosure; [ ] no raw source sent.  
**Suggested commit:** `feat: add grounded AI triage and evaluation`.

## Day 9 — Three remediation PRs and genuine human review

**Timebox:** 0.5h selection; 2h bounded patch adapters/PR creation; 1.5h tests/review; 1h ledger/report.

### Step 1. Select three real findings

Select the top actionable findings from actual validated results, balancing risk and safe fixability. Potential categories are a Kubernetes hardening setting, a supported dependency/base-image update and a validated app/configuration weakness. These are candidate categories, not assertions about the chosen app version.

### Step 2. Generate and validate bounded patches locally

Implement `triage/propose.py` to accept only validated operation types/parameters and an allowlist of target files. Reject path traversal, workflow edits, credential files, redaction changes and arbitrary commands. Limit files/lines changed. Never execute model text as shell or allow the model to select arbitrary repository/branch destinations.

For each fix: capture the original finding, generated plan, local template, actual diff, failing regression before the change, passing regression after, functional tests and scanner rescan. Verify the stated issue is fixed and the app still works. Do not force breaking upgrades solely to reduce vulnerability counts.

### Step 3. Submit three independent PRs

Use branches such as `remediation/pf-001`, `remediation/pf-002`, `remediation/pf-003`. Base each on the intended integration branch after its prerequisite implementation is present. Do not stack unrelated fixes accidentally. In a single-owner repository, test the PR target carefully: a fix PR based on `feature-16-kick-start` should target that branch unless the baseline has already been integrated elsewhere.

The trusted submission step creates branches/commits and draft PRs using narrowly scoped write permissions. A manually created documentation PR does not count as one of the three AI-generated remediation PRs. Keep generation/submission provenance. If Actions PR creation is disabled, document the account restriction and use an authenticated, reviewed local automation path.

PR body template:

```markdown
## Finding and risk
- Finding/rule/advisory IDs:
- Confirmed impact and evidence:
## AI contribution
- Provider/model/date and prompt version:
- Sanitized generated fix plan:
- Local patch template and human edits:
## Verification
- Before regression/scan:
- After regression/scan:
- Functional tests and run URLs:
## Review and rollback
- Reviewer verdict and requested changes:
- Remaining risk and rollback procedure:
```

### Step 4. Obtain human review

Record the reviewer, date, first-review correctness, requested changes, final verdict and any human-authored edits in `docs/reviews.md`. The rubric asks that at least one PR be correct on first review; measure the actual outcome instead of promising it. No bot self-approval or auto-merge.

GitHub does not allow authors to approve their own PRs as an independent approving reviewer. Arrange an authorized teammate/instructor reviewer early. If unavailable for individual work, document your manual review notes and confirm the acceptable assessment evidence with the coordinator; do not invent an approval. Human approval precedes merge.

**Day 9 acceptance:** [ ] three genuine AI-assisted remediation PR links; [ ] separate focused diffs; [ ] before/after evidence; [ ] real review notes; [ ] no auto-merge; [ ] first-review result recorded honestly.  
**Suggested commit:** `docs: record remediation evidence and human reviews`.

## Day 10 — Reproduction, final report and oral defense

**Timebox:** 1.5h fresh reproduction; 2h report/evidence; 1h rehearsal; 0.5h release audit.

### Step 1. Reproduce from a fresh directory

Implement `scripts/reproduce.sh` to perform the documented local sequence without hidden machine state: tool preflight, app install/build/test, image build, source/IaC/image scans, SBOM, ephemeral kind deployment, readiness, ZAP, normalization, gates, mock AI tests and dashboard. Live API must remain opt-in. Ensure failure propagation and named-resource cleanup.

Clone the chosen submission commit into a separate directory and run the script. Compare outputs with the evidence index. The full run must distinguish “findings detected” from “scanner broken” and explain baseline exceptions. A successful mock run alone does not satisfy the real API deliverable.

### Step 2. Finish the evidence-based report

Default 12-page outline, subject to coordinator confirmation:

1. Executive summary, problem, scope and target detection rate.
2. Architecture and requirements mapping.
3. Environment, versions and reproducibility.
4. Baseline runtime vulnerabilities.
5. Six scan jobs, gates and exceptions.
6. Container/IaC hardening and SBOM identity.
7. ZAP findings and coverage limitations.
8. AI architecture, data flow and redaction evidence.
9. Triage results, hallucinations and FP/FN analysis.
10. Three PRs, validation and human review.
11. Dashboard and DevSecOps maturity self-assessment.
12. Ethics, GenAI disclosure, residual risks and references.

Use the course's maturity framework if provided, with its name/scale/source. Compare baseline/final evidence for review controls, test automation, coverage, supply chain, policy, remediation, metrics and AI governance. Do not claim enterprise maturity or full CIS compliance from a short lab. Render the PDF and visually inspect every page, table, caption and link.

GenAI disclosure includes model/provider/date, tasks, prompt versions, data exclusions, redaction verification, human changes, rejected outputs and cost. Preserve the program's confidentiality and lab-only restrictions.

### Step 3. Rehearse the defense

Prepare an approximately 8–10-minute practice demonstration, adapting to the instructor's actual allotted duration: architecture; baseline; blocked unsafe change; repaired run; image/SBOM linkage; dashboard; redaction refusal; hallucination rejection; one reviewed PR; honest limitations. Keep a clearly labeled recorded-run fallback for network failures.

Be ready to explain SAST/SCA/DAST differences, lockfile versus image scanning, SBOM limitations, safe baseline exceptions, why external source-free fix generation needs local adapters, and how you measured missed vulnerabilities.

### Step 4. Freeze and audit

Update all requirement statuses. Record final commit, run URLs, report/SBOM checksums, dashboard inputs and PR review outcomes. Tag a submission only after verified completion; do not label unfinished work “final.” Review the public tree for sensitive data. Push the agreed submission branch/tag without force-pushing shared history.

**Day 10 acceptance:** [ ] fresh reproduction; [ ] all mandatory evidence; [ ] rendered report checked; [ ] maturity assessment; [ ] disclosure/acknowledgement; [ ] rehearsed defense; [ ] no unsupported completion claims.

## 4. Requirement and rubric audit

| PDF requirement / rubric | Weight | Days | Evidence required |
|---|---:|---|---|
| Shift-left problem, 80% target, learning outcomes | Context | 1, 6, 10 | Scope, measured detection rate, maturity comparison |
| Pipeline coverage and sensible gates | 20% | 2–5 | All named jobs; bad/fixed runs; errors/skips fail |
| Container + IaC hardening | 15% | 4–5 | Actual hardened image, Checkov/custom rules, selected CIS mappings, Syft SBOM |
| LLM triage soundness | 20% | 6, 8 | Consolidated JSON, duplicates, priorities, 3–5-line fixes, grounded IDs, FP/FN |
| Redaction layer | 10% | 7–8 | Mock HTTP-body assertions, refusal/no-call tests, no source/secrets |
| Sample remediation PRs | 10% | 9 | Three PRs/default; four/team; review ledger; first-review correctness |
| Metrics + dashboard | 10% | 6, 8–10 | Introduced/caught/missed by stage, feedback time, labeled denominators |
| Report + oral defense | 15% | 1–10 | Final PDF, maturity self-assessment, reproducibility and demonstration |
| Week 1 baseline deliverable | Required | 1–3 | Working pipeline and baseline runtime report |
| Week 2 coverage deliverable | Required | 4–6 | Complete pipeline, SBOM and dashboard |
| Week 3 AI deliverable | Required | 7–10 | Triage, redaction, prompts, PRs and final report |
| Mode/duration/difficulty | Required planning | 1 | Scope decision, 10-day adaptation, effort and team contributions |
| Ethics, lab-only targets, confidentiality, disclosure | Required | Every day | Scope boundary, safe artifacts, acknowledgement before Day 4, disclosure |
| Reference sources | Required | 1, 10 | LMS, relevant official framework/tool references |
| Falco + SIEM stub | Optional | After core passes | Supported driver, actual test alert, sanitized forwarding evidence |
| LLM Checkov policy bot | Optional | After core passes | Plain-language explanation, grounding, same redaction controls |

## 5. Troubleshooting and recovery

| Symptom | First checks | Completion rule |
|---|---|---|
| Docker client works, daemon fails | Desktop/daemon running, context, WSL integration | `docker info` must succeed |
| npm/native build failure | Pinned app's Node support, OS libraries, lockfile | Keep lockfile; rerun supported build/test |
| ImagePullBackOff | Correct kind name, loaded tag, pull policy, manifest image | Exact expected image runs |
| CrashLoopBackOff | Private pod logs, non-root permissions, writable paths, probes | App readiness and functional tests pass |
| ZAP cannot connect | Curl from scanner's namespace, port-forward process/network | Actual app requests observed |
| ZAP cannot write reports | Container UID/GID and mounted directory ownership | JSON/HTML created without broad permission changes |
| Trivy database error | Network/rate limits, bounded retry, supported cache, DB age | No “zero findings” fabricated from an error |
| Semgrep empty unexpectedly | Rule languages, paths/exclusions, positive fixture | Known vulnerable fixture detected |
| Gitleaks misses history | Full history checkout and pinned CLI command | Synthetic canary detected without public leakage |
| Checkov custom rule absent | External-check loading and check ID in report | Pass/fail fixture proves execution |
| API timeout/rate limit | Budget, bounded retry, service status | Record failed triage; retain scanner results |
| Model invented CVE/fix | Schema and allowlist grounding validation | Reject; no PR from unvalidated result |
| Reviewer unavailable | Arrange authorized reviewer, ask coordinator evidence policy | Never record fake approval |

If setup is still blocked at Day 2's end, keep moving on requirements, test fixtures and report skeleton, but revise remaining capacity honestly. The ten-day schedule compresses the calendar, not the evidence standard.

## 6. Daily status template

Copy this into `docs/daily-log.md` for each day:

```markdown
### Day N — YYYY-MM-DD
- Planned / actual hours:
- Branch / commit:
- Objective:
- Commands and actual results:
- CI run URL:
- Sanitized evidence / checksum:
- Acceptance: passed / failed / blocked / accepted exception
- Remaining risk or blocker:
- Next action and owner:
```

## 7. Official references

Version compatibility must be verified against the chosen release at implementation time. These links explain tool behavior; they are not evidence that this project has run.

- [Original project roadmap in this branch](docs/PipelineFortress_Detailed_Roadmap.pdf)
- [OWASP Juice Shop source and supported setup](https://github.com/juice-shop/juice-shop)
- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub privileged PR trigger guidance](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- [Semgrep CLI reference](https://semgrep.dev/docs/cli-reference)
- [Trivy documentation](https://trivy.dev/docs/)
- [gitleaks releases and commands](https://github.com/gitleaks/gitleaks)
- [Checkov Kubernetes scans](https://www.checkov.io/7.Scan%20Examples/Kubernetes.html)
- [Checkov custom policy overview](https://www.checkov.io/3.Custom%20Policies/Custom%20Policies%20Overview.html)
- [Syft SBOM generation](https://github.com/anchore/syft)
- [ZAP baseline scan, options and exit codes](https://www.zaproxy.org/docs/docker/baseline-scan/)
- [Falco documentation, optional](https://falco.org/docs/)
- Program LMS: EC-Council Essentials module outlines/labs and Responsible AI Use/Lab Conduct acknowledgement.
- Assignment frameworks: [MITRE ATT&CK](https://attack.mitre.org), [NIST CSF 2.0](https://www.nist.gov/cyberframework), [OWASP](https://owasp.org), [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks), [CERT-In](https://www.cert-in.org.in).

**Final rule:** claim completion only from actual tests, runs, artifacts and human review. Preserve known limitations and residual risk in the final submission.
