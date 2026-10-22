#!/usr/bin/env python3
"""Keep all study risks visible without exposing private matches or locations."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RANK = {'CRITICAL': 5, 'HIGH': 4, 'UNKNOWN': 3, 'MEDIUM': 2, 'LOW': 1, 'INFO': 0}


def main():
    normalized = json.loads((ROOT / 'reports/private/normalized.json').read_text())
    observations = {f['finding_id']: f for f in normalized['findings']}
    records = []
    for issue in normalized['issues']:
        rows = [observations[i] for i in issue['finding_ids']]
        severity = max((r['severity'] for r in rows), key=RANK.get)
        records.append({'issue_id': issue['issue_id'], 'severity': severity, 'stages': issue['stages'],
                        'observations': len(rows), 'status': 'deferred-study-lab', 'remediation': 'later, per user direction'})
    records.sort(key=lambda r: (-RANK[r['severity']], r['issue_id']))
    counts = dict(Counter(r['severity'] for r in records))
    summary = {'schema_version': 1, 'decision_date': '2026-10-22', 'scope': 'owned study assignment; no production approval',
               'risk_decision': 'User directed completion of the assignment before later remediation.', 'by_severity': counts, 'issues': records}
    target = ROOT / 'reports/sanitized/deferred-risks.json';target.write_text(json.dumps(summary, indent=2) + '\n')
    lines = ['# Deferred remediation register', '', 'The user directed continuing the complete study assignment on 22 October 2026 and fixing findings later. These are visible open risks, not false positives or completed fixes. Scanner execution errors are handled separately.', '',
             'Current unique underlying issues: **' + str(len(records)) + '**. ' + ', '.join(str(v) + ' ' + k.lower() for k, v in counts.items()) + '.', '',
             'Full safe register: [deferred-risks.json](../reports/sanitized/deferred-risks.json). Private normalized evidence maps aliases back to exact rules, advisories, packages and locations. No secret match or private path is copied here.', '',
             '## Critical and high items', '', '| Issue alias | Severity | Detecting stages | State |', '|---|---|---|---|']
    for record in records:
        if record['severity'] in {'CRITICAL', 'HIGH'}:
            lines.append('| ' + record['issue_id'] + ' | ' + record['severity'] + ' | ' + ', '.join(record['stages']) + ' | Deferred for later remediation |')
    lines += ['', 'Next after assignment implementation: prioritize critical/high items, test compatible dependency/base updates, close the NetworkPolicy gap with enforcement evidence, rotate any genuine secret if one is ever confirmed, and validate before/after scanner and functional results. Keep intentional training weaknesses and their educational purpose explicit. Three focused example proposals do not close this backlog.']
    (ROOT / 'docs/deferred-remediation.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'unique_issues': len(records), 'by_severity': counts}))


if __name__ == '__main__':
    main()
