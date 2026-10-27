"""Focused source-authenticity, metadata, and fail-closed boundary tests."""
from __future__ import annotations

import json

import pytest

from phase169_r10e7_ch6_family_source_audit.audit import (
    FAMILIES,
    build_report,
    inspect_generator_metadata,
    inspect_manifest,
    inspect_source_clause,
)


def _sample() -> tuple[str, str, str]:
    text = "\n".join(
        x for spec in FAMILIES
        for x in (spec["section"], spec["clause"])
    ) + "\n" + FAMILIES[-1]["next_section"] + "\n"
    rows = ["id,display,kinds,k,n,orders,latex,stable,stable_orders"]
    rows += [f"{s['id']},{s['name']},0,{s['stem']},{s['minimum_n']},2,{s['latex']},,"
             for s in FAMILIES]
    manifest = {
        "mode": "ORDERED_SOURCE_ONLY_MANIFEST",
        "publication_order_scope": "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION",
        "assertions": [{"chapter": 5, "source_file": "Toda_05_2.tex"}],
    }
    return text, "\n".join(rows), json.dumps(manifest)


def test_r10e7_recognizes_three_independent_definitions_without_proof_steps():
    source, csv_text, manifest = _sample()
    report = build_report(source, csv_text, manifest, (4, 9))
    assert [item["family_id"] for item in report["definitions"]] == [10, 11, 12]
    assert not report["citation_registration_ready"]
    assert report["manifest"]["chapter6_entries"] == 0
    assert report["production_files_modified"] == []
    assert report["full_pytest_run"] is False


def test_r10e7_rejects_missing_or_repeated_clause():
    source, _, _ = _sample()
    spec = FAMILIES[0]
    with pytest.raises(ValueError, match="missing/repeated"):
        inspect_source_clause(source.replace(spec["clause"], "removed"), spec)
    with pytest.raises(ValueError, match="missing/repeated"):
        inspect_source_clause(source + "\n" + spec["clause"], spec)


def test_r10e7_rejects_clause_outside_reviewed_section():
    source, _, _ = _sample()
    spec = FAMILIES[0]
    changed = spec["clause"] + "\n" + source.replace(spec["clause"], "removed")
    with pytest.raises(ValueError, match="outside reviewed section"):
        inspect_source_clause(changed, spec)


def test_r10e7_rejects_wrong_metadata_and_duplicate_family_ids():
    _, csv_text, _ = _sample()
    spec = FAMILIES[1]
    assert inspect_generator_metadata(csv_text, spec)["metadata_only"]
    with pytest.raises(ValueError, match="metadata mismatch"):
        inspect_generator_metadata(csv_text.replace("ν̅,0,8,6", "ν̅,0,7,6"), spec)
    with pytest.raises(ValueError, match="duplicate"):
        inspect_generator_metadata(csv_text + "\n" + csv_text.splitlines()[2], spec)


def test_r10e7_manifest_source_order_is_not_printed_edition_position():
    _, _, manifest = _sample()
    assert not inspect_manifest(manifest)["chapter6_position_covered"]
    with pytest.raises(ValueError, match="provenance"):
        inspect_manifest(manifest.replace(
            "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION", "PUBLICATION_VERIFIED"
        ))
