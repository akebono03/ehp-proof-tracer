"""Source-first generic EHP zero-group inference, not yet production-wired.

If A --Delta--> B --E--> C --H--> D is exact at B and C,
Delta is surjective, and D=0, then C=0. Every premise must be
proved independently. This module creates no GIVEN and no proof leaf.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaProp42ExactnessStatement


RULE_NAME = "EHP exact Delta-E-H sequence with surjective Delta and zero H target"


def ehp_zero_inputs(
    goal: object,
) -> tuple[MapSurjective, TodaProp42ExactnessStatement,
           TodaProp42ExactnessStatement, TodaPrimaryGroupZeroStatement] | None:
    """Construct four independently provable premises from a typed target.

    The EHP indices are derived from the group, not enumerated stems or
    database assertions. A below-diagonal or nonconcrete target is rejected.
    """
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    target = goal.group
    if not isinstance(target, TodaPrimaryGroup):
        return None
    i = target.group_dimension
    sphere = target.sphere_dimension
    if (type(i) is not int or type(sphere) is not int or sphere < 2):
        return None
    n = sphere - 1
    if i < sphere:
        return None

    source = TodaPrimaryGroup(i + 1, 2 * n + 1)
    middle = TodaPrimaryGroup(i - 1, n)
    terminal = TodaPrimaryGroup(i, 2 * n + 1)
    first = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=source,
        middle_term=middle,
        target_term=target,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
    ))
    second = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=middle,
        middle_term=target,
        target_term=terminal,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))
    if (prop42_exactness_indices(first) != (n, i, "delta_e")
            or prop42_exactness_indices(second) != (n, i, "e_h")):
        return None
    return (
        MapSurjective(TodaDeltaMap(source, middle)),
        first,
        second,
        TodaPrimaryGroupZeroStatement(terminal),
    )


def ehp_zero_from_delta_surjectivity_rule(
    goal: TodaPrimaryGroupZeroStatement,
) -> InferenceRule:
    """Return a generic checked rule; no cited facts or GIVENs are made."""
    required = ehp_zero_inputs(goal)
    if required is None:
        raise ValueError("invalid EHP zero-group goal")

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and ehp_zero_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "Exactness gives im(Delta)=ker(E) and im(E)=ker(H). "
            "Surjectivity of Delta makes E the zero map. If the H "
            "codomain is zero, H is zero and E is surjective. Hence "
            "the middle EHP group is zero. All four premises require "
            "separate certified derivations; no target is a GIVEN."
        ),
        premise_patterns=(
            PremisePattern(statement_type=MapSurjective,
                           statement_pattern=required[0],
                           proof_rule=ProofRule.INFERENCE),
            PremisePattern(statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1],
                           proof_rule=ProofRule.INFERENCE),
            PremisePattern(statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[2],
                           proof_rule=ProofRule.INFERENCE),
            PremisePattern(statement_type=TodaPrimaryGroupZeroStatement,
                           statement_pattern=required[3],
                           proof_rule=ProofRule.INFERENCE),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_ehp_zero_from_delta_surjectivity(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Propose one generic backward branch, not a verified ProofStep."""
    required = ehp_zero_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(
        rule=ehp_zero_from_delta_surjectivity_rule(goal),
        subgoals=required,
    ),)
