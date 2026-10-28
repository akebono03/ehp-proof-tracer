"""R6C: source-scoped citations with all original ProofSteps retained."""
from __future__ import annotations

import re

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import (
    build_proof_narrative_model, root_ancestor_step_indices,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def test_r6c_root_scope_does_not_delete_orphans_from_proof_tree():
    unused = ProofStep(
        conclusion="other source", premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(
            name="other-source", literature_reference=LiteratureReference(
                label="Unused source", locator="Unused source",
            ),
        ),
    )
    used = ProofStep(
        conclusion="used premise", premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(
            name="used-source", literature_reference=LiteratureReference(
                label="Used source", locator="Used source",
            ),
        ),
    )
    root = ProofStep(conclusion="derived", premises=(used,),
                     rule=ProofRule.INFERENCE, inference_rule=InferenceRule(name="derived"))
    result = make_partial_proof_result(
        n=8, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(unused, used, root), conclusion="derived",
    )
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert model.root_index == 2
    assert root_ancestor_step_indices(model.steps, 2) == frozenset({1, 2})
    assert tuple(ref.reference.locator for ref in model.citations) == ("Used source",)
    assert model.step_citation_numbers == ((), (1,), ())


def test_r6c_incomplete_model_does_not_filter_early_evidence():
    rule = InferenceRule(name="observed", literature_reference=LiteratureReference(
        label="Observed", locator="Observed",
    ))
    observed = ProofStep(conclusion="observed", premises=(),
                         rule=ProofRule.INFERENCE, inference_rule=rule)
    result = make_partial_proof_result(
        n=8, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(observed,), open_goals=("unresolved",),
    )
    model = build_proof_narrative_model(result)
    assert model.root_index is None
    assert model.step_citation_numbers == ((1,),)
    assert [c.reference.locator for c in model.citations] == ["Observed"]


def test_r6c_invalid_ancestry_fails_closed():
    leaf = ProofStep(conclusion="x", premises=(), rule=ProofRule.GIVEN)
    absent = ProofStep(conclusion="absent", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="y", premises=(absent,), rule=ProofRule.INFERENCE,
                     inference_rule=InferenceRule(name="derive"))
    with pytest.raises(ValueError, match="missing or ambiguous"):
        root_ancestor_step_indices((leaf, root), 1)


@pytest.fixture(scope="module")
def pi108():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=8,k=2,bridge=bridge,context_sink=contexts.append)
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge,result.conclusion)
    verify_proof_tree_for_narrative(result,contexts[0],citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None)
    model = build_linked_proof_narrative_model(result,contexts[0])
    return result, model


def test_r6c_pi108_retains_all_steps_and_removes_only_detached_reference(pi108):
    result, model = pi108
    assert model.steps == result.proven_steps
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    assert len(model.steps) == 9 and len(scope) == 8
    assert len(model.citations) == 2
    assert [c.reference.locator or c.reference.label for c in model.citations] == [
        "DB prior: sphere.csv (n=4, k=2) [参考: Proposition 5.3]", "(4.5)",
    ]
    for citation in model.citations:
        assert all(i in scope for i in citation.step_indices)
    for i in range(len(model.steps)):
        if i not in scope:
            assert model.step_citation_numbers[i] == ()


def test_r6c_pi108_renderer_omits_unused_given_and_keeps_mathematics(pi108):
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    result, model = pi108
    before = (model.steps, model.citations, model.step_citation_numbers)
    displayed = render_model_backed_narrative_markdown(result, model)
    assert "DB prior: sphere.csv (n=7, k=2)" not in displayed
    assert "DB prior: sphere.csv (n=4, k=2)" in displayed
    assert "(4.5)" in displayed
    assert "[R3]" not in displayed
    assert re.search(r"\[R1\]",displayed) and re.search(r"\[R2\]",displayed)
    assert r"E^{4}" in displayed
    assert displayed.rstrip().endswith("□")
    assert (model.steps, model.citations, model.step_citation_numbers) == before


def test_r6c_unreachable_registered_given_is_not_cited():
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
        ReferenceKind, UnifiedStatementRegistry,
    )
    registry = UnifiedStatementRegistry()
    for name in ("unused_prior", "used_prior"):
        registry.add_reference(LiteratureEntry(
            reference_id=name,
            kind=ReferenceKind.PROPOSITION,
            locator=name,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=name, reference_id=name,
            kind=AssertionKind.STATEMENT, content=name,
        ))
    orphan = ProofStep(conclusion="unused_prior",premises=(),rule=ProofRule.GIVEN)
    used = ProofStep(conclusion="used_prior",premises=(),rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="proved", premises=(used,),rule=ProofRule.INFERENCE,
                     inference_rule=InferenceRule(name="derive"))
    result = make_partial_proof_result(
        n=8,k=2,status=ProofSearchStatus.COMPLETE,
        proven_steps=(orphan,used,root),conclusion="proved",
    )
    model = build_proof_narrative_model(
        result,registry=registry,
        proof_links=(ProofStepLink(assertion_id="unused_prior",step=orphan),
                     ProofStepLink(assertion_id="used_prior",step=used)),
    )
    assert len(model.steps) == 3
    assert [x.reference.locator for x in model.citations] == ["used_prior"]
    assert model.step_citation_numbers == ((),(1,),())
