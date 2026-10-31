# R20R2 変更コード全文

## 探索器：`reconstruct_registered_goal()` 全文

```python
def reconstruct_registered_goal(
    goal: object,
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
    expansion_provider: Callable[[object], tuple[GoalExpansion, ...]],
    *,
    verified_assertion_ids: tuple[str, ...] = (),
    lookup_mode: str = "legacy",
    progress_observer: Callable[[str, object, ProofStep | None], None] | None = None,
    completed_internal_proofs: tuple = (),
) -> ProofStep:
    """Return the first completed, checked proof in deterministic proposal order.

    Existing citation gates and scoped obligations are unchanged. Distinct
    eligible direct reference links remain ambiguous and fail closed.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not callable(expansion_provider):
        raise TypeError("expansion_provider must be callable")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    if lookup_mode not in ("legacy", "typed_reference", "typed_reference_ordered", "typed_reference_publication"):
        raise ValueError("unknown lookup mode")
    if progress_observer is not None and not callable(progress_observer):
        raise TypeError("progress_observer must be callable or None")
    bridge.registry.assertion(citing_assertion_id)
    active: list[object] = []
    solved: list[tuple[object, ProofStep]] = []

    def report(kind: str, target: object, step: ProofStep | None = None) -> None:
        if progress_observer is not None:
            progress_observer(kind, target, step)

    def accept(target: object, step: ProofStep) -> ProofStep:
        solved.append((target, step))
        report("proved", target, step)
        return step

    def resolve(target: object) -> ProofStep:
        for earlier, step in solved:
            if type(earlier) is type(target) and earlier == target:
                return step
        if any(type(earlier) is type(target) and earlier == target for earlier in active):
            report("unresolved", target)
            raise RegisteredGoalUnresolved("cyclic proof dependency")
        active.append(target)
        try:
            bound = isinstance(target, SourceBoundGoal)
            actual = target.conclusion if bound else target
            if bound:
                # A scoped obligation MUST derive its conclusion by inference
                # using the cited source. Never reuse a direct GIVEN or alias.
                options = []
            elif lookup_mode == "typed_reference_publication":
                from phase166_r3c_publication_order import precedes_citing_assertion
                options = []
                for assertion in bridge.registry._assertions.values():
                    if not precedes_citing_assertion(bridge, assertion.assertion_id, citing_assertion_id):
                        continue
                    if type(assertion.content) is not type(target) or assertion.content != target:
                        continue
                    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id)
                    if len(links) != 1 or links[0].step is None:
                        continue
                    step = links[0].step
                    if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                            or type(step.conclusion) is not type(target) or step.conclusion != target):
                        raise ValueError("ordered reference has inconsistent ProofStep")
                    options.append(step)
            elif lookup_mode == "typed_reference_ordered":
                from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps
                options = list(ordered_typed_reference_steps(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                ))
            elif lookup_mode == "typed_reference":
                options = list(_typed_reference_steps(bridge, target))
            else:
                candidates = find_eligible_goal_candidates(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                )
                options = [x.proof_step for x in candidates if x.proof_step is not None]
            # R10E4: earlier DB results may be adopted premises; do not
            # manufacture a Toda citation from a database result.
            if (not bound and not options and lookup_mode in
                    ("typed_reference", "typed_reference_ordered", "typed_reference_publication")):
                from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step
                db_step = admitted_db_step(actual, proof_target=goal, bridge=bridge)
                if db_step is not None:
                    options.append(db_step)
            # Multiple direct source links are a citation ambiguity, not
            # multiple inference proofs. Keep that separate gate fail-closed.
            if len(options) > 1:
                report("unresolved", target)
                raise RegisteredGoalUnresolved(
                    f"ambiguous registered direct references for {target!r}, found {len(options)}"
                )
            if (not bound and lookup_mode in
                    ("typed_reference", "typed_reference_ordered", "typed_reference_publication")
                    and options):
                return accept(target, options[0])
            if not bound and lookup_mode == "typed_reference_publication" and not options:
                from phase169_r3n_prior_result_alias import resolve_prior_result_alias_step
                alias_step = resolve_prior_result_alias_step(
                    target, bridge, citing_assertion_id,
                )
                if alias_step is not None:
                    for prior_step in alias_step.premises:
                        report("proved", prior_step.conclusion, prior_step)
                    return accept(target, alias_step)
            if not bound and completed_internal_proofs:
                from phase165_r52_r17_internal_dependency import find_reusable_internal_proof
                internal = find_reusable_internal_proof(target, goal, completed_internal_proofs)
                if internal is not None:
                    return accept(target, internal)
            if not bound and options:
                return accept(target, options[0])
            expansions = expansion_provider(actual)
            if not isinstance(expansions, tuple):
                raise TypeError("expansion provider must return a tuple")
            for expansion in expansions:
                if not isinstance(expansion, GoalExpansion):
                    raise TypeError("invalid inference expansion")
                if bound and expansion.subgoals != (target.source,):
                    continue
                try:
                    premises = tuple(resolve(child) for child in expansion.subgoals)
                except RegisteredGoalUnresolved:
                    continue
                matches = tuple(
                    match for match in find_inference_matches_for_rule(expansion.rule, premises)
                    if len(match.premises) == len(premises)
                    and all(a is b for a, b in zip(match.premises, premises))
                )
                for match in matches:
                    step = derive_inference_proof_step(match)
                    if type(step.conclusion) is type(actual) and step.conclusion == actual:
                        # Keep the existing certified-derivation entry point.
                        # The list is empty here; the first accepted proof wins.
                        append_unique_verified_derivation(options, step)
                        return accept(target, options[0])
            report("unresolved", target)
            raise RegisteredGoalUnresolved(
                f"expected a verified registered derivation for {target!r}, found 0"
            )
        finally:
            active.pop()

    return resolve(goal)
```

## 関連クラス全文

```python
class RegisteredGoalUnresolved(ValueError):
    """The requested proof is not established under the active search gates."""


@dataclass(frozen=True)
class SourceBoundGoal:
    """Require an inferred conclusion derived from this specific cited source.

    This is a search obligation, not a mathematical assertion or a GIVEN leaf.
    The returned ProofStep has the ordinary conclusion type, not this wrapper.
    """
    conclusion: object
    source: object
```

## テスト：import・補助関数・テスト関数全文

```python
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
```
