"""Scoped backward-search routes from R4-R8 inference rules, not completed steps.

This adapter is AUDIT_ONLY.  It never injects a previously inferred ProofStep
into search, never manufactures a GIVEN, and never alters shared production
providers.  Every expansion must be re-proved by the canonical search engine.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from proof import ProofRule, ProofStep


def walk_proof_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    """Visit each concrete proof node once; reject cycles and foreign rule kinds."""
    if not isinstance(root, ProofStep):
        raise TypeError("a real ProofStep root is required")
    visited: set[int] = set()
    active: set[int] = set()
    result: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("all premises must be ProofStep instances")
        identifier = id(step)
        if identifier in active:
            raise ValueError("cyclic proof dependency")
        if identifier in visited:
            return
        active.add(identifier)
        if step.rule is ProofRule.GIVEN:
            if step.premises:
                raise ValueError("GIVEN must be a leaf")
        elif step.rule is ProofRule.INFERENCE:
            if step.inference_rule is None or not step.premises:
                raise ValueError("inferred nodes require a rule and premises")
        else:
            raise ValueError("unverified ProofRule in ancestry")
        for parent in step.premises:
            visit(parent)
        active.remove(identifier)
        visited.add(identifier)
        result.append(step)

    visit(root)
    return tuple(result)


def inference_expansion_catalog(root: ProofStep) -> tuple[tuple[object, GoalExpansion], ...]:
    """Extract *only* rules and subgoal statements, never prior ProofSteps.

    Duplicate conclusions with different derivations are refused: silently
    selecting an arbitrary proof route would break the ambiguity boundary.
    """
    rows: list[tuple[object, GoalExpansion]] = []
    for step in walk_proof_ancestry(root):
        if step.rule is not ProofRule.INFERENCE:
            continue
        proposal = GoalExpansion(
            step.inference_rule,
            tuple(parent.conclusion for parent in step.premises),
        )
        earlier = [old for conclusion, old in rows
                   if type(conclusion) is type(step.conclusion)
                   and conclusion == step.conclusion]
        if earlier:
            if (len(earlier) != 1
                    or earlier[0].rule.name != proposal.rule.name
                    or earlier[0].subgoals != proposal.subgoals):
                raise ValueError("ambiguous inferred route for one typed goal")
            continue
        rows.append((step.conclusion, proposal))
    return tuple(rows)


def scoped_expansion_provider(
    root: ProofStep, fallback_provider,
):
    """Prioritize inferred R4-R8 obligations and retain ordinary fallback.

    This is a local experiment, NOT registration in the public provider.
    """
    if not callable(fallback_provider):
        raise TypeError("fallback_provider must be callable")
    catalog = inference_expansion_catalog(root)
    if not catalog or catalog[-1][0] != root.conclusion:
        raise ValueError("the root must be the last inferred goal")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        matches = tuple(route for conclusion, route in catalog
                        if type(conclusion) is type(goal) and conclusion == goal)
        if matches:
            if len(matches) != 1:
                raise ValueError("ambiguous scoped goal")
            return matches
        ordinary = fallback_provider(goal)
        if not isinstance(ordinary, tuple) or not all(
            isinstance(item, GoalExpansion) for item in ordinary
        ):
            raise TypeError("fallback provider returned invalid proposals")
        return ordinary

    return expand
