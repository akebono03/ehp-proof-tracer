"""Focused R7 tests: arbitrary r, typed images, stable range, publication gate."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r3m_prior_result_catalog.prior_results import PriorGroupResult
from phase169_r7_general_stable_transport import rule as stable
from proof import ProofRule, ProofStep, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule
from toda_rules import Toda45IsomorphismStatement
from unified_statement_registry import UnifiedStatementRegistry


def _element(family: str, n: int, stem: int = 1) -> HomotopyElement:
    return HomotopyElement(
        name=family + str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")),
        dimension=n, source=n + stem, target=n,
        generator=GeneratorSymbol(family=family, index=n),
    )


def _relation(n: int, k: int, generator: object) -> Relation:
    return Relation(TodaPrimaryGroup(n + k, n),
                    FiniteCyclicGroup(2, generator), RelationType.EQUALITY)


def _eta_square(n: int) -> Composition:
    return Composition(_element("η", n), _element("η", n + 1))


def _test_case(*, source_n: int = 4, stem: int = 2, exponent: int = 3,
               family: str = "η") -> tuple[Relation, Relation]:
    if stem == 2 and family == "η":
        source_gen, target_gen = _eta_square(source_n), _eta_square(source_n + exponent)
    else:
        source_gen = _element(family, source_n, stem)
        target_gen = _element(family, source_n + exponent, stem)
    return (_relation(source_n, stem, source_gen),
            _relation(source_n + exponent, stem, target_gen))


def _iso(source: Relation, goal: Relation) -> Toda45IsomorphismStatement:
    return Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=goal.lhs.sphere_dimension - source.lhs.sphere_dimension,
        source_group=source.lhs, target_group=goal.lhs,
    ))


def _mocked_prior(monkeypatch, source: Relation, goal: Relation, *, eligible: bool = True):
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    monkeypatch.setattr(stable, "resolve_specialized_goal_citing_id",
                        lambda current, statement: "target_citation")
    source_n = source.lhs.sphere_dimension
    source_k = source.lhs.group_dimension - source_n
    calls = []

    def resolve(bridge, *, source_n: int, source_k: int, citing_assertion_id: str):
        calls.append((source_n, source_k, citing_assertion_id))
        if source_n == source.lhs.sphere_dimension and source_k == source_k_expected:
            return PriorGroupResult(source_n, source_k, source if eligible else None,
                                    citing_assertion_id, "earlier" if eligible else None,
                                    eligible, "prior_fixed_source" if eligible else "source_not_prior")
        return PriorGroupResult(source_n, source_k, None, citing_assertion_id, None,
                                False, "db_result_missing")

    source_k_expected = source_k
    monkeypatch.setattr(stable, "resolve_prior_group_result", resolve)
    return bridge, calls


@pytest.mark.parametrize("exponent", [1, 2, 3, 4, 7])
def test_r7_arbitrary_count_builds_real_chain_and_inference(exponent):
    source, goal = _test_case(exponent=exponent)
    images = stable._consecutive_generator_image_goals(source, goal)
    assert images is not None and len(images) == exponent
    assert images[0].source_generator == source.rhs.generator
    assert images[-1].target_generator == goal.rhs.generator
    for i in range(exponent - 1):
        assert images[i].target_generator == images[i + 1].source_generator
    iso = _iso(source, goal)
    rule = stable.general_stable_cyclic_transport_rule(goal, source)
    assertions = (source, iso) + images
    steps = tuple(ProofStep(conclusion=assertion, premises=(), rule=ProofRule.INFERENCE)
                  for assertion in assertions)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.conclusion == goal and derived.premises == steps
    assert derived.rule is ProofRule.INFERENCE


def test_r7_missing_or_tampered_proven_image_rejected():
    source, goal = _test_case(exponent=3)
    images = stable._consecutive_generator_image_goals(source, goal)
    assert images is not None
    iso = _iso(source, goal)
    rule = stable.general_stable_cyclic_transport_rule(goal, source)
    steps = tuple(ProofStep(conclusion=x, premises=(), rule=ProofRule.INFERENCE)
                  for x in (source, iso) + images)
    bad_given = steps[:3] + (replace(steps[3], rule=ProofRule.GIVEN),) + steps[4:]
    assert find_inference_matches_for_rule(rule, bad_given) == ()
    wrong_map = replace(iso.map, exponent=2)
    wrong_iso = replace(steps[1], conclusion=Toda45IsomorphismStatement(wrong_map))
    assert find_inference_matches_for_rule(rule, (steps[0], wrong_iso) + steps[2:]) == ()
    assert find_inference_matches_for_rule(rule, steps[:-1]) == ()
    changed = replace(steps[4], conclusion=replace(
        steps[4].conclusion, source_generator=images[0].source_generator,
    ))
    assert find_inference_matches_for_rule(rule, steps[:4] + (changed,)) == ()


@pytest.mark.parametrize("source_n,stem,r,allowed", [
    (3, 1, 2, True),
    (4, 2, 3, True),
    (5, 3, 2, True),
    (3, 2, 2, False),
    (4, 3, 1, False),
])
def test_r7_stable_boundary_without_stem_specific_formula(source_n, stem, r, allowed):
    source, goal = _test_case(source_n=source_n, stem=stem, exponent=r,
                              family="ν" if stem == 3 else "η")
    images = stable._consecutive_generator_image_goals(source, goal)
    assert (images is not None) is allowed


def test_r7_unsafe_generator_identity_is_not_assumed():
    source, _ = _test_case(exponent=3)
    _, named_nu_goal = _test_case(exponent=3, family="ν")
    wrong_target = _relation(7, 2, named_nu_goal.rhs.generator)
    assert stable._consecutive_generator_image_goals(source, wrong_target) is None


@pytest.mark.parametrize("r", [1, 2, 3, 4])
def test_r7_prior_catalog_used_as_subgoal_not_given(monkeypatch, r):
    source, goal = _test_case(exponent=r)
    bridge, calls = _mocked_prior(monkeypatch, source, goal)
    options = stable.expand_prior_general_stable_transport(
        goal, (_iso(source, goal),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert len(options[0].subgoals) == 2 + r
    assert options[0].subgoals[0] == source
    assert options[0].subgoals[1] == _iso(source, goal)
    assert calls == [(4, 2, "target_citation")]
    assert all(type(item).__name__ != "ProofStep" for item in options[0].subgoals)


def test_r7_prior_later_source_or_missing_theorem_fails_closed(monkeypatch):
    source, goal = _test_case(exponent=3)
    bridge, _ = _mocked_prior(monkeypatch, source, goal, eligible=False)
    assert stable.expand_prior_general_stable_transport(
        goal, (_iso(source, goal),), bridge, proof_target=goal,
    ) == ()
    bridge, _ = _mocked_prior(monkeypatch, source, goal, eligible=True)
    assert stable.expand_prior_general_stable_transport(
        goal, (), bridge, proof_target=goal,
    ) == ()
    assert stable.expand_prior_general_stable_transport(
        goal, (_iso(source, goal),), bridge, proof_target=source,
    ) == ()


def test_r7_patch_is_only_provider_function_and_reversible():
    from phase169_r7_general_stable_transport.patch import (
        NEW_TWO, NEW_ONE, OLD_ONE, OLD_TWO, replacement_content,
    )
    sample = ("def shared_expansion_provider():\n"
              "    def expand(goal):\n" + OLD_ONE + "\n" + OLD_TWO +
              "\n        return options\n    return expand\n").encode("utf-8")
    updated, full = replacement_content(sample)
    assert NEW_ONE in full and NEW_TWO in full
    assert b"\r\n" not in updated
    with pytest.raises(RuntimeError):
        replacement_content(updated)
    windows = sample.replace(b"\n", b"\r\n")
    changed, _ = replacement_content(windows)
    assert b"\r\n" in changed
