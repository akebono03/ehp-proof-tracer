"""R3H: cited early (5.3) text is a GIVEN, not an EHP inference."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3h_source_registry import (
    ASSERTION_ID,
    build_adopted_toda53_hopf_reference,
)
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaDeltaInjectiveStatement, TodaHopfInvariantSurjectiveStatement
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def _actual_context():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    assert len(goals) == 1
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    assert citing == "shared:0:boundary:Proposition 5.3:pi5_3_group_relation"
    contexts = []
    upper = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert len(contexts) == 1
    return bridge, contexts[0], target, citing, upper


def test_r3h_exact_source_registers_one_typed_given():
    source = discover_goal_search_inputs().bridge
    registered = build_adopted_toda53_hopf_reference(source)
    assert len(registered.proof_links) == 1
    assertion = registered.registry.assertion(ASSERTION_ID)
    reference = registered.registry.reference(assertion.reference_id)
    assert reference.reference_id == "toda:(5.3)"
    assert reference.locator == "(5.3)"
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert isinstance(assertion.content, Relation)
    assert assertion.content.relation_type is RelationType.EQUALITY
    link = registered.proof_links[0]
    assert link.assertion_id == ASSERTION_ID
    assert link.step is not None
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()
    assert link.step.conclusion == assertion.content


def test_r3h_source_missing_fails_closed():
    empty = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    with pytest.raises(ValueError, match="exactly one archived source"):
        build_adopted_toda53_hopf_reference(empty)
    with pytest.raises(TypeError, match="RegistryBridgeResult"):
        build_adopted_toda53_hopf_reference(None)


def test_r3h_actual_publication_position_is_prior():
    bridge, screened, _, citing, upper = _actual_context()
    source_id = "shared:8:" + ASSERTION_ID
    source_assertion = bridge.registry.assertion(source_id)
    source_reference = bridge.registry.reference(source_assertion.reference_id)
    assert source_reference.publication_position == 8100
    assert precedes_citing_assertion(bridge, source_id, citing)
    source_links = tuple(link for link in screened.proof_links if link.assertion_id == source_id)
    assert len(source_links) == 1
    assert source_links[0].step is not None
    assert source_links[0].step.rule is ProofRule.GIVEN
    assert upper.status is ProofSearchStatus.PARTIAL


def test_r3h_genuine_hopf_source_reconstructs_as_given():
    bridge, screened, goal, citing, _ = _actual_context()
    hopf = expand_registered_ehp_terminal_goal(
        TodaHopfInvariantSurjectiveStatement(
            TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
        ),
        tuple(link.step.conclusion for link in screened.proof_links
              if link.step is not None and link.step.rule is ProofRule.GIVEN),
    )
    assert len(hopf) == 1
    exact_relation = hopf[0].subgoals[0]
    provider = shared_expansion_provider(screened, proof_target=goal)
    step = reconstruct_registered_goal(
        exact_relation, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert step.conclusion == exact_relation
    assert step.rule is ProofRule.GIVEN
    assert step.premises == ()


def test_r3h_historical_terminal_requires_inference_even_after_citation():
    bridge, screened, target, _, upper = _actual_context()
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    hopf = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    delta = TodaDeltaInjectiveStatement(
        TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)),
    )
    h_options = expand_registered_ehp_terminal_goal(hopf, available)
    d_options = expand_registered_ehp_terminal_goal(delta, available)
    assert len(h_options) == len(d_options) == 1
    assert [p.proof_rule for p in h_options[0].rule.premise_patterns] == [
        ProofRule.INFERENCE, ProofRule.INFERENCE,
    ]
    assert [p.proof_rule for p in d_options[0].rule.premise_patterns] == [ProofRule.INFERENCE]
    assert upper.status is ProofSearchStatus.PARTIAL


def test_r3h_pi4_2_remains_complete():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
