# R26 変更コード

変更対象：`phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 全体。既存 import は変更しない。新規モジュール：`phase165_r57_r26_generic_search_connection.py`（ファイル冒頭に追加）。新規関数：`build_generic_backward_expansion_provider()`、`merge_backward_expansions()`（新規モジュール内）。新規テストファイル：`test_phase165_r57_r26_generic_search_connection.py`、`test_phase165_r57_r26_integration.py`。

## `shared_expansion_provider()` 全体

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = (), *, proof_target=None, prior_conclusions: tuple = ()):
    """Build backward proposals from typed source witnesses and common rules."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    available = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            available.append(link.step.conclusion)

    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")

    from phase165_r57_r7_stable_expansion import (
        expand_registered_toda45_finite_cyclic_goal,
    )
    from phase165_r57_r8_eta_specialization import (
        expand_registered_eta_specialization,
    )

    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    from phase165_r57_r19_delta_image_backward import expand_registered_delta_image_goal
    from phase165_r57_r20_general_specialization import expand_cited_general_specialization
    from phase165_r57_r26_generic_search_connection import (
        build_generic_backward_expansion_provider,
        merge_backward_expansions,
    )

    generic_provider = build_generic_backward_expansion_provider()

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        options = []
        if (isinstance(goal, Relation)
                and goal.relation_type is RelationType.EQUALITY
                and isinstance(goal.rhs, FreeCyclicGroup)
                and isinstance(goal.lhs, TodaPrimaryGroup)):
            for image in available:
                if not isinstance(image, GeneratorImage):
                    continue
                if (getattr(image.map, "source_group", None) != goal.lhs
                        or image.source_generator != goal.rhs.generator):
                    continue
                options.append(GoalExpansion(
                    reverse_free_cyclic_transport_rule(),
                    (MapIsomorphism(image.map),
                     Relation(image.map.target_group,
                              FreeCyclicGroup(image.target_generator)),
                     image),
                ))
        options.extend(expand_registered_toda45_finite_cyclic_goal(goal, tuple(available) + prior_conclusions))
        options.extend(expand_registered_eta_specialization(goal, tuple(available)))
        options.extend(expand_registered_delta_image_goal(goal, tuple(available)))
        options.extend(expand_cited_general_specialization(goal, tuple(available)))
        for provider in (
            expand_generic_iso_goal,
            expand_generic_ehp_hopf_goal,
            expand_delta_zero_from_suspension_iso,
            expand_diagonal_suspension,
            expand_existing_pi43_rules,
            *extra_providers,
        ):
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        merged = merge_backward_expansions(tuple(options), generic_provider(goal))
        return retain_ordered_root_expansions(proof_target, goal, merged)
    return expand

```

## 新規モジュール全体

```python
"""R57-R26: connect R23/R24/R25 to the existing canonical backward search.

This adapter only emits typed GoalExpansion proposals. References and ProofSteps
remain exclusively under reconstruct_registered_goal's existing verification.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r24_candidate_discovery import discover_explicit_goal_candidates
from phase165_r57_r25_premise_generation import generate_discovered_premises
from phase165_r8_rule_provider import discover_inference_rules
from proof import InferenceRule


def build_generic_backward_expansion_provider(
    rules: tuple[InferenceRule, ...] | None = None,
):
    """Create an immutable goal-to-expansions provider from existing rule factories.

    The factory inventory is read once rather than once for each recursive goal.
    Only explicitly invertible conclusion and premise patterns can contribute.
    """
    if rules is None:
        rules, _ = discover_inference_rules()
    if not isinstance(rules, tuple) or any(
        not isinstance(rule, InferenceRule) for rule in rules
    ):
        raise TypeError("rules must be a tuple of InferenceRule")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        matches = discover_explicit_goal_candidates(rules, goal)
        results = generate_discovered_premises(matches)
        return tuple(result.expansion for result in results)

    return expand


def merge_backward_expansions(
    existing: tuple[GoalExpansion, ...],
    generic: tuple[GoalExpansion, ...],
) -> tuple[GoalExpansion, ...]:
    """Preserve existing provider order and suppress duplicate identical proposals.

    Different derivations stay distinct for the canonical ambiguity checker.
    """
    if not isinstance(existing, tuple) or not isinstance(generic, tuple):
        raise TypeError("expansions must be tuples")
    output: list[GoalExpansion] = []
    for expansion in existing + generic:
        if not isinstance(expansion, GoalExpansion):
            raise TypeError("expansions must contain GoalExpansion")
        if any(
            previous.rule is expansion.rule
            and previous.subgoals == expansion.subgoals
            for previous in output
        ):
            continue
        output.append(expansion)
    return tuple(output)

```

