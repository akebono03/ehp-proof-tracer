"""Pure checks of the adopted equation and its recorded source order."""
import re

REFERENCE_ID = 'toda:(5.13)'
PROP = r'\begin{proposition}\label{prop:5.11}'
LABEL = r'\begin{equation}\label{eq:5.13}'
NEXT = r'\begin{lemma}\label{lemma:5.12}'
END_PROOF = '(5.13) が示された.'
APPLY = '(5.13) を, 上の完全列に適用することにより,'
FORMULA = (r'\Delta(\nu_9)=\pm\,2(\nu_4^{2}),\qquad'
           r'\Delta(\eta^{2}_{11})=0,\qquad\Delta(\eta_{13})=0.')


def verify_clause(chapter):
    anchors = (PROP, LABEL, END_PROOF, APPLY, NEXT)
    if any(chapter.count(a) != 1 for a in anchors):
        raise ValueError('SOURCE_ANCHOR_NOT_UNIQUE')
    positions = tuple(chapter.index(a) for a in anchors)
    if positions != tuple(sorted(positions)):
        raise ValueError('SOURCE_ORDER_CHANGED')
    block = chapter.split(LABEL, 1)[1].split(r'\end{equation}', 1)[0]
    compact = re.sub(r'\s+', '', re.sub(r'%[^\n]*', '', block))
    if compact != FORMULA:
        raise ValueError('SOURCE_FORMULA_CHANGED: ' + compact)
    return chapter[:positions[1]].count('\n') + 1


def verify_positions(positions):
    keys = ('toda:(5.12)', 'toda:Lemma 5.10', 'toda:Proposition 5.11',
            REFERENCE_ID, 'toda:Lemma 5.12')
    actual = tuple(positions.get(k) for k in keys)
    if actual != (9700, 9800, 9900, 10000, 10100):
        raise ValueError('MANIFEST_ORDER_CHANGED: ' + repr(actual))
    return actual[3]
