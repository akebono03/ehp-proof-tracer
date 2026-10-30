"""The R2J-R3 installer changes only the reviewed R2J-R2 hook boundary."""
from __future__ import annotations

import pytest

from phase171_r2j_r3_ehp_exactness.install import ANCHOR, ADDITION, _insert_hook


def _sample(newline: str = "\n") -> bytes:
    code = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        + ANCHOR
        + "        return ()\n"
        + "    return expand\n"
    )
    return code.replace("\n", newline).encode("utf-8")


def test_installer_preserves_exact_unrelated_code():
    original = _sample()
    result = _insert_hook(original)
    assert result == original.replace(ANCHOR.encode(), (ANCHOR + ADDITION).encode())


def test_installer_preserves_windows_crlf():
    original = _sample("\r\n")
    result = _insert_hook(original)
    assert b"\r\n" in result
    assert result.replace(b"\r\n", b"\n") == _insert_hook(_sample())


def test_installer_rejects_duplicate_apply_and_missing_anchor():
    original = _sample()
    with pytest.raises(RuntimeError):
        _insert_hook(_insert_hook(original))
    with pytest.raises(RuntimeError):
        _insert_hook(b"def unrelated():\n    return 1\n")
