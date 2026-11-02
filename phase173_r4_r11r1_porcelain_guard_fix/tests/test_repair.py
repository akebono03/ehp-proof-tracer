"""Focused source-preserving tests for installer porcelain guard correction."""
from __future__ import annotations
import ast
from hashlib import sha256
from pathlib import Path
import pytest
from phase173_r4_r11r1_porcelain_guard_fix import repair


def _source_pair() -> tuple[bytes, bytes]:
    corrected = Path(repair.__file__).with_name("replacement_install.py.txt").read_bytes()
    original = corrected.replace(b'not in ("", "M " + TARGET):', b'not in ("", " M " + TARGET):')
    return original, corrected


def test_full_replacement_is_only_one_comparison_change() -> None:
    original, corrected = _source_pair()
    assert repair.prepared_replacement(original, corrected) == corrected
    assert ast.parse(original.decode()).body
    assert ast.parse(corrected.decode()).body
    assert sha256(original).hexdigest() == repair.ORIGINAL_HASH
    assert sha256(corrected).hexdigest() == repair.PATCHED_HASH


def test_original_stripping_explains_current_failure() -> None:
    raw = " M " + repair.TARGET
    assert raw.strip() == "M " + repair.TARGET
    assert repair.checked_tracked_status(raw)


@pytest.mark.parametrize("unexpected", (
    "", "M " + repair.TARGET, "MM " + repair.TARGET,
    "A  " + repair.TARGET, " M another_file.py",
    " M " + repair.TARGET + "\n M another_file.py",
))
def test_other_tracked_states_are_rejected(unexpected: str) -> None:
    assert repair.checked_tracked_status(unexpected) is False


def test_unreviewed_replacement_is_rejected() -> None:
    original, corrected = _source_pair()
    wrong = corrected.replace(b'if not target.is_file():', b'if target.is_file():')
    assert wrong != corrected
    with pytest.raises(RuntimeError, match="exact reviewed comparison"):
        repair.prepared_replacement(original, wrong)


def test_unreviewed_original_is_rejected() -> None:
    original, corrected = _source_pair()
    wrong = original.replace(b'if not target.is_file():', b'if target.is_file():')
    assert wrong != original
    with pytest.raises(RuntimeError, match="Unreviewed original"):
        repair.prepared_replacement(wrong, corrected)
