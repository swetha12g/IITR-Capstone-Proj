import importlib.util
import json
from pathlib import Path

import pytest

from triage.evidence import REQUIRED
from triage.test_results import parse_test_totals
from test_aggregate import receipts, mutate

spec = importlib.util.spec_from_file_location('actions_summary', Path(__file__).resolve().parents[2] / 'scripts/build-actions-summary.py')
summary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(summary)


def render(directory):
    return summary.report(directory, run_id='12345', commit='a' * 40, repository='example/study',
                          needs={stage: {'result': 'success'} for stage in REQUIRED})


def current_receipts(directory):
    receipts(directory)
    for stage in REQUIRED:
        mutate(directory, stage, lambda value: value.update(run_id='12345'))


def test_passing_report_retains_high_findings_and_labels_local_snapshot(tmp_path):
    current_receipts(tmp_path)
    text, failed = render(tmp_path)
    assert not failed and 'ZERO CRITICAL · STUDY GATE PASSED' in text
    assert '| Observations | 0 | 7 |' in text
    assert 'pre-commit local snapshot' in text and 'not globally deduplicated' in text
    assert 'unavailable' in text  # no fabricated missing test totals


@pytest.mark.parametrize('case', ['critical', 'missing', 'stale', 'mixed-image'])
def test_summary_cannot_turn_failed_or_stale_evidence_green(tmp_path, case):
    current_receipts(tmp_path)
    if case == 'critical':
        mutate(tmp_path, 'sca', lambda value: value.update(findings_by_severity={'CRITICAL': 1}))
    elif case == 'missing':
        (tmp_path / 'sast.json').unlink()
    elif case == 'stale':
        for stage in REQUIRED:
            mutate(tmp_path, stage, lambda value: value.update(run_id='12222'))
    else:
        mutate(tmp_path, 'container', lambda value: value.update(image_config_id='sha256:' + 'd' * 64))
    text, failed = render(tmp_path)
    assert failed and 'STUDY GATE FAILED / INCOMPLETE' in text
    assert 'ZERO CRITICAL · STUDY GATE PASSED' not in text
    if case != 'critical':
        assert 'UNVERIFIED' in text


def test_summary_omits_arbitrary_scanner_content(tmp_path):
    current_receipts(tmp_path)
    mutate(tmp_path, 'sca', lambda value: value.update(raw_match='<script>sensitive-raw-match</script>'))
    text, failed = render(tmp_path)
    assert not failed and 'sensitive-raw-match' not in text and len(text.encode()) < 1024 * 1024


@pytest.mark.parametrize('prefix', ['ℹ', '#'])
def test_node_summary_parser(prefix):
    text = '\n'.join(f'{prefix} {key} {value}' for key, value in
                     [('tests', 10), ('pass', 8), ('fail', 0), ('cancelled', 0), ('skipped', 2), ('todo', 0)])
    assert parse_test_totals(text, 'node') == {'total': 10, 'passed': 8, 'failed': 0, 'cancelled': 0, 'skipped': 2, 'todo': 0}


def test_vitest_summary_parser():
    assert parse_test_totals('\x1b[32m      Tests  1372 passed (1372)\x1b[0m\n', 'vitest')['passed'] == 1372
    assert parse_test_totals(' Tests  2 failed | 3 passed | 1 skipped (6)\n', 'vitest')['failed'] == 2


@pytest.mark.parametrize('text,runner', [('no summary', 'node'), ('Tests 4 passed (5)', 'vitest'),
                                        ('Tests 4 passed (4)\nTests 4 passed (4)', 'vitest')])
def test_test_counts_do_not_invent_missing_or_inconsistent_totals(text, runner):
    with pytest.raises(ValueError):
        parse_test_totals(text, runner)
