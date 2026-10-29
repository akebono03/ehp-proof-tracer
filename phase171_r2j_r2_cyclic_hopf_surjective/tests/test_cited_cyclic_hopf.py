"""R2J-R2 regression: valid cited derivation and rejected counterfeit premises."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2j_r2_cyclic_hopf_surjective.audit import build_cited_r2j_r2_proof
from phase171_r2j_r2_cyclic_hopf_surjective.source import (
    _coordinates,
    _eligible_group_instance,
    _valid_surjective_pair,
    cyclic_generator_image_surjectivity_rule,
    cyclic_group_from_cited_general_rule,
    expand_cited_cyclic_hopf_surjectivity,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _case():
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    goal = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    return chain, available, group_goal, goal


def test_cited_proof_of_h_surjectivity_contains_both_inferred_premises():
    proof, group, chain, nodes, source_link = build_cited_r2j_r2_proof()
    assert proof.rule is ProofRule.INFERENCE
    assert len(proof.premises) == 2
    assert all(step.rule is ProofRule.INFERENCE for step in proof.premises)
    assert proof.premises[0].conclusion == group
    assert proof.premises[1].conclusion == chain.conclusion
    assert sum(step.rule is ProofRule.GIVEN for step in nodes) == 4
    assert sum(step.conclusion == source_link.step.conclusion
               for step in nodes if step.rule is ProofRule.GIVEN) == 1


def test_cyclic_group_specialization_requires_screened_general_statement():
    chain, available, root, goal = _case()
    offered = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)
    assert len(offered) == 1
    group = offered[0].subgoals[0]
    assert _valid_surjective_pair(goal, group, chain.conclusion)
    group_options = expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=root)
    assert len(group_options) == 1
    assert group_options[0].subgoals[0] in available
    assert _eligible_group_instance(group_options[0].subgoals[0], group)
    assert expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=group) == ()
    assert expand_cited_cyclic_hopf_surjectivity(goal, (), proof_target=root) == ()


def test_rejects_wrong_hopf_degree_and_wrong_generator():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    bad_map = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 6),
    ))
    assert not _valid_surjective_pair(bad_map, group, chain.conclusion)
    assert expand_cited_cyclic_hopf_surjectivity(bad_map, available, proof_target=root) == ()
    unrelated = HomotopyElement(
        "η₇", 7, source=8, target=7, generator=GeneratorSymbol("η", index=7),
    )
    bad_group = replace(group, rhs=FiniteCyclicGroup(2, unrelated))
    assert not _valid_surjective_pair(goal, bad_group, chain.conclusion)
    assert _coordinates(Composition(chain.alpha, chain.eta_next)) == (7, 3)
    assert _coordinates(Composition(chain.beta, chain.eta_next)) == (7, 5)


def test_rejects_forged_given_group_or_hopf_result():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    rule = cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion)
    forged_group = ProofStep(group, (), ProofRule.GIVEN)
    forged_image = ProofStep(chain.conclusion, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (forged_group, forged_image)) == ()
    source = expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=root)[0].subgoals[0]
    group_rule = cyclic_group_from_cited_general_rule(group, source)
    assert find_inference_matches_for_rule(
        group_rule, (ProofStep(source, (), ProofRule.INFERENCE),)
    ) == ()


def test_cited_generator_alias_is_typed_not_textual():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    assert group.rhs.generator != chain.conclusion.rhs or _valid_surjective_pair(
        goal, group, chain.conclusion,
    )
    assert same_registered_group_presentation(
        FiniteCyclicGroup(2, group.rhs.generator),
        FiniteCyclicGroup(2, chain.conclusion.rhs),
    )
    wrong = replace(chain.eta_next, source=80)
    false_image = Relation(
        MapApplication(EHP_H_MAP, Composition(chain.alpha, wrong)),
        chain.conclusion.rhs, RelationType.EQUALITY,
    )
    assert not _valid_surjective_pair(goal, group, false_image)


def test_without_cited_prop53_or_r2i_sources_cannot_propose_surjectivity():
    chain, available, root, goal = _case()
    offered = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)
    assert len(offered) == 1
    group_source = expand_cited_cyclic_hopf_surjectivity(
        offered[0].subgoals[0], available, proof_target=root,
    )[0].subgoals[0]
    without_prop53 = tuple(item for item in available if item != group_source)
    assert expand_cited_cyclic_hopf_surjectivity(goal, without_prop53, proof_target=root) == ()
    hopf_source = Relation(MapApplication(EHP_H_MAP, chain.alpha), chain.beta, RelationType.EQUALITY)
    without_hopf = tuple(item for item in available if item != hopf_source)
    assert expand_cited_cyclic_hopf_surjectivity(goal, without_hopf, proof_target=root) == ()
