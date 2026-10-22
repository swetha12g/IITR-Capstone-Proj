import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('source_stage', Path(__file__).resolve().parents[2] / 'scripts/run-source-stage.py')
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)


def setup_locks(root):
    (root / 'locks/juice-shop').mkdir(parents=True)
    (root / 'app/juice-shop/frontend').mkdir(parents=True)
    for name in ['package-lock.json', 'frontend-package-lock.json']:
        (root / 'locks/juice-shop' / name).write_text('{"lockfileVersion":3}\n')


def test_standalone_sca_restores_retained_locks_in_clean_checkout(tmp_path):
    setup_locks(tmp_path)
    stage.prepare_locks(tmp_path)
    assert (tmp_path / 'app/juice-shop/package-lock.json').read_bytes() == (tmp_path / 'locks/juice-shop/package-lock.json').read_bytes()
    assert (tmp_path / 'app/juice-shop/frontend/package-lock.json').read_bytes() == (tmp_path / 'locks/juice-shop/frontend-package-lock.json').read_bytes()


def test_sca_preserves_and_refuses_changed_local_lock(tmp_path):
    setup_locks(tmp_path)
    target = tmp_path / 'app/juice-shop/package-lock.json'
    target.write_text('local change')
    with pytest.raises(ValueError, match='local file preserved'):
        stage.prepare_locks(tmp_path)
    assert target.read_text() == 'local change'
