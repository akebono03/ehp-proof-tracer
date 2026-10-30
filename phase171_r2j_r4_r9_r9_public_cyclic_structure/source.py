"""Source-screened finite cyclic structure from independently proved orders.

Only proof obligations are proposed. The named element is identified through
an earlier screened typed double relation, not through a database group answer.
The existing order-four root proposer supplies the identical, checked pair of
subgoals; this stage does not attempt to prove either premise.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase171_r2j_r4_r8_cyclic_structure.source import cyclic_group_from_generator_order
from phase171_r2j_r4_r9_r7_public_cyclic_root.source import expand_cited_double_cyclic_root
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def finite_cyclic_structure_from_full_order_rule(
    goal: CyclicStructureStatement,
) -> InferenceRule:
    """Infer the cyclic structure if an element has the full group order.

    ProofStep premises must both be INFERENCE; a database row, a nominal
    source relation, or an unproved requested group cannot discharge either.
    """
    if (
        not isinstance(goal, CyclicStructureStatement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or type(goal.order) is not int
        or goal.order < 2
    ):
        raise ValueError("a positive finite cyclic-structure goal is required")
    requested = Relation(
        goal.group,
        FiniteCyclicGroup(goal.order, goal.generator),
        RelationType.EQUALITY,
    )

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and cyclic_group_from_generator_order(
                premises[0].conclusion,
                premises[1].conclusion,
                requested=requested,
            ) == requested
        )

    return InferenceRule(
        name="proved finite cardinality and full element order imply cyclic structure",
        description=(
            "A finite group of order m with an element of order m is cyclic; "
            "the generator is checked against the typed registered identity."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=FiniteGroupCardinality,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=FiniteElementOrder,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_full_order_cyclic_structure(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Reuse R7's checked source-witness candidate, without importing proof.

    This phase supports only the order-four source shape that R7 already
    exposes, while the mathematical InferenceRule works for any order >= 2.
    Future generic order inference must be independently established.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be screened fixed statements in a tuple")
    if (
        not isinstance(goal, CyclicStructureStatement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or type(goal.order) is not int
        or goal.order < 2
    ):
        return ()
    requested = Relation(
        goal.group,
        FiniteCyclicGroup(goal.order, goal.generator),
        RelationType.EQUALITY,
    )
    routes = expand_cited_double_cyclic_root(requested, available)
    if len(routes) != 1 or len(routes[0].subgoals) != 2:
        return ()
    cardinality, element_order = routes[0].subgoals
    if cyclic_group_from_generator_order(
        cardinality, element_order, requested=requested,
    ) != requested:
        return ()
    return (GoalExpansion(
        finite_cyclic_structure_from_full_order_rule(goal),
        (cardinality, element_order),
    ),)
