"""Targeted R4 import-route and behavioral regression tests."""
from __future__ import annotations

import ast
from pathlib import Path
import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result, render_partial_proof_markdown
from phase165_renderer_narrative_model import build_narrative_proof_model
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from toda_group_proof_narrative_renderer import render_narrative_proof_model, render_toda_group_proof_narrative_markdown
from toda_group_proof_narrative_shared_components import _render_generic_narrative_step
from install import find_legacy_imports


ROOT = Path(__file__).resolve().parent.parent


def test_r4_original_generic_implementation_absent():
    assert not (ROOT / "toda_group_proof_generic_narrative_renderer.py").exists()
    assert not (ROOT / "toda_group_proof_generic_narrative_renderer").exists()


def test_r4_old_static_imports_absent():
    assert find_legacy_imports(ROOT) == []


def test_r4_canonical_public_renderer_is_unique():
    source = (ROOT / "toda_group_proof_narrative_renderer.py").read_text(encoding="utf8")
    tree = ast.parse(source)
    defs = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "render_toda_group_proof_narrative_markdown"]
    assert len(defs) == 1
    assert "def _phase160_r7_pre_transport_narrative(" in source


def test_r4_shared_helper_is_preserved():
    assert callable(_render_generic_narrative_step)


def test_r4_complete_public_markdown():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert "証明対象" in render_partial_proof_markdown(result)
    assert "□" in render_partial_proof_markdown(result)


def test_r4_partial_public_markdown():
    result = make_partial_proof_result(n=200, k=90, status=ProofSearchStatus.NOT_SEARCHED)
    text = render_narrative_proof_model(build_narrative_proof_model(result))
    assert r"\pi_{290}^{200}" in text
    assert "□" not in text


def test_r4_type_guard():
    with pytest.raises(TypeError):
        render_narrative_proof_model(object())


def test_r4_bom_legacy_import_preflight(tmp_path, monkeypatch):
    import install
    sample = tmp_path / "bom_sample.py"
    sample.write_bytes(b"\xef\xbb\xbf" + b"from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step\n")
    assert install.imported_names(sample) == (("_render_generic_narrative_step",),)
    transformed, count = install.rewrite_imports(sample.read_text(encoding="utf-8-sig"))
    assert count == 1
    assert "from toda_group_proof_narrative_shared_components import" in transformed
    assert "toda_group_proof_generic_narrative_renderer" not in transformed


def test_r4_corrects_preexisting_contract_assertions():
    from install import update_legacy_renderer_tests
    source = (ROOT / "test_phase165_r52_r11_common_renderer.py").read_text(encoding="utf-8-sig")
    assert "def test_r11_given_step_does_not_certify_completed_proof():" in source
    assert 'assert "Proposition 5.1" not in text' in source
    assert 'assert "Proposition 5.1" in text' not in source
    assert "def test_r11_same_renderer_handles_completed_proof():" not in source
