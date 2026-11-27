import pytest
from phase178_r16_toda513_isolated.source_contract import (
    PROP, LABEL, NEXT, END_PROOF, APPLY, FORMULA, verify_clause, verify_positions,
)


def fixture():
    return '\n'.join((PROP, LABEL, '% (5.13).', FORMULA, r'\end{equation}', END_PROOF, APPLY, NEXT))


def positions():
    return {'toda:(5.12)': 9700, 'toda:Lemma 5.10': 9800,
            'toda:Proposition 5.11': 9900, 'toda:(5.13)': 10000, 'toda:Lemma 5.12': 10100}


def test_source_clause_and_order():
    assert verify_clause(fixture()) == 2
    assert verify_positions(positions()) == 10000


@pytest.mark.parametrize('old,new', [(r'\pm', ''), (r'2(\nu_4^{2})', r'4(\nu_4^{2})'),
    (r'\eta^{2}_{11}', r'\eta^{2}_{12}'), (r'\Delta(\eta_{13})=0', r'\Delta(\eta_{13})=1'),
    (END_PROOF, ''), (APPLY, ''), (LABEL, LABEL + LABEL)])
def test_reject_source_drift(old,new):
    with pytest.raises(ValueError):
        verify_clause(fixture().replace(old,new))


def test_reject_source_order_reversal():
    with pytest.raises(ValueError):
        verify_clause(fixture().replace(END_PROOF,'SWAP').replace(APPLY,END_PROOF).replace('SWAP',APPLY))
    bad = positions()
    bad['toda:(5.13)'] = 9899
    with pytest.raises(ValueError):
        verify_positions(bad)
