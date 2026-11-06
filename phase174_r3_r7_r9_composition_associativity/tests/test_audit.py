"""Source-first, prior-evidence and SHA guards for the R9 audit."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r9_composition_associativity.audit import (
    REVIEWED_HEAD, SOURCE_BLOBS, TODA_CLAUSES,
    accepted_source_blob, git_blob_sha, validate_r8_evidence,
    verify_git_and_sources,
)


def sample_r8() -> dict:
    return {
        "phase": "174-R3-R7-R8",
        "gate": "PASS_READ_ONLY_COMPOSITE_IMAGE_GAP_DIAGNOSIS",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "public_composite_image_frontier": {"proposal_count": 0},
            "public_left_factor_zero_frontier": {"proposal_count": 1},
            "public_generator_zero_frontier": {"proposal_count": 0},
            "existing_composite_image_rule_candidate_count": 0,
            "left_factor_rule_name": "equality symmetry",
            "source_generator_type": "Composition",
            "public_provider_unchanged": True,
            "source_claim_promoted_to_given": False,
        },
    }


def test_r8_observed_evidence_is_not_promoted_to_proof() -> None:
    verified = validate_r8_evidence(sample_r8())
    assert verified["previous_composite_options"] == 0
    assert verified["previous_left_factor_rule_is_symmetry_only"]
    assert verified["prior_completion_claimed"] is False


@pytest.mark.parametrize("change", (
    "gate", "given", "production", "unproved", "left_factor_rule", "generator_type",
))
def test_r8_contract_fails_closed(change: str) -> None:
    report = sample_r8()
    if change == "gate":
        report["gate"] = "PASS_PREFLIGHT"
    elif change == "given":
        report["new_group_given"] = 1
    elif change == "production":
        report["new_production_inference_rules"] = 1
    elif change == "unproved":
        report["live"]["source_claim_promoted_to_given"] = True
    elif change == "left_factor_rule":
        report["live"]["left_factor_rule_name"] = "unverified source direct GIVEN"
    else:
        report["live"]["source_generator_type"] = "Other"
    with pytest.raises(RuntimeError):
        validate_r8_evidence(report)


@pytest.mark.parametrize("key,count", (
    ("public_composite_image_frontier", 1),
    ("public_left_factor_zero_frontier", 0),
    ("public_generator_zero_frontier", 1),
))
def test_prior_candidate_counts_are_not_guessed(key: str, count: int) -> None:
    report = sample_r8()
    report["live"][key]["proposal_count"] = count
    with pytest.raises(RuntimeError, match="observed frontier changed"):
        validate_r8_evidence(report)


def test_full_sha_guard_accepts_crlf_only_and_rejects_truncation() -> None:
    source = b"A\nB\n"
    sha = git_blob_sha(source)
    assert accepted_source_blob(source, sha)
    assert accepted_source_blob(b"A\r\nB\r\n", sha)
    assert not accepted_source_blob(b"A\nC\n", sha)
    assert not accepted_source_blob(source, sha[:-1])
    assert all(len(value) == 40 for value in SOURCE_BLOBS.values())
    assert len(REVIEWED_HEAD) == 40


def test_toda_annihilator_and_generator_suspension_are_separate_claims() -> None:
    assert "n\\ge6" in TODA_CLAUSES["general_annihilator"]
    assert "nu_6" in TODA_CLAUSES["generator_suspension"]
    assert TODA_CLAUSES["zero_image_conclusion"] == r"E\pi_{10}^5=0"


def test_audit_has_no_production_mutation_methods() -> None:
    path = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "verify_git_and_sources" in names
    assert "inspect_rebracketing_frontier" in names
    assert not {"patch", "install", "register_given", "change_public_provider"} & names


def test_source_guard_rejects_any_unreviewed_head_before_reading_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r9_composition_associativity.audit as mod

    def fake_git(*args: str, cwd: Path = tmp_path) -> str:
        answers = {
            ("rev-parse", "--show-toplevel"): str(tmp_path),
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): "a" * 40,
            ("ls-remote", "origin", "refs/heads/develop"):
                "a" * 40 + "\trefs/heads/develop",
        }
        if args not in answers:
            raise AssertionError("Unexpected call to git " + repr(args))
        return answers[args]

    monkeypatch.setattr(mod, "git", fake_git)
    with pytest.raises(RuntimeError, match="Unreviewed develop HEAD"):
        verify_git_and_sources(tmp_path)
