"""Offline guards for narrowly scoped R4-R1 narrative changes."""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path

import pytest

from phase173_r4_r1_prose_layout_fix.install import (
    PACKAGE, TARGETS, normalize, state_for,
)


def reviewed_files():
    root = Path(__file__).resolve().parents[2]
    for path, (original, revised, blobs) in TARGETS.items():
        replacement = root / PACKAGE / "full_replacements" / path
        yield path, original, revised, replacement


def test_full_replacements_are_reviewed() -> None:
    for path, _, revised, replacement in reviewed_files():
        assert replacement.exists(), path
        data = normalize(replacement.read_bytes())
        assert sha256(data).hexdigest() == revised
        ast.parse(data.decode("utf-8"))
        assert state_for(path, data) == "ALREADY_INSTALLED"


def test_current_source_is_either_reviewed_baseline_or_patch() -> None:
    root = Path(__file__).resolve().parents[2]
    if not (root / ".git").exists():
        pytest.skip("Live source guards require the repository checkout")
    for path, _, _, replacement in reviewed_files():
        current = root / path
        assert current.exists()
        assert state_for(path, current.read_bytes()) in ("NEW", "ALREADY_INSTALLED")


def test_unreviewed_content_is_refused() -> None:
    path = next(iter(TARGETS))
    data = (Path(__file__).resolve().parents[2] / PACKAGE / "full_replacements" / path).read_bytes()
    with pytest.raises(RuntimeError, match="Unreviewed"):
        state_for(path, data + b"# unreviewed\n")


def test_only_prose_projection_function_changes() -> None:
    root = Path(__file__).resolve().parents[2]
    current = root / "phase173_r4_r1_narrative_source_fix/projection.py"
    if not current.exists():
        pytest.skip("Run in source repository for full-function review")
    replacement = (root / PACKAGE / "full_replacements" /
                   "phase173_r4_r1_narrative_source_fix/projection.py")
    original_ast = ast.parse(normalize(current.read_bytes()).decode("utf-8"))
    updated_ast = ast.parse(replacement.read_text(encoding="utf-8"))
    def named(tree):
        return [(node.name, type(node).__name__)
                for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert named(original_ast) == named(updated_ast)
    assert len(named(updated_ast)) == 3
    assert [ast.dump(node, include_attributes=False) for node in updated_ast.body
            if isinstance(node, ast.ImportFrom)] == [
        ast.dump(node, include_attributes=False) for node in original_ast.body
        if isinstance(node, ast.ImportFrom)
    ]


def test_no_new_citation_or_unreviewed_source_label() -> None:
    root = Path(__file__).resolve().parents[2]
    replacement = (root / PACKAGE / "full_replacements" /
                   "phase173_r4_r1_narrative_source_fix/projection.py")
    data = replacement.read_text(encoding="utf-8")
    assert "Toda (5.6) の同型" not in data
    assert "この同型は, " not in data
    assert "Hopf 関係により" not in data
    assert "_unique_citation(model, prop," in data
    assert "_unique_citation(model, hopf.premises[0]," in data
    assert "\\Phi(\\nu',0)=" not in data


def test_runner_uses_importlib_and_no_full_suite() -> None:
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert script.count("--import-mode=importlib") == 2
    assert "python -m pytest -q" in script
    assert "phase173_r4_r1_alpha_literal_fix/tests/test_live.py" in script
    assert "python -m pytest" in script
    assert "pytest ." not in script


def test_revised_narrative_verification_matches_intent() -> None:
    root = Path(__file__).resolve().parents[2]
    rewritten = (root / PACKAGE / "full_replacements" /
                 "phase173_r4_r1_narrative_source_fix/verify.py").read_text(encoding="utf-8")
    assert '"no_redundant_generator_images"' in rewritten
    assert '"no_uncited_toda56_label"' in rewritten
    assert '"sentence_line_breaks"' in rewritten


def test_alpha_previous_offline_tests_remain_supported() -> None:
    root = Path(__file__).resolve().parents[2]
    fixture = root / PACKAGE / "fixtures/alpha_reviewed_projection.py.txt"
    assert sha256(normalize(fixture.read_bytes())).hexdigest() == (
        "1d99e8b135fb49868a185e5edac4b294478ca4c2c6794e36e61242cc544e15a3"
    )
    alpha_test = root / PACKAGE / "full_replacements/phase173_r4_r1_alpha_literal_fix/tests/test_install.py"
    text = alpha_test.read_text(encoding="utf-8")
    assert "def old_source() -> str:" in text
    assert "The reviewed alpha source fixture has changed" in text
    assert "phase173_r4_r1_prose_layout_fix.install import TARGETS" in text
