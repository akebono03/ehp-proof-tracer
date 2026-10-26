"""Phase 169 R3B: minimal verified frontier; no manufactured proof leaves."""
from __future__ import annotations

import pytest

from expression import Composition
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase165_r12_r24_web_search_connection import (
    expand_finite_cyclic_relation,
    finite_cyclic_suspension_transport_inference_rule,
)
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import toda_eta_family_definition_statement


def _goals():
    eta2 = toda_eta_family_definition_statement(2).element
    eta3 = toda_eta_family_definition_statement(3).element
    eta4 = toda_eta_family_definition_statement(4).element
    lower = Relation(
        lhs=TodaPrimaryGroup(4, 2),
        rhs=FiniteCyclicGroup(2, Composition(eta2, eta3)),
        relation_type=RelationType.EQUALITY,
    )
    upper = Relation(
        lhs=TodaPrimaryGroup(5, 3),
        rhs=FiniteCyclicGroup(2, Composition(eta3, eta4)),
        relation_type=RelationType.EQUALITY,
    )
    mapping = TodaSuspensionMap(lower.lhs, upper.lhs)
    return lower, upper, mapping


def test_expansion_contains_three_unproved_typed_premises(monkeypatch):
    import phase166_r3aj_structured_generator as database
    lower, upper, mapping = _goals()
    monkeypatch.setattr(
        database, "database_structured_group_goal_candidates",
        lambda *, n, k: (lower,) if (n, k) == (2, 2) else (),
    )
    options = expand_finite_cyclic_relation(upper)
    assert len(options) == 2
    assert options[0].rule.name == "finite cyclic structure gives group relation"
    proposal = options[1]
    assert proposal.rule.name == "finite cyclic presentation transported by proved suspension isomorphism"
    assert proposal.subgoals == (
        lower,
        TodaSuspensionIsomorphismStatement(mapping),
        GeneratorImage(mapping, lower.rhs.generator, upper.rhs.generator),
    )
    assert proposal.rule.literature_reference is None


def test_inference_derives_only_from_all_three_verified_premises():
    lower, upper, mapping = _goals()
    rule = finite_cyclic_suspension_transport_inference_rule()
    proof_steps = (
        ProofStep(conclusion=lower, premises=(), rule=ProofRule.GIVEN),
        ProofStep(
            conclusion=TodaSuspensionIsomorphismStatement(mapping),
            premises=(), rule=ProofRule.GIVEN,
        ),
        ProofStep(
            conclusion=GeneratorImage(mapping, lower.rhs.generator, upper.rhs.generator),
            premises=(), rule=ProofRule.GIVEN,
        ),
    )
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, proof_steps[:2]) == ()
    matches = find_inference_matches_for_rule(rule, proof_steps)
    assert len(matches) == 1
    inferred = apply_inference_match(matches[0])
    assert inferred.rule is ProofRule.INFERENCE
    assert inferred.conclusion == upper
    assert inferred.premises == proof_steps


def test_wrong_isomorphism_or_generator_image_rejected():
    lower, upper, mapping = _goals()
    rule = finite_cyclic_suspension_transport_inference_rule()
    other = TodaSuspensionMap(lower.lhs, TodaPrimaryGroup(6, 4))
    source_step = ProofStep(conclusion=lower, premises=(), rule=ProofRule.GIVEN)
    image_step = ProofStep(
        conclusion=GeneratorImage(mapping, lower.rhs.generator, upper.rhs.generator),
        premises=(), rule=ProofRule.GIVEN,
    )
    wrong_iso = ProofStep(
        conclusion=TodaSuspensionIsomorphismStatement(other),
        premises=(), rule=ProofRule.GIVEN,
    )
    assert find_inference_matches_for_rule(rule, (source_step, wrong_iso, image_step)) == ()
    iso_step = ProofStep(
        conclusion=TodaSuspensionIsomorphismStatement(mapping),
        premises=(), rule=ProofRule.GIVEN,
    )
    wrong_image = ProofStep(
        conclusion=GeneratorImage(mapping, upper.rhs.generator, lower.rhs.generator),
        premises=(), rule=ProofRule.GIVEN,
    )
    assert find_inference_matches_for_rule(rule, (source_step, iso_step, wrong_image)) == ()


def test_missing_or_ambiguous_registered_source_retains_previous_route(monkeypatch):
    import phase166_r3aj_structured_generator as database
    lower, upper, _ = _goals()
    monkeypatch.setattr(
        database, "database_structured_group_goal_candidates",
        lambda *, n, k: (),
    )
    options = expand_finite_cyclic_relation(upper)
    assert len(options) == 1
    monkeypatch.setattr(
        database, "database_structured_group_goal_candidates",
        lambda *, n, k: (lower, lower),
    )
    assert len(expand_finite_cyclic_relation(upper)) == 1


def test_other_stems_are_unchanged(monkeypatch):
    import phase166_r3aj_structured_generator as database
    lower, upper, _ = _goals()

    def unexpected_database_call(*, n, k):
        pytest.fail("ineligible stem must not query structured source")

    monkeypatch.setattr(database, "database_structured_group_goal_candidates", unexpected_database_call)
    other_stem = Relation(
        lhs=TodaPrimaryGroup(6, 3),
        rhs=upper.rhs,
        relation_type=RelationType.EQUALITY,
    )
    assert len(expand_finite_cyclic_relation(other_stem)) == 1
    assert len(expand_finite_cyclic_relation(lower)) == 1


def test_live_source_and_shared_search_frontier_remain_unproved():
    from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus

    lower_goals = database_structured_group_goal_candidates(n=2, k=2)
    upper_goals = database_structured_group_goal_candidates(n=3, k=2)
    assert len(lower_goals) == 1 and len(upper_goals) == 1
    lower, upper = lower_goals[0], upper_goals[0]
    assert lower.rhs.order == upper.rhs.order == 2
    assert isinstance(lower.rhs.generator, Composition)
    assert isinstance(upper.rhs.generator, Composition)
    options = expand_finite_cyclic_relation(upper)
    assert len(options) == 2
    assert options[1].subgoals[0] == lower
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert contexts
    provider = shared_expansion_provider(contexts[-1], proof_target=upper)
    names = tuple(x.rule.name for x in provider(upper))
    assert "finite cyclic presentation transported by proved suspension isomorphism" in names
    assert result.status is not ProofSearchStatus.COMPLETE
    assert result.conclusion != upper
