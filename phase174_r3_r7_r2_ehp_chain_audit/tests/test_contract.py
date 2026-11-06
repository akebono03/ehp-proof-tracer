"""Pure, repository-independent contracts for R3-R7-R2 read-only audit."""
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from phase174_r3_r7_r2_ehp_chain_audit.audit import (
    REVIEWED_HEAD,
    PREVIOUS_AUDIT_HEAD,
    SOURCE_BLOBS,
    SOURCE_EXCERPTS,
    classify_proposals,
    ehp_chain_dimensions,
    git_blob_sha,
    matches_git_blob,
    validate_previous_report,
    verify_toda_transcription,
)


def previous_snapshot() -> dict:
    return {
        "phase": "174-R3-R7-R1",
        "gate": "PASS_READ_ONLY_ZERO_ROOT_DIAGNOSTIC",
        "git_state": {
            "remote_head": PREVIOUS_AUDIT_HEAD,
            "local_head": PREVIOUS_AUDIT_HEAD,
        },
        "live_zero_root": {
            "zero_root": {"proposal_count": 0},
            "preceding_group": "pi_11^6",
            "preceding_group_status": "search_failed",
            "zero_search_status": "search_failed",
            "direct_zero_target_given": False,
            "screening_path": "independent_source_screened_shared_provider",
        },
        "new_group_given": 0,
        "new_inference_rules": 0,
    }


def test_expected_two_ehp_windows_are_consecutive() -> None:
    windows = ehp_chain_dimensions()
    assert set(windows) == {"delta_e", "e_h"}
    assert windows["delta_e"]["middle"] == windows["e_h"]["source"]
    assert windows["delta_e"]["target"] == windows["e_h"]["middle"]
    assert windows["delta_e"]["expected_indices"] == (6, 12, "delta_e")
    assert windows["e_h"]["expected_indices"] == (6, 12, "e_h")


def test_previous_r1_measured_no_zero_root_and_failed_predecessor() -> None:
    result = validate_previous_report(previous_snapshot())
    assert result["zero_root_proposal_count"] == 0
    assert result["precursor"] == "pi_11^6"
    assert result["precursor_status"] == "search_failed"


def test_reject_prior_r1_not_passed() -> None:
    data = previous_snapshot()
    data["gate"] = "PASS_PREFLIGHT"
    with pytest.raises(RuntimeError, match="did not pass"):
        validate_previous_report(data)


def test_reject_previous_r1_zero_root_candidate_count_changed() -> None:
    data = previous_snapshot()
    data["live_zero_root"]["zero_root"]["proposal_count"] = 1
    with pytest.raises(RuntimeError, match="measured zero-root"):
        validate_previous_report(data)


def test_reject_previous_r1_direct_given() -> None:
    data = previous_snapshot()
    data["live_zero_root"]["direct_zero_target_given"] = True
    with pytest.raises(RuntimeError, match="measured zero-root"):
        validate_previous_report(data)


def test_reject_previous_r1_wrong_head() -> None:
    data = previous_snapshot()
    data["git_state"]["local_head"] = "other"
    with pytest.raises(RuntimeError, match="HEAD differs"):
        validate_previous_report(data)


def test_status_cannot_confuse_candidates_with_proofs() -> None:
    assert classify_proposals(0) == "NO_CANDIDATE"
    assert classify_proposals(1) == "CANDIDATES_NOT_PROOFS"
    assert classify_proposals(4) == "CANDIDATES_NOT_PROOFS"
    with pytest.raises(ValueError):
        classify_proposals(-1)


def test_blob_guard_only_allows_crlf_normalization() -> None:
    body = b"alpha\nbeta\n"
    sha = git_blob_sha(body)
    assert matches_git_blob(body, sha)
    assert matches_git_blob(body.replace(b"\n", b"\r\n"), sha)
    assert not matches_git_blob(body + b"extra", sha)


def test_source_transcription_needs_every_clause(tmp_path: Path) -> None:
    directory = tmp_path / "sources" / "toda"
    directory.mkdir(parents=True)
    file = directory / "Toda_05_2.tex"
    file.write_text("\n".join(SOURCE_EXCERPTS.values()), encoding="utf-8")
    reviewed = verify_toda_transcription(tmp_path)
    assert len(reviewed["checked_excerpts"]) == len(SOURCE_EXCERPTS)
    assert reviewed["original_print_edition_independently_verified"] is False
    last_key = list(SOURCE_EXCERPTS)[-1]
    file.write_text("\n".join(
        value for key, value in SOURCE_EXCERPTS.items() if key != last_key
    ), encoding="utf-8")
    with pytest.raises(RuntimeError, match="Missing Toda"):
        verify_toda_transcription(tmp_path)


def test_new_audit_does_not_define_install_patch_or_apply() -> None:
    module = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(module.read_text(encoding="utf-8"))
    funcs = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "typed_chain_goals" in funcs
    assert "inspect_live_obligations" in funcs
    assert "validate_previous_report" in funcs
    assert "install" not in funcs
    assert "patch" not in funcs
    assert "apply" not in funcs


def test_guard_paths_are_existing_reviewed_paths() -> None:
    assert len(REVIEWED_HEAD) == 40
    assert len(SOURCE_BLOBS) == 9
    assert all(len(sha) == 40 for sha in SOURCE_BLOBS.values())
    assert "phase165_r12_r11_prop42_unified.py" in SOURCE_BLOBS
    assert "phase165_r12_r12_ehp_consequences.py" in SOURCE_BLOBS
    assert "phase165_r55_nk_only_goal.py" in SOURCE_BLOBS


def test_r2_guard_uses_new_head_but_r1_report_retains_old_head() -> None:
    assert PREVIOUS_AUDIT_HEAD == "992975395195a0e49955617ba1ae772127036dde"
    assert REVIEWED_HEAD == "c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c"
    assert PREVIOUS_AUDIT_HEAD != REVIEWED_HEAD
    prior = validate_previous_report(previous_snapshot())
    assert prior["prior_gate"] == "PASS_READ_ONLY_ZERO_ROOT_DIAGNOSTIC"
