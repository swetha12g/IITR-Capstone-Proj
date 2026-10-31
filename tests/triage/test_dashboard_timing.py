import hashlib
import json

from metrics.build_dashboard import timings


def fixture(root):
    private = root / 'reports/private/pipeline/run-fixture'
    private.mkdir(parents=True)
    (private / 'execution.json').write_text(json.dumps({'run_id': 'fixture', 'started_at_utc': '2026-10-22T10:00:00+00:00'}))
    public = root / 'reports/sanitized/pipeline'
    public.mkdir(parents=True)
    path = public / 'sast.json'
    path.write_text(json.dumps({'run_id': 'fixture', 'execution': 'complete', 'observed_at_utc': '2026-10-22T10:00:04+00:00', 'findings_by_severity': {'HIGH': 1}}))
    return {'run_id': 'fixture', 'duration_seconds': 20.0, 'build_test_reused': False,
            'receipts': [{'stage': 'sast', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]}, path


def test_first_feedback_uses_same_run_bound_timestamps(tmp_path):
    pipeline, path = fixture(tmp_path)
    assert timings(tmp_path, pipeline)['first_actionable_seconds'] == 4.0
    assert timings(tmp_path, pipeline)['pipeline_seconds'] == 20.0


def test_changed_or_stale_receipt_cannot_prove_feedback_time(tmp_path):
    pipeline, path = fixture(tmp_path)
    value = json.loads(path.read_text());value['run_id'] = 'other';path.write_text(json.dumps(value))
    assert timings(tmp_path, pipeline)['first_actionable_seconds'] is None
    pipeline['receipts'][0]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    assert timings(tmp_path, pipeline)['first_actionable_seconds'] is None


def test_missing_or_outside_run_timing_is_unavailable(tmp_path):
    pipeline, path = fixture(tmp_path)
    pipeline['duration_seconds'] = 3.0
    assert timings(tmp_path, pipeline)['first_actionable_seconds'] is None
    (tmp_path / 'reports/private/pipeline/run-fixture/execution.json').unlink()
    assert timings(tmp_path, pipeline)['first_actionable_seconds'] is None
