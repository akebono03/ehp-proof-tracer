import pytest

from phase178_r22_final_verified_proof_audit.audit import ancestry, display_observation


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
