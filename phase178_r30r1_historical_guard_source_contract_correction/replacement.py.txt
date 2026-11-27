"""Focused tests of the R4C bridge and source-backed pi6_4 suspension proof."""
from __future__ import annotations

import pytest

from homotopy_groups import (
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r4c_pi64_suspension_iso.rule import (
    expand_pi64_suspension_isomorphism,
    pi64_suspension_isomorphism_rule,
)
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
from phase174_r3_r6_r2_prop44_lemma54.source import (
    TodaPreProp44SplittingStatement,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
)
from phase165_r52_partial_proof import (
    PartialProofResult,
    ProofSearchStatus,
)
from phase168_r3_41p13_trust_boundary.verification import (
    verify_proof_tree_for_narrative,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def _map() -> TodaSuspensionMap:
    return TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))


def _real_context():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=2)
    assert len(goals) == 1
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    assert citing is not None
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    return screened, target, citing, provider


def _ancestors(step: ProofStep) -> tuple[ProofStep, ...]:
    stack = [step]
    seen = set()
    result = []
    while stack:
        current = stack.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        result.append(current)
        stack.extend(current.premises)
    return tuple(result)


def test_r4c_only_exact_pi64_map_is_eligible():
    correct = TodaSuspensionIsomorphismStatement(_map())
    wrong = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(6, 4), TodaPrimaryGroup(7, 5))
    )
    assert len(expand_pi64_suspension_isomorphism(correct)) == 1
    assert expand_pi64_suspension_isomorphism(wrong) == ()
    assert expand_pi64_suspension_isomorphism(MapInjective(_map())) == ()
    with pytest.raises(ValueError):
        pi64_suspension_isomorphism_rule(wrong)


def test_r4c_exact_premise_types_and_map_dimensions():
    goal = TodaSuspensionIsomorphismStatement(_map())
    proposal = expand_pi64_suspension_isomorphism(goal)[0]
    assert proposal.subgoals == (MapInjective(_map()), MapSurjective(_map()))
    assert [x.proof_rule for x in proposal.rule.premise_patterns] == [
        ProofRule.INFERENCE, ProofRule.INFERENCE,
    ]
    assert proposal.rule.conclusion_pattern == goal


def test_r4c_rejects_given_as_completed_map_property():
    rule = pi64_suspension_isomorphism_rule(TodaSuspensionIsomorphismStatement(_map()))
    fake_inj = ProofStep(MapInjective(_map()), (), ProofRule.GIVEN)
    fake_surj = ProofStep(MapSurjective(_map()), (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (fake_inj, fake_surj)) == ()
    supposed_inj = ProofStep(MapInjective(_map()), (), ProofRule.INFERENCE)
    assert find_inference_matches_for_rule(rule, (supposed_inj, fake_surj)) == ()
    assert find_inference_matches_for_rule(rule, (fake_inj, ProofStep(MapSurjective(_map()), (), ProofRule.INFERENCE))) == ()


def test_r4c_rejects_mismatched_inference_map():
    rule = pi64_suspension_isomorphism_rule(TodaSuspensionIsomorphismStatement(_map()))
    incorrect_map = TodaSuspensionMap(TodaPrimaryGroup(6, 4), TodaPrimaryGroup(7, 5))
    injective = ProofStep(MapInjective(_map()), (), ProofRule.INFERENCE)
    surjective = ProofStep(MapSurjective(incorrect_map), (), ProofRule.INFERENCE)
    assert find_inference_matches_for_rule(rule, (injective, surjective)) == ()


def test_r4c_shared_provider_contains_typed_iso_link():
    _, _, _, provider = _real_context()
    goal = TodaSuspensionIsomorphismStatement(_map())
    options = provider(goal)
    assert any(option.rule.name ==
               "pi6_4 suspension isomorphism from proved injectivity and surjectivity"
               for option in options)


def test_r4c_real_screened_iso_proof_has_three_prior_sources():
    screened, _, citing, provider = _real_context()
    mapping = _map()
    goal = TodaSuspensionIsomorphismStatement(mapping)
    proof = reconstruct_registered_goal(
        goal, screened, citing, provider, lookup_mode="typed_reference",
    )
    assert proof.conclusion == goal
    assert proof.rule is ProofRule.INFERENCE
    assert len(proof.premises) == 2
    injection, surjection = proof.premises
    assert injection.rule is ProofRule.INFERENCE
    assert surjection.rule is ProofRule.INFERENCE
    assert injection.conclusion == MapInjective(mapping)
    assert surjection.conclusion == MapSurjective(mapping)

    # Injectivity follows from the independent Hopf splitting.
    assert len(injection.premises) == 1
    prelude = injection.premises[0]
    assert prelude.rule is ProofRule.GIVEN
    assert prelude.conclusion == TodaPreProp44SplittingStatement()
    assert not prelude.premises

    # Surjectivity follows from exactness and connectivity.
    surjection_ancestors = _ancestors(surjection)
    assert {type(step.conclusion) for step in surjection_ancestors
            if step.rule is ProofRule.GIVEN} == {
        TodaProp42GeneralExactnessStatement,
        Toda51BelowDiagonalZeroStatement,
    }
    assert any(
        step.rule is ProofRule.INFERENCE
        and step.conclusion == TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(6, 7))
        for step in surjection_ancestors
    )

    # Every GIVEN must be linked to an earlier fixed source.
    ancestors = _ancestors(proof)
    givens = [step for step in ancestors if step.rule is ProofRule.GIVEN]
    assert len(givens) == 3
    assert {type(step.conclusion) for step in givens} == {
        TodaPreProp44SplittingStatement,
        TodaProp42GeneralExactnessStatement,
        Toda51BelowDiagonalZeroStatement,
    }
    citing_assertion = screened.registry.assertion(citing)
    citing_reference = screened.registry.reference(citing_assertion.reference_id)
    citing_position = citing_reference.publication_position
    assert type(citing_position) is int
    for step in givens:
        assert not step.premises
        valid_links = []
        for link in screened.proof_links:
            if link.step != step:
                continue
            assertion = screened.registry.assertion(link.assertion_id)
            reference = screened.registry.reference(assertion.reference_id)
            if (
                assertion.origin.name == "FIXED_STATEMENT"
                and assertion.content == step.conclusion
                and type(reference.publication_position) is int
                and reference.publication_position < citing_position
            ):
                valid_links.append(link)
        assert valid_links, "Missing prior fixed source: " + type(step.conclusion).__name__

    assert not any(
        link.step is not None and link.step.rule is ProofRule.GIVEN
        and isinstance(link.step.conclusion, TodaLemma54TypedSource)
        for link in screened.proof_links
    )

    # Replay the map proof, not a group presentation.
    result = PartialProofResult(
        target=mapping.target_group, status=ProofSearchStatus.COMPLETE,
        proven_steps=(proof,), conclusion=goal,
    )
    inference_count, given_count = verify_proof_tree_for_narrative(
        result, screened, citing_assertion_id=citing,
    )
    assert given_count == len(givens)
    assert inference_count == sum(step.rule is ProofRule.INFERENCE for step in ancestors)
    print("PHASE178_R30R1_HISTORICAL_REPLAY=VERIFIED")
    print("PHASE178_R30R1_PRIOR_SOURCES=VERIFIED")
