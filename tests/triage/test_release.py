"""Release publication must fail before writes when provenance checks fail."""
import json
import os
from pathlib import Path
import subprocess

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts/publish-release.sh'
SHA = 'a' * 40


def run_release(tmp_path, *, tag='v1.0.0', main=SHA, tag_sha=SHA, sha=SHA, run='12345', notes=True,
                api_failure=False, run_failure=False, publish_failure=False, existing=False, mismatch=False,
                list_failure=False):
    directory = tmp_path / 'bin'
    directory.mkdir()
    stub = directory / 'gh'
    stub.write_text('''#!/usr/bin/env python3
import json,os,sys
with open(os.environ['CALL_LOG'],'a') as f:f.write(json.dumps(sys.argv[1:])+'\\n')
if sys.argv[1]=='api':
 if os.environ['API_FAILURE']=='1':sys.exit(1)
 endpoint = next(x for x in sys.argv[2:] if x.startswith('repos/'))
 if '/releases?' in endpoint:
  if os.environ['LIST_FAILURE']=='1':sys.exit(1)
  if os.environ['EXISTING']=='1':print('456')
 elif endpoint.endswith('/releases/456'):
  print(json.dumps({'tag_name':'v1.0.0','name':'PipelineFortress v1.0.0','body':'Changed notes' if os.environ['MISMATCH']=='1' else 'Release notes for the tested project.','draft':False,'prerelease':False}))
 else:print(os.environ['MAIN_SHA'] if endpoint.endswith('/heads/main') else os.environ['TAG_SHA'])
elif sys.argv[1:3]==['run','list']:
 if os.environ['RUN_FAILURE']=='1':sys.exit(1)
 print(os.environ['CI_RUN'])
elif sys.argv[1:3]==['release','create']:
 if os.environ['PUBLISH_FAILURE']=='1':sys.exit(1)
 print('created')
else:sys.exit(2)
''')
    stub.chmod(0o755)
    if notes:
        p = tmp_path / 'docs/releases/v1.0.0.md'
        p.parent.mkdir(parents=True)
        p.write_text('Release notes for the tested project.\n')
    log = tmp_path / 'calls.jsonl'
    env = dict(os.environ, PATH=str(directory) + ':' + os.environ['PATH'], RELEASE_TAG=tag,
               GITHUB_SHA=sha, GITHUB_REPOSITORY='example/project', MAIN_SHA=main, TAG_SHA=tag_sha,
               CI_RUN=run, CALL_LOG=str(log), API_FAILURE=str(int(api_failure)),
               RUN_FAILURE=str(int(run_failure)), PUBLISH_FAILURE=str(int(publish_failure)),
               EXISTING=str(int(existing)), MISMATCH=str(int(mismatch)), LIST_FAILURE=str(int(list_failure)))
    result = subprocess.run(['bash', str(SCRIPT)], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=10)
    calls = [json.loads(x) for x in log.read_text().splitlines()] if log.exists() else []
    return result, calls


@pytest.mark.parametrize('kwargs', [
    {'tag': 'v1.0.0;invalid'}, {'notes': False}, {'main': 'b' * 40},
    {'run': ''}, {'run': 'not-a-run'}, {'api_failure': True},
    {'tag_sha': 'b' * 40}, {'sha': ''}, {'sha': 'not-a-commit'}, {'run_failure': True},
    {'list_failure': True}, {'existing': True, 'mismatch': True},
])
def test_unverified_release_never_publishes(tmp_path, kwargs):
    result, calls = run_release(tmp_path, **kwargs)
    assert result.returncode != 0
    assert not any(c[:2] == ['release', 'create'] for c in calls)


def test_verified_main_publishes_with_reviewed_notes_and_existing_tag(tmp_path):
    result, calls = run_release(tmp_path)
    assert result.returncode == 0, result.stderr
    writes = [c for c in calls if c[:2] == ['release', 'create']]
    assert len(writes) == 1
    assert writes[0][2] == 'v1.0.0'
    assert '--verify-tag' in writes[0]
    assert writes[0][writes[0].index('--target') + 1] == SHA
    assert writes[0][writes[0].index('--notes-file') + 1] == 'docs/releases/v1.0.0.md'
    selection = next(c for c in calls if c[:2] == ['run', 'list'])
    assert selection[selection.index('--branch') + 1] == 'main'
    assert selection[selection.index('--commit') + 1] == SHA
    assert selection[selection.index('--status') + 1] == 'success'
    assert selection[selection.index('--workflow') + 1] == 'study-pipeline.yml'
    assert selection[selection.index('--event') + 1] == 'push'


def test_failed_publication_does_not_claim_success(tmp_path):
    result, calls = run_release(tmp_path, publish_failure=True)
    assert result.returncode != 0
    assert sum(c[:2] == ['release', 'create'] for c in calls) == 1
    assert 'Published ' not in result.stdout


def test_matching_published_release_is_safe_to_retry(tmp_path):
    result, calls = run_release(tmp_path, existing=True)
    assert result.returncode == 0, result.stderr
    assert not any(c[:2] == ['release', 'create'] for c in calls)
    assert 'Verified existing v1.0.0' in result.stdout
