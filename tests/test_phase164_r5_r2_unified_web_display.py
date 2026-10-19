"""R5-R2 focuses on a single common display path, not proof content quality."""
import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase165_goal_only_search import GoalSearchIncompleteError
import phase164_r5_r2_common_replay as selector
import web_group_proof as web


def test_one_public_web_builder_has_one_common_narrative_renderer():
    source = Path(web.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    builders = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == "build_standard_web_group_proof_view"]
    assert len(builders) == 1
    body = ast.get_source_segment(source, builders[0])
    assert "search_group_from_registered_goal" in body
    assert "build_partial_web_group_proof_view" in body
    assert "build_phase164_r5_web_pi5_3_proof" not in body
    assert "build_phase164_r5_r2_common_replay" not in body



def test_standard_selector_preserves_repository_replay(monkeypatch):
    calls = []
    def replay(**kwargs):
        calls.append(kwargs)
        return (kwargs["group_result"], kwargs["max_depth"])
    monkeypatch.setattr(selector, "build_registered_common_replay", replay)
    for n, k, depth, mode in ((6, 3, 2, "narrative"), (3, 2, 0, "trace")):
        result = SimpleNamespace(target=SimpleNamespace(group_dimension=n + k, sphere_dimension=n))
        assert selector.build_phase164_r5_r2_common_replay(n, k, result, depth, mode) == (result, depth)
    assert [call["mode"] for call in calls] == ["narrative", "trace"]



def test_source_selection_requires_no_markdown_for_ordinary_groups(monkeypatch):
    calls = []
    def replay(**kwargs):
        calls.append(kwargs)
        return kwargs["group_result"]
    monkeypatch.setattr(selector, "build_registered_common_replay", replay)
    for n in range(2, 16):
        for k in range(8):
            result = SimpleNamespace(target=SimpleNamespace(group_dimension=n + k, sphere_dimension=n))
            assert selector.build_phase164_r5_r2_common_replay(n, k, result, 2, "narrative") is result
    assert len(calls) == 112
    assert all(call["mode"] == "narrative" for call in calls)



def test_legacy_special_web_view_is_not_reachable():
    source = Path(web.__file__).read_text(encoding="utf-8")
    block = source[source.index("def build_standard_web_group_proof_view("):]
    assert "_phase158_baseline_render_toda_group_proof_narrative_markdown" not in block


def test_pi53_common_narrative_requires_registered_goal_catalog():
    view = web.build_standard_web_group_proof_view(3, 2, 2, "narrative")
    assert view.n == 3 and view.k == 2
    assert view.mode == "narrative"
    assert view.rendered_lines
    assert view.key in ("generic-complete-proof", "generic-partial-proof")



@pytest.mark.parametrize("n,k", [(4, 1), (5, 1), (4, 2), (6, 3)])
def test_representative_group_uses_single_view(n, k):
    view = web.build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.rendered_lines
    assert view.n == n and view.k == k
    assert view.mode == "narrative"