## テストファイル全体

```python
"""R26 focused tests; synthetic statements do not certify Toda mathematics."""
from dataclasses import dataclass

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r26_generic_search_connection import (
    build_generic_backward_expansion_provider,
    merge_backward_expansions,
)
from proof import InferenceRule, PatternVariable, PremisePattern


@dataclass(frozen=True)
class Claim:
    value: object


def test_r26_proposes_fully_bound_subgoals():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="synthetic",
        conclusion_pattern=Claim(x),
        premise_patterns=(PremisePattern(statement_pattern=Claim(x)),),
    )
    provider = build_generic_backward_expansion_provider((rule,))
    assert provider(Claim(7)) == (GoalExpansion(rule, (Claim(7),)),)


def test_r26_rejects_unbound_premise_variable():
    x, y = PatternVariable("x"), PatternVariable("y")
    rule = InferenceRule(
        name="unbound", conclusion_pattern=Claim(x),
        premise_patterns=(PremisePattern(statement_pattern=Claim(y)),),
    )
    assert build_generic_backward_expansion_provider((rule,))(Claim(2)) == ()


def test_r26_rejects_opaque_builder_only_rule():
    rule = InferenceRule(
        name="builder only", conclusion_builder=lambda premises: Claim(5),
        premise_patterns=(PremisePattern(statement_pattern=Claim(3)),),
    )
    assert build_generic_backward_expansion_provider((rule,))(Claim(5)) == ()


def test_r26_candidate_does_not_prove_a_claim():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="not a proof", conclusion_pattern=Claim(x),
        premise_patterns=(PremisePattern(statement_pattern=Claim(x)),),
    )
    expansion, = build_generic_backward_expansion_provider((rule,))(Claim(3))
    assert isinstance(expansion, GoalExpansion)
    assert not hasattr(expansion, "conclusion")


def test_r26_merger_suppresses_exact_duplicate_identity():
    rule = InferenceRule("reused")
    first = GoalExpansion(rule, (Claim(1),))
    assert merge_backward_expansions((first,), (first,)) == (first,)


def test_r26_merger_retains_distinct_derivations():
    a, b = InferenceRule("same name"), InferenceRule("same name")
    first = GoalExpansion(a, (Claim(1),))
    second = GoalExpansion(b, (Claim(1),))
    assert merge_backward_expansions((first,), (second,)) == (first, second)


def test_r26_invalid_input_rejected():
    with pytest.raises(TypeError):
        build_generic_backward_expansion_provider((object(),))
    with pytest.raises(TypeError):
        merge_backward_expansions([], ())

```

```python
"""R26 wiring checks: no new GIVEN or forged proof assertions."""
from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
import phase165_r52_r9_shared_math as shared
import phase165_r57_r26_generic_search_connection as generic
from proof import InferenceRule
from unified_statement_registry import UnifiedStatementRegistry


@dataclass(frozen=True)
class SyntheticGoal:
    value: int


def test_r26_shared_provider_emits_generic_proposals(monkeypatch):
    rule = InferenceRule("synthetic goal")
    calls = []

    def factory(rules=None):
        calls.append("build")
        return lambda goal: (GoalExpansion(rule, (SyntheticGoal(goal.value - 1),)),) if isinstance(goal, SyntheticGoal) else ()

    monkeypatch.setattr(generic, "build_generic_backward_expansion_provider", factory)
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    provider = shared.shared_expansion_provider(bridge)
    assert provider(SyntheticGoal(4)) == (GoalExpansion(rule, (SyntheticGoal(3),)),)
    assert calls == ["build"]


def test_r26_searcher_itself_is_unchanged():
    import inspect
    from phase165_r3_recursive_search import reconstruct_registered_goal
    source = inspect.getsource(reconstruct_registered_goal)
    assert "find_inference_matches_for_rule" in source
    assert "derive_inference_proof_step" in source
    assert "phase165_r57_r26" not in source

```
