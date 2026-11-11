"""R71 pure regression guard checks (full suite is intentionally excluded)."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r71_common_narrative_regression.audit import (
    COMPLETE_CASES, EXPECTED_REFERENCE_COUNTS, PINS, git_blob_sha,
    reference_body_contract, source_guard,
)
from phase174_r3_r7_r70_verified_narrative_projection.projection import (
    project_verified_general_narrative,
)


def test_source_guard_matches_reviewed_develop() -> None:
    root = Path(__file__).resolve().parents[2]
    assert source_guard(root) == tuple(PINS)


def test_source_guard_fails_closed_for_unreviewed_source(tmp_path: Path) -> None:
    path = next(iter(PINS))
    target = tmp_path / path
    target.parent.mkdir(parents=True)
    target.write_bytes(b"# unexpected source change\n")
    with pytest.raises(RuntimeError, match="R71_UNREVIEWED_SOURCE"):
        source_guard(tmp_path)


def test_git_blob_identity_is_stable() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_complete_reference_contract_accepts_one_reference_and_proof() -> None:
    sample = "使用する結果\n\n[R1] (5.9).\n\n証明\n\n[R1]より, $x=0$.\n\n□\n"
    references, proof = reference_body_contract(sample, 1)
    assert "[R1]" in references
    assert "$x=0$" in proof


def test_complete_reference_contract_rejects_missing_reference() -> None:
    sample = "使用する結果\n\n[R1] (5.9).\n\n証明\n\n$x=0$.\n\n□\n"
    with pytest.raises(RuntimeError, match="R71_MISSING_REFERENCE_R2"):
        reference_body_contract(sample, 2)


def test_complete_reference_contract_rejects_invalid_double_tex_arrow() -> None:
    sample = r"使用する結果" + "\n\n[R1] ref.\n\n証明\n\n" + r"$E:A\\to B$" + ".\n\n□\n"
    with pytest.raises(RuntimeError, match="R71_DOUBLE_ESCAPED_TEX_ARROW"):
        reference_body_contract(sample, 1)


def test_unverified_partial_model_is_unmodified_by_r70_projection() -> None:
    model = SimpleNamespace(root_index=None)
    lines = ["## 証明対象", "", r"$\pi_{12}^{4}$", "", "## 未解決 Goal"]
    assert project_verified_general_narrative(lines, model) is lines


def test_public_sample_contract_is_unique_and_contains_r70_baselines() -> None:
    assert len(COMPLETE_CASES) == len(set(COMPLETE_CASES)) == 8
    assert {(3, 3), (6, 5), (7, 5)} <= set(COMPLETE_CASES)
    assert EXPECTED_REFERENCE_COUNTS == {
        (3, 3): 8, (6, 5): 7, (7, 5): 3,
    }
