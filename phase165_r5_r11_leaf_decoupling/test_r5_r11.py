"""Narrow migration guarantees; independent from broken Phase 59 fixture."""

import ast
from pathlib import Path

import phase162_ehp_leaf_inputs as shared
import phase162_web_narrative_integration as historical
import phase162_pi5_3_web_replay as replay


def test_r5_r11_compatibility_alias_is_identical():
    assert historical._phase162_ehp_leaves is shared._phase162_ehp_leaves


def test_r5_r11_replay_uses_shared_leaf_object():
    assert replay._phase162_ehp_leaves is shared._phase162_ehp_leaves


def test_r5_r11_leaf_module_does_not_import_narrative():
    tree = ast.parse(Path(shared.__file__).read_text(encoding="utf-8-sig"))
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    assert "phase162_web_narrative_integration" not in imported
    assert "phase162_r3_narrative_connection" not in imported


def test_r5_r11_original_module_has_no_leaf_definition():
    tree = ast.parse(Path(historical.__file__).read_text(encoding="utf-8-sig"))
    assert not [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_phase162_ehp_leaves"]


def test_r5_r11_leaf_window_count_and_order(monkeypatch):
    sentinel = object()
    hopf = object()
    windows = []
    monkeypatch.setattr(shared, "build_phase55_representative_result", lambda: {"prop51_steps": (sentinel,)})
    monkeypatch.setattr(shared, "build_phase58_representative_result", lambda: {"final_hopf_step": hopf, "expected_final_hopf": object()})
    monkeypatch.setattr(shared, "cite_verified_fixed_statement", lambda *args, **kwargs: hopf)
    def record(*, conclusion, premises, rule):
        assert premises == ()
        assert rule is shared.ProofRule.GIVEN
        windows.append(conclusion.window)
        return conclusion
    monkeypatch.setattr(shared, "create_legacy_given_proof_step", record)
    first, second, exactness = shared._phase162_ehp_leaves()
    assert first is sentinel
    assert second is hopf
    assert len(exactness) == len(windows) == 4
    assert [w.middle_term.group_dimension for w in windows] == [5, 5, 6, 4]
