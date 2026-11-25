"""Diagnostic helper tests; no fabricated accepted proof."""
from phase176_r3r60_citation_redundant_premise_audit.audit import (
    juxtaposition, row_for, usage_after,
)


def test_normalization_preserves_noncomposition_math():
    assert juxtaposition(r'$E(a\circ b)=0$.') == '$E(ab)=0$.'
    assert juxtaposition(r'$E(a\circ b)c=0$.') == '$E(ab)c=0$.'


def test_unique_body_anchor():
    row = {'text':'[R2]より, $E(a)=0$.','line':3}
    assert row_for([row],row['text']) is row
    assert row_for([row,row],row['text']) is None
    assert row_for([row],'unknown') is None


def test_unused_reference_diagnostic():
    rows = [{'text':'[R2]より, $a=0$.'}, {'text':'[R2]より, $ab=0$.'},
            {'text':'[R8], [R9], [R10]を用いて, $x=y$.'}, {'text':'[R8]より, $c=d$.'}]
    assert usage_after(rows,[rows[0]['text']],{rows[2]['text']:'[R10]より, $x=y$.'}) == [2,8,10]
