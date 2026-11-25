"""Focused tests for the diagnostic fixture and classification only."""
import pytest
from phase177_r4_general_iterated_suspension_audit import audit


def test_case_types_and_endpoints():
    cases = audit.cases()
    assert set(cases) == {'eta', 'nu_cited', 'sigma_cited', 'epsilon_cited', 'formal_stable', 'formal_unstable'}
    for x, y, z in cases.values():
        a, b = audit.span(x)
        assert audit.span(y) == (a+1, b+1)
        assert audit.span(z) == (a+2, b+2)
        assert len(audit.goals(x,y,z)) == 6


@pytest.mark.parametrize('missing, expected', [
    ((), 'DOUBLE_EQUALITY_REUSABLE'),
    (('double_equality', 'first_image'), 'ONE_STEP_IMAGE_FRONTIER'),
    (('double_equality', 'first_equality'), 'IMAGE_TO_EQUALITY_FRONTIER'),
    (('double_equality', 'nested_to_iterated'), 'ITERATED_NOTATION_FRONTIER'),
    (('double_equality',), 'DOUBLE_EQUALITY_SEARCH_OR_COMPOSITION_FRONTIER'),
])
def test_diagnostic(missing, expected):
    names = ('first_image','second_image','first_equality','second_equality','double_equality','nested_to_iterated')
    assert audit.classify({key: {'proved': key not in missing} for key in names}) == expected


def test_formal_reflexivity_not_evidence_of_transport():
    rows = {'double_equality': {'proved': True, 'reflexive': True},
            'nested_to_iterated': {'proved': False}}
    assert audit.classify(rows) == 'FORMAL_ITERATED_NOTATION_FRONTIER'
    rows['nested_to_iterated']['proved'] = True
    assert audit.classify(rows) == 'FORMAL_ITERATION_REUSABLE'


def test_wrong_dimensions_rejected():
    x, _, z = audit.cases()['eta']
    with pytest.raises(ValueError):
        audit.image(x, z)
