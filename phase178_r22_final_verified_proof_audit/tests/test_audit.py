import pytest

from phase178_r22_final_verified_proof_audit.audit import (
    OLD_TEST, PACKAGE_PINS, R22_COMMITTED_PATHS, R22_FIX_PATHS, TARGET,
    ancestry, display_observation, validate_change_scope,
)


def test_ancestry_is_root_scoped_and_shared_nodes_are_counted_once():
    nodes = {0: {'premises': [1, 2]}, 1: {'premises': [3]},
             2: {'premises': [3]}, 3: {'premises': []}, 4: {'premises': []}}
    assert ancestry(nodes, 0) == {0, 1, 2, 3}
    assert ancestry(nodes, 2) == {2, 3}


@pytest.mark.parametrize('nodes', [{0: {'premises': [1]}}, {0: {'premises': [0]}},
                                  {0: {'premises': [1]}, 1: {'premises': [0]}}])
def test_ancestry_rejects_missing_nodes_and_cycles(nodes):
    with pytest.raises(RuntimeError, match='INVALID_PROOF_GRAPH'):
        ancestry(nodes, 0)


def test_display_observation_distinguishes_actual_fields_and_duplicate_isomorphism():
    factors = (r'E(\nu_{5})=\nu_{6}', r'E(\nu_{8})=\nu_{9}')
    composite = r'E(\nu_{5}^{2})=\nu_{6}^{2}'
    iso = r'E: \pi_{11}^{5}\to \pi_{12}^{6}'
    lines = [f'WebGroupProofRenderedLineView(statement_latex={tex!r}, suffix={suffix!r})'
             for tex,suffix in [(factors[0],'.'),(factors[1],'.'),(composite,'.'),
                                (iso,' は同型.'),(iso,' は同型.'),(iso,' は単射.')]]
    assert display_observation(lines, factors, composite, iso) == {
        'factor_line_counts': [1,1], 'composite_line_count': 1, 'isomorphism_line_count': 2}
    assert display_observation(lines[2:], factors, composite, iso)['factor_line_counts'] == [0,0]


def test_preflight_accepts_reviewed_r22_commit_and_audit_only_fix():
    committed = {TARGET, OLD_TEST} | set(PACKAGE_PINS) | R22_COMMITTED_PATHS
    validate_change_scope(committed, set(), R22_FIX_PATHS)
    validate_change_scope(committed, R22_FIX_PATHS, set())
    validate_change_scope(committed, set(), set())


@pytest.mark.parametrize('kind', ['extra_committed', 'missing_committed', 'later_math',
                                  'dirty_math', 'dirty_run_script'])
def test_preflight_rejects_unrelated_changes(kind):
    committed = {TARGET, OLD_TEST} | set(PACKAGE_PINS) | R22_COMMITTED_PATHS
    later, dirty = set(), set()
    if kind == 'extra_committed':
        committed.add('proof.py')
    elif kind == 'missing_committed':
        committed.remove(TARGET)
    elif kind == 'later_math':
        later.add(TARGET)
    elif kind == 'dirty_math':
        dirty.add(TARGET)
    else:
        dirty.update(R22_COMMITTED_PATHS - R22_FIX_PATHS)
    with pytest.raises(RuntimeError, match='UNRELATED_'):
        validate_change_scope(committed, later, dirty)
