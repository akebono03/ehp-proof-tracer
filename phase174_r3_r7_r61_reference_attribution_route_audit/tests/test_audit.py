"""R61 static and negative focused tests; public proof is checked by run.ps1."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r61_reference_attribution_route_audit.audit import (
    PINS, ROUTES, git_blob_sha, renderer_route_contract,
    source_guard, source_numbers_in_rendered_proof,
)


def test_pins_match_reviewed_sources() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 6
    assert len(source_guard(root)) == 6


def test_renderer_three_actual_routes_are_owned_by_model() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (root / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8-sig")
    contract = renderer_route_contract(source)
    assert contract["local_route_count"] == len(ROUTES) == 3
    assert {item["route"] for item in contract["route_call_sites"]} == set(ROUTES)
    assert contract["fully_centralized"] is False


def test_refuses_renderer_without_source_owned_route() -> None:
    with pytest.raises(RuntimeError, match="R61_RENDERER_ENTRY_MISMATCH"):
        renderer_route_contract("def unrelated():\n    return 0\n")


def test_refuses_unsafe_or_unknown_citation_tags() -> None:
    with pytest.raises(RuntimeError, match="R61_UNKNOWN_RENDERED_REFERENCE"):
        source_numbers_in_rendered_proof("[R1]より。 [R9]より。", (1, 2))


def test_known_citations_are_not_inferred_from_names() -> None:
    result = source_numbers_in_rendered_proof(
        "**[R1] 定理.**\n\n証明\n\n[R1]より, [R2]を用いる.\n", (1, 2)
    )
    assert result == (1, 1, 2)


def test_invalid_markdown_type_is_rejected() -> None:
    with pytest.raises(TypeError):
        source_numbers_in_rendered_proof(None, (1,))


def test_source_guard_rejects_tampered_renderer(tmp_path: Path) -> None:
    for name in PINS:
        dest = tmp_path / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"tampered\n")
    with pytest.raises(RuntimeError, match="R61_REVIEWED_BLOB_MISMATCH"):
        source_guard(tmp_path)


def test_git_blob_sha_has_expected_known_value() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
