"""Focused Renderer-only tests for cited incomplete ProofSteps."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def test_incomplete_registered_and_rule_citations_remain_attached_to_their_step():
    """Different registered/rule sources on a single GIVEN stay in model order."""
    ref = LiteratureReference(label="Rule Source", locator="Rule Source")
    step = ProofStep(conclusion="observed", premises=(), rule=ProofRule.GIVEN,
                     inference_rule=InferenceRule(name="test", literature_reference=ref))
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(step,), open_goals=("pending",),
        references=("UNVERIFIED REFERENCE",),
    )
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="example-1", kind=ReferenceKind.PROPOSITION,
        locator="Registered Source",
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="example-assertion", reference_id="example-1",
        kind=AssertionKind.STATEMENT, content="observed",
    ))
    model = build_proof_narrative_model(
        result, registry=registry,
        proof_links=(ProofStepLink(assertion_id="example-assertion", step=step),),
    )
    assert model.step_citation_numbers == ((1, 2),)
    text = render_model_backed_narrative_markdown(result, model)
    assert "- 与件: [R1], [R2]より, observed" in text
    assert "**[R1] Registered Source.**" in text
    assert "**[R2] Rule Source.**" in text
    assert "UNVERIFIED REFERENCE" not in text
    assert "未解決 Goal" in text and "pending" in text
    assert "□" not in text


def test_incomplete_inference_rule_citation_and_uncited_given_are_distinguished():
    """An inference cite is not copied to an unrelated unreferenced given."""
    given = ProofStep("observed", (), ProofRule.GIVEN)
    rule = InferenceRule(name="test inference", literature_reference=LiteratureReference(
        label="Inference Source", locator="Inference Source"))
    inference = ProofStep("inferred", (given,), ProofRule.INFERENCE,
                          inference_rule=rule)
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(given, inference), open_goals=("pending",),
    )
    model = build_proof_narrative_model(result)
    assert model.step_citation_numbers == ((), (1,))
    text = render_model_backed_narrative_markdown(result, model)
    assert "- 与件: observed" in text
    assert "- 与件: [R1]" not in text
    assert "- 推論: [R1]を用いて, inferred" in text
    assert "未解決 Goal" in text
    assert "□" not in text


def test_not_searched_and_search_failed_have_no_invented_reference():
    """Do not add tags or a QED for results with zero observed ProofSteps."""
    for status in (ProofSearchStatus.NOT_SEARCHED, ProofSearchStatus.SEARCH_FAILED):
        result = make_partial_proof_result(
            n=17, k=4, status=status,
            open_goals=("pending",),
            diagnostics=("unresolved",), references=("UNVERIFIED SOURCE",),
        )
        model = build_proof_narrative_model(result)
        output = render_model_backed_narrative_markdown(result, model)
        assert "## 未解決 Goal" in output
        assert "## 探索診断" in output
        assert "UNVERIFIED SOURCE" not in output
        assert "[R1]" not in output
        assert "□" not in output


def test_malformed_step_citation_mapping_remains_rejected():
    step = ProofStep("observed", (), ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(step,), open_goals=("pending",),
    )
    model = build_proof_narrative_model(result)
    wrong = replace(model, step_citation_numbers=((9,),))
    with pytest.raises(ValueError, match="missing or unrelated"):
        render_model_backed_narrative_markdown(result, wrong)


def test_real_certified_prefix_preserves_registered_bodies_and_links():
    """Reconstructed audited prefix, never represented as a natural PARTIAL search."""
    from phase168_r3_41e_certified_prefix_reference_audit.audit import run_certified_prefix_case

    report, markdown, view = run_certified_prefix_case()
    assert report["not_a_genuine_partial_search"]
    audit = report["step_inline_citation_audit"]
    assert audit["cited_steps"] >= 1
    assert audit["issues"] == []
    assert audit["missing_inline_citation_steps"] == []
    assert report["citation_body_count"] >= 1
    assert report["reference_projection"]["issues"] == []
    assert all(body["raw_reference_present"] and body["web_reference_present"]
               for citation in report["reference_projection"]["citations"]
               for body in citation["bodies"])
    assert report["unresolved_goal_kept"]
    assert report["diagnostics_kept"]
    assert view.partial_result
    assert "□" not in markdown
