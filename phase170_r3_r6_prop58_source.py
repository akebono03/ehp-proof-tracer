"""Source-checked typed adoption of Toda Proposition 5.8's pi_7^3 clause.

The registered result is a cited literature statement, not a result derived
from sphere.csv or a previously saved proof. Its exact printed clause must
agree with the structural generator representation before the assertion can
be used as an independently positioned GIVEN.
"""
from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from pathlib import Path

from expression import Composition
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from phase166_r3aj_structured_generator import (
    database_structured_group_goal_candidates,
    structured_generator_from_ids,
)
from proof import Relation, RelationType
from unified_statement_registry import AssertionKind, AssertionOrigin, UnifiedStatementRegistry


SOURCE_ID = "toda:tex:ch5:0016"
SOURCE_DIGEST = "4e41470cead5382bc042b39634ae4bbc9bc184cda06801ddafa1331be6f0d124"
COMPONENT_ID = "boundary:Proposition 5.8:pi7_3_group_relation"
SOURCE_CLAUSE = r"\(\pi^{3}_{7}=\mathbb Z_2\gen{\nu'\circ\eta_6},\)"


def _source_checked_pi73_relation(base: RegistryBridgeResult) -> Relation:
    """Match exactly one archived TeX clause with the typed HyoujiGen factors."""
    archives = tuple(
        assertion for assertion in base.registry._assertions.values()
        if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(assertion.content, dict)
        and assertion.content.get("source_statement_id") == SOURCE_ID
    )
    if len(archives) != 1:
        raise ValueError("unique archived Proposition 5.8 source required")
    archive = archives[0].content
    text = archive.get("source_text")
    if (not isinstance(text, str)
            or archive.get("source_sha256") != SOURCE_DIGEST
            or sha256(text.encode("utf-8")).hexdigest() != SOURCE_DIGEST
            or r"\begin{proposition}\label{prop:5.8}" not in text
            or text.count(SOURCE_CLAUSE) != 1
            or r"\end{proposition}" not in text):
        raise ValueError("Proposition 5.8 pi_7^3 printed source not verified")

    relations = database_structured_group_goal_candidates(n=3, k=4)
    if len(relations) != 1:
        raise ValueError("unique typed pi_7^3 presentation unavailable")
    relation = relations[0]
    if (not isinstance(relation, Relation)
            or relation.relation_type is not RelationType.EQUALITY
            or relation.lhs != TodaPrimaryGroup(7, 3)
            or not isinstance(relation.rhs, FiniteCyclicGroup)
            or relation.rhs.order != 2
            or not isinstance(relation.rhs.generator, Composition)):
        raise ValueError("pi_7^3 group presentation disagrees with source")
    expected_generator = structured_generator_from_ids(
        ids=(3, 2), start_dimension=3,
        generator_csv=Path(__file__).resolve().with_name("data") / "HyoujiGen.csv",
    )
    if expected_generator is None or relation.rhs.generator != expected_generator:
        raise ValueError("pi_7^3 generator differs from the printed nu-prime eta6")
    return relation


def register_source_checked_prop58_pi73(base: RegistryBridgeResult) -> RegistryBridgeResult:
    """Replace only one legacy metadata component with its verified fixed claim."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("typed bridge required")
    assertion = base.registry.assertion(COMPONENT_ID)
    reference = base.registry.reference(assertion.reference_id)
    if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or assertion.kind is not AssertionKind.STATEMENT
            or assertion.component_position != 2
            or reference.locator != "Proposition 5.8"
            or type(assertion.content).__name__ != "TodaFixedStatementComponent"
            or getattr(assertion.content, "component_key", None) != "pi7_3_group_relation"
            or getattr(assertion.content, "reference_locator", None) != "Proposition 5.8"):
        raise ValueError("unreviewed Proposition 5.8 registry component")
    rows = tuple(r for r in base.records if r.assertion_id == COMPONENT_ID)
    if len(rows) != 1 or rows[0].status is not MigrationStatus.METADATA_ONLY:
        raise ValueError("expected one metadata-only Proposition 5.8 component")

    typed = _source_checked_pi73_relation(base)
    registry = UnifiedStatementRegistry()
    for original_reference in base.registry._references.values():
        registry.add_reference(original_reference)
    for original_assertion in base.registry._assertions.values():
        if original_assertion.assertion_id == COMPONENT_ID:
            original_assertion = replace(original_assertion, content=typed)
        registry.add_assertion(original_assertion)
    records = tuple(
        replace(record, status=MigrationStatus.STRUCTURED,
                detail="Source-checked typed Proposition 5.8 pi_7^3 clause; no saved proof adopted")
        if record.assertion_id == COMPONENT_ID else record
        for record in base.records
    )
    return RegistryBridgeResult(registry, records, base.proof_links)
