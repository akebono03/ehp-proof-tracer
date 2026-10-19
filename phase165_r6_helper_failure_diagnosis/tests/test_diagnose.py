from diagnose import summarize


def test_classifies_module_failure():
    report = {'status': 'CANDIDATE_FAILED_REVERTED', 'candidates': [{'source': 'git:HEAD'}]}
    result = summarize(report, "ModuleNotFoundError: No module named 'obsolete_module'\n1 error in 0.1s")
    assert result['detected_issues']['missing_module'] == ['obsolete_module']
    assert result['candidate_count'] == 1


def test_classifies_missing_export():
    result = summarize({}, "ImportError: cannot import name 'foo' from 'bar' (bar.py)")
    assert result['detected_issues']['missing_export'] == ['foo|bar']


def test_classifies_test_failure():
    result = summarize({}, 'FAILED tests/test_x.py::test_y - AssertionError\n1 failed, 2 passed in 0.1s')
    assert result['detected_issues']['failed_assertions'] == ['tests/test_x.py::test_y - AssertionError']
    assert result['pytest_summaries']
