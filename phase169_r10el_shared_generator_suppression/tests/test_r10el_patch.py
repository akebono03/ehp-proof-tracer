"""Offline, exact-source R10EL package and patch regressions."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase169_r10el_shared_generator_suppression.patch import (
    FILES, ROOT, digest, replace_checked,
)


def test_r10el_two_reviewed_files_only():
    assert tuple(row[0] for row in FILES) == (
        "phase169_r10a_verified_stable_chain_projection/projection.py",
        "phase169_r10ec_direct_sum_narrative_projection/projection.py",
    )


def test_r10el_exact_baselines_and_full_outputs():
    for relative, old, full in FILES:
        before = (ROOT / old).read_bytes()
        expected = (ROOT / full).read_bytes()
        assert replace_checked(relative, before) == expected
        assert digest(before) != digest(expected)
        assert "hidden_indices=tuple(sorted(eligible))" not in expected.decode("utf-8")
        ast.parse(expected.decode("utf-8"))


def test_r10el_rejects_any_unreviewed_source_bytes():
    for relative, old, full in FILES:
        before = (ROOT / old).read_bytes()
        with pytest.raises(ValueError, match="unreviewed source bytes"):
            replace_checked(relative, before + b"# unreviewed\n")


def test_r10el_rejects_unreviewed_path():
    with pytest.raises(ValueError, match="not a reviewed"):
        replace_checked("phase165_r3_recursive_search.py", b"")


def test_r10el_only_existing_public_functions_changed():
    for relative, old, full in FILES:
        before = ast.parse((ROOT / old).read_text(encoding="utf-8"))
        after = ast.parse((ROOT / full).read_text(encoding="utf-8"))
        def signatures(tree):
            return [(type(n).__name__, getattr(n, "name", None)) for n in tree.body]
        assert signatures(before) == signatures(after)
        assert len(before.body) == len(after.body)
        changed = [
            a.name for a, b in zip(before.body, after.body)
            if ast.dump(a, include_attributes=False) != ast.dump(b, include_attributes=False)
        ]
        assert changed == [
            "project_verified_stable_image_chain"
            if "r10a_" in relative else "project_verified_direct_sum_transport"
        ]


def test_r10el_shared_core_is_fail_closed_and_preserves_proofsteps():
    core = (ROOT / "core.py").read_text(encoding="utf-8")
    ast.parse(core)
    assert "if require_all and hidden != eligible:" in core
    assert "not consumers.issubset(hidden | {root_index})" in core
    assert "candidate.rule is ProofRule.INFERENCE" in core
    assert "not links[index]" in core
    assert "candidate.premises" in core
    assert "ProofStep(" not in core
