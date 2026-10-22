import copy
import json

import pytest

from triage.evidence import aggregate, REQUIRED
from metrics.build_dashboard import scores


def receipts(directory):
    for stage in REQUIRED:
        scanners = {'sast': ['sast'], 'sca': ['sca'], 'secrets': ['secrets-history', 'secrets-tree'],
                    'iac': ['iac', 'iac'], 'container': ['container'], 'dast': ['dast'], 'build-test': []}[stage]
        record = {'schema_version': 1, 'stage': stage, 'execution': 'complete', 'profile': 'study-lab',
                  'run_id': 'fixture-run', 'commit': 'a' * 40, 'findings_by_severity': {'HIGH': 1},
                  'reports': [{'scanner_stage': s, 'exit_code': 0, 'sha256': 'b' * 64} for s in scanners],
                  'image_config_id': 'sha256:' + 'c' * 64, 'routes_verified': True, 'cleanup_verified': True}
        (directory / (stage + '.json')).write_text(json.dumps(record))


def mutate(directory, stage, operation):
    path = directory / (stage + '.json');data = json.loads(path.read_text());operation(data);path.write_text(json.dumps(data))


def test_study_findings_do_not_block(tmp_path):
    receipts(tmp_path)
    verdict = aggregate(tmp_path)
    assert verdict['verdict'] == 'PASS_WITH_DEFERRED_RISKS' and not verdict['operational_errors']
    assert verdict['security_scan_stages'] == 6


def test_critical_findings_block_without_hiding_counts(tmp_path):
    receipts(tmp_path)
    mutate(tmp_path, 'sca', lambda d: d.update(findings_by_severity={'HIGH': 1, 'CRITICAL': 1}))
    verdict = aggregate(tmp_path)
    assert verdict['verdict'] == 'FAIL_CRITICAL'
    assert verdict['security_blockers'] == ['critical-vulnerabilities-remain']
    assert verdict['critical_observations'] == 1
    assert verdict['findings_by_severity']['HIGH'] == 7
    assert not verdict['operational_errors']


def test_mixed_project_tree_cannot_pass(tmp_path):
    receipts(tmp_path)
    for stage in REQUIRED:
        mutate(tmp_path, stage, lambda d: d.update(project_tree_sha256='e' * 64))
    assert aggregate(tmp_path)['verdict'] == 'PASS_WITH_DEFERRED_RISKS'
    mutate(tmp_path, 'sca', lambda d: d.update(project_tree_sha256='f' * 64))
    assert 'mixed-or-invalid-project-tree' in aggregate(tmp_path)['operational_errors']


@pytest.mark.parametrize('case', ['missing', 'skipped', 'mixed-commit', 'mixed-run', 'mixed-image',
                                  'malformed-count', 'missing-report', 'bad-hash', 'error-exit', 'missing-coverage', 'missing-cleanup'])
def test_incomplete_execution_never_passes(tmp_path, case):
    receipts(tmp_path)
    if case == 'missing':(tmp_path / 'sast.json').unlink()
    elif case == 'skipped':mutate(tmp_path, 'sast', lambda d: d.update(execution='skipped'))
    elif case == 'mixed-commit':mutate(tmp_path, 'sast', lambda d: d.update(commit='d' * 40))
    elif case == 'mixed-run':mutate(tmp_path, 'sast', lambda d: d.update(run_id='other'))
    elif case == 'mixed-image':mutate(tmp_path, 'dast', lambda d: d.update(image_config_id='sha256:' + 'd' * 64))
    elif case == 'malformed-count':mutate(tmp_path, 'sast', lambda d: d.update(findings_by_severity={'HIGH': 'zero'}))
    elif case == 'missing-report':mutate(tmp_path, 'secrets', lambda d: d['reports'].pop())
    elif case == 'bad-hash':mutate(tmp_path, 'sca', lambda d: d['reports'][0].update(sha256='bad'))
    elif case == 'error-exit':mutate(tmp_path, 'sca', lambda d: d['reports'][0].update(exit_code=124))
    elif case == 'missing-coverage':mutate(tmp_path, 'dast', lambda d: d.update(routes_verified=False))
    elif case == 'missing-cleanup':mutate(tmp_path, 'dast', lambda d: d.update(cleanup_verified=False))
    result = aggregate(tmp_path)
    assert result['verdict'] == 'ERROR' and result['operational_errors']


def test_github_skipped_job_does_not_pass(tmp_path):
    receipts(tmp_path)
    needs = {stage: {'result': 'success'} for stage in REQUIRED};needs['dast']['result'] = 'skipped'
    assert aggregate(tmp_path, needs)['verdict'] == 'ERROR'


def test_metrics_count_known_miss_and_zero_denominators():
    labels = [{'ground_truth_positive': True, 'detected': True}, {'ground_truth_positive': True, 'detected': False},
              {'ground_truth_positive': False, 'detected': True}, {'ground_truth_positive': False, 'detected': False}]
    result = scores(labels)
    assert [result[k] for k in ['TP', 'FP', 'FN', 'TN']] == [1, 1, 1, 1]
    assert result['precision'] == result['recall'] == result['f1'] == 0.5
    assert scores([])['precision'] is None and scores([])['recall'] is None
