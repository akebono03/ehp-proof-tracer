"""Tests for R3-40E, a renderer-only cleanup with no visible output change."""
from pathlib import Path

from phase168_r3_40e_remove_deferred_render.apply import (
    FUNCTION_NAME,
    extract_function,
    patch_source,
)
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_38_frozen_fulltext_audit.audit import capture


def test_patch_removes_only_dead_deferred_loop():
    root = Path(__file__).resolve().parent.parent.parent
    package = root / "phase168_r3_40e_remove_deferred_render"
    old = (root / "phase168_r3_40d_runner_module_fix" / "full_functions"
           / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
    new = (package / "full_functions"
           / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
    deferred = (
        "        for postponed in entry.after_indices:\n"
        "            postponed_step = model.steps[postponed]\n"
        "            sentence = typed_sentence(postponed_step.conclusion, postponed_step)\n"
        "            if sentence is not None:\n"
        "                lines.extend((sentence, \"\"))\n"
    )
    assert old.count(deferred) == 1
    assert new == old.replace(deferred, "")
    source = '"""Synthetic module."""\n' + old
    changed = patch_source(source, old, new)
    assert extract_function(changed, FUNCTION_NAME) == new
    assert patch_source(changed, old, new) == changed


def test_projection_never_emits_legacy_deferred_entries_in_four_groups():
    for n in (2, 3, 4, 5):
        _, model, _ = capture(n, 1)
        entries = project_narrative_order(model)
        assert all(entry.after_indices == () for entry in entries)
        assert sorted(entry.step_index for entry in entries) == list(range(len(model.steps)))
