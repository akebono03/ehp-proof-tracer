"""Phase 165 R14-R5: reuse existing EHP goal expansions without inventing evidence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from phase165_r3_recursive_search import GoalExpansion
from phase161_r3_backward_goal_schema import expand_phase161_r3_goal


def adapt_registered_goal_expansion(
    goal: object,
    legacy_expander: Callable[[object], object | None],
) -> tuple[GoalExpansion, ...]:
    """Convert existing typed expansion contract to the common R3 contract.

    This is a structure adapter, not a citation or proof certification.
    """
    found = legacy_expander(goal)
    if found is None:
        return ()
    if type(found.goal) is not type(goal) or found.goal != goal:
        raise ValueError("EHP expansion goal mismatch")
    if not isinstance(found.subgoals, tuple):
        raise TypeError("EHP subgoals must be a tuple")
    if found.inference_rule is None:
        raise ValueError("EHP rule missing")
    return (GoalExpansion(found.inference_rule, found.subgoals),)


def expand_registered_ehp_goal(goal: object) -> tuple[GoalExpansion, ...]:
    """Common provider for existing EHP rules; no group-specific proof replay."""
    return adapt_registered_goal_expansion(goal, expand_phase161_r3_goal)


def expand_registered_ehp_terminal_goal(
    goal: object, screened_claims: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Expose only the existing n=3 terminal rules and their unproved premises.

    screened_claims must come from the common provider's citation-screened
    FIXED_STATEMENT GIVEN context. A cited composite is used to bind the exact
    target subgoal; the historical rule still insists on an INFERENCE step.
    No conclusion, ProofStep or GIVEN is created here.
    """
    if not isinstance(screened_claims, tuple):
        raise TypeError("screened_claims must be a tuple")

    from phase161_r4_literature_premise_matching import expand_phase161_r4_literature_goal
    from toda_rules import (
        TodaDeltaInjectiveStatement,
        TodaHopfInvariantSurjectiveStatement,
        TodaProp51FiniteDimensionalStatement,
    )

    plan = expand_phase161_r4_literature_goal(goal)
    if plan is None:
        return ()
    claims = tuple(
        claim for claim in screened_claims
        if isinstance(claim, TodaProp51FiniteDimensionalStatement)
    )
    if len(claims) != 1:
        return ()
    proposition = claims[0]

    if isinstance(goal, TodaDeltaInjectiveStatement):
        # The historical rule demands a separately derived INFERENCE,
        # rather than accepting the screened literature GIVEN itself.
        return (GoalExpansion(plan.inference_rule, (proposition,)),)

    if isinstance(goal, TodaHopfInvariantSurjectiveStatement):
        # This exact mathematical prerequisite is dictated by the already
        # registered n=3 historical rule. It is a GOAL, not an assertion.
        from expression import GeneratorSymbol, HomotopyElement, MapApplication
        from map_facts import EHP_H_MAP
        from proof import Relation, RelationType

        nu_prime = HomotopyElement(
            name="ν′", dimension=3, source=6, target=3,
            generator=GeneratorSymbol(family="ν", decoration="′"),
        )
        eta5 = HomotopyElement(
            name="η₅", dimension=5, source=6, target=5,
            generator=GeneratorSymbol(family="η", index=5),
        )
        required_relation = Relation(
            lhs=MapApplication(map=EHP_H_MAP, expression=nu_prime),
            rhs=eta5,
            relation_type=RelationType.EQUALITY,
        )
        return (GoalExpansion(
            plan.inference_rule, (required_relation, proposition),
        ),)
    return ()


def expand_cited_ehp_terminal_goal(
    goal: object, screened_claims: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Derive the existing n=3 EHP conclusions from exact cited GIVENs.

    The legacy rule remains untouched. Its mathematical guard and conclusion
    builder are reused with explicitly cited proof leaves as premises; only
    its historical requirement that the leaves be INFERENCE is specialized.
    The shared caller supplies citation-screened, fixed-statement GIVEN values.
    No proof leaf, conclusion, or mathematical fact is manufactured here.
    """
    from dataclasses import replace
    from proof import ProofRule

    if not isinstance(screened_claims, tuple):
        raise TypeError("screened_claims must be a tuple")
    proposals = expand_registered_ehp_terminal_goal(goal, screened_claims)
    if len(proposals) != 1:
        return ()
    proposal = proposals[0]
    original = proposal.rule
    patterns = original.premise_patterns
    if len(patterns) != len(proposal.subgoals) or not all(
        pattern.proof_rule is ProofRule.INFERENCE for pattern in patterns
    ):
        raise RuntimeError("historical EHP premise contract changed")
    if original.match_guard is None or original.conclusion_builder is None:
        raise RuntimeError("historical EHP rule has no mathematical contract")
    # Exactly one cited typed GIVEN must match *each* mathematical prerequisite.
    # A mere registered assertion without a screened proof link is insufficient.
    for prerequisite in proposal.subgoals:
        if sum(
            type(source) is type(prerequisite) and source == prerequisite
            for source in screened_claims
        ) != 1:
            return ()
    cited_rule = replace(
        original,
        name="cited prior sources: " + original.name,
        premise_patterns=tuple(
            replace(pattern, proof_rule=ProofRule.GIVEN)
            for pattern in patterns
        ),
    )
    return (GoalExpansion(cited_rule, proposal.subgoals),)


def audit_ehp_connection(goal: object, bridge) -> dict:
    """Report precisely whether a typed group goal has an expansion.

    This intentionally does not call the registered prover with a made-up
    citing assertion or approved literature ids.
    """
    options = expand_registered_ehp_goal(goal)
    matches = tuple(
        entry for entry in bridge.registry._assertions.values()
        if type(entry.content) is type(goal) and entry.content == goal
    )
    return {
        "phase": "165 R14-R5",
        "goal": repr(goal),
        "available_root_expansions": len(options),
        "registered_exact_goal_matches": len(matches),
        "registered_typed_leaf_certified": False,
        "proof_steps_created": 0,
        "legacy_proof_used": False,
        "status": (
            "ROOT_RULE_CATALOG_MISSING"
            if not options else "EHP_EXPANSIONS_AVAILABLE_NOT_CERTIFIED"
        ),
        "next_dependency": (
            "Find general, typed group-structure/iso derivation rule for this goal"
            if not options else "Verify and link all registered premise assertions"
        ),
        "full_pytest_run": False,
    }
