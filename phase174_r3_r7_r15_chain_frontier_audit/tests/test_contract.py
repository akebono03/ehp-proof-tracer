"""Read-only audit guards; intentionally no production source modification."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r15_chain_frontier_audit.audit import (
    PINS, PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, R14_DIR, R14_SHARED_BLOB,
    SHARED_MATH, blob_sha, classify_frontier, matches_pinned_blob,
    reviewed_lineage, summarize_options, validate_r14_report,
)


def sample_committed_paths() -> tuple[str, ...]:
    return (SHARED_MATH, R14_DIR + "audit.py", R14_DIR + "tests/test_public.py")


def sample_r14_report() -> dict:
    return {
        "phase": "174-R3-R7-R14",
        "gate": "PASS_PUBLIC_CITED_GENERAL_SOURCE_N6_INFERENCE_ROOT_PENDING",
        "new_group_given": 0,
        "new_direct_concrete_relation_given": 0,
        "full_pytest_run": False,
        "completion_claimed": False,
        "live": {
            "public_general_source_givens": 1,
            "public_n6_specialization_proposals": 1,
            "public_n6_cited_parent": True,
            "new_group_given": 0,
            "goal_complete_claimed": False,
        },
    }


def test_handoff_and_merged_lineages_are_both_guarded() -> None:
    paths = sample_committed_paths()
    assert reviewed_lineage(
        PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, paths, (SHARED_MATH,),
    ) == "LOCAL_PRE_R14_WITH_EXACT_WORKTREE_PATCH"
    assert reviewed_lineage(
        REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, paths, (),
    ) == "R14_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,paths,tracked", (
    (PRE_R14_HEAD, PRE_R14_HEAD, sample_committed_paths(), (SHARED_MATH,)),
    ("a" * 40, REVIEWED_REMOTE_HEAD, sample_committed_paths(), ()),
    (REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, (SHARED_MATH, "proof.py"), ()),
    (REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, (R14_DIR + "audit.py",), ()),
    (PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, sample_committed_paths(), ("proof.py",)),
    (REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, sample_committed_paths(), (SHARED_MATH,)),
))
def test_lineage_rejects_unreviewed_state(
    local: str, remote: str, paths: tuple[str, ...], tracked: tuple[str, ...],
) -> None:
    with pytest.raises(RuntimeError):
        reviewed_lineage(local, remote, paths, tracked)


def test_pinned_blobs_allow_only_uniform_line_ends() -> None:
    raw = b"a\nb\n"
    sha = blob_sha(raw)
    assert matches_pinned_blob(raw, sha)
    assert matches_pinned_blob(b"a\r\nb\r\n", sha)
    assert not matches_pinned_blob(b"a\r\nb\n", sha)
    assert not matches_pinned_blob(b"a\rb\r", sha)
    assert not matches_pinned_blob(raw + b"c", sha)
    assert not matches_pinned_blob(raw, sha[:39])
    assert len(R14_SHARED_BLOB) == 40
    assert len(PINS) >= 10


def test_r14_success_is_read_as_inference_not_root_completion() -> None:
    checked = validate_r14_report(sample_r14_report())
    assert checked["n6_inference_has_cited_parent"] is True
    assert checked["root_complete"] is False


@pytest.mark.parametrize("key,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_direct_concrete_relation_given", 1),
    ("full_pytest_run", True),
    ("completion_claimed", True),
))
def test_bad_r14_top_level_evidence_fails_closed(key: str, value: object) -> None:
    report = sample_r14_report()
    report[key] = value
    with pytest.raises(RuntimeError):
        validate_r14_report(report)


@pytest.mark.parametrize("key,value", (
    ("public_general_source_givens", 0),
    ("public_n6_specialization_proposals", 0),
    ("public_n6_cited_parent", False),
    ("new_group_given", 1),
    ("goal_complete_claimed", True),
))
def test_bad_r14_proof_evidence_fails_closed(key: str, value: object) -> None:
    report = deepcopy(sample_r14_report())
    report["live"][key] = value
    with pytest.raises(RuntimeError):
        validate_r14_report(report)


def test_cannot_promote_isolated_candidate_to_proof() -> None:
    assert classify_frontier((), "generic") == "NO_PUBLIC_CANDIDATE_OBSERVED"
    assert classify_frontier(("other",), "generic") == "OTHER_PUBLIC_CANDIDATES_UNVERIFIED"
    assert classify_frontier(("generic",), "generic") == "NAMED_RULE_PRESENT_CANDIDATE_NOT_PROOF"


def test_provider_summary_rejects_non_expansion() -> None:
    with pytest.raises(TypeError):
        summarize_options((object(),))
    with pytest.raises(TypeError):
        summarize_options([])
