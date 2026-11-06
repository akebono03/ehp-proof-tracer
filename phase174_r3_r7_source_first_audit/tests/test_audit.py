"""Pure focused tests for the read-only Phase 174 R3-R7 audit contract."""
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from phase174_r3_r7_source_first_audit.audit import (
    PRIOR_HEAD,
    REVIEWED_HEAD,
    SOURCE_BLOBS,
    TARGETS,
    accepted_blob,
    git_blob,
    historical_n4_status,
    is_exact_given,
    statement_description,
)


def test_git_blob_and_crlf_tolerance() -> None:
    sample = b"first\nsecond\n"
    actual = git_blob(sample)
    assert len(actual) == 40
    assert accepted_blob(sample, actual)
    assert accepted_blob(b"first\r\nsecond\r\n", actual)
    assert not accepted_blob(sample + b"modified", actual)


def test_exact_given_preserves_type_identity() -> None:
    assert is_exact_given(4, (4,))
    assert not is_exact_given(4, (4.0,))
    assert not is_exact_given("4", (4,))
    assert not is_exact_given(4, ())


def test_goal_diagnostic_truncates_without_promoting_it() -> None:
    result = statement_description("a" * 600, limit=35)
    assert result["type"] == "str"
    assert "[truncated for diagnostics]" in result["repr"]
    assert len(result["repr"]) < 100


def test_readonly_audit_does_not_contain_proof_mutators() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    fn_names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "inspect_live_selected_targets" in fn_names
    assert "source_screened_frontier" in fn_names
    assert "verify_math_sources" in fn_names
    assert "make_report" in fn_names
    assert "install" not in fn_names
    assert "patch" not in fn_names
    assert "apply" not in fn_names


def test_target_set_only_records_diagnostic_sample() -> None:
    assert TARGETS == (
        (5, 3), (4, 8), (4, 9), (3, 8), (7, 5), (3, 9), (7, 6)
    )
    assert len(SOURCE_BLOBS) == 6
    assert PRIOR_HEAD != REVIEWED_HEAD


def test_historical_report_does_not_claim_live_results(tmp_path: Path) -> None:
    data = {
        "head_reviewed": "historical",
        "summary": {"all_registered_groups": 33, "all_status_counts": {"PENDING": 26},
                    "k_ge_8_abstract_only": [8, 9]},
        "rows": [
            {"n": 4, "k": k, "search_status": "search_failed",
             "category": "ABSTRACT_ONLY_NAMED_PENDING", "open_goal_types": [],
             "proven_steps": 0}
            for k in range(1, 34)
        ],
    }
    path = tmp_path / "phase173_r4_r15r12r3_all_n4_status_audit"
    path.mkdir()
    (path / "all_n4_status_report.json").write_text(
        json.dumps(data), encoding="utf-8"
    )
    report = historical_n4_status(tmp_path)
    assert report["historical_only_not_new_live_evidence"] is True
    assert report["recorded_head"] == "historical"
    assert report["selected_frontiers"]["8"]["category"] == "ABSTRACT_ONLY_NAMED_PENDING"


def test_historical_report_fails_on_incomplete_group_inventory(tmp_path: Path) -> None:
    path = tmp_path / "phase173_r4_r15r12r3_all_n4_status_audit"
    path.mkdir()
    (path / "all_n4_status_report.json").write_text(
        json.dumps({"summary": {}, "rows": [{"n": 4, "k": 8}]}),
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="missing required rows"):
        historical_n4_status(tmp_path)
