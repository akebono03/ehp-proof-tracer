"""Focused checks for the Phase 167 R4 renderer deletion."""
from __future__ import annotations

import inspect
from pathlib import Path

import phase165_r56_presentation_adapter as adapter
import phase165_r57_r10_step_narrative as ancestry


def test_completed_adapter_has_single_public_renderer():
    source = inspect.getsource(adapter.render_completed_shared_narrative)
    assert "return render_toda_group_proof_narrative_markdown(presentation)" in source
    assert "render_completed_from_proofsteps" not in source
    assert "has_transport_proof_ancestry" not in source
    assert "_phase160_r7_render_stable_finite_cyclic_transport_narrative" not in source


def test_obsolete_renderer_is_removed_but_shared_ancestry_remains():
    assert not hasattr(ancestry, "render_completed_from_proofsteps")
    assert hasattr(ancestry, "ordered_proof_ancestry")
    assert hasattr(ancestry, "has_transport_proof_ancestry")
    source = Path(ancestry.__file__).read_text(encoding="utf-8")
    assert "def _math_statement(" not in source
    assert "def _reference_label(" not in source


def test_stable_first_stem_capture_matches_baseline():
    from json import loads
    root = Path(__file__).resolve().parent.parent
    results = root / "phase167_r4_remove_obsolete_renderer_testfix_results"
    before, after = results / "before", results / "after"
    for n in (2, 3, 4, 5, 6):
        filename = f"pi{n+1}_{n}.json"
        baseline = loads((before / filename).read_text(encoding="utf-8"))
        updated = loads((after / filename).read_text(encoding="utf-8"))
        assert baseline == updated, filename
        assert baseline["status"] == "complete", filename
