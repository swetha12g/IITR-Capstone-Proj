import hashlib
import json

import pytest

from triage import client


def current_report(tmp_path):
    private = tmp_path / 'reports/private'
    (private / 'pipeline').mkdir(parents=True)
    report = private / 'current.json'
    report.write_text(json.dumps({'SchemaVersion': 2, 'Results': [{'Target': 'package-lock.json', 'Type': 'npm',
        'Vulnerabilities': [{'VulnerabilityID': 'CVE-2021-23337', 'Severity': 'HIGH', 'PkgName': 'lodash',
                            'InstalledVersion': '4.17.20', 'FixedVersion': '4.17.21'}]}]}))
    (private / 'pipeline/latest-index.json').write_text(json.dumps({'reports': [{'stage': 'sca', 'path': str(report),
        'sha256': hashlib.sha256(report.read_bytes()).hexdigest(), 'run_id': 'fixture', 'commit': 'a' * 40,
        'observed_at_utc': '2026-10-22T00:00:00Z'}]}))
    return report


def test_fresh_catalog_uses_current_hash_bound_reports_without_historical_baseline(tmp_path, monkeypatch):
    current_report(tmp_path)
    monkeypatch.setattr(client, 'ROOT', tmp_path)
    assert client.verified_catalog()['CVE-2021-23337'] == {'versions': {'4.17.20'}, 'fixed_versions': {'4.17.21'}}


def test_fresh_catalog_refuses_changed_raw_report(tmp_path, monkeypatch):
    report = current_report(tmp_path)
    report.write_text('{}')
    monkeypatch.setattr(client, 'ROOT', tmp_path)
    with pytest.raises(ValueError):
        client.verified_catalog()
