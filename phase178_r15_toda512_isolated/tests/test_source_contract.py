import pytest
from phase178_r15_toda512_isolated.source_contract import (
    LABEL, LEMMA, PROPOSITION, NEXT, verify_clause, verify_positions,
)

FORMULA = r'''\Delta:\ \pi^{2n+1}_{n+7}\ \longrightarrow\ \pi^{n}_{n+5}
\quad\text{は, }n=4,5,6\text{ で単射である. }'''
CHAPTER = '\n'.join((LABEL, '% (5.12).', FORMULA, r'\end{equation}', LEMMA, PROPOSITION, NEXT))
POSITIONS = {'toda:(5.12)': 9700, 'toda:Lemma 5.10': 9800,
             'toda:Proposition 5.11': 9900, 'toda:(5.13)': 10000}


def test_clause():
    assert verify_clause(CHAPTER) == 1


@pytest.mark.parametrize('old,new', [('単射','全射'), ('4,5,6','4,5,7'), ('n+7','n+8'), (LABEL,LABEL+LABEL), (NEXT,''), (LEMMA, NEXT)])
def test_reject_changed_source(old,new):
    with pytest.raises(ValueError):
        verify_clause(CHAPTER.replace(old,new))


def test_positions():
    assert verify_positions(POSITIONS) == 9700
    with pytest.raises(ValueError):
        verify_positions(dict(POSITIONS, **{'toda:(5.12)': 10000}))
