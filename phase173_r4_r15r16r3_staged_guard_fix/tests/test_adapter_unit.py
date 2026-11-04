"""Isolated integration of the exact common-renderer call and tree guards."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
import runpy
import sys
from types import ModuleType, SimpleNamespace

import pytest


def _load_isolated_adapter(monkeypatch):
    class Group:
        pass

    class Status:
        PARTIAL = "partial"

    class Rule(Enum):
        GIVEN = "given"
        INFERENCE = "inference"

    class Step:
        def __init__(self, *, rule, premises=(), name=""):
            self.rule = rule
            self.premises = premises
            self.name = name
            self.inference_rule = SimpleNamespace(
                match_guard=lambda premises, bindings: bool(premises),
            ) if rule is Rule.INFERENCE else None

    results = []

    class Result:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            results.append(self)

    def bind(result):
        return SimpleNamespace(citations=(SimpleNamespace(number=1),))

    def render(result, model):
        return (
            "## 証明対象\n\n$\\pi$\n\n## 使用する結果\n\n"
            "**[R1] Example source.**\n\n---\n\n## 証明\n\n"
            "**探索状態：部分証明・未完成**\n\n"
            "### 確認済み ProofStep（与件を含む）\n\n"
            "- 与件: $\\pi_{3}^{2}=0$\n"
            "- 推論: UnsupportedStatement（数式表示未対応）\n"
        )

    packages = {
        "homotopy_groups": {"TodaPrimaryGroup": Group},
        "phase165_r52_partial_proof": {"PartialProofResult": Result, "ProofSearchStatus": Status},
        "phase168_r3_3_proof_narrative_model": {"build_proof_narrative_model": bind},
        "phase168_r3_5_model_renderer": {"render_model_backed_narrative_markdown": render},
        "proof": {"ProofRule": Rule, "ProofStep": Step},
    }
    for name, contents in packages.items():
        module = ModuleType(name)
        for key, value in contents.items():
            setattr(module, key, value)
        monkeypatch.setitem(sys.modules, name, module)
    source = Path(__file__).resolve().parents[1] / "tree_adapter.py"
    namespace = runpy.run_path(str(source))
    return namespace, Group, Rule, Step, results


def test_uses_original_verified_tree_and_standard_model_renderer(monkeypatch):
    namespace, Group, Rule, Step, results = _load_isolated_adapter(monkeypatch)
    leaf = Step(rule=Rule.GIVEN)
    root = Step(rule=Rule.INFERENCE, premises=(leaf,))
    target = Group()
    lines = namespace["render_verified_tree_progress"](target, root)
    assert results[-1].target is target
    assert results[-1].proven_steps == (leaf, root)
    assert results[-1].status == "partial"
    assert "**[R1] Example source.**" in lines
    assert "- 与件: $\\pi_{3}^{2}=0$" in lines
    assert not any("UnsupportedStatement" in line for line in lines)
    assert "### 検証済み ProofStep" in lines


def test_cyclic_or_unverified_evidence_fails_closed(monkeypatch):
    namespace, Group, Rule, Step, results = _load_isolated_adapter(monkeypatch)
    unverified = Step(rule=Rule.INFERENCE, premises=())
    with pytest.raises(ValueError, match="inference guard"):
        namespace["verified_tree_postorder"](unverified)
    cycle = Step(rule=Rule.INFERENCE)
    cycle.premises = (cycle,)
    with pytest.raises(ValueError, match="cyclic proof ancestry"):
        namespace["verified_tree_postorder"](cycle)
