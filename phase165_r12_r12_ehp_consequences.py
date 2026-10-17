"""Generic typed consequences of cited Proposition 4.2 exactness.

A cited general theorem is resolved by the existing R11 specialization provider.
This module does not introduce any GIVEN proof steps or target-specific facts.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class EHPImageEqualsKernelStatement:
    """The first map's image equals the second map's kernel in a window."""
    window: TodaEHPExactnessWindow


def ehp_image_equals_kernel_inference_rule() -> InferenceRule:
    """Infer im(first)=ker(second) from the matching typed exactness."""
    def guard(premises, bindings):
        exact = premises[0].conclusion
        return (
            isinstance(exact, TodaProp42ExactnessStatement)
            and prop42_exactness_indices(exact) is not None
        )

    def conclusion(premises):
        return EHPImageEqualsKernelStatement(premises[0].conclusion.window)

    return InferenceRule(
        name="EHP exactness implies image equals kernel",
        description="At consecutive maps in an exact sequence, Im(f) = Ker(g).",
        premise_patterns=(PremisePattern(statement_type=TodaProp42ExactnessStatement),),
        match_guard=guard,
        conclusion_builder=conclusion,
    )


def suspension_surjective_from_zero_target_inference_rule() -> InferenceRule:
    """Infer E surjectivity from E->H exactness and a proved zero H target."""
    def guard(premises, bindings):
        exact, zero = (item.conclusion for item in premises)
        if not isinstance(exact, TodaProp42ExactnessStatement):
            return False
        if not isinstance(zero, TodaPrimaryGroupZeroStatement):
            return False
        window = exact.window
        return (
            prop42_exactness_indices(exact) is not None
            and window.first_map == EHP_E_MAP
            and window.second_map == EHP_H_MAP
            and zero.group == window.target_term
        )

    def conclusion(premises):
        window = premises[0].conclusion.window
        return MapSurjective(TodaSuspensionMap(window.source_term, window.middle_term))

    return InferenceRule(
        name="EHP exactness and zero Hopf target imply suspension surjectivity",
        description="Exactness at B and a zero group C imply E:A->B is surjective.",
        premise_patterns=(
            PremisePattern(statement_type=TodaProp42ExactnessStatement),
            PremisePattern(statement_type=TodaPrimaryGroupZeroStatement),
        ),
        match_guard=guard,
        conclusion_builder=conclusion,
    )


def expand_ehp_exactness_consequences(goal: object) -> tuple[GoalExpansion, ...]:
    """Construct necessary exactness/zero subgoals; never invent proven leaves."""
    if isinstance(goal, EHPImageEqualsKernelStatement):
        exact = TodaProp42ExactnessStatement(goal.window)
        if prop42_exactness_indices(exact) is None:
            return ()
        return (GoalExpansion(
            ehp_image_equals_kernel_inference_rule(), (exact,),
        ),)
    if isinstance(goal, MapSurjective) and isinstance(goal.map, TodaSuspensionMap):
        source, middle = goal.map.source_group, goal.map.target_group
        if not isinstance(source, TodaPrimaryGroup) or not isinstance(middle, TodaPrimaryGroup):
            return ()
        n = source.sphere_dimension
        i = middle.group_dimension
        if type(n) is not int or type(i) is not int:
            return ()
        target = TodaPrimaryGroup(i, 2 * n + 1)
        window = TodaEHPExactnessWindow(
            source_term=source,
            middle_term=middle,
            target_term=target,
            first_map=EHP_E_MAP,
            second_map=EHP_H_MAP,
        )
        exact = TodaProp42ExactnessStatement(window)
        if prop42_exactness_indices(exact) is None:
            return ()
        return (GoalExpansion(
            suspension_surjective_from_zero_target_inference_rule(),
            (exact, TodaPrimaryGroupZeroStatement(target)),
        ),)
    return ()


def proof_has_general_prop42_ancestor(step: ProofStep) -> bool:
    """Check actual proof-tree ancestry rather than a textual reference label."""
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    seen: set[int] = set()

    def visit(node: ProofStep) -> bool:
        if id(node) in seen:
            return False
        seen.add(id(node))
        if (
            node.rule is ProofRule.GIVEN
            and isinstance(node.conclusion, TodaProp42GeneralExactnessStatement)
        ):
            return True
        return any(visit(parent) for parent in node.premises)

    return visit(step)
