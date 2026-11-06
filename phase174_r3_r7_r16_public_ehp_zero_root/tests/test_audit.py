"""R16 reviewed lineage, source pins, and R15 evidence contract tests."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r16_public_ehp_zero_root.audit import (
    PINS, PRE_R15_HEAD, REVIEWED_HEAD, R15_PREFIX,
    matches_blob, validate_lineage, validate_r15_report,
)
from phase174_r3_r7_r16_public_ehp_zero_root.patch import TARGET, blob_sha


def sample_r15() -> dict:
    return {
        "phase": "174-R3-R7-R15",
        "gate": "PASS_READ_ONLY_CHAIN_FRONTIER_NO_ROOT_CLAIM",
        "full_pytest_run": False,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "completion_claimed": False,
        "live": {
            "new_verified_proof_steps": 0,
            "public_provider_changed": False,
            "public_goal_frontiers": {"final_pi12_7_zero": {"count": 0}},
        },
    }


def test_r15_evidence_never_becomes_root_proof() -> None:
    result = validate_r15_report(sample_r15())
    assert result["root_candidates_before"] == 0
    assert result["new_verifications_before"] == 0


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("full_pytest_run", True),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("completion_claimed", True),
))
def test_prior_report_corruption_fails_closed(field: str, value: object) -> None:
    report = sample_r15()
    report[field] = value
    with pytest.raises(RuntimeError):
        validate_r15_report(report)


@pytest.mark.parametrize("field,value", (
    ("new_verified_proof_steps", 1),
    ("public_provider_changed", True),
))
def test_r15_live_candidate_cannot_be_promoted(field: str, value: object) -> None:
    report = deepcopy(sample_r15())
    report["live"][field] = value
    with pytest.raises(RuntimeError):
        validate_r15_report(report)


def test_r15_zero_root_baseline_must_be_real() -> None:
    report = sample_r15()
    report["live"]["public_goal_frontiers"]["final_pi12_7_zero"]["count"] = 1
    with pytest.raises(RuntimeError):
        validate_r15_report(report)


def test_reviewed_two_local_layouts_accept_only_one_r15_successor() -> None:
    paths = (R15_PREFIX + "audit.py", R15_PREFIX + "tests/test_contract.py")
    assert validate_lineage(PRE_R15_HEAD, REVIEWED_HEAD, paths, (), False) == "R15_MERGED_REMOTE_LOCAL_R14"
    assert validate_lineage(REVIEWED_HEAD, REVIEWED_HEAD, paths, (), False) == "R15_MERGED_CLEAN"
    assert validate_lineage(PRE_R15_HEAD, REVIEWED_HEAD, paths, (TARGET.as_posix(),), True) == "R15_MERGED_REMOTE_LOCAL_R14"
    assert validate_lineage(REVIEWED_HEAD, REVIEWED_HEAD, paths, (TARGET.as_posix(),), True) == "R15_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,paths,modified,patched", (
    (PRE_R15_HEAD, PRE_R15_HEAD, (R15_PREFIX + "audit.py",), (), False),
    ("f" * 40, REVIEWED_HEAD, (R15_PREFIX + "audit.py",), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, ("proof.py",), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, (), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, (R15_PREFIX + "audit.py",), ("proof.py",), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, (R15_PREFIX + "audit.py",), (), True),
))
def test_unreviewed_git_state_never_passes(
    local: str, remote: str, paths: tuple[str, ...],
    modified: tuple[str, ...], patched: bool,
) -> None:
    with pytest.raises(RuntimeError):
        validate_lineage(local, remote, paths, modified, patched)


def test_pinned_git_blobs_reject_mixed_endings_and_mutations() -> None:
    reference = b"Toda source\nnext line\n"
    sha = blob_sha(reference)
    assert matches_blob(reference, sha)
    assert matches_blob(b"Toda source\r\nnext line\r\n", sha)
    assert not matches_blob(b"Toda source\r\nnext line\n", sha)
    assert not matches_blob(reference + b"change", sha)
    assert not matches_blob(reference, sha[:-1])
    assert len(PINS) >= 6
    assert all(len(s) == 40 for s in PINS.values())
