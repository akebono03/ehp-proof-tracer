"""Offline tests for the reviewed one-line R4-R1 raw-f-string fix."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from phase173_r4_r1_alpha_literal_fix import install as installer
from phase173_r4_r1_alpha_literal_fix.install import (
    BASE_SHA256, NEW, OLD, PATCHED_SHA256,
    normalize, source_state, transform,
)


def old_source() -> str:
    root = Path(__file__).resolve().parents[2]
    source = root / "phase173_r4_r1_narrative_source_fix/projection.py"
    if not source.exists():
        pytest.skip("Run in EHP Proof Tracer root for reviewed source content")
    existing = normalize(source.read_bytes())
    try:
        state = source_state(existing)
    except RuntimeError:
        from phase173_r4_r1_prose_layout_fix.install import TARGETS
        path = "phase173_r4_r1_narrative_source_fix/projection.py"
        expected_revised = TARGETS[path][1]
        if hashlib.sha256(existing).hexdigest() != expected_revised:
            raise
        fixture = (root / "phase173_r4_r1_prose_layout_fix/fixtures/"
                   "alpha_reviewed_projection.py.txt")
        existing = normalize(fixture.read_bytes())
        if hashlib.sha256(existing).hexdigest() != PATCHED_SHA256:
            raise RuntimeError("The reviewed alpha source fixture has changed")
        state = source_state(existing)
    if state == "ALREADY_INSTALLED":
        return existing.decode("utf-8").replace(NEW, OLD, 1)
    return existing.decode("utf-8")


def test_reviewed_single_character_change() -> None:
    source = old_source()
    patched = transform(source)
    assert source.count(OLD) == 1
    assert patched.count(NEW) == 1
    assert patched == source.replace(OLD, NEW, 1)
    assert source_state(source.encode("utf-8")) == "NEW"
    assert source_state(patched.encode("utf-8")) == "ALREADY_INSTALLED"
    assert len(BASE_SHA256) == len(PATCHED_SHA256) == 64


def test_fixed_literal_evaluates_to_real_latex() -> None:
    tree = ast.parse(transform(old_source()))
    literals = (
        node for node in ast.walk(tree)
        if isinstance(node, ast.JoinedStr)
        and any(
            isinstance(value, ast.Constant)
            and isinstance(value.value, str)
            and "に適用する" in value.value
            for value in node.values
        )
    )
    expr = next(literals)
    result = eval(compile(ast.Expression(expr), "<reviewed literal>", "eval"), {"prop_n": 1})
    assert r"\alpha=\nu_4" in result
    assert "\x07" not in result
    assert "\n" not in result


def test_repeated_patch_rejected() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform(transform(old_source()))


def test_unreviewed_edit_rejected() -> None:
    data = old_source().encode("utf-8") + b"# unreviewed\n"
    with pytest.raises(RuntimeError, match="Unreviewed"):
        source_state(data)


def test_original_imports_and_other_functions_preserved() -> None:
    source = old_source()
    patched = transform(source)
    a, b = ast.parse(source), ast.parse(patched)
    assert len(a.body) == len(b.body)
    assert [type(node).__name__ for node in a.body] == [type(node).__name__ for node in b.body]
    assert patched.replace(NEW, OLD, 1) == source


def _committed_fixture(tmp_path, monkeypatch):
    """A committed adapter that differs from reviewed baseline by only its hook."""
    from phase173_r4_r1_narrative_source_fix import install as narrative

    original = b"def reviewed():\n    return 1\n"
    recorded = original + narrative.HOOK.encode("utf-8")
    adapter = tmp_path / narrative.TARGET
    adapter.write_bytes(recorded)
    installer_source = tmp_path / "phase173_r4_r1_narrative_source_fix/install.py"
    installer_source.parent.mkdir(parents=True, exist_ok=True)
    installer_source.write_bytes(b"narrative installer fixture")
    baseline_sha = hashlib.sha1(
        b"blob " + str(len(original)).encode("ascii") + b"\x00" + original
    ).hexdigest()
    monkeypatch.setattr(narrative, "EXPECTED_TARGET_BLOB", baseline_sha)
    monkeypatch.setattr(installer, "COMMITTED_NARRATIVE_ADAPTER_BLOB", "committed-adapter")
    monkeypatch.setattr(installer, "COMMITTED_NARRATIVE_INSTALLER_BLOB", "committed-installer")
    monkeypatch.setattr(installer, "COMMITTED_NARRATIVE_PROJECTION_BLOB", "committed-projection")
    monkeypatch.setattr(narrative, "reviewed_public_state", lambda root: "COMMITTED_INSTALLED")
    def old_preflight_fails(root):
        raise AssertionError("The pre-commit narrative installer must not be called")
    monkeypatch.setattr(narrative, "preflight", old_preflight_fails)
    committed_paths = {
        narrative.TARGET.as_posix(): "committed-adapter",
        "phase173_r4_r1_narrative_source_fix/install.py": "committed-installer",
        installer.TARGET.as_posix(): "committed-projection",
    }
    monkeypatch.setattr(installer, "git", lambda root, *args: committed_paths[args[-1].removeprefix("HEAD:")])
    monkeypatch.setattr(narrative, "git_bytes", lambda root, path: (
        recorded if path == narrative.TARGET.as_posix() else
        b"narrative installer fixture"
    ))
    return adapter


def test_committed_adapter_preflight_skips_stale_original_installer(tmp_path, monkeypatch) -> None:
    _committed_fixture(tmp_path, monkeypatch)
    assert installer.reviewed_narrative_state(tmp_path) == "COMMITTED_INSTALLED"


def test_committed_adapter_refuses_dirty_worktree(tmp_path, monkeypatch) -> None:
    adapter = _committed_fixture(tmp_path, monkeypatch)
    adapter.write_bytes(adapter.read_bytes() + b"# unauthorized edit\n")
    with pytest.raises(RuntimeError, match="differs from reviewed"):
        installer.reviewed_narrative_state(tmp_path)


def test_committed_adapter_refuses_altered_dependency(tmp_path, monkeypatch) -> None:
    _committed_fixture(tmp_path, monkeypatch)
    (tmp_path / "phase173_r4_r1_narrative_source_fix/install.py").write_bytes(
        b"changed narrative installer"
    )
    with pytest.raises(RuntimeError, match="installer worktree changed"):
        installer.reviewed_narrative_state(tmp_path)


def test_committed_adapter_refuses_altered_stored_hook(tmp_path, monkeypatch) -> None:
    adapter = _committed_fixture(tmp_path, monkeypatch)
    from phase173_r4_r1_narrative_source_fix import install as narrative
    altered = adapter.read_bytes().replace(narrative.HOOK.encode("utf-8"), b"# changed hook\n")
    adapter.write_bytes(altered)
    monkeypatch.setattr(narrative, "git_bytes", lambda root, path: (
        altered if path == narrative.TARGET.as_posix() else
        b"narrative installer fixture"
    ))
    with pytest.raises(RuntimeError, match="differs from reviewed"):
        installer.reviewed_narrative_state(tmp_path)


def test_focused_runner_isolates_same_named_test_live_modules() -> None:
    script = Path(__file__).resolve().parents[1] / "run.ps1"
    contents = script.read_text(encoding="utf-8")
    focused = contents.split("PHASE173_R4_R1_ALPHA_FOCUSED_PYTEST_START", 1)[1]
    focused = focused.split("if ($LASTEXITCODE -ne 0)", 1)[0]
    assert "python -m pytest -q -p no:cacheprovider --import-mode=importlib" in focused
    assert "phase173_r4_r1_alpha_literal_fix/tests/test_live.py" in focused
    assert "phase173_r4_r1_narrative_source_fix/tests/test_live.py" in focused
