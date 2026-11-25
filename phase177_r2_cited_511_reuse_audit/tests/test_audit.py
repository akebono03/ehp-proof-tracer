"""Pure diagnostic tests; repository-dependent observations are in audit.main."""
from types import SimpleNamespace

import pytest

from phase177_r2_cited_511_reuse_audit import audit


def test_blob_accepts_windows_line_endings():
    raw = b'a\nb\n'
    assert audit.matches_blob(raw.replace(b'\n', b'\r\n'), audit.blob(raw))
    assert not audit.matches_blob(b'changed', audit.blob(raw))


@pytest.mark.parametrize('m,i,j,expected', [(4,9,10,True),(4,9,11,False),(3,6,10,True),(4,9,8,False),(True,9,10,False)])
def test_arithmetic(m,i,j,expected):
    assert audit.arithmetic(m,i,j) is expected


def test_candidate_records_preserve_order():
    a = SimpleNamespace(rule=SimpleNamespace(name='a'), subgoals=('x',))
    b = SimpleNamespace(rule=SimpleNamespace(name='b'), subgoals=('y',))
    rows = audit.matching_calls('goal', [('other',(b,)), ('goal',(a,b)), ('goal',())])
    assert rows == [[{'rule':'a','subgoals':[repr('x')]},{'rule':'b','subgoals':[repr('y')]}], []]
    assert audit.classify_calls(rows) == 'CANDIDATES_PRESENT'


def test_frontier_classification():
    assert audit.classify_calls([]) == 'NOT_REACHED'
    assert audit.classify_calls([[],[]]) == 'NO_CANDIDATES'


def test_head_and_sources_are_pinned():
    assert audit.HEAD == '45d648fab515d1a7d2f48c4a411933926d9d57e9'
    assert 'sources/toda/Toda_02_2.tex' in audit.PINS
    assert 'sources/toda/Toda_05_2.tex' in audit.PINS
    assert all(len(pin) == 40 for pin in audit.PINS.values())


@pytest.mark.parametrize('local_ok,remote_ok', [(False, True), (True, False), (False, False)])
def test_preflight_reports_both_heads_and_rejects_mismatch(monkeypatch, local_ok, remote_ok):
    local = audit.HEAD if local_ok else '1' * 40
    remote = audit.HEAD if remote_ok else '2' * 40
    values = {
        ('rev-parse', '--show-toplevel'): str(audit.ROOT),
        ('branch', '--show-current'): 'develop',
        ('rev-parse', 'HEAD'): local,
        ('rev-parse', 'origin/develop'): remote,
    }
    monkeypatch.setattr(audit, 'git', lambda *args: values[args])
    with pytest.raises(RuntimeError) as error:
        audit.preflight()
    assert str(error.value) == (
        f'REVIEWED_HEAD_REQUIRED:expected={audit.HEAD};local={local};origin/develop={remote}'
    )
