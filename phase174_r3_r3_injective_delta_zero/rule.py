"""Generic EHP consequence: injective E and exact Delta-E window imply Delta=0.

The matched inputs must be two independently inferred ProofSteps. This module
adds no fixed statements, mathematical axioms, citation overrides, or public
search registrations. It does not assume any particular homotopy group.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement


def delta_e_injectivity_inputs(
    goal: object,
) -> tuple[MapInjective, TodaProp42ExactnessStatement] | None:
    """Build the unique consecutive Delta-E window for a typed zero-Delta goal.

    Do not treat the resulting goals as proofs. The EHP indices and source,
    middle and target dimensions are independently checked.
    """
    if not isinstance(goal, TodaDeltaZeroStatement):
        return None
    delta = goal.map
    if not isinstance(delta, TodaDeltaMap):
        return None
    source, middle = delta.source_group, delta.target_group
    if not isinstance(source, TodaPrimaryGroup) or not isinstance(middle, TodaPrimaryGroup):
        return None
    q, n = middle.group_dimension, middle.sphere_dimension
    if type(q) is not int or type(n) is not int or n < 1 or q < n:
        return None
    if source != TodaPrimaryGroup(q + 2, 2 * n + 1):
        return None
    if source.group_dimension < source.sphere_dimension:
        return None
    target = TodaPrimaryGroup(q + 1, n + 1)
    suspension = TodaSuspensionMap(middle, target)
    exactness = TodaProp42ExactnessStatement(
        TodaEHPExactnessWindow(
            source_term=source,
            middle_term=middle,
            target_term=target,
            first_map=EHP_DELTA_MAP,
            second_map=EHP_E_MAP,
        )
    )
    if prop42_exactness_indices(exactness) is None:
        return None
    return MapInjective(suspension), exactness


def delta_zero_from_injection_rule(goal: TodaDeltaZeroStatement) -> InferenceRule:
    """Require inferred E-injectivity and independently inferred EHP exactness."""
    requirements = delta_e_injectivity_inputs(goal)
    if requirements is None:
        raise ValueError("invalid typed Delta-E zero-map goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == requirements
            and delta_e_injectivity_inputs(goal) == requirements
        )

    return InferenceRule(
        name="EHP injective suspension and Delta-E exactness imply zero Delta",
        description=(
            "Exactness identifies im(Delta) with ker(E). A separately proved "
            "injective E has zero kernel, so Delta is the zero map."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaProp42ExactnessStatement,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_delta_zero_from_injection(goal: object) -> tuple[GoalExpansion, ...]:
    """Propose checked subgoals; never register or accept evidence by itself."""
    requirements = delta_e_injectivity_inputs(goal)
    if requirements is None:
        return ()
    return (GoalExpansion(delta_zero_from_injection_rule(goal), requirements),)
