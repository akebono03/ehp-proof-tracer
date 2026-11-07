"""Pure focused regression tests: Git paths must be POSIX across Windows/Linux."""
from __future__ import annotations

import ast
import pytest

from phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch import (
    AUDITED_TRACKED, EXPECTED_HEAD, NEW_HELPER, NEW_LINE, OLD_LINE, patched_bytes,
    sha256, transform, normalized,
)


def original_fixture() -> str:
    return (
        "from pathlib import Path\n"
        "TEST_TARGET = Path('phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py')\n"
        "DISPLAY_TARGET = Path('web_group_proof_common.py')\n"
        "\n\n"
        "ROOT = Path('.')\n\n"
        "def verify_source_and_state(*, applied: bool, root: Path = ROOT) -> dict[str, object]:\n"
        + OLD_LINE
        + "    return expected_changed\n"
    )


def test_windows_git_slash_mismatch_is_repaired_without_broadening_guard() -> None:
    previous = original_fixture()
    corrected = transform(previous)
    ast.parse(corrected)
    assert OLD_LINE not in corrected
    assert corrected.count(NEW_LINE) == 1
    assert corrected.count(NEW_HELPER) == 1
    namespace: dict[str, object] = {}
    exec(compile(corrected, "fixture", "exec"), namespace)
    expected = (
        "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
        "web_group_proof_common.py",
    )
    assert namespace["verify_source_and_state"](applied=True) == expected
    assert namespace["verify_source_and_state"](applied=False) == ()
    assert namespace["verify_source_and_state"](applied=True) != expected + ("other.py",)


def test_expected_tracked_paths_requires_boolean_applied() -> None:
    corrected = transform(original_fixture())
    scope: dict[str, object] = {}
    exec(compile(corrected, "fixture", "exec"), scope)
    for invalid in (None, 1, "True", (), object()):
        with pytest.raises(TypeError):
            scope["expected_tracked_paths"](applied=invalid)


def test_patch_rejects_missing_repeated_and_previous_transformation() -> None:
    source = original_fixture()
    with pytest.raises(RuntimeError):
        transform(source.replace(OLD_LINE, ""))
    with pytest.raises(RuntimeError):
        transform(source + OLD_LINE)
    with pytest.raises(RuntimeError):
        transform(transform(source))


def test_patch_bytes_preserve_crlf_or_lf() -> None:
    source = original_fixture().encode("utf-8")
    lf = patched_bytes(source)
    crlf = patched_bytes(source.replace(b"\n", b"\r\n"))
    assert b"\r\n" not in lf
    assert b"\r\n" in crlf
    assert normalized(lf) == normalized(crlf)
    assert normalized(crlf).count("def expected_tracked_paths(") == 1


def test_mixed_eol_is_rejected_and_expected_head_is_pinned() -> None:
    source = original_fixture().encode("utf-8")
    with pytest.raises(RuntimeError):
        normalized(source.replace(b"\n", b"\r\n", 1))
    assert len(EXPECTED_HEAD) == 40
    assert len(sha256(source)) == 64


def test_expected_tracked_modifications_are_the_exact_two_reviewed_files() -> None:
    assert AUDITED_TRACKED == (
        "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
        "web_group_proof_common.py",
    )
