"""Phase 165 R12: batch source-shape normalization and typed candidate catalog.

Adopted TeX source assertions are quotations, not automatically checked
formal propositions. No ProofStep or citation permission is produced here.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r6_binding_candidates import inventory_typed_source_bindings
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class AdoptedTexStatement:
    """Strongly typed *source record*, not a mathematical conclusion."""

    assertion_id: str
    source_statement_id: str
    reference_id: str
    locator: str
    source_text: str
    source_sha256: str
    source_chapter: int
    source_position: int
    component_position: int | None
    proof_eligible: bool = False


@dataclass(frozen=True)
class TypedBindingRecord:
    source: AdoptedTexStatement
    candidate_assertion_ids: tuple[str, ...]
    status: str
    proof_step: None = None


@dataclass(frozen=True)
class BatchBindingResult:
    records: tuple[TypedBindingRecord, ...]
    unique_candidates: int
    ambiguous_candidates: int
    unmatched: int
    mathematically_typed: int = 0
    proof_eligible: int = 0


def build_batch_typed_bindings(bridge: RegistryBridgeResult) -> BatchBindingResult:
    """Normalize ALL adopted TeX records; expose locator candidates separately.

    A locator match is never semantic identity. A mathematical converter will
    need to check the variables, conditions and ranges against source_text.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    catalog = inventory_typed_source_bindings(bridge)
    unique = {item.source_assertion_id: item.typed_assertion_id
              for item in catalog.candidates}
    ambiguous = set(catalog.ambiguous_source_ids)
    unmatched = set(catalog.unmatched_source_ids)
    records = []
    for assertion in bridge.registry._assertions.values():
        if (assertion.origin is not AssertionOrigin.SOURCE_ARCHIVE
                or not assertion.assertion_id.startswith("phase163:archive:")):
            continue
        body = assertion.content
        if not isinstance(body, dict):
            raise ValueError("adopted source assertion must carry source metadata")
        source_text = body.get("source_text")
        checksum = body.get("source_sha256")
        chapter = body.get("source_chapter")
        position = body.get("source_position")
        if (not isinstance(source_text, str) or not source_text
                or not isinstance(checksum, str)
                or hashlib.sha256(source_text.encode("utf-8")).hexdigest() != checksum
                or type(chapter) is not int or not 1 <= chapter <= 5
                or type(position) is not int or position <= 0
                or body.get("proof_eligible") is not False):
            raise ValueError("source integrity or eligibility contract failed")
        source = AdoptedTexStatement(
            assertion_id=assertion.assertion_id,
            source_statement_id=body["source_statement_id"],
            reference_id=assertion.reference_id,
            locator=bridge.registry.reference(assertion.reference_id).locator,
            source_text=source_text,
            source_sha256=checksum,
            source_chapter=chapter,
            source_position=position,
            component_position=assertion.component_position,
        )
        if assertion.assertion_id in unique:
            ids = (unique[assertion.assertion_id],)
            status = "UNIQUE_LOCATOR_UNVERIFIED_SEMANTICS"
        elif assertion.assertion_id in ambiguous:
            ids = tuple(sorted(
                item.assertion_id
                for item in bridge.registry._assertions.values()
                if (item.origin is AssertionOrigin.FIXED_STATEMENT
                    and bridge.registry.reference(item.reference_id).locator == source.locator)
            ))
            status = "AMBIGUOUS_LOCATOR_UNVERIFIED_SEMANTICS"
        elif assertion.assertion_id in unmatched:
            ids = ()
            status = "NO_TYPED_CANDIDATE"
        else:
            raise ValueError("source assertion omitted from binding inventory")
        records.append(TypedBindingRecord(source, ids, status))
    records.sort(key=lambda r: (r.source.source_chapter, r.source.source_position,
                                r.source.assertion_id))
    if len(records) != (len(unique) + len(ambiguous) + len(unmatched)):
        raise ValueError("binding inventory cardinality mismatch")
    return BatchBindingResult(tuple(records), len(unique), len(ambiguous), len(unmatched))
