"""Focused contracts for the read-only four-premise diagnostic."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r7r1_pi84_premise_diagnostic import audit


@dataclass(frozen=True)
class Statement:
    name: str


@dataclass(frozen=True)
class Step:
    conclusion: Statement
    rule: str
    note: str | None = None
    inference_rule: object | None = None


class AlwaysFalseRule:
    def match_guard(self, premises, bindings) -> bool:
        return False


def test_missing_second_prior_remains_missing() -> None:
    obligations = tuple(Statement(str(i)) for i in range(4))
    observed = (Step(obligations[0], "GIVEN"),
                Step(obligations[1], "GIVEN", "ADOPTED_DATABASE_PRIOR"),
                Step(obligations[3], "INFERENCE"))
    db_steps = (None, observed[1], Step(obligations[2], "GIVEN"), None)
    rows = audit.premise_diagnosis(
        obligations, observed, observed, db_steps,
        lambda i, step: step == db_steps[i], AlwaysFalseRule(),
    )
    assert len(rows) == 4
    assert rows[2]["observed_count"] == 0
    assert rows[2]["adopted_db_available"] is True
    assert rows[1]["observed_verified_db"] == [True]
    assert rows[0]["direct_fixed_count"] == 1


def test_non_database_given_is_never_mislabelled() -> None:
    obligations = tuple(Statement(str(i)) for i in range(4))
    bad = Step(obligations[2], "GIVEN", "CITED_FIXED")
    expected = Step(obligations[2], "GIVEN", "ADOPTED_DATABASE_PRIOR")
    rows = audit.premise_diagnosis(
        obligations, (bad,), (bad,), (None, None, expected, None),
        lambda i, step: step == expected, AlwaysFalseRule(),
    )
    assert rows[2]["observed_verified_db"] == [False]
    assert rows[2]["observed_db_equal"] == [False]
    assert rows[2]["direct_fixed_count"] == 1


def test_rejects_non_four_obligations() -> None:
    with pytest.raises(ValueError, match="four"):
        audit.premise_diagnosis((Statement("one"),), (), (), (), lambda i, s: True, AlwaysFalseRule())


def test_rejects_noncallable_db_verifier() -> None:
    obligations = tuple(Statement(str(i)) for i in range(4))
    with pytest.raises(TypeError, match="callable"):
        audit.premise_diagnosis(obligations, (), (), (None,) * 4, None, AlwaysFalseRule())


def test_preflight_rejects_wrong_commit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path.resolve()
    responses = {("rev-parse", "--show-toplevel"): str(root),
                 ("branch", "--show-current"): "develop",
                 ("rev-parse", "HEAD"): "incorrect"}
    monkeypatch.setattr(audit, "git", lambda base, *args: responses[args])
    with pytest.raises(RuntimeError, match="unreviewed"):
        audit.preflight(root, remote=False)


def test_preflight_rejects_dirty_worktree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path.resolve()
    responses = {("rev-parse", "--show-toplevel"): str(root),
                 ("branch", "--show-current"): "develop",
                 ("rev-parse", "HEAD"): audit.REVIEWED_HEAD,
                 ("status", "--porcelain", "--untracked-files=no"): " M proof.py"}
    monkeypatch.setattr(audit, "git", lambda base, *args: responses[args])
    with pytest.raises(RuntimeError, match="tracked"):
        audit.preflight(root, remote=False)


def test_dryrun_never_calls_live_search(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda root, remote: {
        "branch": "develop", "head": audit.REVIEWED_HEAD, "source_guard": "PASS"})
    monkeypatch.setattr(audit, "inspect_live", lambda root: pytest.fail("DryRun must not search"))
    assert audit.run(tmp_path, dry_run=True, remote=False) == 0
    reports = list((tmp_path / "EHPProofTracerRecovery").glob("*/audit.json"))
    assert len(reports) == 1
    data = json.loads(reports[0].read_text(encoding="utf-8"))
    assert data["result"] == "DRY_RUN_PASS"
    assert data["tracked_unchanged"] is True


def test_constants_are_strict() -> None:
    assert len(audit.REVIEWED_HEAD) == 40
    assert all(len(value) == 40 for value in audit.REVIEWED_BLOBS.values())
    assert audit.REVIEWED_HEAD.startswith("fc6631c1")
