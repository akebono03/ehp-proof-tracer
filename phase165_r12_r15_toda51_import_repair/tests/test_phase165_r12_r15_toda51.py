"""Focused checks of cited Toda (5.1) zero specialization and E-surjectivity."""
from __future__ import annotations

from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r15_toda51 import (
    Toda51BelowDiagonalZeroStatement,
    build_adopted_toda51_zero_reference,
    below_diagonal_zero_specialization_inference_rule,
    expand_cited_toda51_zero,
    proof_has_toda51_zero_ancestor,
    prove_surjectivity_in_screened_context,
)
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r3_recursive_search import reconstruct_registered_goal, RegisteredGoalUnresolved
from proof import ProofRule, Relation, RelationType, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def _target():
    return Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)


def _context():
    bridge = build_shared_typed_bridge()
    citing = next(iter(bridge.registry._assertions))
    return bridge, citing, _target()


def test_r15_toda51_source_is_one_universal_cited_leaf():
    path = Path.cwd() / "phase165_r14_r39_toda51.tex"
    bridge = build_adopted_toda51_zero_reference(path)
    assert len(bridge.proof_links) == 1
    step = bridge.proof_links[0].step
    assert step.rule is ProofRule.GIVEN
    assert isinstance(step.conclusion, Toda51BelowDiagonalZeroStatement)
    assert bridge.registry.reference(next(iter(bridge.registry._references))).locator == "(5.1)"


def test_r15_specialization_is_real_inference_with_cited_ancestor():
    bridge, citing, target = _context()
    screened = screen_shared_proof_context(bridge, goal=target, citing_assertion_id=citing)
    source = tuple(link.step.conclusion for link in screened.proof_links
                   if isinstance(link.step.conclusion, Toda51BelowDiagonalZeroStatement))
    assert len(source) == 1
    zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(4, 5))
    expansions = expand_cited_toda51_zero(zero, source)
    assert len(expansions) == 1
    proof = reconstruct_registered_goal(
        zero, screened, citing_assertion_id=citing,
        expansion_provider=lambda goal: expand_cited_toda51_zero(goal, source),
        lookup_mode="typed_reference",
    )
    assert proof.rule is ProofRule.INFERENCE
    assert len(proof.premises) == 1
    assert proof_has_toda51_zero_ancestor(proof)


def test_r15_general_non_matching_indices_rejected():
    source = (Toda51BelowDiagonalZeroStatement(),)
    for i, n in ((5, 5), (6, 5), (-1, 3), (2, 1), (True, 5), (4, True)):
        target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, n))
        assert expand_cited_toda51_zero(target, source) == ()
        with pytest.raises(ValueError):
            below_diagonal_zero_specialization_inference_rule(target)


def test_r15_same_general_rule_handles_other_dimensions():
    source = (Toda51BelowDiagonalZeroStatement(),)
    for i, n in ((0, 2), (2, 3), (5, 8)):
        target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, n))
        expansion, = expand_cited_toda51_zero(target, source)
        assert expansion.subgoals == source


def test_r15_missing_reference_cannot_certify_surjectivity():
    bridge, citing, target = _context()
    empty = RegistryBridgeResult(bridge.registry, bridge.records, ())
    result = prove_surjectivity_in_screened_context(
        MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3))),
        empty, citing_assertion_id=citing, proof_target=target,
    )
    assert result.status != "CERTIFIED"
    assert result.proof is None


def test_r15_actual_surjectivity_has_both_literature_ancestors():
    bridge, citing, target = _context()
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)))
    result = prove_surjectivity_in_screened_context(
        goal, bridge, citing_assertion_id=citing, proof_target=target,
    )
    assert result.status == "CERTIFIED", result.blocker
    assert result.proof.rule is ProofRule.INFERENCE
    assert proof_has_toda51_zero_ancestor(result.proof)


def test_r15_no_universal_source_no_zero_expansion():
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(4, 5))
    assert expand_cited_toda51_zero(target, ()) == ()
