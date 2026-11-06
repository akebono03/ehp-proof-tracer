"""R11 strict source, lineage and diagnostic provenance contract tests."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r11_canonical_fixture_audit.audit import (
    BASE_HEAD,
    REVIEWED_SUCCESSOR_PREFIX,
    SOURCE_BLOBS,
    reviewed_head_lineage,
    strict_family_comparison,
    validate_r10_evidence,
)


def sample_r10() -> dict:
    return {
        "phase": "174-R3-R7-R10",
        "gate": "PASS_READ_ONLY_CITED_FAMILY_OBLIGATIONS",
        "new_group_given": 0,
        "new_production_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "public_original_left_image_frontier": {"proposal_count": 0},
            "public_canonical_nu_image_frontier": {"proposal_count": 1},
            "public_right_factor_image_frontier": {"proposal_count": 1},
            "public_right_associated_image_frontier": {"proposal_count": 1},
            "source_matches_canonical": True,
            "target_matches_canonical": False,
            "screened_nu_family_given_count": 1,
            "isolated_cited_family_candidate_count": 1,
            "nu_family_definition_position_verified": True,
            "public_provider_unchanged": True,
            "new_verified_steps": 0,
            "toda_general_annihilator_directly_admitted": False,
        },
    }


def test_r10_certified_evidence_is_accepted_without_proof_promotion() -> None:
    checked = validate_r10_evidence(sample_r10())
    assert checked["original_target_noncanonical"] is True
    assert checked["canonical_nu_proposals"] == 1
    assert checked["new_verified_steps"] == 0


@pytest.mark.parametrize("field,bad", (
    ("phase", "174-R3-R7-R9"),
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_production_rules", 1),
    ("public_provider_changed", True),
    ("completion_claimed", True),
))
def test_r10_trust_boundary_rejects_mutated_claims(field: str, bad: object) -> None:
    source = sample_r10()
    source[field] = bad
    with pytest.raises(RuntimeError):
        validate_r10_evidence(source)


@pytest.mark.parametrize("field,bad", (
    ("public_original_left_image_frontier", 1),
    ("public_canonical_nu_image_frontier", 0),
    ("public_right_factor_image_frontier", 0),
    ("public_right_associated_image_frontier", 0),
))
def test_r10_candidate_counts_are_not_fabricated(field: str, bad: int) -> None:
    source = sample_r10()
    source["live"][field]["proposal_count"] = bad
    with pytest.raises(RuntimeError, match="observed proposal"):
        validate_r10_evidence(source)


@pytest.mark.parametrize("field,bad", (
    ("source_matches_canonical", False),
    ("target_matches_canonical", True),
    ("screened_nu_family_given_count", 0),
    ("isolated_cited_family_candidate_count", 0),
    ("nu_family_definition_position_verified", False),
    ("public_provider_unchanged", False),
    ("new_verified_steps", 1),
    ("toda_general_annihilator_directly_admitted", True),
))
def test_r10_symbol_provenance_is_not_overstated(field: str, bad: object) -> None:
    source = sample_r10()
    source["live"][field] = bad
    with pytest.raises(RuntimeError, match="symbol gap"):
        validate_r10_evidence(source)


def test_base_head_only_with_exactly_matching_remote() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(BASE_HEAD, "f" * 40, (), ())


def test_one_restricted_r10_successor_is_accepted() -> None:
    later = "a" * 40
    assert reviewed_head_lineage(
        later, later, (later,),
        (REVIEWED_SUCCESSOR_PREFIX + "audit.py",),
    ) == "REVIEWED_ONE_R10_ONLY_SUCCESSOR"


@pytest.mark.parametrize("commits,paths", (
    (("a" * 40, "b" * 40), (REVIEWED_SUCCESSOR_PREFIX + "audit.py",)),
    (("b" * 40,), ("proof.py",)),
    (("b" * 40,), (REVIEWED_SUCCESSOR_PREFIX + "audit.py", "README.md")),
    ((), (REVIEWED_SUCCESSOR_PREFIX + "audit.py",)),
    (("b" * 40,), ()),
))
def test_lineage_never_allows_unreviewed_changes(
    commits: tuple[str, ...], paths: tuple[str, ...],
) -> None:
    with pytest.raises(RuntimeError):
        reviewed_head_lineage("b" * 40, "b" * 40, commits, paths)


def test_symbol_comparison_is_full_metadata_not_ascii_guess() -> None:
    registered = SimpleNamespace(
        name="ν₆", dimension=6, source=9, target=6,
        generator=SimpleNamespace(family="ν", index=6),
    )
    diagnostic = SimpleNamespace(
        name="nu_6", dimension=6, source=9, target=6,
        generator=SimpleNamespace(family="nu", index=6),
    )
    result = strict_family_comparison(diagnostic, registered)
    assert result["exactly_equal"] is False
    assert "generator" in result["different_attributes"]
    assert "name" in result["different_attributes"]
    assert result["can_use_as_proof_of_equality"] is False


def test_same_display_name_with_different_symbol_is_not_equal() -> None:
    registered = SimpleNamespace(
        name="ν₆", dimension=6, source=9, target=6,
        generator=SimpleNamespace(family="ν", index=6),
    )
    wrong = SimpleNamespace(
        name="ν₆", dimension=6, source=9, target=6,
        generator=SimpleNamespace(family="nu", index=6),
    )
    result = strict_family_comparison(wrong, registered)
    assert result["exactly_equal"] is False
    assert result["different_attributes"] == ["generator"]


def test_pinned_files_are_all_full_git_blob_shas() -> None:
    assert len(SOURCE_BLOBS) == 14
    assert all(len(sha) == 40 and all(ch in "0123456789abcdef" for ch in sha)
               for sha in SOURCE_BLOBS.values())
    assert SOURCE_BLOBS["data/HyoujiGen.csv"] == "26f33db0c83ba7f151433583fe861598399cbe6a"


def test_audit_is_read_only_and_requires_source_first() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {
        "verify_git_and_sources", "validate_r10_evidence",
        "strict_family_comparison", "inspect_live_frontier", "make_report",
    } <= functions
    assert not {"install", "patch", "register_given", "mutate_production"} & functions
    body = source.read_text(encoding="utf-8")
    assert "screen_independent_sources_for_derived_goal" in body
    assert "public_provider_unchanged" in body
