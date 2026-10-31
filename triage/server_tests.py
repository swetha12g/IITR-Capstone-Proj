"""Verify every server test case without publishing test names or runner paths."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def inventory(xml_path, app):
    root = ET.parse(xml_path).getroot()
    if root.tag != 'testsuites':
        raise ValueError('invalid-server-junit')
    cases = []
    failed = skipped = critical_passed = 0
    for case in root.iter('testcase'):
        path = Path(case.attrib['file'])
        relative = (path if path.is_absolute() else app / path).resolve().relative_to(app.resolve()).as_posix()
        if not relative.startswith('test/server/') or not relative.endswith('.unit.test.ts'):
            raise ValueError('invalid-server-case-location')
        is_failed = case.find('failure') is not None or case.find('error') is not None
        is_skipped = case.find('skipped') is not None
        if is_failed and is_skipped:
            raise ValueError('invalid-server-case-status')
        status = 'failed' if is_failed else 'skipped' if is_skipped else 'passed'
        identity = json.dumps([relative, case.get('classname', ''), case.attrib['name'], status], separators=(',', ':'))
        cases.append((relative, hashlib.sha256(identity.encode()).hexdigest()))
        failed += is_failed
        skipped += is_skipped
        critical_passed += relative == 'test/server/criticalRemediation.unit.test.ts' and status == 'passed'
    if not cases:
        raise ValueError('empty-server-junit')
    return sorted(cases), {'total': len(cases), 'passed': len(cases) - failed - skipped, 'failed': failed, 'skipped': skipped}, critical_passed


def verify_inventory(xml_path, app, baseline):
    cases, totals, critical_passed = inventory(xml_path, app)
    expected = [(row['file'], fingerprint) for row in baseline['files'] for fingerprint in row['case_fingerprints']]
    missing = Counter(expected) - Counter(cases)
    unexpected = Counter(cases) - Counter(expected)
    return {'matched': not missing and not unexpected, 'expected_cases': len(expected), 'executed_cases': len(cases),
            'missing_cases': sum(missing.values()), 'unexpected_cases': sum(unexpected.values()),
            'expected_files': len(baseline['files']), 'executed_files': len({name for name, _ in cases}),
            'file_counts': dict(sorted(Counter(name for name, _ in cases).items())),
            'critical_regressions': critical_passed,
            'case_inventory_sha256': hashlib.sha256(json.dumps(cases).encode()).hexdigest(), 'junit_totals': totals}
