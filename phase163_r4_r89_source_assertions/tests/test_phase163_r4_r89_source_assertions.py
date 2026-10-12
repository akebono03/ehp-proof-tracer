import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r89_source_assertions import (
    build_source_only_registry,
    write_report,
)
from unified_statement_registry import AssertionOrigin

PROJECT = Path(__file__).resolve().parents[2]


def inputs():
    return (
        json.loads((PROJECT / "phase163_r4_r86_output" / "claim_review_catalog.json").read_text(encoding="utf-8")),
        json.loads((PROJECT / "phase163_r4_r88_output" / "scope_conditions.json").read_text(encoding="utf-8")),
    )


def test_all_nine_archived_without_semantic_promotion():
    registry, report = build_source_only_registry(*inputs())
    assert report["reference_count"] == 4
    assert report["assertion_count"] == 9
    assert report["production_registry_modified"] is False
    assert report["proof_search_connected"] is False
    for record in report["records"]:
        item = registry.assertion(record["assertion_id"])
        assert item.origin is AssertionOrigin.SOURCE_ARCHIVE
        assert item.content["proof_eligible"] is False
        assert item.content["mathematics_verified"] is False


def test_same_component_can_have_two_subpositions():
    registry, report = build_source_only_registry(*inputs())
    rows = [x for x in report["records"] if x["reference_id"] == "toda:Theorem 2.4"]
    assert [(x["component_position"], x["subposition"]) for x in rows] == [(1, 1), (2, 1), (2, 2)]
    assert len(registry.assertions_for("toda:Theorem 2.4")) == 3


def test_tampered_claim_rejected():
    r86, r88 = inputs()
    r86["records"][0]["claim_text"] += "tampering"
    with pytest.raises(ValueError, match="digest"):
        build_source_only_registry(r86, r88)


def test_semantic_promotion_rejected():
    r86, r88 = inputs()
    r88["records"][0]["proof_eligible"] = True
    with pytest.raises(ValueError, match="ineligible"):
        build_source_only_registry(r86, r88)


def test_missing_review_rejected():
    r86, r88 = inputs()
    r88["records"].pop()
    with pytest.raises(ValueError, match="record count"):
        build_source_only_registry(r86, r88)


def test_write_report(tmp_path):
    _, report = build_source_only_registry(*inputs())
    write_report(report, tmp_path)
    saved = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert saved["assertion_count"] == 9
    assert "SOURCE_ONLY" in (tmp_path / "report.md").read_text(encoding="utf-8")
