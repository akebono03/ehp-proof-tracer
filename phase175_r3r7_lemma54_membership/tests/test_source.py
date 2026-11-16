"""Pin full Lemma 5.4 source and independent publication ordering."""
from __future__ import annotations

import json

import pytest

from phase173_r4_r1_lemma54_source_bridge.source import (
    DOUBLE_TEXT, HOPF_TEXT, MEMBERSHIP_TEXT,
)
from phase175_r3r7_lemma54_membership import source


def lemma_text() -> str:
    return (
        "\\begin{lemma}[]\n\\label{lem:5.4}\n"
        + MEMBERSHIP_TEXT + "\n"
        + HOPF_TEXT + ",\\qquad " + DOUBLE_TEXT + ".\n"
        + "\\end{lemma}"
    )


def manifest() -> dict:
    return {
        "mode": "ORDERED_SOURCE_ONLY_MANIFEST",
        "assertions": [
            {
                "reference_id": "toda:Lemma 5.4",
                "statement_id": source.LEMMA54_SOURCE_ID,
                "source_sha256": source.LEMMA54_SHA256,
                "publication_position": 8300,
                "review_needed": False,
                "source_text": lemma_text(),
            },
            {
                "reference_id": "toda:Lemma 5.7",
                "statement_id": "toda:tex:ch5:0015",
                "source_sha256": "01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c",
                "publication_position": 9100,
                "review_needed": False,
                "source_text": "source unit checked separately",
            },
            {
                "reference_id": "toda:Proposition 5.8",
                "statement_id": "toda:tex:ch5:0016",
                "source_sha256": "4e41470cead5382bc042b39634ae4bbc9bc184cda06801ddafa1331be6f0d124",
                "publication_position": 9200,
                "review_needed": False,
                "source_text": "source unit checked separately",
            },
        ],
    }


def setup_source(monkeypatch, tmp_path, data: dict) -> None:
    monkeypatch.setattr(source, "verify_reviewed_toda_source", lambda root: {"source_blob": "verified"})
    monkeypatch.setattr(source, "verify_lemma57_manifest", lambda root: {"source": "verified"})
    manuscript = tmp_path / source.CHAPTER
    manuscript.parent.mkdir(parents=True, exist_ok=True)
    manuscript.write_text(lemma_text(), encoding="utf-8")
    report = tmp_path / source.MANIFEST
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def test_all_cited_source_clauses_and_order_required(monkeypatch, tmp_path) -> None:
    setup_source(monkeypatch, tmp_path, manifest())
    result = source.verify_lemma54_before_lemma57(tmp_path)
    assert result["lemma54_position"] == 8300
    assert result["lemma57_position"] == 9100
    assert result["new_specific_given"] == 0


@pytest.mark.parametrize("mutation", [
    "missing", "bad_sha", "bad_order", "needs_review", "missing_double", "duplicate",
])
def test_source_pin_fail_closed(monkeypatch, tmp_path, mutation: str) -> None:
    data = manifest()
    item = data["assertions"][0]
    if mutation == "missing":
        data["assertions"].pop(0)
    elif mutation == "bad_sha":
        item["source_sha256"] = "a" * 64
    elif mutation == "bad_order":
        item["publication_position"] = 9300
    elif mutation == "needs_review":
        item["review_needed"] = True
    elif mutation == "missing_double":
        item["source_text"] = item["source_text"].replace(DOUBLE_TEXT, "REMOVED")
    elif mutation == "duplicate":
        data["assertions"].append(dict(item))
    setup_source(monkeypatch, tmp_path, data)
    with pytest.raises((ValueError, RuntimeError)):
        source.verify_lemma54_before_lemma57(tmp_path)


def test_actual_checkout_sources_are_reviewed() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    evidence = source.verify_lemma54_before_lemma57(root)
    assert evidence["new_specific_given"] == 0
    assert evidence["source_blob"] == "579661138928499ba04a51327f686d9b971b5314"
