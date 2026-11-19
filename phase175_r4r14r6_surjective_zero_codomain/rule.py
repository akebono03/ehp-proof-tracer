"""Derive a zero codomain from a proved surjection with zero image.

This mathematical rule is independent of the Toda (5.9) source and of
any particular (n, k). The backward candidate uses the canonical E map
ending in a typed Toda zero-group goal; both premises must be proved.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = "surjective suspension with zero image has zero codomain"


def surjective_zero_codomain_inputs(
    goal: object,
) -> tuple[MapSurjective, ImageZeroStatement] | None:
    """Choose only a well-typed canonical suspension into the target group."""
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    target = goal.group
    if not isinstance(target, TodaPrimaryGroup):
        return None
    q, n = target.group_dimension, target.sphere_dimension
    if (type(q) is not int or type(n) is not int
            or n < 3 or q < n):
        return None
    source = TodaPrimaryGroup(q - 1, n - 1)
    mapping = TodaSuspensionMap(source, target)
    return MapSurjective(mapping), ImageZeroStatement(mapping)


def surjective_zero_codomain_rule(
    goal: TodaPrimaryGroupZeroStatement,
) -> InferenceRule:
    """Require independently inferred surjectivity and zero-image proofs."""
    required = surjective_zero_codomain_inputs(goal)
    if required is None:
        raise ValueError("a typed suspension zero-codomain goal is required")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and surjective_zero_codomain_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If a proved surjective homomorphism E:A->B has proved image zero, "
            "then B=im(E)=0. The map properties are separate inferred premises."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=MapSurjective,
                statement_pattern=required[0],
                proof_rule=ProofRule.INFERENCE,
            ),
            PremisePattern(
                statement_type=ImageZeroStatement,
                statement_pattern=required[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_surjective_zero_codomain(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Supply one unproved root branch, without making any source leaf."""
    required = surjective_zero_codomain_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(surjective_zero_codomain_rule(goal), required),)
