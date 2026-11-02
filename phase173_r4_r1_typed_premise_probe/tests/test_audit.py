"""Offline focused tests for the R4-R1 proof-premise audit only."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase173_r4_r1_typed_premise_probe import audit


def test_rule_inventory_has_six_unique_factories() -> None:
    assert len(audit.RULE_FACTORIES) == 6
    assert len(set(audit.RULE_FACTORIES)) == 6


def test_extract_rule_factory_and_references() -> None:
    source = """
def toda_prop44_isomorphism_inference_rule():
    return InferenceRule(name='old iso', premise_patterns=(PremisePattern(),), conclusion_pattern='x')
"""
    found = audit.inspect_factories(source)
    assert found[0]["definition_count"] == 1
    assert found[0]["registered_rule_names"] == ["old iso"]
    assert found[0]["uses_typed_premises"] is True
    assert found[0]["has_explicit_reference"] is False
    assert found[1]["definition_count"] == 0


def test_duplicate_rule_factory_is_not_accepted_as_unique() -> None:
    source = """
def toda_prop44_isomorphism_inference_rule():
    return 1

def toda_prop44_isomorphism_inference_rule():
    return 2
"""
    assert audit.inspect_factories(source)[0]["definition_count"] == 2


def test_candidate_summary_does_not_claim_success() -> None:
    class Rule:
        name = "candidate"
    class Option:
        rule = Rule()
        subgoals = ("unproved",)
    assert audit.candidate_summary((Option(),)) == [
        {"rule_name": "candidate", "premise_types": ["str"],
         "premises": ["'unproved'"]}
    ]


def test_reviewed_head_is_strictly_pinned() -> None:
    assert audit.REVIEWED_HEADS == {
        "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941",
        "6f5adde0a0e0f124d5247ef6b1c255f83697f42b",
        "c352f7d24d3156ba7cde26ebb0933c4680a8c813",
    }


def test_production_blob_guard_fails_on_changed_source(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941"
        if args[:1] == ("rev-parse",):
            return "unreviewed"
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="Committed reviewed source blob changed"):
        audit.guard_source_files(tmp_path)


@pytest.mark.parametrize("exit_code", [1, 2, 128])
def test_tracked_source_changes_rejected(monkeypatch, tmp_path: Path, exit_code: int) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941"
        if args[:1] == ("rev-parse",):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: type("Result", (), {"returncode": exit_code})())
    with pytest.raises(RuntimeError, match="Reviewed source has local modifications"):
        audit.guard_source_files(tmp_path)


def test_audit_has_no_production_write_functions() -> None:
    from inspect import getsource
    source = getsource(audit)
    assert "git reset" not in source
    assert "git checkout" not in source
    assert "git restore" not in source
    assert "production_changes\": []" in source


def test_reviewed_c352_head_accepts_only_unchanged_source_blobs(monkeypatch, tmp_path: Path) -> None:
    expected_head = "c352f7d24d3156ba7cde26ebb0933c4680a8c813"
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return expected_head
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(
        audit.subprocess, "run",
        lambda *args, **kwargs: type("GitResult", (), {"returncode": 0})(),
    )
    report = audit.guard_source_files(tmp_path)
    assert report["head"] == expected_head
    assert report["reviewed_unchanged"] is True
    assert report["git_mutated"] is False
    assert set(report["source_paths"]) == set(audit.REVIEWED_BLOBS)


def test_unknown_new_head_still_rejected(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "not-reviewed-after-c352"
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="Unreviewed HEAD"):
        audit.guard_source_files(tmp_path)
