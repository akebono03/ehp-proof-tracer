"""Presentation helper guards; the public proof is checked by audit.py."""
from types import SimpleNamespace

from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase176_r3r56_cited_source_display_isolated.projection import (
    insert_reference_clause, matches_registered_id, project_cited_sources,
    tag_exact_sentence,
)


def test_exact_and_shared_ids_only():
    assert matches_registered_id('toda:example', 'toda:example')
    assert matches_registered_id('shared:21:toda:example', 'toda:example')
    assert not matches_registered_id('other:21:toda:example', 'toda:example')
    assert not matches_registered_id('shared:x:toda:example', 'toda:example')
    assert not matches_registered_id('shared:21:toda:example:other', 'toda:example')


def test_reference_insert_preserves_other_clause_and_is_idempotent():
    cite = SimpleNamespace(number=2, reference=SimpleNamespace(locator='Lemma 5.7'))
    lines = ['使用する結果', '', '**[R2] Lemma 5.7.**', '', '$b=c$.', '',
             '**[R3] Other.**', '', '証明', '', '$b=c$.', '□']
    insert_reference_clause(lines, cite, '$a=0$.')
    assert lines == ['使用する結果', '', '**[R2] Lemma 5.7.**', '', '$b=c$.', '',
                     '$a=0$.', '', '**[R3] Other.**', '', '証明', '', '$b=c$.', '□']
    before = list(lines)
    insert_reference_clause(lines, cite, '$a=0$.')
    assert lines == before


def test_reference_missing_or_ambiguous_header_is_unchanged():
    cite = SimpleNamespace(number=2, reference=SimpleNamespace(locator='Lemma 5.7'))
    for lines in (['証明', '□'], ['**[R2] Lemma 5.7.**', '**[R2] Lemma 5.7.**', '証明']):
        before = list(lines)
        insert_reference_clause(lines, cite, '$a=0$.')
        assert lines == before


def test_body_tag_does_not_change_reference_or_ambiguous_body():
    lines = ['$a=b$.', '証明', '$a=b$.', '□']
    tag_exact_sentence(lines, '$a=b$.', '[R2]より, $a=b$.')
    assert lines == ['$a=b$.', '証明', '[R2]より, $a=b$.', '□']
    lines = ['証明', '$a=b$.', '$a=b$.']
    before = list(lines)
    tag_exact_sentence(lines, '$a=b$.', '[R2]より, $a=b$.')
    assert lines == before


def test_partial_and_unrooted_model_remain_unchanged():
    markdown = '使用する結果\n\n証明\n\n$a=b$.\n'
    for status in (ProofSearchStatus.COMPLETE, ProofSearchStatus.PARTIAL):
        model = ProofNarrativeModel((), (), (), None, status=status)
        assert project_cited_sources(markdown, model) == markdown
