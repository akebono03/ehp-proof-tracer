import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase163_r4_r92_gap_completion.phase163_r4_r92_gap_completion import (
    audit_catalog,
    coverage_gaps,
    item_components,
    mask_comments,
    register_subitems,
    sha256,
    validate_r91,
    write_outputs,
)
from phase163_r4_registry_bridge import build_registry_bridge
from unified_statement_registry import AssertionOrigin

PROJECT = Path(__file__).resolve().parents[2]
SOURCE = PROJECT / "sources" / "toda"
CATALOG = PROJECT / "phase163_r4_r91_output" / "source_catalog.json"


def load_catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_full_r91_catalog_integrity_and_order():
    catalog = load_catalog()
    sources = validate_r91(catalog, SOURCE)
    assert sorted(sources) == [1, 2, 3, 4, 5]
    assert len(catalog["records"]) == 96


def test_real_source_items_are_extracted_without_certification():
    audit = audit_catalog(load_catalog(), SOURCE)
    assert audit["r91_parent_record_count"] == 96
    assert audit["source_subitem_count"] == 9
    assert audit["r91_review_count"] == 8
    assert all(x["proof_eligible"] is False for x in audit["source_subitems"])
    assert all(x["mathematical_semantics_verified"] is False for x in audit["source_subitems"])
    assert {x["parent_locator"] for x in audit["source_subitems"]} == {
        "Proposition 1.2", "Theorem 2.4", "Proposition 3.4"
    }


def test_source_only_bridge_adds_subitems_and_does_not_add_proof_links():
    catalog = load_catalog()
    audit = audit_catalog(catalog, SOURCE)
    bridge = build_registry_bridge()
    before_links = bridge.proof_links
    result = register_subitems(catalog, audit, bridge=bridge)
    assert result["r91_assertion_count"] == 96
    assert result["subitem_assertion_added_count"] == 9
    assert result["source_only_assertion_count"] == 105
    assert bridge.proof_links == before_links
    for item in audit["source_subitems"]:
        assertion = bridge.registry.assertion(item["source_id"])
        assert assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        assert assertion.content["proof_eligible"] is False
        assert assertion.available_after_position is None


def test_bad_source_digest_rejected():
    source = load_catalog()
    source["records"][0]["source_text"] += "TAMPER"
    with pytest.raises(ValueError, match="checksum"):
        validate_r91(source, SOURCE)


def test_missing_source_text_rejected():
    source = load_catalog()
    source["records"][0]["source_sha256"] = sha256("not source")
    with pytest.raises(ValueError, match="checksum"):
        validate_r91(source, SOURCE)


def test_publication_order_tampering_rejected():
    source = load_catalog()
    source["records"][0]["publication_position"] = 99
    with pytest.raises(ValueError, match="publication order"):
        validate_r91(source, SOURCE)


def test_item_comments_do_not_create_fake_components():
    text = ("\\begin{proposition}\\label{prop:1.1}\n"
            "\\begin{enumerate}\n"
            "% \\item fake\n"
            "\\item alpha\n\\item beta\n"
            "\\end{enumerate}\n\\end{proposition}")
    row = {"environment": "proposition", "source_text": text,
           "source_id": "s", "source_sha256": sha256(text),
           "locator": "Proposition 1.1", "chapter": 1, "source_file": "test.tex"}
    assert len(item_components(row)) == 2


def test_nested_equation_remains_a_review_candidate(tmp_path):
    raw = ("\\begin{proposition}\\label{prop:1.1}\n"
           "\\begin{equation}X\\end{equation}\n"
           "\\end{proposition}\n")
    rows = [{"chapter": 1, "start_line": 1, "end_line": 3}]
    gaps = coverage_gaps({"records": rows}, {1: raw})
    assert len(gaps) == 1
    assert gaps[0]["kind"] == "UNREGISTERED_EQUATION_OR_NESTED_ALIAS"


def test_unlabelled_inline_definition_found():
    raw = "\\emph{secondary composition} を次で定める。\n"
    gaps = coverage_gaps({"records": []}, {1: raw})
    assert any(gap["kind"] == "INLINE_DEFINITION_CANDIDATE" for gap in gaps)


def test_tampered_subitem_cannot_be_registered():
    source = load_catalog()
    audit = audit_catalog(source, SOURCE)
    tampered = copy.deepcopy(audit)
    tampered["source_subitems"][0]["source_text"] += "bad"
    bridge = build_registry_bridge(components_by_reference={}, theorem_facts=SimpleNamespace(entries=()))
    with pytest.raises(ValueError, match="provenance"):
        register_subitems(source, tampered, bridge=bridge)


def test_report_written(tmp_path):
    catalog = load_catalog()
    audit = audit_catalog(catalog, SOURCE)
    write_outputs(audit, {"subitem_assertion_added_count": 9}, tmp_path)
    saved = json.loads((tmp_path / "audit.json").read_text(encoding="utf-8"))
    assert saved["r91_parent_record_count"] == 96
    assert "原文" in (tmp_path / "report.md").read_text(encoding="utf-8")
