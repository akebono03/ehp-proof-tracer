"""R4-R11: typed integrity checks for remaining Proposition 5.6 components.

This reads structured registry snapshots. It does not infer a citation,
change a renderer, or silently substitute group generators or range facts.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import GeneratorSymbol, HomotopyElement, ScalarProduct, ScalarSum, ScalarSymbol, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement


LOCATOR = "Proposition 5.6"
COMPONENT_KEYS = (
    "pi6_3_group_relation",
    "pi7_4_group_relation",
    "pi8_5_group_relation",
    "higher_nu_group_relation",
)


@dataclass(frozen=True)
class ComponentIntegrity:
    component_key: str
    generator: object
    order: object
    scope: str | None
    status: str


def _nu(element: object, *, index: int | None = None, prime: bool = False) -> bool:
    if not isinstance(element, HomotopyElement):
        return False
    symbol = element.generator
    if not isinstance(symbol, GeneratorSymbol) or symbol.family != "ν":
        return False
    if prime:
        return symbol.decoration == "′"
    return symbol.index == index and symbol.decoration is None


def _relation(snapshot: RegistryBridgeResult, key: str) -> Relation:
    if not isinstance(snapshot, RegistryBridgeResult):
        raise TypeError("snapshot must be RegistryBridgeResult")
    if key not in COMPONENT_KEYS:
        raise ValueError("Unsupported Proposition 5.6 component")
    assertion_id = f"boundary:{LOCATOR}:{key}"
    records = [record for record in snapshot.records if record.assertion_id == assertion_id]
    if len(records) != 1 or records[0].status is not MigrationStatus.STRUCTURED:
        raise ValueError(f"{key} must be uniquely STRUCTURED")
    conclusion = snapshot.registry.assertion(assertion_id).content
    if not isinstance(conclusion, Relation) or conclusion.relation_type is not RelationType.EQUALITY:
        raise ValueError("Expected typed equality Relation")
    return conclusion


def verify_prop56_remaining_component(
    snapshot: RegistryBridgeResult,
    component_key: str,
    *,
    higher_range: object | None = None,
) -> ComponentIntegrity:
    """Require exact structural generator data, not only abstract group order."""
    statement = _relation(snapshot, component_key)
    left, right = statement.lhs, statement.rhs
    if not isinstance(left, TodaPrimaryGroup):
        raise ValueError("Expected TodaPrimaryGroup")

    if component_key == "pi6_3_group_relation":
        if (left.group_dimension, left.sphere_dimension) != (6, 3):
            raise ValueError("Wrong pi6_3 group")
        if not isinstance(right, FiniteCyclicGroup) or right.order != 4 or not _nu(right.generator, prime=True):
            raise ValueError("pi6_3 order or nu-prime generator mismatch")
        return ComponentIntegrity(component_key, right.generator, 4, None, "GENERATOR_PRESERVED")

    if component_key == "pi7_4_group_relation":
        if (left.group_dimension, left.sphere_dimension) != (7, 4):
            raise ValueError("Wrong pi7_4 group")
        if not isinstance(right, DirectSumGroup) or len(right.summands) != 2:
            raise ValueError("pi7_4 must retain both direct summands")
        free, torsion = right.summands
        if not isinstance(free, FreeCyclicGroup) or not _nu(free.generator, index=4):
            raise ValueError("pi7_4 free generator mismatch")
        if (not isinstance(torsion, FiniteCyclicGroup) or torsion.order != 4
                or not isinstance(torsion.generator, Suspension)
                or not _nu(torsion.generator.expression, prime=True)):
            raise ValueError("pi7_4 torsion generator mismatch")
        return ComponentIntegrity(component_key, (free.generator, torsion.generator), (0, 4), None, "GENERATORS_PRESERVED")

    if component_key == "pi8_5_group_relation":
        if (left.group_dimension, left.sphere_dimension) != (8, 5):
            raise ValueError("Wrong pi8_5 group")
        if not isinstance(right, FiniteCyclicGroup) or right.order != 8 or not _nu(right.generator, index=5):
            raise ValueError("pi8_5 order or nu5 generator mismatch")
        return ComponentIntegrity(component_key, right.generator, 8, "n = 5", "GENERATOR_PRESERVED")

    if (not isinstance(left.sphere_dimension, ScalarSymbol)
            or left.sphere_dimension.name != "n"):
        raise ValueError("Higher group must retain symbolic n")
    n = left.sphere_dimension
    if left.group_dimension != ScalarSum(n, 3):
        raise ValueError("Higher group dimension must be n+3")
    if not isinstance(right, FiniteCyclicGroup) or right.order != 8:
        raise ValueError("Higher cyclic group must have order 8")
    if not _nu(right.generator, index=n):
        raise ValueError("Higher group must retain nu_n generator")
    if not isinstance(higher_range, ScalarGreaterEqualStatement) or higher_range.left != n or higher_range.right != 6:
        raise ValueError("Higher-group scope n >= 6 must be supplied and checked")
    assertion = snapshot.registry.assertion(f"boundary:{LOCATOR}:{component_key}")
    if assertion.scope != "n >= 6":
        raise ValueError("Higher-group registry scope must be n >= 6")
    return ComponentIntegrity(component_key, right.generator, 8, "n >= 6", "GENERATOR_AND_SCOPE_PRESERVED")
