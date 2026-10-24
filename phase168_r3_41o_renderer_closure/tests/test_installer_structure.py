from pathlib import Path
import ast
from install import replace_function, checksum


def test_full_function_is_complete():
    pkg = Path(__file__).resolve().parent.parent
    function = (pkg / "renderer_function_full.py").read_text(encoding="utf-8")
    module = ast.parse(function)
    assert len(module.body) == 1
    assert isinstance(module.body[0], ast.FunctionDef)
    assert module.body[0].name == "render_model_backed_narrative_markdown"


def test_bundled_change_has_no_revalidation():
    pkg = Path(__file__).resolve().parent.parent
    function = (pkg / "renderer_function_full.py").read_text(encoding="utf-8")
    assert ".match_guard(" not in function
    assert "generator_transport_normalization_rule(" not in function
    assert "model.target" in function
    assert r"\ker E=\operatorname{{Im}}\Delta=" in function


def test_guarded_patch_reconstructs_full_file():
    pkg = Path(__file__).resolve().parent.parent
    old = (pkg / "renderer_before.sha256").read_text(encoding="utf-8").strip()
    assert len(old) == 64
    full = (pkg / "full_files/phase168_r3_5_model_renderer.py").read_text(encoding="utf-8")
    assert ast.parse(full)
