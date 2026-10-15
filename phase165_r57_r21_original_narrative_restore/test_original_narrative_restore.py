"""Focused restoration checks for completed vs incomplete public narrative."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def test_completed_entry_calls_original_adapter(monkeypatch):
    import phase165_r56_presentation_adapter as adapter
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    monkeypatch.setattr(adapter, "render_completed_shared_narrative", lambda _: "ORIGINAL_NARRATIVE_SENTINEL")
    assert render_partial_proof_markdown(result) == "ORIGINAL_NARRATIVE_SENTINEL"


def test_incomplete_entry_stays_partial_renderer(monkeypatch):
    import toda_group_proof_generic_narrative_renderer as generic
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    monkeypatch.setattr(generic, "render_toda_partial_proof_narrative_markdown", lambda _: "PARTIAL_SENTINEL")
    assert render_partial_proof_markdown(result) == "PARTIAL_SENTINEL"


def test_real_completed_pi32_uses_original_narrative():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    actual = render_partial_proof_markdown(result)
    assert actual == render_completed_shared_narrative(result)
    assert "証明" in actual
    assert "以上より" in actual
    assert "前提（出典情報未接続）" not in actual


def test_restored_adapter_preserves_original_call():
    project = Path(__file__).resolve().parent.parent
    source = (project / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    ast.parse(source)
    assert "build_complete_toda_group_result_proof_replay" in source
    assert "render_toda_group_proof_narrative_markdown" in source


def test_restore_is_idempotent():
    from importlib.util import module_from_spec, spec_from_file_location
    folder = Path(__file__).resolve().parent
    spec = spec_from_file_location("phase165_restore_installer", folder / "install.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.install(folder.parent, folder) == "ALREADY_INSTALLED"
