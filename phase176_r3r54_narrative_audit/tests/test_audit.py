"""Test textual diagnostics only; fixtures are not accepted proofs."""
import pytest

from phase176_r3r54_narrative_audit.audit import equations, inspect_markdown


def test_body_only_diagnostics_keep_reference_occurrences_separate():
    md = '使用する結果\n**[R1] Source.**\n$a=b$.\n**[R2] Other.**\n証明\n[R1]より, $a=b$.\n$b=a$.\n$a=b$.\n$c=c$.\n□\n'
    original = md
    report = inspect_markdown(md, [{'index': 3, 'latex': 'a=b'}, {'index': 4, 'latex': 'a=b'}])
    assert md == original
    assert report['references'][1]['body'] == ['$a=b$.']
    assert report['empty_reference_bodies'] == [2]
    assert report['references_without_explicit_body_use'] == [2]
    assert report['identities'] == [{'equation': ['c', 'c'], 'lines': [9]}]
    assert report['repeated_equations'] == [{'equation': ['a', 'b'], 'lines': [6, 8]}]
    assert report['reversed_equations'] == [{'equation': ['a', 'b'], 'lines': [6, 8], 'reverse_lines': [7]}]
    assert report['body_rows'][0]['candidate_step_indices'] == [3, 4]


def test_literal_equations_do_not_identify_different_renderings():
    assert equations('$a=a$ $a=b=c$ $a = b$ $a= b$ $x$') == [('a','a'), ('a','b'), ('a','b')]
    assert equations('$E(a)=b$ $Ea=b$') == [('E(a)', 'b'), ('Ea', 'b')]


def test_unknown_citation_and_missing_boundary_fail_closed():
    with pytest.raises(ValueError, match='UNKNOWN_BODY_REFERENCE'):
        inspect_markdown('証明\n[R4] $a=b$.', [])
    with pytest.raises(ValueError, match='EXPECTED_ONE_PROOF_BOUNDARY'):
        inspect_markdown('使用する結果\n$a=b$.', [])
