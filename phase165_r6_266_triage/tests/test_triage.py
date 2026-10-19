import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from triage import make_report


def test_two_error_types():
    log = """_____ ERROR collecting tests/test_phase159_a.py _____
E   ModuleNotFoundError: No module named 'tests.test_phase143_19_method_evidence'
_____ ERROR collecting tests/test_phase80_b.py _____
E   ImportError: cannot import name 'x' from 'toda_rules' (file)
2 errors in 1.00s
"""
    report = make_report(log, 'fixture')
    assert report['error_count'] == 2
    assert report['category_counts']['MISSING_SHARED_TEST_HELPER'] == 1
    assert report['category_counts']['OTHER_MISSING_EXPORT'] == 1


def test_unmatched_count_fails():
    import pytest
    with pytest.raises(ValueError, match='mismatch'):
        make_report('_____ ERROR collecting tests/test_a.py _____\nE   ModuleNotFoundError: No module named \'x\'\n2 errors in 1.00s', 'fixture')


def test_exact_blocker_categories():
    log = """_____ ERROR collecting tests/test_phase80_x.py _____
E   ModuleNotFoundError: No module named 'repository_inference'
_____ ERROR collecting tests/test_phase162_x.py _____
E   ImportError: cannot import name 'toda_pi4_3_delta_image_free_cyclic_inference_rule' from 'toda_rules'
2 errors in 1.00s
"""
    report = make_report(log, 'fixture')
    assert report['category_counts']['RETIRED_REPOSITORY'] == 1
    assert report['category_counts']['RETIRED_PROBE_RULE'] == 1
