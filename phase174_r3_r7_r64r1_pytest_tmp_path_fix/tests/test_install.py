"""R64R1 isolated negative tests and exact one-function replacement."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r64r1_pytest_tmp_path_fix.install import (
    EXPECTED_FIXED_BLOB, EXPECTED_OLD_BLOB, ORIGINAL_FUNCTION,
    PINNED_UNCHANGED, REPLACEMENT_FUNCTION, TARGET, git_blob_sha,
    patch_test, review,
)


def create_review_fixture(tmp_path: Path, source: str = ORIGINAL_FUNCTION) -> Path:
    """Construct only the pinned inputs; do not mutate production or Git state."""
    from phase174_r3_r7_r64r1_pytest_tmp_path_fix.install import normalized_contents
    real_root = Path(__file__).resolve().parents[2]
    for relative in PINNED_UNCHANGED:
        original = real_root / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(original.read_bytes())
    real_source = (real_root / TARGET).read_bytes()
    actual, _bom, _eol = normalized_contents(real_source)
    fixed_or_original = actual.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION)
    destination = tmp_path / TARGET
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(fixed_or_original if source == ORIGINAL_FUNCTION else source, encoding="utf-8")
    return tmp_path


def test_original_and_patched_hashes_match_contract(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    source = (tmp_path / TARGET).read_text(encoding="utf-8")
    assert git_blob_sha(source.encode("utf-8")) == EXPECTED_OLD_BLOB
    patched = patch_test(source)
    assert git_blob_sha(patched.encode("utf-8")) == EXPECTED_FIXED_BLOB
    assert patched.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION) == source
    assert patched.count(REPLACEMENT_FUNCTION) == 1


def test_review_accepts_original_then_patched_and_does_not_mutate(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    status, original, after = review(tmp_path)
    assert status == "PATCH_REQUIRED"
    assert original != after
    assert (tmp_path / TARGET).read_bytes() == original
    (tmp_path / TARGET).write_bytes(after)
    status2, original2, after2 = review(tmp_path)
    assert status2 == "ALREADY_APPLIED"
    assert original2 == after2 == after


def test_patch_rejects_unrelated_or_modified_functions() -> None:
    for source in ("def unrelated():\n    pass\n",
                   ORIGINAL_FUNCTION.replace("target.write_bytes", "target.touch"),
                   ORIGINAL_FUNCTION + ORIGINAL_FUNCTION):
        with pytest.raises(RuntimeError):
            patch_test(source)


def test_review_rejects_unreviewed_test_blob(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    target = tmp_path / TARGET
    target.write_bytes(target.read_bytes() + b"\n# unreviewed\n")
    with pytest.raises(RuntimeError, match="R64R1_UNREVIEWED_TEST_BLOB"):
        review(tmp_path)


def test_review_rejects_modified_audit_file(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    relative = next(iter(PINNED_UNCHANGED))
    target = tmp_path / relative
    target.write_bytes(target.read_bytes() + b"\n# unreviewed\n")
    with pytest.raises(RuntimeError, match="R64R1_UNREVIEWED_SOURCE"):
        review(tmp_path)


def test_review_accepts_crlf_line_endings(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    target = tmp_path / TARGET
    normalized = target.read_bytes().replace(b"\r\n", b"\n")
    target.write_bytes(normalized.replace(b"\n", b"\r\n"))
    status, _original, after = review(tmp_path)
    assert status == "PATCH_REQUIRED"
    assert b"\r\n" in after
    assert b"\r\r\n" not in after
    target.write_bytes(after)
    assert review(tmp_path)[0] == "ALREADY_APPLIED"
