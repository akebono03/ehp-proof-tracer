"""Audit guard regression tests on real temporary Git histories."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

from phase175_r3r7_lemma54_membership import audit


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def commit(root: Path, message: str) -> str:
    git(root, "add", "-A")
    git(root, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "baseline.py").write_text("production = 'unchanged'\n", encoding="utf-8")
    start = commit(root, "reviewed source state")
    return root, start


@pytest.mark.parametrize("path", [
    "phase175_r3r6_lemma57_general/rule.py",
    "phase175_r3r7_lemma54_membership/rule.py",
    "phase175_r3r7_lemma54_membership/tests/test_rule.py",
])
def test_only_named_audit_additions_accepted(repo, path: str) -> None:
    root, start = repo
    file = root / path
    file.parent.mkdir(parents=True)
    file.write_text("isolated audit only\n", encoding="utf-8")
    end = commit(root, "add reviewed audit file")
    result = audit.verify_lineage(root, {"preflight": {"head": start}}, {"head": end})
    assert result["audit_only_paths"] == [path]
    assert result["r3r7_added_paths"] == ([path] if path in audit.ALLOWED_NEW_FILES else [])


@pytest.mark.parametrize("path", [
    "src/core.py",
    "phase175_r3r7_lemma54_membership/unreviewed_rule.py",
    "phase175_r3r6_lemma57_general/secret.py",
])
def test_unknown_addition_rejected(repo, path: str) -> None:
    root, start = repo
    file = root / path
    file.parent.mkdir(parents=True)
    file.write_text("unexpected\n", encoding="utf-8")
    end = commit(root, "unreviewed new file")
    with pytest.raises(RuntimeError, match="R3R7_UNKNOWN_LINEAGE_ADDITION"):
        audit.verify_lineage(root, {"preflight": {"head": start}}, {"head": end})


def test_modified_production_rejected(repo) -> None:
    root, start = repo
    (root / "baseline.py").write_text("production = 'changed'\n", encoding="utf-8")
    end = commit(root, "modify production")
    with pytest.raises(RuntimeError, match="R3R7_NON_AUDIT_CHANGE_IN_LINEAGE"):
        audit.verify_lineage(root, {"preflight": {"head": start}}, {"head": end})


def test_success_report_required_before_any_audit(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    with pytest.raises(RuntimeError, match="R3R7_NO_VERIFIED_R3R6"):
        audit.latest_successful_r3r6()
    parent = tmp_path / "EHPProofTracerAudit" / "phase175_r3r6_lemma57_general" / "20260101"
    parent.mkdir(parents=True)
    (parent / "report.json").write_text(json.dumps({
        "phase": "175-R3R6", "dry_run": False,
        "result": "PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED",
        "tracked_unchanged": True, "new_production_given": 0,
        "worker": {"data": {
            "source_general_given_count": 1,
            "particular_nu_prime_given_count": 0,
            "observations": [
                {"name": "double_suspension_membership", "status": "UNRESOLVED"},
                {"name": "lemma57_zero_generator_image", "status": "UNRESOLVED"},
            ],
        }},
    }), encoding="utf-8")
    assert audit.latest_successful_r3r6() == parent / "report.json"
