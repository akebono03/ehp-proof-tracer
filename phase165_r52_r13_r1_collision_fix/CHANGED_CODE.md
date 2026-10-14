# Full replacement function (imports unchanged)

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
) -> ProofStep:
    """Derive a goal with optional read-only progress reporting.

    The observer receives ('proved', goal, step) only after an accepted unique
    derivation and ('unresolved', goal, None) for a failed search branch.
    Supplying no observer preserves the existing API and search semantics.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not callable(expansion_provider):
        raise TypeError("expansion_provider must be callable")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    if lookup_mode not in ("legacy", "typed_reference"):
        raise ValueError("unknown lookup mode")
    if progress_observer is not None and not callable(progress_observer):
        raise TypeError("progress_observer must be callable or None")
    bridge.registry.assertion(citing_assertion_id)
    active: list[object] = []
    solved: list[tuple[object, ProofStep]] = []

    def report(kind: str, target: object, step: ProofStep | None = None) -> None:
        if progress_observer is not None:
            progress_observer(kind, target, step)

    def resolve(target: object) -> ProofStep:
        for earlier, step in solved:
            if type(earlier) is type(target) and earlier == target:
                return step
        if any(type(earlier) is type(target) and earlier == target for earlier in active):
            report("unresolved", target)
            raise RegisteredGoalUnresolved("cyclic proof dependency")
        active.append(target)
        try:
            if lookup_mode == "typed_reference":
                options = list(_typed_reference_steps(bridge, target))
            else:
                candidates = find_eligible_goal_candidates(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                )
                options = [x.proof_step for x in candidates if x.proof_step is not None]
            # A uniquely registered fixed Reference is a complete proof leaf.
            # Do not count a second derivation of the same statement as ambiguity.
            # Multiple direct references remain ambiguous and are rejected below.
            if lookup_mode == "typed_reference" and len(options) == 1:
                step = options[0]
                solved.append((target, step))
                report("proved", target, step)
                return step
            expansions = expansion_provider(target)
            if not isinstance(expansions, tuple):
                raise TypeError("expansion provider must return a tuple")
            for expansion in expansions:
                if not isinstance(expansion, GoalExpansion):
                    raise TypeError("invalid inference expansion")
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
                    if type(step.conclusion) is type(target) and step.conclusion == target:
                        options.append(step)
            if len(options) != 1:
                report("unresolved", target)
                raise RegisteredGoalUnresolved(
                    f"expected one registered derivation for {target!r}, found {len(options)}"
                )
            step = options[0]
            solved.append((target, step))
            report("proved", target, step)
            return step
        finally:
            active.pop()

    return resolve(goal)
```

# New test module (all imports and full functions)

```python
"""R52-R13-R1 focused regression: direct fixed Reference vs derived route."""
from dataclasses import dataclass

import pytest

from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_r13_reference_registration import register_adopted_composite_reference
from phase165_r52_r12_component_bridge import expand_cited_given_components
from proof import ProofRule


@dataclass(frozen=True)
class SampleClaims:
    fact: int
    companion: str


def _bridge():
    return expand_cited_given_components(register_adopted_composite_reference(
        assertion_id='test:composite',
        locator='Proposition Test',
        source_id='adopted source',
        content=SampleClaims(17, 'another fact'),
    ))


def test_r13_r1_direct_registered_leaf_wins_without_expansion():
    bridge = _bridge()
    calls = []
    def expansion(target):
        calls.append(target)
        return ()
    step = reconstruct_registered_goal(
        17, bridge, 'test:composite', expansion,
        lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == 17
    assert calls == []


def test_r13_r1_other_registered_component_reusable():
    bridge = _bridge()
    step = reconstruct_registered_goal(
        'another fact', bridge, 'test:composite', lambda target: (),
        lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN


def test_r13_r1_unregistered_goal_keeps_expansion_path():
    bridge = _bridge()
    calls = []
    def expansion(target):
        calls.append(target)
        return ()
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            999, bridge, 'test:composite', expansion,
            lookup_mode='typed_reference',
        )
    assert calls == [999]


def test_r13_r1_real_prop51_pi32_is_direct_leaf():
    from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
    bridge = expand_cited_given_components(build_adopted_prop51_reference())
    parent = bridge.registry.assertion('toda:adopted:prop5.1:finite_dimensional')
    goal = parent.content.pi3_2_group_relation
    step = reconstruct_registered_goal(
        goal, bridge, parent.assertion_id,
        lambda target: (), lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == goal

```
