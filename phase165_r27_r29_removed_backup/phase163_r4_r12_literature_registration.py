"""Phase 163 R4-R12: typed source-unverified registrations for Toda 5.1/5.3.

Uses existing aggregate statement values, not their proof ancestry. A typed
registration is not evidence that the printed literature has been checked.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import sys

from expression import Composition, HomotopyElement, MapApplication, Multiple, ScalarSum, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement
from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp51FiniteDimensionalStatement, TodaProp53FiniteDimensionalStatement
from unified_statement_registry import AssertionKind, UnifiedStatementRegistry

COMPONENTS = {
    "Proposition 5.1": (
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    ),
    "Proposition 5.3": (
        "pi4_2_group_relation", "pi5_3_group_relation",
        "pi6_4_group_relation", "higher_eta_squared_group_relation",
    ),
}
SCOPES = {"Proposition 5.1": 3, "Proposition 5.3": 5}


@dataclass(frozen=True)
class LiteratureComponentInput:
    locator: str
    component_key: str
    statement: object
    source_description: str
    scope_statement: object | None = None

    def __post_init__(self) -> None:
        if self.locator not in COMPONENTS or self.component_key not in COMPONENTS[self.locator]:
            raise ValueError("unrecognized literature component")
        if not isinstance(self.source_description, str) or not self.source_description.strip():
            raise ValueError("source_description is required")
        if self.statement is None:
            raise ValueError("statement is required")


@dataclass(frozen=True)
class LiteratureComponentEvidence:
    assertion_id: str
    source_description: str
    verification_status: str = "SOURCE_UNVERIFIED"
    proof_status: str = "PROOF_ANCESTRY_NOT_CHECKED"


@dataclass(frozen=True)
class LiteratureComponentRegistrationResult:
    snapshot: RegistryBridgeResult
    evidence: tuple[LiteratureComponentEvidence, ...]


def _eta(element: object, index: int | ScalarSymbol | ScalarSum) -> bool:
    return (
        isinstance(element, HomotopyElement)
        and element.generator is not None
        and element.generator.family == "η"
        and element.generator.index == index
    )


def _group_relation(value: object, k: int, n: int, order: int | None) -> None:
    if not isinstance(value, Relation) or value.relation_type is not RelationType.EQUALITY:
        raise ValueError("expected group equality Relation")
    if value.lhs != TodaPrimaryGroup(group_dimension=k, sphere_dimension=n):
        raise ValueError("wrong homotopy group")
    if order is None:
        if not isinstance(value.rhs, FreeCyclicGroup):
            raise ValueError("free cyclic group required")
    else:
        if not isinstance(value.rhs, FiniteCyclicGroup) or value.rhs.order != order:
            raise ValueError("wrong finite cyclic order")
    if value.rhs.generator is None:
        raise ValueError("generator is missing")


def _scope(value: object, minimum: int) -> ScalarSymbol:
    if not isinstance(value, ScalarGreaterEqualStatement):
        raise ValueError("typed higher-dimensional scope is required")
    if value.right != minimum or value.left != ScalarSymbol(name="n"):
        raise ValueError("higher-dimensional scope mismatch")
    return value.left


def _validate_component(item: LiteratureComponentInput) -> None:
    key = item.component_key
    statement = item.statement
    higher_key = COMPONENTS[item.locator][-1]
    if key == higher_key:
        n = _scope(item.scope_statement, SCOPES[item.locator])
        if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
            raise ValueError("higher group relation must be an equality")
        expected_offset = 1 if item.locator == "Proposition 5.1" else 2
        if statement.lhs != TodaPrimaryGroup(
            group_dimension=ScalarSum(left=n, right=expected_offset), sphere_dimension=n
        ):
            raise ValueError("higher group dimension mismatch")
        if not isinstance(statement.rhs, FiniteCyclicGroup) or statement.rhs.order != 2:
            raise ValueError("higher cyclic group must have order two")
        gen = statement.rhs.generator
        if item.locator == "Proposition 5.1":
            if not _eta(gen, n):
                raise ValueError("higher eta generator mismatch")
        else:
            if not isinstance(gen, Composition) or not _eta(gen.left, n):
                raise ValueError("higher eta-squared generator mismatch")
            if not _eta(gen.right, ScalarSum(left=n, right=1)):
                raise ValueError("higher eta-squared second factor mismatch")
        return
    if item.scope_statement is not None:
        raise ValueError("unexpected scope for concrete statement")
    if item.locator == "Proposition 5.1":
        if key == "pi3_2_group_relation":
            _group_relation(statement, 3, 2, None)
            if not _eta(statement.rhs.generator, 2):
                raise ValueError("pi3_2 generator must be eta2")
        elif key == "eta2_hopf_relation":
            if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
                raise ValueError("Hopf equality required")
            if not isinstance(statement.lhs, MapApplication) or statement.lhs.map != EHP_H_MAP:
                raise ValueError("Hopf map must be H")
            if not _eta(statement.lhs.expression, 2):
                raise ValueError("Hopf relation argument must be eta2")
            if statement.rhs is None:
                raise ValueError("Hopf value is missing")
        elif key == "delta_iota5_relation":
            if not isinstance(statement, TodaDeltaImageUpToSignStatement):
                raise ValueError("signed Delta-image statement required")
            if not isinstance(statement.positive_value, Multiple) or statement.positive_value.coefficient != 2:
                raise ValueError("Delta positive value must be twice a generator")
            if not _eta(statement.positive_value.expression, 2):
                raise ValueError("Delta image requires eta2")
    else:
        indices = {
            "pi4_2_group_relation": (4, 2),
            "pi5_3_group_relation": (5, 3),
            "pi6_4_group_relation": (6, 4),
        }
        k, n = indices[key]
        _group_relation(statement, k, n, 2)
        gen = statement.rhs.generator
        if not isinstance(gen, Composition) or not _eta(gen.left, n) or not _eta(gen.right, n + 1):
            raise ValueError("eta-square generator not preserved")


def register_prop51_prop53_literature_statements(
    base: RegistryBridgeResult,
    inputs: tuple[LiteratureComponentInput, ...],
) -> LiteratureComponentRegistrationResult:
    """Copy validated mathematical contents into a new metadata-bridge snapshot."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(inputs, tuple) or any(not isinstance(i, LiteratureComponentInput) for i in inputs):
        raise TypeError("inputs must be typed tuple")
    expected = {(locator, key) for locator, keys in COMPONENTS.items() for key in keys}
    keys = [(i.locator, i.component_key) for i in inputs]
    if len(keys) != len(expected) or set(keys) != expected:
        raise ValueError("exactly eight distinct 5.1/5.3 components required")
    lookup = {r.assertion_id: r for r in base.records}
    for item in inputs:
        assertion_id = f"boundary:{item.locator}:{item.component_key}"
        record = lookup.get(assertion_id)
        if record is None or record.source != "boundary" or record.status is not MigrationStatus.METADATA_ONLY:
            raise ValueError("target boundary must be metadata_only")
        _validate_component(item)
    replacements = {
        f"boundary:{item.locator}:{item.component_key}": item.statement
        for item in inputs
    }
    registry = UnifiedStatementRegistry()
    seen_references: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        assertion = base.registry.assertion(record.assertion_id)
        if assertion.reference_id not in seen_references:
            registry.add_reference(base.registry.reference(assertion.reference_id))
            seen_references.add(assertion.reference_id)
        if record.assertion_id in replacements:
            assertion = replace(assertion, kind=AssertionKind.STATEMENT, content=replacements[record.assertion_id])
        registry.add_assertion(assertion)
    records = tuple(
        replace(record, status=MigrationStatus.STRUCTURED,
                detail="Typed source-unverified candidate; no proof ancestry certification")
        if record.assertion_id in replacements else record
        for record in base.records
    )
    evidence = tuple(LiteratureComponentEvidence(
        assertion_id=f"boundary:{item.locator}:{item.component_key}",
        source_description=item.source_description,
    ) for item in inputs)
    return LiteratureComponentRegistrationResult(
        snapshot=RegistryBridgeResult(registry, records, base.proof_links),
        evidence=evidence,
    )


