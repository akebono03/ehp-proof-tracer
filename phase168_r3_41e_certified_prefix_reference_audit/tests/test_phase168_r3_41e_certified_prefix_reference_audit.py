"""Read-only audit tests; no implementation patch or new proof assertion."""
from dataclasses import dataclass

import pytest

from phase168_r3_41e_certified_prefix_reference_audit.audit import (
    audit_inline_step_sources, select_closed_proof_prefix,
)


@dataclass(frozen=True)
class FakeStep:
    conclusion: str
    premises: tuple = ()


@dataclass(frozen=True)
class FakeResult:
    proven_steps: tuple
    conclusion: str


def test_proof_prefix_preserves_actual_step_instances_and_prerequisites():
    given = FakeStep("given")
    inference = FakeStep("inferred", (given,))
    forward = FakeStep("skip", (FakeStep("unknown"),))
    root = FakeStep("root", (inference,))
    result = FakeResult((given, inference, forward, root), "root")
    selected = select_closed_proof_prefix(result, limit=3)
    assert selected == (given, inference)
    assert selected[0] is given and selected[1] is inference
    assert root not in selected


def test_select_prefix_validates_limits():
    result = FakeResult((FakeStep("a"), FakeStep("root")), "root")
    with pytest.raises(ValueError, match="positive int"):
        select_closed_proof_prefix(result, limit=0)
    with pytest.raises(ValueError, match="positive int"):
        select_closed_proof_prefix(result, limit=True)


def test_inline_source_audit_does_not_count_reference_heading_as_step_tag():
    from types import SimpleNamespace
    from proof import ProofRule
    from phase168_r3_41e_certified_prefix_reference_audit.audit import audit_inline_step_sources

    model = SimpleNamespace(
        steps=(SimpleNamespace(rule=ProofRule.GIVEN),),
        step_citation_numbers=((1,),),
    )
    markdown = "## 使用する結果\n\n**[R1] Proposition 5.1.**\n\n## 証明\n\n- 与件: $X$\n"
    report = audit_inline_step_sources(model, markdown)
    assert report["cited_steps"] == 1
    assert report["missing_inline_citation_steps"][0]["missing_numbers"] == [1]
    assert report["issues"] == []


def test_inline_source_audit_accepts_correct_step_number():
    from types import SimpleNamespace
    from proof import ProofRule

    model = SimpleNamespace(
        steps=(SimpleNamespace(rule=ProofRule.GIVEN),),
        step_citation_numbers=((1,),),
    )
    markdown = "## 使用する結果\n\n**[R1] Proposition 5.1.**\n\n## 証明\n\n- 与件: [R1]より, $X$\n"
    report = audit_inline_step_sources(model, markdown)
    assert not report["missing_inline_citation_steps"]
    assert report["rendered_steps"] == 1


def test_inline_source_audit_detects_missing_step_count():
    from types import SimpleNamespace
    from proof import ProofRule

    model = SimpleNamespace(
        steps=(SimpleNamespace(rule=ProofRule.GIVEN),),
        step_citation_numbers=((1,),),
    )
    markdown = "## 使用する結果\n\n**[R1] Proposition 5.1.**\n\n## 証明\n"
    report = audit_inline_step_sources(model, markdown)
    assert "RENDERED_STEP_COUNT_MISMATCH" in report["issues"]


def test_real_certified_control_prefix_has_registry_reference_bodies():
    from phase168_r3_41e_certified_prefix_reference_audit.audit import run_certified_prefix_case

    report, markdown, view = run_certified_prefix_case()
    assert report["not_a_genuine_partial_search"]
    assert report["selected_observed_proof_steps"] < report["full_control_step_count"]
    assert report["model_citation_count"] >= 1
    assert report["registered_assertion_citation_count"] >= 1
    assert report["citation_body_count"] >= 1
    assert report["original_proof_steps_not_recreated"]
    assert report["step_inline_citation_audit"]["cited_steps"] >= 1
    assert all(body["raw_reference_present"] and body["web_reference_present"]
               for citation in report["reference_projection"]["citations"]
               for body in citation["bodies"])
    assert report["unresolved_goal_kept"]
    assert report["diagnostics_kept"]
    assert view.partial_result
    assert "□" not in markdown
