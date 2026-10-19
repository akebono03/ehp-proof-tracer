import pytest
from apply import failing_nodes, plan, PROTECTED


def test_failing_nodes_group_parameterized():
    nodes, grouped = failing_nodes('FAILED tests/test_a.py::test_a[0]\nFAILED tests/test_a.py::test_a[1]\n')
    assert len(nodes) == 2
    assert grouped['tests/test_a.py'] == {'test_a'}


def test_protected_files_count():
    assert len(PROTECTED) == 6
    assert 'tests/test_phase164_r5_r1_common_renderer.py' in PROTECTED


def test_expected_count_fail_closed(tmp_path):
    with pytest.raises(RuntimeError, match='Expected 113'):
        plan(tmp_path, 'FAILED tests/test_a.py::test_a')
