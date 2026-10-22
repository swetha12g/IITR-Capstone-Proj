#!/usr/bin/env python3
"""Render a twelve-page report from verified project evidence and explicit limits."""
from collections import Counter
from datetime import datetime, timezone
import html
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String, Line

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf/PipelineFortress_Study_Report.pdf'
NAVY = colors.HexColor('#153047')
TEAL = colors.HexColor('#166e79')
PALE = colors.HexColor('#eef5f7')
AMBER = colors.HexColor('#fff1d3')
GRAY = colors.HexColor('#526c7b')
WIDTH = A4[0] - 84
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='PFBody', fontName='Helvetica', fontSize=10.2, leading=15.2, textColor=NAVY, spaceAfter=9))
styles.add(ParagraphStyle(name='PFSmall', fontName='Helvetica', fontSize=8.6, leading=12.3, textColor=GRAY, spaceAfter=7, wordWrap='CJK'))
styles.add(ParagraphStyle(name='PFTitle', fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=NAVY, spaceAfter=16))
styles.add(ParagraphStyle(name='PFSub', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=TEAL, spaceBefore=12, spaceAfter=8))
styles.add(ParagraphStyle(name='PFCell', fontName='Helvetica', fontSize=8.7, leading=12.3, textColor=NAVY, wordWrap='CJK'))
styles.add(ParagraphStyle(name='PFHead', fontName='Helvetica-Bold', fontSize=8.7, leading=12.3, textColor=colors.white))
story = []
markdown = []


def read(relative, default=None):
    path = ROOT / relative
    return json.loads(path.read_text()) if path.exists() else default


def p(text, small=False):
    story.append(Paragraph(html.escape(text), styles['PFSmall' if small else 'PFBody']))
    markdown.append(text + '\n')


def heading(number, title):
    if story:story.append(PageBreak())
    story.append(Paragraph(f'{number:02d} / PIPELINEFORTRESS', styles['PFSmall']))
    story.append(Paragraph(html.escape(title), styles['PFTitle']))
    markdown.append('\n## ' + str(number) + '. ' + title + '\n')


def sub(title):
    story.append(Paragraph(html.escape(title), styles['PFSub']))
    markdown.append('\n### ' + title + '\n')


def table(rows, widths=None):
    data = [[Paragraph(html.escape(str(c)), styles['PFHead' if index == 0 else 'PFCell']) for c in row] for index, row in enumerate(rows)]
    result = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    result.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), NAVY), ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE]), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LINEBELOW', (0, 0), (-1, 0), 0.6, NAVY), ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.HexColor('#dce6ec'))]))
    story.extend([result, Spacer(1, 12)])
    markdown.append('| ' + ' | '.join(str(v) for v in rows[0]) + ' |\n|' + '|'.join('---' for _ in rows[0]) + '|')
    markdown.extend('| ' + ' | '.join(str(v).replace('|', '/') for v in row) + ' |' for row in rows[1:])
    markdown.append('')


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#d5e1e7'));canvas.line(42, 39, A4[0] - 42, 39)
    canvas.setFont('Helvetica', 8);canvas.setFillColor(GRAY)
    canvas.drawString(42, 25, 'Owned study lab | 22 October 2026 | Evidence and limitations retained')
    canvas.drawRightString(A4[0] - 42, 25, f'{doc.page} / 12')
    canvas.restoreState()


def architecture():
    drawing = Drawing(WIDTH, 190)
    for index, label in enumerate(['SAST', 'SCA', 'Secrets', 'IaC', 'Image', 'DAST']):
        x = index * (WIDTH / 6)
        drawing.add(Rect(x + 2, 140, WIDTH / 6 - 8, 35, fillColor=TEAL, strokeColor=None, rx=4))
        drawing.add(String(x + WIDTH / 12 - 2, 153, label, textAnchor='middle', fillColor=colors.white, fontName='Helvetica-Bold', fontSize=9))
        drawing.add(Line(x + WIDTH / 12, 140, WIDTH / 12, 110, strokeColor=GRAY, strokeWidth=0.6))
    for x, label in [(0, 'Normalize + retain provenance'), (WIDTH / 2 + 6, 'Study gate + deferred register')]:
        drawing.add(Rect(x, 75, WIDTH / 2 - 8, 35, fillColor=PALE, strokeColor=TEAL, rx=4))
        drawing.add(String(x + WIDTH / 4 - 4, 88, label, textAnchor='middle', fillColor=NAVY, fontName='Helvetica', fontSize=8.2))
    drawing.add(Line(WIDTH / 2 - 8, 92, WIDTH / 2 + 6, 92, strokeColor=GRAY))
    labels = ['Allowlisted egress', 'OpenAI / mock', 'Validate', 'Local patch adapter']
    for index, label in enumerate(labels):
        x = index * WIDTH / 4
        drawing.add(Rect(x + 2, 12, WIDTH / 4 - 8, 35, fillColor=AMBER if index == 1 else PALE, strokeColor=None, rx=4))
        drawing.add(String(x + WIDTH / 8 - 2, 25, label, textAnchor='middle', fillColor=NAVY, fontName='Helvetica', fontSize=8.1))
        if index < 3:drawing.add(Line(x + WIDTH / 4 - 6, 29, x + WIDTH / 4 + 2, 29, strokeColor=GRAY))
    return drawing


