import ast
import importlib.util
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent


def load_apply():
    spec = importlib.util.spec_from_file_location("r43_installer", BASE / "apply.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_typed_module_parses():
    ast.parse((BASE / "toda_typed_applicability.py").read_text(encoding="utf-8"))


def test_no_legacy_repository_dependency():
    tree = ast.parse((BASE / "toda_typed_applicability.py").read_text(encoding="utf-8"))
    imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
    assert not any(name.startswith("repository_") or name in ("standard_production_repository", "proof_repository") for name in imports)


def test_empty_steps_and_rules(tmp_path, monkeypatch):
    import toda_typed_applicability as api
    assert api.find_typed_applicable_rules((), rules=()) == ()


def test_invalid_steps_rejected():
    import toda_typed_applicability as api
    with pytest.raises(TypeError):
        api.find_typed_applicable_rules((object(),), rules=())


def test_invalid_rules_rejected():
    import toda_typed_applicability as api
    with pytest.raises(TypeError):
        api.find_typed_applicable_rules((), rules=(object(),))


def test_matching_rule_uses_shared_matcher(monkeypatch):
    import toda_typed_applicability as api
    from proof import InferenceRule
    # Use a real rule object from an existing zero-argument rule factory.
    from relation_rules import equality_symmetry_inference_rule
    rule = equality_symmetry_inference_rule()
    monkeypatch.setattr(api, "find_inference_matches_for_rule", lambda selected, steps: ("match",))
    results = api.find_typed_applicable_rules((), rules=(rule,))
    assert len(results) == 1
    assert results[0].rule is rule
    assert results[0].matches == ("match",)


def test_installer_guard_does_not_overwrite(tmp_path, monkeypatch):
    mod = load_apply()
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TARGET", tmp_path / "toda_typed_applicability.py")
    monkeypatch.setattr(mod, "AUDIT", tmp_path / "audit.json")
    mod.TARGET.write_text("custom content", encoding="utf-8")
    with pytest.raises(RuntimeError):
        mod.install()
    assert mod.TARGET.read_text() == "custom content"
