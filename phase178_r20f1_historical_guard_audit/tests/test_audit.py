"""Report classifier: only the precise historical failure may remain open."""
import xml.etree.ElementTree as ET

import pytest

from phase178_r20f1_historical_guard_audit.audit import classify_baseline, GUARD, MISSING


def report(tmp_path, *, name=GUARD, message=MISSING, failure=True, skipped=False):
    suite = ET.Element('testsuite')
    for index in range(5):
        ET.SubElement(suite, 'testcase', name='test_'+str(index))
    case = ET.SubElement(suite, 'testcase', name=name)
    if failure:
        ET.SubElement(case, 'failure', message=message)
    if skipped:
        ET.SubElement(case, 'skipped')
    path = tmp_path/'result.xml'
    ET.ElementTree(suite).write(path, encoding='utf-8')
    return path


def test_exact_historical_guard(tmp_path):
    assert classify_baseline(1, report(tmp_path)) == 'KNOWN_GUARD_REPRODUCED_OPEN'


def test_all_pass(tmp_path):
    assert classify_baseline(0, report(tmp_path, failure=False)) == 'PASS_ALL_6'


@pytest.mark.parametrize('kwargs', [{'name':'different'}, {'message':'other failure'}, {'skipped':True}])
def test_other_outcomes_rejected(tmp_path, kwargs):
    with pytest.raises(RuntimeError):
        classify_baseline(1, report(tmp_path, **kwargs))