def main():
    metrics = read('reports/sanitized/dashboard/index.json')
    pipeline = read('reports/sanitized/pipeline/aggregate.json')
    dast = read('reports/sanitized/day5/dast.json')
    day4 = read('reports/sanitized/day4/gate-summary.json')
    proposals = read('reports/sanitized/day9/proposals.json', {'proposals': []})
    api_error = read('reports/sanitized/day8/triage-live-error.json', {})
    live = read('reports/sanitized/day8/triage-live.json', {})
    reproduction = read('reports/sanitized/reproduction/run.json', {})
    prs = read('reports/sanitized/day9/pr-receipt.json', {'prs': []})
    risks = read('reports/sanitized/deferred-risks.json')
    checks = read('reports/sanitized/day7/redaction-tests.json')
    detection = metrics['detection']

    heading(1, 'PipelineFortress')
    p('Secure CI/CD with GenAI-assisted triage. CAP-DSE-3W individual study implementation and evidence report.')
    table([['Six security stages', 'Application tests', 'Underlying issues'], ['Executed locally', '2,326 passed / 7 skipped', str(metrics['counts']['unique_issues']) + ' open and deferred']], [WIDTH / 3] * 3)
    sub('Outcome and operating decision')
    p('The owned lab now executes SAST, dependency, secret, IaC, image and passive runtime scans. A hardened source-built image is linked through deployment, container inventory and scan evidence. Source-free normalization, mock triage, refusal tests and bounded local patch templates are implemented.')
    p('On 22 October the project owner directed completing the study assignment before later vulnerability remediation. The study profile therefore records security findings and continues. It does not convert findings into fixes or authorize production promotion.')
    sub('Completion boundary')
    p('Local pipeline execution and the three example proposal regressions are verified. Successful live API triage remains unverified: the selected OpenAI credential passed model lookup but three bounded generation attempts returned HTTP429. Genuine human review is recorded only when received. Hosted and fresh-directory status are shown explicitly later in this report.')
    p('This report is an evidence snapshot, not an assertion that every assessment dependency has been fulfilled.', small=True)

    heading(2, 'Architecture and trust boundaries')
    story.append(architecture())
    p('Every scanner retains raw reports in ignored local storage and publishes only execution receipts, aggregate counts, opaque finding fingerprints and checksums. Job receipts bind one run and commit; build, container and DAST receipts must agree on the image configuration ID.')
    p('Normalization creates observation IDs and underlying-issue IDs. Source/container dependency observations share an issue when advisory, component and version agree; detecting stages and every source record remain available. A matching title alone is not a deduplication key.')
    p('The AI boundary constructs a new allowlisted object. It sends synthetic IDs, verified rule/advisory references, severity/category, aliases and verified public versions. Private locations, source, matches, account details and raw scanner messages remain local. The model receives no shell, repository, file or write tools.')
    p('Validated operations map to fixed local templates. A human review step is separate from generation, scanner success and author self-review. No automatic merge is implemented.')

    heading(3, 'Environment and application verification')
    table([['Component', 'Verified configuration'], ['Target', 'OWASP Juice Shop 20.3.0; immutable imported source; original license retained'],
           ['Node / Python', 'Build Node 24.22.0; runtime 24.22.1; isolated Python 3.10'], ['Scanners', 'Semgrep 1.181.0; Trivy 0.76.0; Gitleaks 8.30.1'],
           ['IaC / inventory / runtime', 'Checkov 3.3.30; Syft 1.55.0; ZAP 2.17.0'], ['Kubernetes lab', 'kind 0.33.0; Kubernetes/kubectl 1.37.0'],
           ['Installation boundary', 'Project/user-local tools; scanner distributions and base images pinned']], [130, WIDTH - 130])
    p('The fresh offline application profile passes root/frontend installation, explicit production build, frontend tests, server tests and local API tests. Counts are 1,372 frontend, 417 server and 537 API tests passed, with seven upstream skips and zero selected failures.')
    p('A separate online attempt retained six failures from external-service DNS lookup errors. The offline profile excludes the entire nine-test internet-resource availability suite. It does not suppress a local application test failure. Historical online baseline counts remain separate.')
    p('Application source and both retained dependency locks are preserved. Supported runtimes, lock comparisons and exact image identity are checked rather than inferred from a tag.')

    heading(4, 'Observed runtime baseline')
    table([['Observation', 'Hardened runtime result', 'Interpretation'], ['Home / products / languages', 'HTTP200; data present', 'Application remains usable'],
           ['Coding snippet', 'HTTP200', 'Training source snippets remain available locally'], ['FTP directory', 'HTTP200', 'Intentional directory listing remains'],
           ['Metrics', 'HTTP200', 'Unauthenticated metrics remain observable'], ['Malformed product search', 'HTTP500 with SQL error shape', 'Training error disclosure remains']], [150, 150, WIDTH - 300])
    p('Seven functional/training checks pass in Docker and Kubernetes. The observations are against the owned lab only. No external exploitation, authenticated coverage or customer-data access is claimed.')
    p('Infrastructure hardening preserves the intentionally vulnerable application. Its behavior is part of the study baseline and remains in the deferred register. A passing runtime check establishes the expected behavior, not absence of security weaknesses.')
    p('The active hardened workload is Ready with zero restarts at verification. Earlier readiness issues in other pre-existing system pods are retained as a lab limitation; application readiness is not a complete cluster-health or CIS assessment.')

    heading(5, 'Six stages and the authoritative verdict')
    rows = [['Stage', 'Normalized observations', 'Execution']]
    for stage, counts in metrics['stage_observations'].items():rows.append([stage.upper(), sum(counts.values()), 'Complete; findings deferred'])
    table(rows, [120, 150, WIDTH - 270])
    p('The complete local run is ' + pipeline['run_id'] + '. Its aggregate verdict is ' + pipeline['verdict'] + ', with ' + str(len(pipeline['operational_errors'])) + ' operational errors. The stage receipts retain raw report hashes and exact image linkage.')
    p('That execution took ' + str(pipeline['duration_seconds']) + ' seconds after explicit reuse of a freshly verified build/test. The application check stages took 144.17 seconds separately; these observations do not establish a pipeline percentile or include every bootstrap/download cost.')
    p('The hosted workflow defines six scan jobs, build/test and one final aggregate job. It uses read-only PR permissions, pinned action SHAs, full history for secrets, an integrity-checked image archive between jobs and cleanup of its own staging cluster. Skipped jobs, malformed/missing receipts, scanner errors and mixed identities cannot pass the execution check.')

    heading(6, 'Hardening and software inventory')
    table([['Measure', 'Baseline', 'Hardened'], ['Failed Kubernetes checks', 15, 1], ['Failed Dockerfile checks', 2, 0],
           ['Image vulnerability identities', 101, 100], ['Critical / high / unknown', '11 / 27 / 1', '11 / 27 / 0'],
           ['Image bytes', '351,789,266', '345,391,667'], ['CycloneDX components', 'Not claimed here', day4['sbom']['components']]], [210, (WIDTH - 210) / 2, (WIDTH - 210) / 2])
    p('The runtime uses UID/GID 65532, no effective or bounding capabilities, no-new-privileges, RuntimeDefault seccomp and a read-only root filesystem. Application code and immutable seed reject writes. Explicit bounded writable mounts preserve SQLite, restored training files, translations, customized frontend media, uploads, logs, CSAF metadata and temporary files.')
    p('Both immutable image configuration IDs were scanned under one frozen Trivy database. One unknown CA-certificate advisory was removed; no new identity was introduced in that comparison. The 38 high/critical image identities remain. Syft CycloneDX 1.6 validates against hash-pinned official schemas and representative installed package versions.')
    p('Selected controls are mapped to CIS Kubernetes 2.0.0. NetworkPolicy remains a declared gap and enforcement is unverified. No full benchmark or cluster certification is claimed. A Docker configuration ID, a registry base index digest and a local containerd manifest digest are different identifiers.')

    heading(7, 'Passive DAST and coverage limits')
    table([['Item', 'Observed result'], ['Scanner', 'ZAP ' + str(dast['zap_version']) + '; official image pinned by digest'],
           ['URLs recorded', dast['urls_reached']], ['Alert groups by risk code', json.dumps(dast['alerts_by_risk'])],
           ['Verified seed routes', 'Home, product search, languages, FTP and metrics'], ['Rule policy', 'Selected header rules retain FAIL classification; study verdict defers findings'],
           ['Isolation / cleanup', 'Owned node network namespace; loopback API; scanner container removed']], [170, WIDTH - 170])
    p('The scan uses a traditional unauthenticated crawler and passive checks. It does not establish full single-page-app navigation, login/role coverage, active attack coverage, business-logic correctness or endpoint completeness. Passive alert-instance limits are retained as scanner coverage limits.')
    p('Early scanner-start attempts exposed loopback IPv6 and API Host-header allowlist mismatches. The corrections allow only the local API client and retain diagnostics. Successful scanning is supported by recorded app routes and report hashes, rather than a container exit code alone.')
    p('HTTP findings remain visible in normalization and the deferred register. The security result is not rewritten as clean merely because assignment execution continues.')

    heading(8, 'Detection evaluation and dashboard')
    table([['TP', 'FP', 'FN', 'TN', 'Labeled cases'], [detection['TP'], detection['FP'], detection['FN'], detection['TN'], detection['sample_size']]], [WIDTH / 5] * 5)
    table([['Precision', 'Recall', 'F1', 'Known introduced / caught'], [f"{100*detection['precision']:.1f}%", f"{100*detection['recall']:.1f}%", f"{100*detection['f1']:.1f}%", str(detection['introduced_known_issues']) + ' / ' + str(detection['caught_known_issues'])]], [WIDTH / 4] * 4)
    p('The curated set combines deliberately unsafe and repaired source, advisory, canary, configuration, image and response-header cases. It includes a real scanner miss: the six authored SAST pattern rules do not detect an unprotected synthetic export route. That fixture is never executed against a real service.')
    p('The measured 93.3% fixture recall exceeds the scenario target on this small set. Labels were curated after the broader study work and are not independently human reviewed. The result is not an estimate of all real-world vulnerabilities, a blinded benchmark or evidence that remaining app defects were found.')
    p('The dashboard recomputes from normalized evidence and labels, exports JSON/CSV, separates observations from underlying issues and displays known misses. Empty denominators are N/A. It does not present percentiles from one timing observation. Current global underlying issue count is ' + str(metrics['counts']['unique_issues']) + '.')

    heading(9, 'AI safeguards and honest live status')
    table([['Boundary', 'Implemented evidence'], ['Input construction', 'Exact field allowlist; synthetic IDs and aliases; independent scanner-derived version catalog'],
           ['Refusal behavior', 'Unknown fields, invalid schemas, unverified/encoded metadata and duplicate IDs refuse before transport'],
           ['Actual HTTP body', 'Mock captures final serialized request; private paths/source/canaries excluded'], ['Grounding', 'Unknown IDs, invented CVEs/versions, unsupported operations and omissions rejected'],
           ['Live restrictions', 'OpenAI only; no tools; store=false; bounded tokens, attempts and conservative reservations']], [140, WIDTH - 140])
    p(str(checks.get('tests', 58)) + ' tests cover the relevant normalization, aggregate, boundary, grounding and bounded-patch behavior. A twenty-finding mock batch validates; mock output is deterministic policy behavior and is not reported as a real model evaluation.')
    if live.get('mode') == 'live' and live.get('validation') == 'passed':
        p('Successful live receipt: model ' + live['model'] + ', input tokens ' + str(live['input_tokens']) + ', output tokens ' + str(live['output_tokens']) + ', estimated token-rate cost USD ' + str(live['estimated_usage_usd']) + '. This is an estimate from returned usage, not a billing invoice.')
    else:
        p('The user-selected existing OpenAI key passed read-only model lookup. All three bounded generation attempts returned HTTP429; a specific underlying cause was not established. No successful model output or actual token/invoice cost is fabricated. The request cap is exhausted. No credits were purchased, account topped up or billing settings changed.')
    p('OpenAI documents standard abuse-monitoring retention separately from response storage. store=false does not establish zero retention or an account-specific ZDR setting. Only source-free metadata was submitted, and account-level retention settings were not independently verified.', small=True)

    heading(10, 'Three focused remediation examples')
    rows = [['Proposal', 'Control', 'Measured verification']]
    for item in proposals['proposals']:
        rows.append([item['id'], item['operation'], 'Checkov fails before / passes after; both deployments Ready; home/products pass; namespace cleaned'])
    table(rows, [75, 125, WIDTH - 200])
    p('These examples modify only the legacy baseline deployment manifest through fixed local templates. They disable unnecessary service-account token mounting, explicitly require non-root execution and add a liveness probe. The original baseline image already runs non-root; the second proposal adds an explicit policy guarantee rather than claiming an observed root process was removed.')
    p('Each proposal has a bounded single-file diff, before/after hashes, actual selected-check evidence, functional observations and rollback instructions. Unsupported operations, path traversal, credential access, arbitrary commands and workflow edits are outside the adapter allowlist.')
    p('The Codex coding assistant authored the templates. The unavailable external application API is not credited with generating them. Three examples do not close the larger risk backlog, which remains deferred by the user.')
    p('Draft PR links recorded: ' + str(len(prs.get('prs', []))) + '. Genuine review/first-review correctness is pending unless the review ledger records a real verdict. No author self-approval, fabricated independent review or automatic merge is claimed.')

    heading(11, 'Reproduction and maturity self-assessment')
    p('Reproduction bootstraps project-local Python/pip/Node and verified scanner/tool distributions, runs the selected application suites, rebuilds the image, scans all stages, deploys into a uniquely named temporary kind cluster, runs passive DAST, normalizes, checks mock AI safeguards and regenerates the dashboard. Live API usage is excluded from reproduction by default.')
    p('Fresh-directory result: ' + reproduction.get('verdict', 'not yet recorded') + '. The script deletes only its own temporary cluster and retains sanitized execution evidence. The original study cluster is a separate resource.')
    sub('OWASP SAMM v2 lens')
    table([['Practice', 'Baseline', 'Current lab evidence / limit'], ['Secure Build', 'Manual setup and selected tests', 'Repeatable pinned build, dependency inventory and automation; mature production prevention not claimed'],
           ['Security Testing', 'Runtime observations', 'Six scanner stages and negative controls; known misses and limited DAST coverage retained'], ['Defect Management', 'Findings not consolidated', 'Deduplicated register, labels and focused proposals; real human reviews still required'],
           ['Strategy and Metrics', 'Planning estimates', 'Recomputable counts, fixture precision/recall and execution timings; one lab/run is limited evidence']], [105, 125, WIDTH - 230])
    p('SAMM uses maturity activities across three levels and fifteen practices. Selected level-one and automation activities are evidenced here, but this short project does not complete a formal SAMM assessment or justify an overall organizational score. Deferred production defects and missing independent review prevent a mature-production assurance claim.', small=True)

    heading(12, 'Ethics, residual risks and references')
    p('The target is the owned local training application and ephemeral CI/reproduction labs. The acknowledgement was confirmed before Day 4 implementation resumed. Signed material, API credentials, raw scanner matches, private paths and the complete SBOM remain outside public artifacts.')
    p('The current deferred register contains ' + str(metrics['counts']['unique_issues']) + ' underlying issues, including ' + str(risks['by_severity'].get('CRITICAL', 0)) + ' critical and ' + str(risks['by_severity'].get('HIGH', 0)) + ' high. Deferral is an explicit study decision, not remediation. Later work should prioritize compatible dependency fixes, tested traffic isolation, genuine-secret response if ever confirmed and human-reviewed behavior-preserving changes.')
    p('GenAI disclosure: the Codex coding assistant authored implementation, tests, documentation and bounded proposals. OpenAI GPT-6 Luna is the configured external triage model; unsuccessful live attempts and mock results are separated. Human review and remaining assessment dependencies are not invented.')
    refs = [('Project evidence', 'docs/evidence-index.md and docs/project-completion.md'),
            ('ZAP baseline behavior', 'https://www.zaproxy.org/docs/docker/baseline-scan/'), ('Kubernetes controls', 'https://kubernetes.io/docs/tasks/configure-pod-container/security-context/'),
            ('CIS benchmark scope', 'https://www.cisecurity.org/benchmark/kubernetes'), ('OWASP SAMM v2', 'https://owaspsamm.org/model/'),
            ('OpenAI model / price', 'https://developers.openai.com/api/docs/models/gpt-6-luna'), ('OpenAI data controls', 'https://developers.openai.com/api/docs/guides/your-data')]
    table([['Reference', 'Location'], *refs], [125, WIDTH - 125])
    p('Submission limits: successful external live triage, genuine PR review and any unrecorded hosted/fresh run must remain open requirements. No grade, exhaustive detection, full CIS compliance or production readiness is asserted.', small=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=40, bottomMargin=54,
                                 title='PipelineFortress - study implementation and evidence', author='Project study team')
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    (ROOT / 'docs/final-report.md').write_text(('# PipelineFortress study report\n\nGenerated from the current verified evidence. PDF: `output/pdf/PipelineFortress_Study_Report.pdf`. Remaining dependencies are stated explicitly.\n' + '\n'.join(markdown)).rstrip() + '\n')
    print(str(OUT))


if __name__ == '__main__':
    main()
