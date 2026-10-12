"""R5-R2 focuses on a single common display path, not proof content quality."""
import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

import phase164_r5_r2_common_replay as selector
import web_group_proof as web


def test_one_public_web_builder_has_one_common_narrative_renderer():
    source = Path(web.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    builders = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == "build_standard_web_group_proof_view"]
    assert len(builders) == 1
    body = ast.get_source_segment(source, builders[0])
    assert body.count("render_toda_group_proof_narrative_markdown(presentation)") == 1
    assert body.count("build_toda_group_proof_presentation(replay)") == 1
    assert "build_phase162_r4_b3_web_common_display_view" not in body
    assert "build_phase164_r5_web_pi5_3_proof" not in body
    assert "build_phase164_r5_r2_common_replay" in body


def test_standard_selector_preserves_repository_replay(monkeypatch):
    sentinel = object()
    monkeypatch.setattr(selector, "build_toda_group_result_proof_replay",
                        lambda result, max_depth: (result, max_depth))
    assert selector.build_phase164_r5_r2_common_replay(6, 3, sentinel, 2, "narrative") == (sentinel, 2)
    assert selector.build_phase164_r5_r2_common_replay(3, 2, sentinel, 0, "trace") == (sentinel, 0)


def test_source_selection_requires_no_markdown_for_ordinary_groups(monkeypatch):
    calls = []
    monkeypatch.setattr(selector, "build_toda_group_result_proof_replay",
                        lambda result, max_depth: calls.append((result, max_depth)) or result)
    for n in range(2, 16):
        for k in range(8):
            if (n, k) in ((3, 2), (4, 1), (5, 1)):
                continue
            item = (n, k)
            assert selector.build_phase164_r5_r2_common_replay(
                n, k, item, 2, "narrative"
            ) == item
    assert len(calls) == 109


def test_legacy_special_web_view_is_not_reachable():
    source = Path(web.__file__).read_text(encoding="utf-8")
    block = source[source.index("def build_standard_web_group_proof_view("):]
    assert "_phase158_baseline_render_toda_group_proof_narrative_markdown" not in block


def test_pi53_common_narrative_is_renderable():
    view = web.build_standard_web_group_proof_view(3, 2, 2, "narrative")
    assert view.phase == "164 R5"
    assert view.rendered_lines
    assert view.mode == "narrative"


@pytest.mark.parametrize("n,k", [(4, 1), (5, 1), (4, 2), (6, 3)])
def test_representative_group_uses_single_view(n, k):
    view = web.build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.rendered_lines
    assert view.n == n and view.k == k
    assert view.mode == "narrative"
