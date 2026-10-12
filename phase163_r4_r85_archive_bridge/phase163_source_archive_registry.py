"""Phase 163 R4-R83: opt-in archival source registration; never proof eligible."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from phase163_r4_registry_bridge import build_registry_bridge
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
)

CATALOG_PATH = Path(__file__).with_name("phase163_source_archive_catalog.json")
OWNERS = {
    "prop:1-6": ("Proposition 1.6", ReferenceKind.PROPOSITION, 3),
    "thm:2.4": ("Theorem 2.4", ReferenceKind.THEOREM, 2),
    "prop:2.5": ("Proposition 2.5", ReferenceKind.PROPOSITION, 2),
    "prop:4.2": ("Proposition 4.2", ReferenceKind.PROPOSITION, 1),
}


def load_source_archive_catalog(path: Path = CATALOG_PATH) -> dict:
    """Load a checked, immutable source transcript; refuse missing/corrupted evidence."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if (document.get("schema") != "phase163-r83-source-archive-v1"
            or document.get("original_edition_verified") is not False
            or document.get("proof_eligible") is not False):
        raise ValueError("unrecognized or over-claimed source archive")
    records = document.get("records")
    evidence = document.get("locator_evidence")
    if not isinstance(records, list) or len(records) != 8 or not isinstance(evidence, list) or len(evidence) != 4:
        raise ValueError("unexpected source archive cardinality")
    grouped = {owner: [] for owner in OWNERS}
    checked_evidence = set()
    for item in evidence:
        owner = item["owner"]
        if owner not in OWNERS or owner in checked_evidence:
            raise ValueError("duplicate or unknown evidence owner")
        checked_evidence.add(owner)
        locator, kind, count = OWNERS[owner]
        if (item["locator"] != locator or item["kind"] != kind.value
                or bool(item["live_bridge_reference_found"]) != (owner == "prop:2.5")):
            raise ValueError("source locator evidence mismatch")
        if item["existing_boundary_component_count"] != (1 if owner == "prop:2.5" else 0):
            raise ValueError("source boundary component drift")
    if checked_evidence != set(OWNERS):
        raise ValueError("missing reference evidence")
    seen = set()
    for item in records:
        owner = item["owner"]
        if owner not in grouped or not isinstance(item["component_position"], int):
            raise ValueError("unknown owner or invalid position")
        candidate_id = item["proposed_assertion_key"]
        if not isinstance(candidate_id, str) or not candidate_id.startswith("proposal:" + owner + ":") or candidate_id in seen:
            raise ValueError("source candidate identity collision")
        seen.add(candidate_id)
        text = item["claim_text"]
        if (not isinstance(text, str) or not text.strip()
                or hashlib.sha256(text.encode("utf-8")).hexdigest() != item["source_claim_sha256"]):
            raise ValueError("source transcript checksum mismatch")
        if (not item["shared_scope_note"] or not isinstance(item["boundary_issues"], list)
                or item["start_line"] > item["end_line"]):
            raise ValueError("missing source provenance")
        grouped[owner].append(item)
    for owner, (_, _, count) in OWNERS.items():
        if [item["component_position"] for item in grouped[owner]] != list(range(1, count + 1)):
            raise ValueError("source component order mismatch")
    return document


def build_registry_with_source_archive(catalog_path: Path = CATALOG_PATH, *, bridge=None):
    """Return a NEW registry plus an audit summary; never change proof/search catalogs.

    Exact transcribed TeX is archival metadata. `AssertionKind.STATEMENT`
    reflects the registry schema, not semantic verification. There is no
    ProofStepLink or theorem eligibility decision here.
    """
    document = load_source_archive_catalog(catalog_path)
    if bridge is None:
        bridge = build_registry_bridge()
    registry = bridge.registry
    refs_added = []
    refs_reused = []
    entries_added = []
    for owner, (locator, kind, _) in OWNERS.items():
        key = "toda:" + locator
        try:
            current = registry.reference(key)
        except KeyError:
            registry.add_reference(LiteratureEntry(
                reference_id=key, kind=kind, locator=locator,
                source_id="Toda translated TeX (original edition unverified)",
            ))
            refs_added.append(key)
        else:
            if current.kind is not kind or current.locator != locator:
                raise ValueError("existing reference identity conflict")
            refs_reused.append(key)
        for item in (row for row in document["records"] if row["owner"] == owner):
            entry_id = "archive:" + item["proposed_assertion_key"].removeprefix("proposal:")
            content = {
                "source_text": item["claim_text"],
                "source_file": item["source_file"],
                "source_lines": (item["start_line"], item["end_line"]),
                "source_sha256": item["source_claim_sha256"],
                "boundary_issues": tuple(item["boundary_issues"]),
                "original_edition_verified": False,
                "mathematics_verified": False,
                "proof_eligible": False,
            }
            registry.add_assertion(AssertionEntry(
                assertion_id=entry_id, reference_id=key,
                kind=AssertionKind.STATEMENT, content=content,
                origin=AssertionOrigin.SOURCE_ARCHIVE,
                component_position=item["component_position"],
                scope=item["shared_scope_note"],
                available_after_position=None,
            ))
            entries_added.append(entry_id)
    return registry, {
        "phase": "163 R4-R83",
        "mode": "PERSISTENT_OPT_IN_SOURCE_ARCHIVE",
        "reference_reused_count": len(refs_reused),
        "reference_added_count": len(refs_added),
        "source_text_assertion_added_count": len(entries_added),
        "reference_ids_added": refs_added,
        "reference_ids_reused": refs_reused,
        "source_text_assertion_ids": entries_added,
        "original_edition_verified": False,
        "mathematics_verified_count": 0,
        "proof_eligible_count": 0,
        "proof_search_connected": False,
        "production_auto_connected": False,
        "full_suite_run": False,
    }
