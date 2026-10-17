"""General bridge between a certified cyclic-structure statement and a group relation.

The rule itself is not a certificate: its premise must be established independently.
No Toda group, generator, map, or literature premise is hard-coded here.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from proof import InferenceRule, PatternVariable, PremisePattern, Relation, RelationType


def finite_cyclic_structure_as_relation_inference_rule() -> InferenceRule:
    """Translate proved finite cyclic structure into the canonical group goal."""
    group = PatternVariable("group")
    generator = PatternVariable("generator")
    order = PatternVariable("order")
    return InferenceRule(
        name="finite cyclic structure gives group relation",
        description=(
            "If a group has a proven positive finite cyclic order and generator, "
            "identify it with the corresponding FiniteCyclicGroup."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=CyclicStructureStatement,
                statement_pattern=CyclicStructureStatement(group, generator, order),
            ),
        ),
        conclusion_pattern=Relation(
            lhs=group,
            rhs=FiniteCyclicGroup(order=order, generator=generator),
            relation_type=RelationType.EQUALITY,
        ),
    )
