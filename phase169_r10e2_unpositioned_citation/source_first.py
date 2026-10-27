"""Screen independently positioned source assertions for a derived DB goal.

No claim about the DB goal's publication position is invented. A fixed source
must have independently recorded publication metadata and be supplied as a
screened proof link. The common solver still has to prove every inference.
"""
from __future__ import annotations

from dataclasses import is_dataclass, replace

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation
from unified_statement_registry import AssertionKind, AssertionOrigin, ProofStepLink


def _target_group(goal: object) -> object | None:
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        return goal.group
    if isinstance(goal, Relation):
        return goal.lhs
    return None


def screen_independent_sources_for_derived_goal(
    bridge: RegistryBridgeResult, *, goal: object,
) -> RegistryBridgeResult:
    """Screen positioned FIXED statements without inventing a target citation.

    A fixed claim at the same concrete group as the new target is excluded:
    that would assert the result rather than derive it. No file-based or DB
    group row is promoted into a proof premise. Original source links are
    retained when valid; the standard typed, positioned source-registration
    policy may construct a GIVEN for other fixed assertions as in the existing
    explicit-publication source screen.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("typed RegistryBridgeResult required")
    target_group = _target_group(goal)
    if target_group is None:
        raise ValueError("a typed group proof target is required")

    selected: list[ProofStepLink] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if assertion.kind not in (AssertionKind.STATEMENT, AssertionKind.DEFINITION):
            continue
        if not is_dataclass(assertion.content) or isinstance(assertion.content, type):
            continue
        if type(assertion.content).__name__ == "TodaFixedStatementComponent":
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None:
            continue
        if assertion.content == goal or _target_group(assertion.content) == target_group:
            continue
        duplicates = tuple(
            item for item in bridge.proof_links
            if item.assertion_id == assertion.assertion_id
        )
        if len(duplicates) > 1:
            continue
        if duplicates:
            step = duplicates[0].step
            if (not isinstance(step, ProofStep)
                    or step.rule is not ProofRule.GIVEN
                    or step.premises
                    or step.conclusion != assertion.content):
                continue
        else:
            step = ProofStep(assertion.content, (), ProofRule.GIVEN)
        if (step.inference_rule is None
                or step.inference_rule.literature_reference is None):
            if not isinstance(reference.locator, str) or not reference.locator:
                continue
            step = replace(
                step,
                inference_rule=InferenceRule(
                    name="Screened fixed source: " + reference.locator,
                    literature_reference=LiteratureReference(
                        label="Toda " + reference.locator,
                        locator=reference.locator,
                    ),
                ),
            )
        # Repeated references to the same typed mathematical fact should not
        # manufacture two competing GIVEN derivations of one subgoal. The
        # registry preserves the other references for provenance inspection.
        if any(
            old.step is not None
            and type(old.step.conclusion) is type(step.conclusion)
            and old.step.conclusion == step.conclusion
            for old in selected
        ):
            continue
        selected.append(ProofStepLink(assertion.assertion_id, step=step))
    return RegistryBridgeResult(bridge.registry, bridge.records, tuple(selected))


def uniquely_screened_prior_sources(
    bridge: RegistryBridgeResult, *, goal: object, source_n: int,
) -> tuple[object, ...]:
    """Find uniquely cited earlier group results, never unsigned DB rows.

    For a fixed source_n, competing nonidentical group structures are
    ambiguous, not alternatives the solver may select for convenience.
    """
    from phase169_r10e1_general_group_transport.transport import (
        _goal_group, generator_images_for_group_transport,
    )
    target = _goal_group(goal)
    if target is None or type(source_n) is not int:
        return ()
    k = target.group_dimension - target.sphere_dimension
    if (type(k) is not int or k < 0
            or source_n < k + 2 or source_n >= target.sphere_dimension):
        return ()
    expected_group_dimension = source_n + k
    matched: list[object] = []
    for link in bridge.proof_links:
        step = link.step
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or reference.publication_position is None
                or step.premises
                or step.conclusion != assertion.content):
            continue
        group = _goal_group(step.conclusion)
        if (group is None or group.sphere_dimension != source_n
                or group.group_dimension != expected_group_dimension):
            continue
        if generator_images_for_group_transport(step.conclusion, goal) is None:
            continue
        if not any(type(old) is type(step.conclusion)
                   and old == step.conclusion for old in matched):
            matched.append(step.conclusion)
    return tuple(matched) if len(matched) == 1 else ()
