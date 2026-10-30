"""Focused and negative tests for cited Hopf surjectivity."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from expression import GeneratorSymbol, HomotopyElement, MapApplication
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    expand_registered_eta_specialization,
)
from phase169_r3h_source_registry import ASSERTION_ID as HOPF_ASSERTION_ID
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r4_cited_hopf_surjectivity.audit import (
    _git,
    screened_source_link,
)
from phase171_r2j_r4_r4_cited_hopf_surjectivity.source import (
    cited_hopf_cyclic_surjectivity_rule,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    find_inference_matches_for_rule,
)


def _fixtures():
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    eta = HomotopyElement(
        name="η₅", dimension=5, source=6, target=5,
        generator=GeneratorSymbol(family="η", index=5),
    )
    group = Relation(
        TodaPrimaryGroup(6, 5), FiniteCyclicGroup(2, replace(eta, name="η_5")),
        RelationType.EQUALITY,
    )
    image = Relation(MapApplication(EHP_H_MAP, nu), eta, RelationType.EQUALITY)
    goal = MapSurjective(TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)))
    return goal, group, image


def test_cited_hopf_and_proved_generator_admit_typed_rule():
    goal, group, image = _fixtures()
    rule = cited_hopf_cyclic_surjectivity_rule(goal, group, image)
    assert rule.conclusion_pattern == goal
    assert len(rule.premise_patterns) == 2
    assert rule.premise_patterns[0].proof_rule is ProofRule.INFERENCE
    assert rule.premise_patterns[1].proof_rule is ProofRule.GIVEN


def test_cited_hopf_rule_rejects_given_group():
    goal, group, image = _fixtures()
    rule = cited_hopf_cyclic_surjectivity_rule(goal, group, image)
    steps = (
        ProofStep(group, (), ProofRule.GIVEN),
        ProofStep(image, (), ProofRule.GIVEN),
    )
    assert find_inference_matches_for_rule(rule, steps) == ()


def test_cited_hopf_rule_rejects_inferred_image_without_cited_source():
    goal, group, image = _fixtures()
    rule = cited_hopf_cyclic_surjectivity_rule(goal, group, image)
    steps = (
        ProofStep(group, (), ProofRule.INFERENCE),
        ProofStep(image, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(rule, steps) == ()


def test_cited_hopf_rule_rejects_given_with_premises():
    goal, group, image = _fixtures()
    rule = cited_hopf_cyclic_surjectivity_rule(goal, group, image)
    source = ProofStep("source", (), ProofRule.GIVEN)
    invalid = ProofStep(image, (source,), ProofRule.GIVEN)
    steps = (ProofStep(group, (), ProofRule.INFERENCE), invalid)
    assert find_inference_matches_for_rule(rule, steps) == ()


def test_cited_hopf_rule_constructs_real_inference_step():
    goal, group, image = _fixtures()
    rule = cited_hopf_cyclic_surjectivity_rule(goal, group, image)
    group_step = ProofStep(group, (), ProofRule.INFERENCE)
    image_step = ProofStep(image, (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(rule, (group_step, image_step))
    assert len(matches) == 1
    root = derive_inference_proof_step(matches[0])
    assert root.rule is ProofRule.INFERENCE
    assert root.conclusion == goal
    assert root.premises == (group_step, image_step)


def test_hopf_rule_rejects_wrong_map_or_generator():
    goal, group, image = _fixtures()
    wrong_map = MapSurjective(TodaHopfInvariantMap(TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5)))
    with pytest.raises(ValueError):
        cited_hopf_cyclic_surjectivity_rule(wrong_map, group, image)
    unrelated = HomotopyElement(
        name="η₆", dimension=6, source=7, target=6,
        generator=GeneratorSymbol(family="η", index=6),
    )
    with pytest.raises(ValueError):
        cited_hopf_cyclic_surjectivity_rule(goal, group, replace(image, rhs=unrelated))


def test_hopf_rule_rejects_invalid_group_order():
    goal, group, image = _fixtures()
    bad = replace(group, rhs=FiniteCyclicGroup(1, group.rhs.generator))
    with pytest.raises(ValueError):
        cited_hopf_cyclic_surjectivity_rule(goal, bad, image)


def test_screened_source_link_rejects_unauthorized_or_missing_source():
    context = SimpleNamespace(proof_links=())
    with pytest.raises(RuntimeError):
        screened_source_link(context, "missing", assertion_id="absent")


def test_only_read_only_git_operations_permitted():
    with pytest.raises(ValueError):
        _git("restore", ".")


def test_existing_eta_specialization_rejects_non_cited_available_sources():
    _, group, _ = _fixtures()
    assert expand_registered_eta_specialization(group, ()) == ()


def test_real_prefixed_hopf_source_is_found_with_publication_screening():
    screened, _, citing = _screened_context()
    link = screened_source_link(
        screened, citing, assertion_id=HOPF_ASSERTION_ID, locator="(5.3)",
        predicate=lambda item: isinstance(item, Relation),
    )
    assert link.assertion_id.endswith(":" + HOPF_ASSERTION_ID)
    assert link.assertion_id != HOPF_ASSERTION_ID
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()
    assert link.step.conclusion == screened.registry.assertion(link.assertion_id).content


def test_real_prop51_source_and_wrong_hopf_identifier_boundaries():
    screened, _, citing = _screened_context()
    prior = screened_source_link(
        screened, citing, locator="Proposition 5.1",
        predicate=_is_generic_eta_group_relation,
    )
    assert prior.step.rule is ProofRule.GIVEN
    assert prior.step.premises == ()
    assert _is_generic_eta_group_relation(prior.step.conclusion)
    with pytest.raises(RuntimeError):
        screened_source_link(
            screened, citing, assertion_id="fabricated:" + HOPF_ASSERTION_ID,
            locator="(5.3)",
        )
    with pytest.raises(RuntimeError):
        screened_source_link(
            screened, citing, assertion_id=HOPF_ASSERTION_ID,
            locator="Proposition 5.1",
        )
