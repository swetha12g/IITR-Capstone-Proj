import json
from pathlib import Path

import pytest

from triage.normalize import normalize, adapt


def trivy():
    return {'SchemaVersion': 2, 'Results': [{'Target': 'package-lock.json', 'Type': 'npm',
        'Vulnerabilities': [{'VulnerabilityID': 'CVE-2021-23337', 'Severity': 'HIGH', 'PkgName': 'lodash',
                             'InstalledVersion': '4.17.20', 'FixedVersion': '4.17.21'}]}]}


def test_cross_stage_dedup_retains_all_provenance(tmp_path):
    first = tmp_path / 'sca.json'
    second = tmp_path / 'image.json'
    first.write_text(json.dumps(trivy()))
    second.write_text(json.dumps(trivy()))
    result = normalize([('sca', first, {'run_id': 'source'}), ('container', second, {'run_id': 'image'})])
    assert result['counts'] == {'observations': 2, 'unique_issues': 1, 'by_stage': {'sca': 1, 'container': 1}}
    assert result['issues'][0]['stages'] == ['container', 'sca']
    assert {f['source_records'][0]['run_id'] for f in result['findings']} == {'source', 'image'}


def test_different_component_not_collapsed(tmp_path):
    data = trivy()
    data['Results'][0]['Vulnerabilities'].append({**data['Results'][0]['Vulnerabilities'][0], 'PkgName': 'other-package'})
    path = tmp_path / 'report.json';path.write_text(json.dumps(data))
    assert normalize([('sca', path, {})])['counts']['unique_issues'] == 2


def test_secret_values_and_contacts_discarded(tmp_path):
    path = tmp_path / 'report.json'
    path.write_text(json.dumps([{'RuleID': 'github-pat', 'File': 'app/juice-shop/test.ts', 'StartLine': 2,
                                'Secret': 'PRIVATE_SECRET_CANARY', 'Match': 'PRIVATE_MATCH_CANARY', 'Email': 'PRIVATE_CONTACT_CANARY'}]))
    result = json.dumps(normalize([('secrets-tree', path, {})]))
    assert 'PRIVATE_SECRET_CANARY' not in result and 'PRIVATE_MATCH_CANARY' not in result and 'PRIVATE_CONTACT_CANARY' not in result


@pytest.mark.parametrize('stage,data', [('unsupported', {}), ('sca', {'SchemaVersion': 1}),
                                     ('sast', {'results': [], 'errors': ['error']}), ('secrets-tree', {}),
                                     ('iac', {'summary': {'parsing_errors': 1}}), ('dast', {})])
def test_unknown_or_broken_report_rejected(stage, data):
    with pytest.raises((ValueError, KeyError)):
        list(adapt(stage, data))
