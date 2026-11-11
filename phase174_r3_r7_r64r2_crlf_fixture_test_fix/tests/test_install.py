"""R64R2 focused, fail-closed EOL fixture regression tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r64r2_crlf_fixture_test_fix.install import (
    EXPECTED_FIXED_BLOB,
    EXPECTED_OLD_BLOB,
    ORIGINAL_FUNCTION,
    PINNED_UNCHANGED,
    REPLACEMENT_FUNCTION,
    TARGET,
    git_blob_sha,
    normalized_contents,
    patch_test,
    review,
)


def fixture_root(tmp_path: Path, *, eol: str = "lf") -> Path:
    """Copy reviewed sources, simulate the pre-fix R64R1 test on either OS."""
    source_root = Path(__file__).resolve().parents[2]
    for relative in (*PINNED_UNCHANGED, TARGET):
        src = source_root / relative
        dst = tmp_path / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    target = tmp_path / TARGET
    original, _bom, _current_eol = normalized_contents(target.read_bytes())
    original = original.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION)
    assert git_blob_sha(original.encode("utf-8")) == EXPECTED_OLD_BLOB
    if eol == "crlf":
        target.write_bytes(original.replace("\n", "\r\n").encode("utf-8"))
    elif eol == "lf":
        target.write_bytes(original.encode("utf-8"))
    else:
        raise ValueError("unknown fixture EOL")
    return tmp_path


def test_actual_repo_reviewed_and_already_applied() -> None:
    root = Path(__file__).resolve().parents[2]
    status, original, after = review(root)
    assert status == "ALREADY_APPLIED"
    assert original == after


def test_patch_is_exact_and_only_one_function() -> None:
    assert ORIGINAL_FUNCTION != REPLACEMENT_FUNCTION
    assert "target.read_bytes().replace" in ORIGINAL_FUNCTION
    assert "normalized = target.read_bytes().replace" in REPLACEMENT_FUNCTION
    replacement = patch_test(ORIGINAL_FUNCTION)
    assert replacement == REPLACEMENT_FUNCTION
    assert "not in after" in replacement


@pytest.mark.parametrize("starting_eol", ("lf", "crlf"))
def test_review_fixes_fixture_for_both_line_endings(
    tmp_path: Path, starting_eol: str,
) -> None:
    root = fixture_root(tmp_path, eol=starting_eol)
    target = root / TARGET
    initial = target.read_bytes()
    status, original, after = review(root)
    assert status == "PATCH_REQUIRED"
    assert original == initial
    assert after != initial
    assert b"\r\r\n" not in after
    if starting_eol == "crlf":
        assert b"\r\n" in after
    else:
        assert b"\r\n" not in after
    target.write_bytes(after)
    status2, current, after2 = review(root)
    assert status2 == "ALREADY_APPLIED"
    assert current == after2 == after


def test_pins_match_exact_reviewed_code(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    for relative, expected in PINNED_UNCHANGED.items():
        text, _bom, _eol = normalized_contents((root / relative).read_bytes())
        assert git_blob_sha(text.encode("utf-8")) == expected
    _, original, after = review(root)
    before_text, _bom, _eol = normalized_contents(original)
    after_text, _bom2, _eol2 = normalized_contents(after)
    assert git_blob_sha(before_text.encode("utf-8")) == EXPECTED_OLD_BLOB
    assert git_blob_sha(after_text.encode("utf-8")) == EXPECTED_FIXED_BLOB


def test_rejects_unreviewed_fixture_test(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    target = root / TARGET
    target.write_bytes(target.read_bytes() + b"\n# tampering\n")
    with pytest.raises(RuntimeError, match="R64R2_UNREVIEWED_TARGET_BLOB"):
        review(root)


def test_rejects_modified_audit_source(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    target = root / next(iter(PINNED_UNCHANGED))
    target.write_bytes(target.read_bytes() + b"\n# tampering\n")
    with pytest.raises(RuntimeError, match="R64R2_REVIEWED_SOURCE_MISMATCH"):
        review(root)


def test_rejects_double_crlf(tmp_path: Path) -> None:
    root = fixture_root(tmp_path, eol="crlf")
    target = root / TARGET
    target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
    with pytest.raises(RuntimeError, match="R64R2_UNEXPECTED_CR_ONLY_OR_DOUBLE_CR"):
        review(root)


def test_rejects_unrelated_function() -> None:
    with pytest.raises(RuntimeError, match="R64R2_UNREVIEWED_OR_AMBIGUOUS_FUNCTION"):
        patch_test("def unrelated():\n    pass\n")