def existing_prop51_prop53_candidates() -> tuple[LiteratureComponentInput, ...]:
    """Use existing aggregate Statement objects, not their derivation ancestry."""
    tests_dir = Path(__file__).resolve().parent / "tests"
    if str(tests_dir) not in sys.path:
        sys.path.insert(0, str(tests_dir))
    from toda_prop56_zero_bootstrap import _build_prop51_step
    from test_phase59_prop53_integration import build_phase59_8_data

    prop51 = _build_prop51_step().conclusion
    prop53_fixture = build_phase59_8_data()
    prop53 = prop53_fixture["integration_step"].conclusion
    if not isinstance(prop51, TodaProp51FiniteDimensionalStatement):
        raise ValueError("unexpected Proposition 5.1 aggregate Statement")
    if not isinstance(prop53, TodaProp53FiniteDimensionalStatement):
        raise ValueError("unexpected Proposition 5.3 aggregate Statement")
    inputs: list[LiteratureComponentInput] = []
    for locator, aggregate in (("Proposition 5.1", prop51), ("Proposition 5.3", prop53)):
        for key in COMPONENTS[locator]:
            inputs.append(LiteratureComponentInput(
                locator=locator,
                component_key=key,
                statement=getattr(aggregate, key),
                source_description=f"Existing typed aggregate {type(aggregate).__name__}.{key}",
                scope_statement=(
                    prop53_fixture["higher_range_step"].conclusion
                    if locator == "Proposition 5.3"
                    else ScalarGreaterEqualStatement(left=ScalarSymbol(name="n"), right=3)
                ) if key == COMPONENTS[locator][-1] else None,
            ))
    return tuple(inputs)
