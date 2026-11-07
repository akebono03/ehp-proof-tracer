"""Read-only source and Git-lineage guards for R19."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r19_delta_generator_source_audit.audit import (
    ALLOWED_MERGE_PREFIXES,
    PINS,
    PRIOR_HEAD,
    PROP_GROUP,
    PROP_START,
    PROOF_HOPF_IMAGE,
    PROOF_ROOT_ZERO,
    PROOF_SUSPENSION_ZERO,
    R18_AUDIT_PATH,
    REVIEWED_HEAD,
    classify_lineage,
    git_blob_sha,
    inspect_generator_row,
    inspect_toda_proposition,
    matches_reviewed_checkout,
)


def _merge_paths() -> tuple[str, ...]:
    return (R18_AUDIT_PATH, ALLOWED_MERGE_PREFIXES[0] + "patch.py",
            ALLOWED_MERGE_PREFIXES[1] + "patch.py")


def test_accept_only_two_reviewed_lineage_states() -> None:
    assert classify_lineage(REVIEWED_HEAD, REVIEWED_HEAD, (), _merge_paths(), 1) == (
        "R18R2_MERGED_CLEAN"
    )
    assert classify_lineage(PRIOR_HEAD, REVIEWED_HEAD, (R18_AUDIT_PATH,), _merge_paths(), 1) == (
        "R18R2_PATCH_UNCOMMITTED_MATCH_REMOTE"
    )


@pytest.mark.parametrize("local,remote,tracked,changed,commits", (
    ("a" * 40, REVIEWED_HEAD, (), _merge_paths(), 1),
    (REVIEWED_HEAD, "b" * 40, (), _merge_paths(), 1),
    (PRIOR_HEAD, REVIEWED_HEAD, (), _merge_paths(), 1),
    (REVIEWED_HEAD, REVIEWED_HEAD, (R18_AUDIT_PATH,), _merge_paths(), 1),
    (PRIOR_HEAD, REVIEWED_HEAD, (R18_AUDIT_PATH, "other.py"), _merge_paths(), 1),
    (REVIEWED_HEAD, REVIEWED_HEAD, (), _merge_paths(), 0),
    (REVIEWED_HEAD, REVIEWED_HEAD, (), _merge_paths(), 2),
    (REVIEWED_HEAD, REVIEWED_HEAD, (), ("unknown.py",), 1),
    (REVIEWED_HEAD, REVIEWED_HEAD, (), (R18_AUDIT_PATH, "proof.py"), 1),
))
def test_reject_unreviewed_lineage(local: str, remote: str,
                                  tracked: tuple[str, ...],
                                  changed: tuple[str, ...], commits: int) -> None:
    with pytest.raises(RuntimeError):
        classify_lineage(local, remote, tracked, changed, commits)


def test_mixed_git_eols_and_exact_checkout_variants() -> None:
    stored = b"first\r\nsecond\nthird\r\n"
    pinned = git_blob_sha(stored)
    assert matches_reviewed_checkout(stored, stored, pinned)
    assert matches_reviewed_checkout(b"first\nsecond\nthird\n", stored, pinned)
    assert matches_reviewed_checkout(b"first\r\nsecond\r\nthird\r\n", stored, pinned)
    assert not matches_reviewed_checkout(stored + b"unreviewed", stored, pinned)
    assert not matches_reviewed_checkout(stored, stored, "0" * 40)


def _prop_text() -> str:
    return (PROP_START + "\n" + PROP_GROUP + "\n\\end{proposition}\n"
            + PROOF_SUSPENSION_ZERO + "\n" + PROOF_HOPF_IMAGE + "\n"
            + PROOF_ROOT_ZERO + "\n\\qed\n")


def test_toda_source_clause_contract() -> None:
    result = inspect_toda_proposition(_prop_text())
    assert result["proposition_lists_free_cyclic_generator"]
    assert result["proposition_group_result_is_not_independent_given"]
    assert result["original_print_edition_verified"] is False


@pytest.mark.parametrize("tamper", (PROP_GROUP, PROOF_HOPF_IMAGE, PROOF_ROOT_ZERO,
                                     PROOF_SUSPENSION_ZERO))
def test_toda_missing_clause_refused(tamper: str) -> None:
    with pytest.raises(RuntimeError):
        inspect_toda_proposition(_prop_text().replace(tamper, "[MISSING]"))


def test_toda_wrong_proof_order_refused() -> None:
    modified = _prop_text().replace(PROOF_SUSPENSION_ZERO, "[TEMP]").replace(
        PROOF_HOPF_IMAGE, PROOF_SUSPENSION_ZERO).replace("[TEMP]", PROOF_HOPF_IMAGE)
    with pytest.raises(RuntimeError, match="order"):
        inspect_toda_proposition(modified)


def _csv() -> str:
    return "id,display,kinds,k,n,latex\n5,Δ(ι13),1,5,6,\\Delta(\\iota_{13})\n"


def test_notation_db_is_not_a_proof() -> None:
    report = inspect_generator_row(_csv())
    assert report["display"] == "Δ(ι13)"
    assert report["database_row_is_proof"] is False
    assert report["typed_delta_application_in_csv"] is False


@pytest.mark.parametrize("tamper", (
    "5,Δ(ι13),1,6,6,", "5,Δ(ι13),0,5,6,", "5,Δ(ι15),1,5,6,",
))
def test_wrong_generator_row_refused(tamper: str) -> None:
    with pytest.raises(RuntimeError):
        inspect_generator_row(_csv().replace("5,Δ(ι13),1,5,6,", tamper))


def test_source_pins_production_untouched() -> None:
    assert len(PINS) >= 12
    assert "sources/toda/Toda_05_2.tex" in PINS
    assert "phase174_r3_r7_r18_delta_image_surjectivity/rule.py" in PINS
    assert "phase165_r57_r19_delta_image_backward.py" in PINS
    assert "phase166_r3aj_structured_generator.py" in PINS
    assert all(len(digest) == 40 for digest in PINS.values())


def test_audit_has_no_install_or_unreviewed_proof_steps() -> None:
    source = Path(__file__).resolve().parents[1].joinpath("audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {item.name for item in tree.body if isinstance(item, ast.FunctionDef)}
    assert not names.intersection({"install", "patch", "apply", "build_given", "add_proof_step"})
    assert "git reset" not in source
    assert "git checkout" not in source
