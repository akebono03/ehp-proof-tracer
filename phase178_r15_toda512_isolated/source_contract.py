"""Pure checks for the adopted source clause and its manifest order."""
import re

LABEL = r'\begin{equation}\label{eq:5.12}'
LEMMA = r'\begin{lemma}\label{lemma:5.10}'
PROPOSITION = r'\begin{proposition}\label{prop:5.11}'
NEXT = r'\begin{equation}\label{eq:5.13}'
REFERENCE_ID = 'toda:(5.12)'


def verify_clause(chapter):
    anchors = (LABEL, LEMMA, PROPOSITION, NEXT)
    if any(chapter.count(a) != 1 for a in anchors):
        raise ValueError('SOURCE_ANCHOR_NOT_UNIQUE')
    indices = tuple(chapter.index(a) for a in anchors)
    if indices != tuple(sorted(indices)):
        raise ValueError('SOURCE_ORDER_CHANGED')
    block = chapter.split(LABEL, 1)[1].split(r'\end{equation}', 1)[0]
    compact = re.sub(r'\s+', '', re.sub(r'%[^\n]*', '', block))
    expected = (r'\Delta:\\pi^{2n+1}_{n+7}\\longrightarrow\\pi^{n}_{n+5}'
                r'\quad\text{は,}n=4,5,6\text{で単射である.}')
    if compact != expected:
        raise ValueError('SOURCE_FORMULA_CHANGED: ' + compact)
    return chapter[:indices[0]].count('\n') + 1


def verify_positions(positions):
    keys = (REFERENCE_ID, 'toda:Lemma 5.10', 'toda:Proposition 5.11', 'toda:(5.13)')
    actual = tuple(positions.get(k) for k in keys)
    if actual != (9700, 9800, 9900, 10000):
        raise ValueError('MANIFEST_ORDER_CHANGED: ' + repr(actual))
    return actual[0]
