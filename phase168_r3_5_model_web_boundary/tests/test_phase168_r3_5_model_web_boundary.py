from dataclasses import replace

import pytest

from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry


def _example():
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from proof import Relation

    eta3 = HomotopyElement(name="η₃", dimension=3, source=4, target=3, generator=GeneratorSymbol(family="η", index=3))
    premise_statement = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta3))
    result_statement = Relation(TodaPrimaryGroup(4, 2), FiniteCyclicGroup(2, eta3))
    given = ProofStep(conclusion=premise_statement, premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion=result_statement, premises=(given,), rule=ProofRule.INFERENCE, inference_rule=InferenceRule(name="test transport", literature_reference=LiteratureReference(label="Toda (5.2)", locator="(5.2)")))
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(reference_id="prop51", kind=ReferenceKind.PROPOSITION, locator="Proposition 5.1"))
    registry.add_assertion(AssertionEntry(assertion_id="g43", reference_id="prop51", kind=AssertionKind.STATEMENT, content=premise_statement))
    bridge = RegistryBridgeResult(registry, (), (ProofStepLink(assertion_id="g43", step=given),))
    result = make_partial_proof_result(n=2, k=2, status=ProofSearchStatus.COMPLETE, proven_steps=(given, root), conclusion=root.conclusion)
    return result, build_linked_proof_narrative_model(result, bridge)


def test_model_web_contains_both_citations():
    result, model = _example()
    view = build_partial_web_group_proof_view(result, narrative_model=model)
    content = "\n".join(line.prefix + (line.statement_latex or "") + line.suffix for line in view.rendered_lines)
    assert "Proposition 5.1" in content
    assert "(5.2)" in content
    assert "[R1]" in content
    assert "[R2]" in content


def test_model_rejects_other_search_steps():
    result, model = _example()
    bad_model = replace(model, steps=model.steps[:-1])
    with pytest.raises(ValueError, match="model steps"):
        render_model_backed_narrative_markdown(result, bad_model)


def test_trace_mode_keeps_no_rendered_lines():
    result, model = _example()
    view = build_partial_web_group_proof_view(result, mode="trace", narrative_model=model)
    assert view.rendered_lines == ()
