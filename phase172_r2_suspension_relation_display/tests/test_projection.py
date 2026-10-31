"""Phase 172 R2: exact proof-ancestry-only suspension prose suppression."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Suspension
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase172_r2_suspension_relation_display.projection import (
    redundant_suspension_relation_indices,
    same_typed_generator,
)
from proof import ProofRule, Relation, RelationType


@pytest.fixture(scope="module")
def verified_pi63():
    original = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=original, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(original, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    return result, build_linked_proof_narrative_model(result, contexts[0])


def _verified_direct_and_symmetric_relation_indices(model):
    direct = [
        index for index, step in enumerate(model.steps)
        if isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and len(step.premises) == 1
        and isinstance(step.premises[0].conclusion, GeneratorSuspension)
        and isinstance(step.conclusion.lhs, Suspension)
        and same_typed_generator(
            step.conclusion.lhs.expression,
            step.premises[0].conclusion.source_generator,
        )
        and same_typed_generator(
            step.conclusion.rhs,
            step.premises[0].conclusion.target_generator,
        )
    ]
    assert len(direct) == 1
    source_index = direct[0]
    symmetric = [
        index for index, step in enumerate(model.steps)
        if isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and len(step.premises) == 1
        and (step.premises[0] is model.steps[source_index]
             or step.premises[0] == model.steps[source_index])
        and step.conclusion.lhs == model.steps[source_index].conclusion.rhs
        and step.conclusion.rhs == model.steps[source_index].conclusion.lhs
    ]
    assert len(symmetric) == 1
    return source_index, symmetric[0]


def test_real_public_tree_hides_only_derived_suspension_equation_and_symmetry(
    verified_pi63,
):
    result, model = verified_pi63
    assert model.root_index is not None
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_26_exactness_projection import project_exactness_chains
    chains = project_exactness_chains(model)
    omitted = {index for chain in chains for index in chain.step_indices}
    order = tuple(row.step_index for row in project_narrative_order(model, omitted))
    indices = redundant_suspension_relation_indices(model, order)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    assert indices == frozenset({direct, symmetric})
    assert all(model.steps[i].rule is ProofRule.INFERENCE for i in indices)
    assert all(not model.step_citation_numbers[i] for i in indices)
    assert any(
        child is not model.steps[symmetric]
        and any(parent is model.steps[direct] or parent == model.steps[direct]
                for parent in child.premises)
        for child in model.steps
    )
    assert any(
        any(parent is model.steps[symmetric] or parent == model.steps[symmetric]
            for parent in child.premises)
        for child in model.steps
    )
    assert result.proven_steps == model.steps


def test_real_complete_narrative_retains_cited_source_and_hopf_conclusion(
    verified_pi63,
):
    result, model = verified_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    assert "[R3] Chapter V, i)." in references
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert r"$E\eta_{5} = \eta_{6}$." not in body
    assert r"$\eta_{6} = E\eta_{5}$." not in body
    assert "[R4] Proposition 2.2." in references
    assert "[R5] (5.3)." in references
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert len(model.citations) == 8


def test_citation_on_relation_prevents_suppression(verified_pi63):
    _, model = verified_pi63
    edited = list(model.step_citation_numbers)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    edited[direct] = (3,)
    changed = replace(model, step_citation_numbers=tuple(edited))
    order = tuple(range(len(model.steps)))
    hidden = redundant_suspension_relation_indices(changed, order)
    assert direct not in hidden and symmetric not in hidden


def test_missing_source_citation_preserves_both_lines(verified_pi63):
    _, model = verified_pi63
    edited = list(model.step_citation_numbers)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    cited_family_source = next(
        index for index, step in enumerate(model.steps)
        if type(step.conclusion).__name__ == "TodaEtaFamilyGeneralDefinition"
        and model.step_citation_numbers[index]
    )
    edited[cited_family_source] = ()
    changed = replace(model, step_citation_numbers=tuple(edited))
    order = tuple(range(len(model.steps)))
    hidden = redundant_suspension_relation_indices(changed, order)
    assert direct not in hidden and symmetric not in hidden


def test_hidden_source_or_missing_root_does_not_suppress(verified_pi63):
    _, model = verified_pi63
    order = tuple(range(len(model.steps)))
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    source = model.steps[direct].premises[0]
    source_index = next(index for index, step in enumerate(model.steps)
                        if step is source or step == source)
    hidden = redundant_suspension_relation_indices(model, order, {source_index})
    assert direct not in hidden and symmetric not in hidden
    partial_like = replace(model, root_index=None)
    assert redundant_suspension_relation_indices(partial_like, order) == frozenset()


def test_typed_identity_recognizes_a_display_alias_without_matching_others(
    verified_pi63,
):
    _, model = verified_pi63
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    suspension = model.steps[direct].premises[0].conclusion
    equality = model.steps[direct].conclusion
    assert isinstance(suspension, GeneratorSuspension)
    assert isinstance(equality.lhs, Suspension)
    # Two recorded names differ, but their registered structural types agree.
    assert suspension.source_generator.name != equality.lhs.expression.name
    assert same_typed_generator(
        suspension.source_generator, equality.lhs.expression,
    )
    assert not same_typed_generator(
        suspension.source_generator, suspension.target_generator,
    )
    assert not same_typed_generator(equality.lhs, suspension.source_generator)
    assert not same_typed_generator(object(), suspension.source_generator)
    assert symmetric != direct
