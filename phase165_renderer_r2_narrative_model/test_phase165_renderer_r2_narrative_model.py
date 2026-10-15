"""R2 model contract: one evidence shape; no changes to existing renderers."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from phase165_renderer_narrative_model import (
    NarrativeProofModel,
    build_narrative_proof_model,
)
from proof import ProofRule, ProofStep


def test_r2_unsearched_model_keeps_original_target():
    result = make_partial_proof_result(n=200, k=90, status=ProofSearchStatus.NOT_SEARCHED)
    model = build_narrative_proof_model(result)
    assert isinstance(model, NarrativeProofModel)
    assert model.source is result
    assert model.target is result.target
    assert model.status is ProofSearchStatus.NOT_SEARCHED
    assert model.conclusion is None
    assert model.proven_steps == ()
    assert model.root_step is None


def test_r2_partial_keeps_goal_diagnostics_reference_and_step_identity():
    step = ProofStep(conclusion="known", premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.PARTIAL,
        proven_steps=(step,), open_goals=("unknown",),
        references=("Toda Proposition 4.2",), diagnostics=("missing premise",),
    )
    model = build_narrative_proof_model(result)
    assert model.source_kind == "search_result"
    assert model.proven_steps[0] is step
    assert model.open_goals == ("unknown",)
    assert model.references == ("Toda Proposition 4.2",)
    assert model.diagnostics == ("missing premise",)
    assert model.conclusion is None


def test_r2_complete_search_model_root_identity_without_rederivation():
    step = ProofStep(conclusion="final", premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion="final",
    )
    model = build_narrative_proof_model(result)
    assert model.status is ProofSearchStatus.COMPLETE
    assert model.root_step is step
    assert model.conclusion == "final"
    assert model.proven_steps == (step,)


def test_r2_presentation_model_keeps_actual_replay_steps():
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r56_presentation_adapter import render_completed_shared_narrative
    from homotopy_groups import FreeCyclicGroup, FiniteCyclicGroup
    from proof import ProofRule
    from proof_repository import ProofRepositoryEntry
    from toda_group_result import TodaGroupResult
    from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
    from toda_group_proof_presentation import build_toda_group_proof_presentation

    search = search_group_from_registered_goal(n=2, k=1)
    assert search.status is ProofSearchStatus.COMPLETE
    structure = search.conclusion.rhs
    assert isinstance(structure, (FreeCyclicGroup, FiniteCyclicGroup))
    root = tuple(
        step for step in search.proven_steps if step.conclusion == search.conclusion
    )
    assert len(root) == 1 and root[0].rule is ProofRule.INFERENCE
    entry = ProofRepositoryEntry(key="r2:model:pi32", step=root[0], phase="165")
    group = TodaGroupResult(
        target=search.target, group_structure=structure,
        generators=(structure.generator,),
        generator_orders=(None if isinstance(structure, FreeCyclicGroup) else structure.order,),
        source_entry=entry, proof_step=root[0],
    )
    presentation = build_toda_group_proof_presentation(
        build_complete_toda_group_result_proof_replay(group)
    )
    model = build_narrative_proof_model(presentation)
    assert model.status is ProofSearchStatus.COMPLETE
    assert model.source is presentation
    assert model.root_step is presentation.root_step
    assert model.proven_steps == tuple(node.proof_step for node in presentation.nodes)
    assert model.target == search.target
    assert model.open_goals == ()
    assert "証明対象" in render_completed_shared_narrative(search)


def test_r2_rejects_unknown_sources():
    with pytest.raises(TypeError):
        build_narrative_proof_model(object())


def test_r2_does_not_mutate_existing_markdown():
    result = make_partial_proof_result(n=3, k=1, status=ProofSearchStatus.NOT_SEARCHED)
    before = render_partial_proof_markdown(result)
    model = build_narrative_proof_model(result)
    after = render_partial_proof_markdown(result)
    assert model.source is result
    assert before == after
