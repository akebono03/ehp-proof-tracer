"""Phase 163 R4-R10: verify generator preservation in a typed fixed statement.

Read-only inspection of a registry snapshot; no renderer or proof changes.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation, RelationType


ASSERTION_ID = "boundary:Proposition 5.6:pi5_2_group_relation"
CANONICAL_LATEX = r"\pi_5^2=\mathbb{Z}/2\{\eta_2^3\}"


@dataclass(frozen=True)
class GeneratorIntegrityResult:
    assertion_id: str
    group_dimension: int
    sphere_dimension: int
    order: int
    generator: object
    canonical_latex: str
    status: str


def _eta_index(value: object, index: int) -> bool:
    return (
        isinstance(value, HomotopyElement)
        and isinstance(value.generator, GeneratorSymbol)
        and value.generator.family == "η"
        and value.generator.index == index
    )


def verify_prop56_pi5_2_generator(
    snapshot: RegistryBridgeResult,
) -> GeneratorIntegrityResult:
    """Fail closed unless the registered content includes the expected generator.

    The exact typed composite is checked: eta_2 o (eta_3 o eta_4).
    The mathematical notation eta_2^3 is a *display alias*, not a rewrite
    of the underlying Composition expression.
    """
    if not isinstance(snapshot, RegistryBridgeResult):
        raise TypeError("snapshot must be RegistryBridgeResult")
    records = tuple(r for r in snapshot.records if r.assertion_id == ASSERTION_ID)
    if len(records) != 1 or records[0].status is not MigrationStatus.STRUCTURED:
        raise ValueError("Proposition 5.6 pi5_2 must be uniquely STRUCTURED")
    statement = snapshot.registry.assertion(ASSERTION_ID).content
    if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
        raise ValueError("Registered content must be an equality Relation")
    group, cyclic = statement.lhs, statement.rhs
    if not isinstance(group, TodaPrimaryGroup) or (group.group_dimension, group.sphere_dimension) != (5, 2):
        raise ValueError("Unexpected source homotopy group")
    if not isinstance(cyclic, FiniteCyclicGroup) or cyclic.order != 2:
        raise ValueError("Expected a cyclic group of order two")
    generator = cyclic.generator
    if not (
        isinstance(generator, Composition)
        and _eta_index(generator.left, 2)
        and isinstance(generator.right, Composition)
        and _eta_index(generator.right.left, 3)
        and _eta_index(generator.right.right, 4)
    ):
        raise ValueError("Generator is missing or is not eta_2 o eta_3 o eta_4")
    return GeneratorIntegrityResult(
        assertion_id=ASSERTION_ID,
        group_dimension=5,
        sphere_dimension=2,
        order=2,
        generator=generator,
        canonical_latex=CANONICAL_LATEX,
        status="GENERATOR_PRESERVED",
    )
