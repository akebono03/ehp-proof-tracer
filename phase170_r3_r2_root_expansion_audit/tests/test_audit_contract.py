"""Offline contract tests for root-expansion diagnostics; no production imports."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest


def audit_module():
    file_path = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("phase170_r3_r2_contract", file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_zero_root_proposals_are_not_certified_missing_theorems():
    assert audit_module().classify_root_evidence({"root_expansion_count": 0}) == "NO_ROOT_EXPANSION_PROPOSED"


def test_root_candidates_with_open_subgoals_are_classified_conservatively():
    result = audit_module().classify_root_evidence({
        "root_expansion_count": 3,
        "proposed_subgoal_occurrences": 7,
        "directly_given_subgoal_occurrences": 2,
    })
    assert result == "ROOT_EXPANSIONS_WITH_UNPROVED_SUBGOALS"


def test_root_candidates_without_unmatched_direct_goals_not_certified_complete():
    result = audit_module().classify_root_evidence({
        "root_expansion_count": 1,
        "proposed_subgoal_occurrences": 2,
        "directly_given_subgoal_occurrences": 2,
    })
    assert result == "ROOT_EXPANSIONS_PRESENT_REPLAY_UNRESOLVED"


@pytest.mark.parametrize("invalid", [None, -1, True, "3", 2.0])
def test_invalid_root_expansion_counts_are_not_accepted(invalid):
    assert audit_module().classify_root_evidence({"root_expansion_count": invalid}) == "PROPOSAL_AUDIT_UNDETERMINED"


def test_preview_clips_long_repr():
    shortened = audit_module().clipped("x" * 50, 10)
    assert shortened.endswith(" [TRUNCATED]")
    assert len(shortened) < 50


def test_reviewed_source_hash_guard_rejects_modified_audit(tmp_path):
    source = tmp_path / "phase170_r3_r1_failure_frontier_audit" / "audit.py"
    source.parent.mkdir()
    source.write_text("# unreviewed version\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="differs"):
        audit_module().load_reviewed_r3_code(tmp_path)


def test_report_guard_rejects_malformed_r3(tmp_path):
    path = tmp_path / "audit.json"
    path.write_text(json.dumps({"phase": "170 R3-R1", "mode": "AUDIT_ONLY"}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="not a reviewed"):
        audit_module().check_reports(SimpleNamespace(), tmp_path, path)


def test_report_guard_rejects_wrong_filename(tmp_path):
    path = tmp_path / "evidence.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(RuntimeError, match="audit.json"):
        audit_module().check_reports(SimpleNamespace(), tmp_path, path)


def test_expansion_audit_finds_exact_given_without_proving(monkeypatch):
    expansion_module = ModuleType("phase165_r3_recursive_search")
    proof_module = ModuleType("proof")

    class GoalExpansion:
        def __init__(self, rule, subgoals):
            self.rule = rule
            self.subgoals = subgoals

    class ProofRule:
        GIVEN = object()

    expansion_module.GoalExpansion = GoalExpansion
    proof_module.ProofRule = ProofRule
    monkeypatch.setitem(sys.modules, "phase165_r3_recursive_search", expansion_module)
    monkeypatch.setitem(sys.modules, "proof", proof_module)
    step = SimpleNamespace(rule=ProofRule.GIVEN, conclusion="a")
    screened = SimpleNamespace(proof_links=(SimpleNamespace(step=step),))
    proposals = (GoalExpansion(SimpleNamespace(name="rule", literature_reference=None), ("a", "b")),)
    report = audit_module().evaluate_root_proposals(proposals, screened, "root")
    assert report["root_expansion_count"] == 1
    assert report["root_exact_given_count"] == 0
    assert report["directly_given_subgoal_occurrences"] == 1
    assert report["proposals"][0]["subgoals"][1]["screened_exact_given"] is False


def test_expansion_audit_rejects_non_expansion_objects(monkeypatch):
    expansion_module = ModuleType("phase165_r3_recursive_search")
    proof_module = ModuleType("proof")

    class GoalExpansion:
        pass

    expansion_module.GoalExpansion = GoalExpansion
    proof_module.ProofRule = SimpleNamespace(GIVEN=object())
    monkeypatch.setitem(sys.modules, "phase165_r3_recursive_search", expansion_module)
    monkeypatch.setitem(sys.modules, "proof", proof_module)
    with pytest.raises(TypeError, match="typed GoalExpansion"):
        audit_module().evaluate_root_proposals((object(),), SimpleNamespace(proof_links=()), "root")


def test_root_expansion_audit_caps_display_not_total(monkeypatch):
    expansion_module = ModuleType("phase165_r3_recursive_search")
    proof_module = ModuleType("proof")

    class GoalExpansion:
        def __init__(self):
            self.rule = SimpleNamespace(name="r", literature_reference=None)
            self.subgoals = ()

    expansion_module.GoalExpansion = GoalExpansion
    proof_module.ProofRule = SimpleNamespace(GIVEN=object())
    monkeypatch.setitem(sys.modules, "phase165_r3_recursive_search", expansion_module)
    monkeypatch.setitem(sys.modules, "proof", proof_module)
    report = audit_module().evaluate_root_proposals(
        tuple(GoalExpansion() for _ in range(42)), SimpleNamespace(proof_links=()), "x"
    )
    assert report["root_expansion_count"] == 42
    assert report["recorded_expansion_count"] == 40
    assert report["unrecorded_expansion_count"] == 2


def test_root_report_markdown_explains_nonproof_status():
    markdown = audit_module().render_markdown({
        "head": "test", "r3_report": "R3", "tracked_unchanged": True,
        "cases": [],
    })
    assert "候補の存在は証明の完成" in markdown
    assert "全体 pytest: 未実行" in markdown
