"""R41 inspected source/installation contract regression."""
from __future__ import annotations

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.install import (
    full_changed_function,
)
from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import (
    BASE_BLOB, INSERT, normalized, verified_state,
)


def test_checked_source_guard_after_install():
    result = verified_state()
    assert result["source_guard"] == "PASS"
    assert result["shared_math_mode"] == "INSTALLED"
    assert result["reviewed_r40_sha256_files"] == 3
    assert len(BASE_BLOB) == 40


def test_complete_function_extractor_preserves_entire_body():
    synthetic = "import os\n\ndef shared_expansion_provider():\n    return 1\n\ndef other():\n    return 2\n"
    assert full_changed_function(synthetic) == "def shared_expansion_provider():\n    return 1\n"


def test_import_and_full_function_emitted_from_actual_file():
    from pathlib import Path
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import ROOT, TARGET
    directory = Path(__file__).resolve().parents[1]
    actual = normalized((ROOT / TARGET).read_bytes()).decode("utf-8")
    function = (directory / "CHANGED_FUNCTION_FULL.py").read_text(encoding="utf-8")
    assert function == full_changed_function(actual)
    assert INSERT in function
    imports = (directory / "IMPORTS_FULL.txt").read_text(encoding="utf-8")
    assert imports == actual.split("def shared_expansion_provider(", 1)[0]
