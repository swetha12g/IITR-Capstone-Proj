from pathlib import Path

import pytest

from triage.propose import patch_text, ROOT, TARGET


@pytest.mark.parametrize('operation,required', [('disable-sa-token', 'automountServiceAccountToken: false'),
                                             ('require-nonroot', 'runAsNonRoot: true'), ('add-liveness-probe', 'livenessProbe:')])
def test_bounded_control_patch(operation, required):
    before = (ROOT / 'tests/fixtures/day9/baseline-deployment.yaml').read_text()
    after = patch_text(before, operation)
    assert required in after and after != before
    assert 'image: pipelinefortress:baseline' in after
    with pytest.raises(ValueError):patch_text(after, operation)


@pytest.mark.parametrize('operation', ['../../.env', 'shell:rm', 'workflow-edit', 'credential-read', 'arbitrary-command'])
def test_unknown_operations_refused(operation):
    with pytest.raises(ValueError):patch_text((ROOT / 'tests/fixtures/day9/baseline-deployment.yaml').read_text(), operation)
