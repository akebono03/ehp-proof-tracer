"""Pure trust, git lineage and Toda source contracts for R3-R7-R8."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r8_composite_image_gap.audit import (
    BASE_HEAD, REVIEWED_R7_HEAD, REVIEWED_PREFIX, EXPECTED_R7,
    SOURCE_BLOBS, TODA_CLAUSES, accepts_blob, blob_sha,
    describe_candidate_options, reviewed_head_lineage,
    validate_r7_evidence, verify_toda_source,
)


def sample_r7() -> dict:
    return {
        "phase": "174-R3-R7-R7",
        "gate": "PASS_ISOLATED_COMPOSITE_ZERO_CHILDREN_PENDING",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "isolated_generator_zero_candidate_count": 1,
            "public_composite_image_frontier": {"proposal_count": 0},
            "public_left_factor_zero_frontier": {"proposal_count": 1},
            "public_generator_zero_frontier": {"proposal_count": 0},
            "candidate_from_toda_text_is_not_evidence": True,
            "public_provider_unchanged": True,
            "new_verified_steps": 0,
        },
    }


def test_accepts_r7_certified_live_report_without_certifying_new_proof() -> None:
    result = validate_r7_evidence(sample_r7())
    assert result["observed_counts"] == EXPECTED_R7
    assert result["observed_counts"]["public_composite_image_frontier"] == 0


@pytest.mark.parametrize("wrong", (
    "phase", "gate", "given", "production", "provider", "completion",
))
def test_invalid_prior_gate_or_proof_mutation_is_rejected(wrong: str) -> None:
    report = sample_r7()
    if wrong == "phase":
        report["phase"] = "174-R3-R7-R6"
    elif wrong == "gate":
        report["gate"] = "PASS_PREFLIGHT"
    elif wrong == "given":
        report["new_group_given"] = 1
    elif wrong == "production":
        report["new_production_inference_rules"] = 1
    elif wrong == "provider":
        report["public_provider_changed"] = True
    else:
        report["completion_claimed"] = True
    with pytest.raises(RuntimeError):
        validate_r7_evidence(report)


@pytest.mark.parametrize("key,count", (
    ("isolated_generator_zero_candidate_count", 0),
    ("public_composite_image_frontier", 1),
    ("public_left_factor_zero_frontier", 0),
    ("public_generator_zero_frontier", 1),
))
def test_prior_live_counts_cannot_be_fabricated(key: str, count: int) -> None:
    report = sample_r7()
    if key == "isolated_generator_zero_candidate_count":
        report["live"][key] = count
    else:
        report["live"][key]["proposal_count"] = count
    with pytest.raises(RuntimeError):
        validate_r7_evidence(report)


@pytest.mark.parametrize("key,value", (
    ("candidate_from_toda_text_is_not_evidence", False),
    ("public_provider_unchanged", False),
    ("new_verified_steps", 1),
))
def test_prior_candidate_must_remain_unproved(key: str, value: object) -> None:
    report = sample_r7()
    report["live"][key] = value
    with pytest.raises(RuntimeError):
        validate_r7_evidence(report)


def test_reviewed_git_lineage_accepts_only_previous_r7_commit() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    assert reviewed_head_lineage(
        REVIEWED_R7_HEAD, REVIEWED_R7_HEAD,
        (REVIEWED_R7_HEAD,),
        (REVIEWED_PREFIX + "audit.py",),
    ) == "REVIEWED_R7_ONLY_SUCCESSOR"


@pytest.mark.parametrize("local,remote,commits,paths", (
    (BASE_HEAD, REVIEWED_R7_HEAD, (), ()),
    ("a" * 40, "a" * 40, ("a" * 40,), (REVIEWED_PREFIX + "audit.py",)),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (), (REVIEWED_PREFIX + "audit.py",)),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (REVIEWED_R7_HEAD,), ("proof.py",)),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (REVIEWED_R7_HEAD,), ()),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (BASE_HEAD, REVIEWED_R7_HEAD),
     (REVIEWED_PREFIX + "audit.py",)),
))
def test_unreviewed_or_mismatched_lineage_rejected(
    local: str, remote: str, commits: tuple[str, ...], paths: tuple[str, ...],
) -> None:
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(local, remote, commits, paths)


def test_blob_guard_normalizes_newlines_only() -> None:
    source = b"source\nclaim\n"
    expected = blob_sha(source)
    assert accepts_blob(source, expected)
    assert accepts_blob(b"source\r\nclaim\r\n", expected)
    assert not accepts_blob(b"source\nfalse\n", expected)


def test_toda_transcription_source_order_and_independent_claims(tmp_path: Path) -> None:
    file = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    file.parent.mkdir(parents=True)
    file.write_text(
        "\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_CLAUSES["general_nu_eta_zero"] + "\n"
        + TODA_CLAUSES["generator_suspension_composite"] + "\n"
        + TODA_CLAUSES["whole_suspension_zero_conclusion"] + "\n"
        + "\\qed\n", encoding="utf-8",
    )
    result = verify_toda_source(tmp_path)
    assert result["general_formula_is_not_a_certified_step"] is True
    assert result["derived_generator_image_not_given"] is True


def test_toda_transcription_rejects_wrong_order(tmp_path: Path) -> None:
    file = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    file.parent.mkdir(parents=True)
    file.write_text(
        "\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_CLAUSES["whole_suspension_zero_conclusion"] + "\n"
        + TODA_CLAUSES["general_nu_eta_zero"] + "\n"
        + TODA_CLAUSES["generator_suspension_composite"] + "\n"
        + "\\qed\n", encoding="utf-8",
    )
    with pytest.raises(RuntimeError):
        verify_toda_source(tmp_path)


def test_describes_composite_expansions_without_proof_promotion() -> None:
    data = describe_candidate_options((
        SimpleNamespace(rule=SimpleNamespace(name="generic composition"),
                        subgoals=("factor one", "factor two")),
    ))
    assert len(data) == 1
    assert data[0]["rule"] == "generic composition"
    assert data[0]["child_count"] == 2
    assert [child["repr"] for child in data[0]["children"]] == [
        "'factor one'", "'factor two'",
    ]


def test_rejects_bad_proposal_shapes() -> None:
    with pytest.raises(TypeError):
        describe_candidate_options([])
    with pytest.raises(TypeError):
        describe_candidate_options((SimpleNamespace(subgoals=[]),))


def test_no_production_mutation_in_audit_source() -> None:
    script = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(script.read_text(encoding="utf-8"))
    function_names = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "inspect_source_screened_frontier" in function_names
    assert "validate_r7_evidence" in function_names
    assert not {"install", "patch", "register_given", "modify_production"} & function_names
    assert len(SOURCE_BLOBS) == 12

def test_pinned_sha1_contract_uses_full_40_character_git_blob_hashes() -> None:
    """Prevent the 39-character pinned generic-isomorphism SHA regression."""
    assert all(
        isinstance(sha, str)
        and len(sha) == 40
        and all(letter in "0123456789abcdef" for letter in sha)
        for sha in SOURCE_BLOBS.values()
    )
    assert (
        SOURCE_BLOBS["phase165_r14_r6_generic_iso.py"]
        == "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7"
    )
