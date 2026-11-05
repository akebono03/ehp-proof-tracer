"""Focused no-repository-mutation tests for the R3-R7-R1 preflight audit."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path

import pytest

from phase174_r3_r7_r1_zero_root_audit.audit import (
    EVIDENCE,
    EVIDENCE_SHA256,
    PREVIOUS_HEAD,
    REVIEWED_HEAD,
    SOURCE_BLOBS,
    accepted_blob,
    git_blob,
    summarize_other_frontiers,
    validate_previous_audit,
    verify_toda_proof_route,
)


def evidence() -> dict:
    return json.loads(EVIDENCE.read_text(encoding="utf-8-sig"))


def test_uploaded_previous_evidence_is_reviewed_and_has_zero_frontier() -> None:
    summary = validate_previous_audit(evidence())
    assert summary["reviewed_evidence_head"] == PREVIOUS_HEAD
    assert summary["zero_target"] == "pi_12^7"
    assert summary["zero_goal_open_count"] == 1
    assert summary["previous_zero_root_proposal_count_measured"] is False


def test_previous_report_did_not_probe_zero_root_proposals() -> None:
    data = evidence()
    row = next(row for row in data["selected_targets"] if row["group"] == "pi_12^7")
    assert row["typed_registered_relation_count"] == 0
    assert "root" not in row["source_screened_frontier"]
    assert row["source_screened_frontier"]["direct_given_registered"] is False


def test_previous_audit_rejects_direct_given() -> None:
    data = copy.deepcopy(evidence())
    data["new_group_given"] = 1
    with pytest.raises(RuntimeError, match="runtime errors or new group GIVEN"):
        validate_previous_audit(data)


def test_previous_audit_rejects_changed_zero_goal() -> None:
    data = copy.deepcopy(evidence())
    row = next(row for row in data["selected_targets"] if row["group"] == "pi_12^7")
    row["open_goals"][0]["repr"] = "wrong group"
    with pytest.raises(RuntimeError, match="zero frontier changed"):
        validate_previous_audit(data)


def test_other_frontier_counts_come_from_evidence() -> None:
    rows = summarize_other_frontiers(evidence()["selected_targets"])
    by_group = {row["group"]: row for row in rows}
    assert len(rows) == 5
    assert by_group["pi_11^3"]["cyclic_structure_blockers"] == 1
    assert by_group["pi_12^4"]["cyclic_structure_blockers"] == 1
    assert by_group["pi_13^7"]["cyclic_structure_blockers"] == 1
    assert by_group["pi_13^4"]["only_equality_symmetry_for_all_open_goals"]
    assert by_group["pi_12^3"]["only_equality_symmetry_for_all_open_goals"]


def test_git_blobs_accept_unmodified_crlf_only() -> None:
    unix = b"first\nsecond\n"
    assert accepted_blob(unix, git_blob(unix))
    assert accepted_blob(unix.replace(b"\n", b"\r\n"), git_blob(unix))
    assert not accepted_blob(b"first\nchanged\n", git_blob(unix))


def test_toda_proof_route_requires_every_independent_excerpt(tmp_path: Path) -> None:
    path = tmp_path / "sources" / "toda"
    path.mkdir(parents=True)
    fragments = (
        r"\pi^{n}_{n+5}=0\ (n\ge7)",
        r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
        r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
        r"\pi^{6}_{11}\xrightarrow{E}\pi^{7}_{12}",
        r"\pi_{12}^{13}=0",
        r"\pi_{12}^7=0",
        r"(4.5) により, Propの最後の結果が得られる",
    )
    (path / "Toda_05_2.tex").write_text("\n".join(fragments), encoding="utf-8")
    result = verify_toda_proof_route(tmp_path)
    assert len(result["source_checks"]) == 7
    assert all(result["source_checks"].values())
    assert result["printed_source_result_not_a_given"]
    (path / "Toda_05_2.tex").write_text("\n".join(fragments[:-1]), encoding="utf-8")
    with pytest.raises(RuntimeError, match="Toda proof excerpts absent"):
        verify_toda_proof_route(tmp_path)


def test_readonly_script_has_no_production_file_write_calls() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "live_zero_frontier" in names
    assert "verify_toda_proof_route" in names
    assert "validate_previous_audit" in names
    assert "install" not in names
    assert "patch" not in names
    assert "apply" not in names


def test_reviewed_version_and_paths_are_explicit() -> None:
    assert REVIEWED_HEAD != PREVIOUS_HEAD
    assert hashlib.sha256(EVIDENCE.read_bytes()).hexdigest() == EVIDENCE_SHA256
    assert len(SOURCE_BLOBS) == 7
    assert "phase174_r3_r7_source_first_audit/audit.py" in SOURCE_BLOBS
    assert "toda_stable_group_transport.py" in SOURCE_BLOBS
