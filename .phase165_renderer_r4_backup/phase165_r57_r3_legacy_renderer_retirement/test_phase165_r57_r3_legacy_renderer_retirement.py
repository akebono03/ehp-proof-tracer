"""R57-R3: the retired routes do not produce a second narrative."""
import ast
from pathlib import Path

import phase165_r14_r39_web_connection as compatibility
import toda_group_proof_generic_narrative_renderer as common


def test_r57_r3_legacy_generic_proof_entry_is_removed():
    assert not hasattr(common, "render_toda_group_proof_generic_proof_markdown")
    assert hasattr(common, "_render_generic_narrative_step")


def test_r57_r3_r39_api_forwards_without_per_group_prose(monkeypatch):
    calls = []

    def fake_standard(*, n, k, max_depth, mode):
        calls.append((n, k, max_depth, mode))
        return object_result

    object_result = object()
    monkeypatch.setattr(compatibility, "build_standard_web_group_proof_view", fake_standard)
    actual = compatibility.build_phase165_pi32_web_view(max_depth=1, mode="outline")
    assert actual is object_result
    assert calls == [(2, 1, 1, "outline")]


def test_r57_r3_legacy_module_has_no_fixed_narrative():
    source = Path(compatibility.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.JoinedStr) for node in ast.walk(tree))
    assert "完全性より" not in source
    assert "## 使用する結果" not in source


def test_r57_r3_public_renderer_entry_preserved():
    from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
    assert callable(render_toda_group_proof_narrative_markdown)
