"""R20R2: verified inference first-success and unchanged citation trust gates."""
from __future__ import annotations

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    SourceBoundGoal,
    reconstruct_registered_goal,
)
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _bridge(*, duplicate_direct: bool = False) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "reference", ReferenceKind.PROPOSITION, "Cited premise",
        source_id="synthetic", publication_position=1,
    ))
    registry.add_reference(LiteratureEntry(
        "target-reference", ReferenceKind.PROPOSITION, "Goal",
        source_id="synthetic", publication_position=2,
    ))
    registered = (
        ("a", "premise A"),
        ("b", "premise A" if duplicate_direct else "premise B"),
    )
    links = []
    for assertion_id, content in registered:
        registry.add_assertion(AssertionEntry(
            assertion_id, "reference", AssertionKind.STATEMENT, content,
            available_after_position=1,
        ))
        links.append(ProofStepLink(
            assertion_id, step=ProofStep(content, (), ProofRule.GIVEN),
        ))
    registry.add_assertion(AssertionEntry(
        "goal", "target-reference", AssertionKind.STATEMENT, "result",
    ))
    return RegistryBridgeResult(registry, (), tuple(links))


def _expansion(name: str, premise: str, *, conclusion: str = "result") -> GoalExpansion:
    rule = InferenceRule(
        name=name,
        premise_patterns=(PremisePattern(statement_type=str),),
        match_guard=lambda steps, bindings, expected=premise: (
            steps[0].conclusion == expected
        ),
        conclusion_builder=lambda steps, value=conclusion: value,
    )
    return GoalExpansion(rule, (premise,))


def test_first_independent_proof_wins_without_exploring_second():
    bridge = _bridge()
    events = []
    second = _expansion("second valid route", "premise B")
    first = _expansion("first valid route", "premise A")
    used_goals = []

    def provider(target):
        used_goals.append(target)
        if target == "result":
            return (first, second)
        return ()

    found = reconstruct_registered_goal(
        "result", bridge, "goal", provider,
        lookup_mode="typed_reference", progress_observer=lambda *args: events.append(args),
    )
    assert found.rule is ProofRule.INFERENCE
    assert found.inference_rule.name == "first valid route"
    assert found.premises[0].conclusion == "premise A"
    assert "premise B" not in used_goals
    assert [event[0] for event in events if event[1] == "result"] == ["proved"]


def test_bad_conclusion_is_not_accepted_and_second_route_succeeds():
    bridge = _bridge()
    first = _expansion("wrong conclusion", "premise A", conclusion="wrong")
    second = _expansion("correct conclusion", "premise B")
    result = reconstruct_registered_goal(
        "result", bridge, "goal",
        lambda target: (first, second) if target == "result" else (),
        lookup_mode="typed_reference",
    )
    assert result.inference_rule.name == "correct conclusion"
    assert result.premises[0].conclusion == "premise B"


def test_unsolved_subgoal_does_not_block_next_candidate():
    bridge = _bridge()
    missing = _expansion("unproved", "missing")
    valid = _expansion("proved", "premise B")
    result = reconstruct_registered_goal(
        "result", bridge, "goal",
        lambda target: (missing, valid) if target == "result" else (),
        lookup_mode="typed_reference",
    )
    assert result.inference_rule.name == "proved"


def test_cyclic_candidate_does_not_block_next_candidate():
    bridge = _bridge()
    cycle = GoalExpansion(_expansion("cycle", "result").rule, ("result",))
    valid = _expansion("acyclic", "premise A")
    result = reconstruct_registered_goal(
        "result", bridge, "goal",
        lambda target: (cycle, valid) if target == "result" else (),
        lookup_mode="typed_reference",
    )
    assert result.inference_rule.name == "acyclic"


def test_source_bound_goal_still_requires_exact_source_and_inference():
    bridge = _bridge()
    bound = SourceBoundGoal("result", "premise B")
    first = _expansion("wrong source", "premise A")
    second = _expansion("required source", "premise B")
    result = reconstruct_registered_goal(
        bound, bridge, "goal",
        lambda target: (first, second) if target == "result" else (),
        lookup_mode="typed_reference",
    )
    assert result.rule is ProofRule.INFERENCE
    assert result.inference_rule.name == "required source"
    assert result.premises[0].conclusion == "premise B"
    assert result.conclusion == "result"


def test_duplicate_eligible_direct_sources_still_fail_closed():
    bridge = _bridge(duplicate_direct=True)
    with pytest.raises(RegisteredGoalUnresolved, match="ambiguous registered direct references"):
        reconstruct_registered_goal(
            "premise A", bridge, "goal", lambda target: (),
            lookup_mode="typed_reference",
        )


def test_unique_eligible_direct_given_is_reused_without_new_proof():
    bridge = _bridge()
    step = next(link.step for link in bridge.proof_links if link.assertion_id == "a")
    result = reconstruct_registered_goal(
        "premise A", bridge, "goal", lambda target: (),
        lookup_mode="typed_reference",
    )
    assert result is step
    assert result.rule is ProofRule.GIVEN


def test_no_verified_candidate_is_still_unresolved():
    bridge = _bridge()
    with pytest.raises(RegisteredGoalUnresolved, match="found 0"):
        reconstruct_registered_goal(
            "unregistered result", bridge, "goal", lambda target: (),
            lookup_mode="typed_reference",
        )


def test_invalid_expansion_type_is_not_reclassified_as_success():
    bridge = _bridge()
    with pytest.raises(TypeError, match="invalid inference expansion"):
        reconstruct_registered_goal(
            "result", bridge, "goal",
            lambda target: (object(),) if target == "result" else (),
            lookup_mode="typed_reference",
        )


def test_completed_internal_proof_is_reused_as_before():
    from phase165_r52_r17_internal_dependency import CompletedInternalProof

    bridge = _bridge()
    given = next(link.step for link in bridge.proof_links if link.assertion_id == "a")
    internal_rule = InferenceRule(
        name="previously checked derived premise",
        premise_patterns=(PremisePattern(statement_type=str),),
        conclusion_builder=lambda premises: "internal conclusion",
    )
    internal_root = ProofStep(
        "internal conclusion", (given,), ProofRule.INFERENCE,
        inference_rule=internal_rule,
    )
    expansion = _expansion("use internal result", "internal conclusion")
    result = reconstruct_registered_goal(
        "result", bridge, "goal",
        lambda target: (expansion,) if target == "result" else (),
        lookup_mode="typed_reference",
        completed_internal_proofs=(CompletedInternalProof(internal_root),),
    )
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == (internal_root,)


def test_source_bound_cannot_shortcut_with_direct_given_for_conclusion():
    bridge = _bridge()
    given_result = ProofStep("result", (), ProofRule.GIVEN)
    augmented = RegistryBridgeResult(
        bridge.registry, bridge.records,
        bridge.proof_links + (ProofStepLink("goal", step=given_result),),
    )
    scoped = SourceBoundGoal("result", "premise B")
    only_valid = _expansion("bound inference", "premise B")
    result = reconstruct_registered_goal(
        scoped, augmented, "goal",
        lambda target: (only_valid,) if target == "result" else (),
        lookup_mode="typed_reference",
    )
    assert result.rule is ProofRule.INFERENCE
    assert result is not given_result
    assert result.premises[0].conclusion == "premise B"
