"""Generic EHP: im(E)=0 and exactness at B imply ker(H)=0.

The mathematical inference is independent of any specific n, k or generator.
No source fact, ProofStep, GIVEN or production search registration is created.
The zero-image premise is intentionally left as a separate proof obligation.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from map_property_rules import ImageZeroStatement
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaProp42ExactnessStatement


RULE_NAME = "EHP exact E-H window and zero suspension image imply Hopf injectivity"


def hopf_injectivity_from_zero_image_inputs(
    goal: object,
) -> tuple[ImageZeroStatement, TodaProp42ExactnessStatement] | None:
    """Derive a type-checked, dimensionally valid pair of independent goals."""
    if not isinstance(goal, MapInjective):
        return None
    hopf = goal.map
    if not isinstance(hopf, TodaHopfInvariantMap):
        return None
    middle = hopf.source_group
    target = hopf.target_group
    if not isinstance(middle, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    q = middle.group_dimension
    sphere = middle.sphere_dimension
    if (type(q) is not int or type(sphere) is not int
            or sphere < 2 or q < sphere
            or target != TodaPrimaryGroup(q, 2 * sphere - 1)):
        return None
    preceding = TodaPrimaryGroup(q - 1, sphere - 1)
    e = TodaSuspensionMap(preceding, middle)
    exactness = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=preceding,
        middle_term=middle,
        target_term=target,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))
    if prop42_exactness_indices(exactness) != (sphere - 1, q, "e_h"):
        return None
    return ImageZeroStatement(e), exactness


def hopf_injective_from_zero_image_rule(goal: MapInjective) -> InferenceRule:
    """Construct a general rule requiring two independently proved premises."""
    required = hopf_injectivity_from_zero_image_inputs(goal)
    if required is None:
        raise ValueError("invalid typed EHP Hopf-injectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and hopf_injectivity_from_zero_image_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "By EHP exactness, im(E)=ker(H). If the suspension image "
            "is independently proved zero, then ker(H)=0, so H is "
            "injective. A zero preceding group is not required."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=ImageZeroStatement,
                statement_pattern=required[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaProp42ExactnessStatement,
                statement_pattern=required[1],
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_hopf_injective_from_zero_image(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Return one unproved backward branch; do not create proof leaves."""
    required = hopf_injectivity_from_zero_image_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(
        rule=hopf_injective_from_zero_image_rule(goal),
        subgoals=required,
    ),)
