"""R13 evidence, source-lineage and source-first trust boundary tests."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r14_public_annihilator_connection.audit import (
    BASE_HEAD, R13_PREFIX, SOURCE_BLOBS, checked_source_blob,
    reviewed_head_lineage, validate_r13_report,
)


def sample_r13() -> dict:
    return {
        "phase": "174-R3-R7-R13",
        "gate": "PASS_ISOLATED_CITED_SOURCE_INFERENCE_PUBLIC_UNCHANGED",
        "source_order_position": 9300,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "new_production_source_given": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "live": {
            "isolated_general_source_screened_count": 1,
            "isolated_n6_inference_count": 1,
            "public_general_source_given_count": 0,
            "public_n6_goal_proposal_count": 1,
            "isolated_n6_goal_proposal_count": 2,
            "isolated_n6_inference_has_cited_parent": True,
            "public_n6_goal_proposal_rule_names": ["equality symmetry"],
            "public_provider_unchanged": True,
            "production_files_changed": False,
            "root_proof_completed": False,
        },
    }


def test_completed_r13_evidence_is_accepted_not_promoted_to_target_proof() -> None:
    prior = validate_r13_report(sample_r13())
    assert prior["isolated_ancestor_cited"] is True


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("new_production_source_given", 1),
    ("public_provider_changed", True),
    ("completion_claimed", True),
    ("full_pytest_run", True),
    ("source_order_position", 9400),
))
def test_r13_top_level_contract_fails_closed(field: str, value: object) -> None:
    report = sample_r13()
    report[field] = value
    with pytest.raises(RuntimeError):
        validate_r13_report(report)


@pytest.mark.parametrize("field,value", (
    ("isolated_general_source_screened_count", 0),
    ("isolated_n6_inference_count", 0),
    ("public_general_source_given_count", 1),
    ("public_n6_goal_proposal_count", 2),
    ("isolated_n6_goal_proposal_count", 1),
    ("isolated_n6_inference_has_cited_parent", False),
    ("public_provider_unchanged", False),
    ("production_files_changed", True),
    ("root_proof_completed", True),
))
def test_r13_proof_evidence_cannot_be_overstated(field: str, value: object) -> None:
    report = deepcopy(sample_r13())
    report["live"][field] = value
    with pytest.raises(RuntimeError):
        validate_r13_report(report)


def test_r13_symmetry_only_root_is_required() -> None:
    report = sample_r13()
    report["live"]["public_n6_goal_proposal_rule_names"] = ["cited source"]
    with pytest.raises(RuntimeError):
        validate_r13_report(report)


def test_strict_reviewed_head_or_one_r13_successor_only() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    successor = "f" * 40
    assert reviewed_head_lineage(
        successor, successor, (successor,), (R13_PREFIX + "registry.py",)
    ) == "REVIEWED_ONE_R13_ONLY_SUCCESSOR"
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(successor, successor, (successor,), ("proof.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(successor, successor, (successor, successor), (R13_PREFIX + "audit.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(successor, BASE_HEAD, (), ())


def test_fixed_pins_reject_truncated_sha_and_changed_content() -> None:
    example = b"abc\n"
    from phase174_r3_r7_r14_public_annihilator_connection.patch import git_blob_sha
    sha = git_blob_sha(example)
    assert checked_source_blob(example, sha)
    assert checked_source_blob(b"abc\r\n", sha)
    assert not checked_source_blob(example, sha[:-1])
    assert not checked_source_blob(example + b"x", sha)
    assert all(len(v) == 40 for v in SOURCE_BLOBS.values())
    assert len(SOURCE_BLOBS) == 11


def test_original_crlf_git_blob_pin_is_accepted_without_weakening_guard() -> None:
    from phase174_r3_r7_r14_public_annihilator_connection.patch import git_blob_sha

    original_crlf = b"Toda source\r\nSecond line\r\n"
    reviewed_crlf_sha = git_blob_sha(original_crlf)
    assert checked_source_blob(original_crlf, reviewed_crlf_sha)
    assert checked_source_blob(b"Toda source\nSecond line\n", reviewed_crlf_sha)
    assert not checked_source_blob(b"Toda source CHANGED\r\nSecond line\r\n", reviewed_crlf_sha)


def test_source_guard_rejects_bare_cr_mixed_endings_and_invalid_sha() -> None:
    from phase174_r3_r7_r14_public_annihilator_connection.patch import git_blob_sha

    reviewed = b"a\r\nb\r\n"
    sha = git_blob_sha(reviewed)
    assert not checked_source_blob(b"a\rb\r", sha)
    assert not checked_source_blob(b"a\r\nb\n", sha)
    assert not checked_source_blob(reviewed, sha[:-1])
    assert not checked_source_blob(reviewed, "f" * 40)
    assert SOURCE_BLOBS["sources/toda/Toda_05_2.tex"] == "579661138928499ba04a51327f686d9b971b5314"
