"""R23 source-order, lineage and read-only compatibility contracts."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r23_prop27_typed_inference_audit.audit import (
    EXACT_SEQUENCE, GENERATOR_FORMULA, HOPF_FORMULA, KERNEL_FORMULA,
    NEXT_LEMMA, PARENT_HEAD, PROP27, PROP59, REVIEWED_HEAD,
    classify_lineage, inspect_prop27_source, matches_checkout,
)


def sample_source() -> str:
    return (PROP27 + "\n" + PROP59 + "\n" + "\n".join((
        EXACT_SEQUENCE, KERNEL_FORMULA, HOPF_FORMULA, GENERATOR_FORMULA,
    )) + "\n" + NEXT_LEMMA)


def test_source_clause_order_and_independence() -> None:
    outcome = inspect_prop27_source(sample_source())
    assert outcome["general_prop27_formula_present"] is True
    assert outcome["prop59_proof_dependency_count"] == 4
    assert outcome["text_is_typed_proof_step"] is False
    assert outcome["formula_specialization_independently_certified"] is False


@pytest.mark.parametrize("clause", (PROP27, EXACT_SEQUENCE, KERNEL_FORMULA,
                                   HOPF_FORMULA, GENERATOR_FORMULA))
def test_missing_source_clause_rejected(clause: str) -> None:
    with pytest.raises(ValueError):
        inspect_prop27_source(sample_source().replace(clause, "MISSING"))


def test_reordered_proof_clauses_rejected() -> None:
    s = sample_source().replace(KERNEL_FORMULA, "TEMP").replace(
        HOPF_FORMULA, KERNEL_FORMULA).replace("TEMP", HOPF_FORMULA)
    with pytest.raises(ValueError, match="order"):
        inspect_prop27_source(s)


def test_duplicate_proof_clause_rejected() -> None:
    with pytest.raises(ValueError):
        inspect_prop27_source(sample_source().replace(HOPF_FORMULA, HOPF_FORMULA * 2))


def test_r22_merge_lineage_only() -> None:
    changed = ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",)
    assert classify_lineage(REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1,
                            changed, ()) == "R22_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,parent,commits,changed,tracked", (
    ("0" * 40, REVIEWED_HEAD, PARENT_HEAD, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, "0" * 40, PARENT_HEAD, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, "0" * 40, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 2, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1, ("proof.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1, (), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ("proof.py",)),
))
def test_unreviewed_lineage_rejected(local: str, remote: str, parent: str,
                                     commits: int, changed: tuple[str, ...],
                                     tracked: tuple[str, ...]) -> None:
    with pytest.raises(RuntimeError):
        classify_lineage(local, remote, parent, commits, changed, tracked)


def test_reviewed_windows_eol_equivalence() -> None:
    stored = b"one\r\ntwo\nthree\r\n"
    assert matches_checkout(stored, stored)
    assert matches_checkout(b"one\ntwo\nthree\n", stored)
    assert matches_checkout(b"one\r\ntwo\r\nthree\r\n", stored)
    assert not matches_checkout(b"one\ntwo\nchanged\n", stored)


def test_no_unreviewed_mathematical_proof_construction() -> None:
    module_path = Path(__file__).resolve().parents[1] / "audit.py"
    code = module_path.read_text(encoding="utf-8")
    functions = {node.name for node in ast.parse(code).body if isinstance(node, ast.FunctionDef)}
    assert not functions.intersection({"install", "apply", "patch", "register_rule", "add_given"})
    assert "git reset" not in code and "git checkout" not in code
