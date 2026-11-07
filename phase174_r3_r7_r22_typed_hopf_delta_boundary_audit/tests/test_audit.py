"""R22 source/lineage and proof-boundary focused contracts."""
from __future__ import annotations

import ast
from pathlib import Path
import pytest

from phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit import (
    CLAUSES, END, PARENT_HEAD, REVIEWED_HEAD, START,
    classify_lineage, inspect_source, matches_checkout,
)


def example_source() -> str:
    return (r"H\Delta(\iota_{2n+1}) = \pm2\iota_{2m-1}" + "\n" + START
            + "\n" + "\n".join(CLAUSES) + "\n" + END)


def test_source_chain_remains_seven_independent_text_clauses() -> None:
    result = inspect_source(example_source())
    assert result["adopted_source_clauses"] == 7
    assert result["source_is_verified_proof_step"] is False
    assert result["original_print_edition_verified"] is False


@pytest.mark.parametrize("token", CLAUSES)
def test_missing_clause_fails_closed(token: str) -> None:
    with pytest.raises(ValueError):
        inspect_source(example_source().replace(token, "MISSING"))


def test_reordered_clause_fails_closed() -> None:
    first, second = CLAUSES[2], CLAUSES[3]
    bad = example_source().replace(first, "HOLDER").replace(second, first).replace("HOLDER", second)
    with pytest.raises(ValueError, match="order"):
        inspect_source(bad)


def test_reviewed_clean_and_untracked_handoff_lineage() -> None:
    paths = ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",
             "phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py")
    assert classify_lineage(REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, paths, 1, ()) == "R21_MERGED_CLEAN"
    assert classify_lineage(PARENT_HEAD, REVIEWED_HEAD, PARENT_HEAD, paths, 1, ()) == "R21_MERGED_REMOTE_PARENT_LOCAL_UNTRACKED_HANDOFF"


@pytest.mark.parametrize("local,remote,parent,paths,count,tracked", [
    ("x" * 40, REVIEWED_HEAD, PARENT_HEAD, ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",), 1, ()),
    (REVIEWED_HEAD, "x" * 40, PARENT_HEAD, ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, "x" * 40, ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, ("proof.py",), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, (), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, ("phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py",), 2, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, ("phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py",), 1, ("proof.py",)),
])
def test_unreviewed_lineage_fails(local: str, remote: str, parent: str,
                                  paths: tuple[str, ...], count: int,
                                  tracked: tuple[str, ...]) -> None:
    with pytest.raises(RuntimeError):
        classify_lineage(local, remote, parent, paths, count, tracked)


def test_checkout_whole_file_EOL_variants() -> None:
    stored = b"alpha\r\nbeta\ngamma\r\n"
    assert matches_checkout(stored, stored)
    assert matches_checkout(b"alpha\nbeta\ngamma\n", stored)
    assert matches_checkout(b"alpha\r\nbeta\r\ngamma\r\n", stored)
    assert not matches_checkout(b"alpha\nbeta\nCHANGED\n", stored)


def test_readonly_audit_has_no_proof_registration_or_installer() -> None:
    source = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert not names.intersection({"install", "patch", "register_rule", "insert_given", "add_proof_step"})
    assert "git reset" not in source
    assert "git checkout" not in source
