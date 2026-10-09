"""Focused R10-R4 tests; no whole-suite execution."""
import re
from dataclasses import replace

from phase162_r10_reference_identity import fixed_citation_identity
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
    extract_toda_group_proof_step_literature_reference,
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
    filter_toda_group_proof_narrative_reference_entries_by_body_usage,
)
from toda_literature_statement_boundary import (
    TodaLiteratureStatementClassification,
    classify_toda_literature_statement_step,
)
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from proof import FoundationalReferenceIdentity, ProofRule


def _presentation():
    return build_toda_group_proof_presentation(build_phase162_pi5_3_web_replay(max_depth=40))


def test_r10_r4_valid_citation_recognized_in_reference_pipeline():
    presentation=_presentation()
    cited=[node.proof_step for node in presentation.nodes if fixed_citation_identity(node.proof_step) is not None]
    assert len(cited)==2
    assert len([step for step in cited if step.rule is ProofRule.GIVEN])==1
    wrapper=next(step for step in cited if step.rule is ProofRule.INFERENCE)
    assert classify_toda_literature_statement_step(wrapper).classification is TodaLiteratureStatementClassification.FIXED_STATEMENT
    assert classify_toda_literature_statement_step(wrapper).component_key=='nu_prime_hopf_relation'
    assert all(extract_toda_group_proof_step_literature_reference(step).locator=='(5.3)' for step in cited)
    fixed=filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
        build_toda_group_proof_narrative_reference_entries(presentation),presentation.root_step)
    assert '(5.3)' in [entry.reference.locator for entry in fixed]


def test_r10_r4_rejects_invalid_citation_identity():
    presentation=_presentation()
    wrapper=next(node.proof_step for node in presentation.nodes if node.proof_step.rule is ProofRule.INFERENCE and fixed_citation_identity(node.proof_step))
    forged=replace(wrapper, foundational_reference=FoundationalReferenceIdentity(
        key='literature:(5.3):unregistered_component',label='(5.3)'))
    assert fixed_citation_identity(forged) is None
    assert classify_toda_literature_statement_step(forged).classification is not TodaLiteratureStatementClassification.FIXED_STATEMENT
    mismatch=replace(wrapper, premises=())
    assert fixed_citation_identity(mismatch) is None


def test_r10_r4_preserves_used_citation_in_body_usage_filter():
    presentation=_presentation()
    fixed=filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
        build_toda_group_proof_narrative_reference_entries(presentation),presentation.root_step)
    filtered,_,_=filter_toda_group_proof_narrative_reference_entries_by_body_usage(
        fixed,{},'[R1]より確認する。')
    assert '(5.3)' in [e.reference.locator for e in filtered]
    assert all(e.reference.locator in [r.reference.locator for r in fixed] for e in filtered)


def test_r10_r4_web_reference_section_includes_cited_fact():
    presentation=_presentation()
    markdown=render_toda_group_proof_narrative_markdown(presentation)
    assert '## 使用する結果' in markdown
    section=markdown.split('## 使用する結果',1)[1].split('## 証明',1)[0]
    assert re.search(r'\[R\d+\] \(5\.3\)',section),section
