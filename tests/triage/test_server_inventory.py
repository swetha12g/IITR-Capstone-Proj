import hashlib
import json
import xml.etree.ElementTree as ET

import pytest

from triage.server_tests import verify_inventory


def fixture(tmp_path):
    app = tmp_path / 'app'
    app.mkdir()
    relative = 'test/server/fixture.unit.test.ts'
    root = ET.Element('testsuites')
    suite = ET.SubElement(root, 'testsuite', name='parameterized')
    fingerprints = []
    for index in range(3):
        name = 'case-' + str(index)
        ET.SubElement(suite, 'testcase', name=name, classname='parameterized', file=str(app / relative))
        fingerprints.append(hashlib.sha256(json.dumps([relative, 'parameterized', name, 'passed'], separators=(',', ':')).encode()).hexdigest())
    path = tmp_path / 'server.xml';ET.ElementTree(root).write(path)
    return app, path, {'files': [{'file': relative, 'case_fingerprints': fingerprints}]}


def test_all_parameterized_cases_must_be_present(tmp_path):
    app, path, baseline = fixture(tmp_path)
    checked = verify_inventory(path, app, baseline)
    assert checked['matched'] and checked['executed_cases'] == 3 and checked['missing_cases'] == 0


@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'new-skip'])
def test_missing_duplicate_or_newly_skipped_cases_cannot_pass(tmp_path, mutation):
    app, path, baseline = fixture(tmp_path)
    tree = ET.parse(path);suite = tree.getroot()[0]
    if mutation == 'missing':suite.remove(suite[-1])
    elif mutation == 'duplicate':suite[-1].set('name', suite[0].get('name'))
    else:ET.SubElement(suite[-1], 'skipped')
    tree.write(path)
    assert not verify_inventory(path, app, baseline)['matched']


def test_runner_paths_outside_the_application_are_refused(tmp_path):
    app, path, baseline = fixture(tmp_path)
    tree = ET.parse(path);tree.getroot()[0][0].set('file', str(tmp_path / 'private.unit.test.ts'));tree.write(path)
    with pytest.raises(ValueError):verify_inventory(path, app, baseline)


def test_empty_reports_are_not_successful_coverage(tmp_path):
    app, path, baseline = fixture(tmp_path)
    path.write_text('<testsuites/>')
    with pytest.raises(ValueError):verify_inventory(path, app, baseline)
