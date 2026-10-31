#!/usr/bin/env python3
"""Build a bounded, honest fixture evaluation with a verified scanner miss."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = json.loads((ROOT / 'reports/sanitized/day3/fixture-evidence.json').read_text())
    policy = json.loads((ROOT / 'reports/sanitized/day4/policy-fixtures.json').read_text())
    miss = json.loads((ROOT / 'reports/sanitized/day6/known-miss.json').read_text())
    image = json.loads((ROOT / 'reports/sanitized/day4/gate-summary.json').read_text())
    path = Path((ROOT / 'reports/private/day5/latest-dast-manifest.txt').read_text().strip())
    zap = json.loads((path.parent / 'zap.json').read_text())
    zap_ids = {str(a['pluginid']) for site in zap['site'] for a in site['alerts']}
    cases = {c['case']: c for c in policy['cases']}
    labels = []
    def add(stage, issue, positive, detected, rationale, reference):
        labels.append({'stage': stage, 'issue_id': issue, 'ground_truth_positive': positive, 'detected': detected,
                       'rationale': rationale, 'evidence': reference, 'label_author_role': 'coding-agent fixture curator'})
    for name in ['sql-template', 'eval', 'shell-command', 'weak-hash', 'tls-validation', 'jwt-decode']:
        add('sast', 'fixture-sast-' + name, True, source['bad']['all_six_source_rules_detected'],
            'Unsafe pattern introduced in the non-executed fixture before the recorded scanner run.', 'day3/fixture-evidence.json')
    add('sast', 'fixture-sast-authorization', True, miss['detected'], 'An unprotected export route is a known authorization defect outside the six pattern checks.', 'day6/known-miss.json')
    add('sast', 'fixture-sast-safe', False, not source['fixed']['gate_passed'], 'Repaired fixture has no authored-rule findings.', 'day3/fixture-evidence.json')
    for stage, name, detected in [('sca', 'reviewed-advisory', source['bad']['advisory_detected'] == 'CVE-2021-23337'),
                                   ('secrets', 'synthetic-canary', source['bad']['secret_rule_detected'] == 'github-pat')]:
        add(stage, 'fixture-' + stage + '-' + name, True, detected, 'Deliberate nonfunctional/isolated positive fixture.', 'day3/fixture-evidence.json')
        add(stage, 'fixture-' + stage + '-safe', False, not source['fixed']['gate_passed'], 'Clean isolated fixed fixture, not the history-retention probe.', 'day3/fixture-evidence.json')
    add('iac', 'fixture-iac-mutable-image', True, 'CKV_PF_K8S_1' in cases['latest']['failed_ids'], 'Mutable reference is deliberately introduced.', 'day4/policy-fixtures.json')
    add('iac', 'fixture-iac-escalation', True, 'CKV_K8S_20' in cases['privilege-escalation']['failed_ids'], 'Privilege escalation deliberately enabled.', 'day4/policy-fixtures.json')
    add('iac', 'fixture-iac-restricted', False, bool(cases['digest']['failed_ids']), 'Restricted digest-pinned fixture passes both selected checks.', 'day4/policy-fixtures.json')
    baseline = set(image['container']['baseline']['fingerprints']);hardened = set(image['container']['hardened']['fingerprints'])
    add('container', 'baseline-ca-advisory', True, bool(baseline - hardened), 'Known CA advisory present in the baseline image.', 'day4/gate-summary.json')
    add('container', 'baseline-retained-critical', True, image['container']['baseline']['by_severity'].get('CRITICAL', 0) > 0, 'Pinned training dependencies retain confirmed critical advisories.', 'day4/gate-summary.json')
    add('container', 'hardened-ca-advisory', False, bool(hardened - baseline), 'The removed baseline CA identity is absent after the supported base update.', 'day4/gate-summary.json')
    for rule, name in [('10038', 'csp-header'), ('10021', 'content-type-options')]:
        add('dast', 'lab-dast-' + name, True, rule in zap_ids, 'Directly observed training response-header gap; passive scanner evidence retained.', 'day5/dast.json')
    add('dast', 'lab-dast-frame-header', False, '10020' in zap_ids, 'The app provides a frame-protection header; no alert for the selected rule.', 'day5/dast.json')
    result = {'schema_version': 1, 'scope': 'post-hoc curated fixture/control set; not independent real-world coverage or an exhaustive benchmark',
              'human_review': 'not independently reviewed', 'labels': labels}
    target = ROOT / 'metrics/labels.json';target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'labeled_cases': len(labels), 'known_misses': sum(x['ground_truth_positive'] and not x['detected'] for x in labels)}))


if __name__ == '__main__':
    main()
