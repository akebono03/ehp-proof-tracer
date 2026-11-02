"""Offline tests of the Phase 173 R4-R3 read-only audit boundaries."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r3_premise_frontier_audit import audit


class FiniteCyclicGroup:
    def __init__(self, order: int):
        self.order = order


class FreeCyclicGroup:
    pass


class TodaPrimaryGroupZeroStatement:
    pass


class DirectSumGroup:
    def __init__(self, *summands: object):
        self.summands = tuple(summands)


class Relation:
    def __init__(self, rhs: object):
        self.rhs = rhs


def test_structure_is_only_an_abstract_comparison() -> None:
    target = Relation(DirectSumGroup(FiniteCyclicGroup(2), FreeCyclicGroup()))
    assert audit.abstract_signature(target) == ("Z", "Z/2")
    assert audit.abstract_signature(Relation(TodaPrimaryGroupZeroStatement())) == ()
    assert audit.abstract_signature(FiniteCyclicGroup(8)) == ("Z/8",)


def test_structure_rejects_unsupported_and_invalid_orders() -> None:
    assert audit.abstract_signature(object()) is None
    assert audit.abstract_signature(FiniteCyclicGroup(1)) is None
    assert audit.abstract_signature(FiniteCyclicGroup(True)) is None
    assert audit.abstract_signature(DirectSumGroup(FiniteCyclicGroup(2), object())) is None


def test_source_coordinates_4_group_replay() -> None:
    assert audit.SOURCE_COORDINATES == ((7, 0), (7, 1), (7, 2), (7, 3))
    assert audit.REVIEWED_HEAD == "8be7b92a12bb3a58119d13491db5dbcffd71eb91"


def test_preflight_fails_on_wrong_head(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    answers = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "old",
        ("rev-parse", "--show-toplevel"): str(tmp_path),
    }
    monkeypatch.setattr(audit, "git", lambda root, *args: answers[args])
    with pytest.raises(RuntimeError, match="unreviewed"):
        audit.preflight(tmp_path, remote=False)


def test_worker_validates_typed_coordinate_and_sentinel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    row = {"n": 7, "k": 1, "search_status": "complete", "web_key": "generic-complete-proof",
           "open_goals": 0, "proven_steps": 3, "diagnostics": []}
    observed = {}

    def fake_run(cmd, **kwargs):
        observed["cmd"] = cmd
        return SimpleNamespace(returncode=0, stdout=audit.WEB_SENTINEL + json.dumps(row), stderr="")

    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    result = audit.source_worker(tmp_path, 7, 1, 5, tmp_path)
    assert result["status"] == "complete"
    assert result["open_goals"] == 0
    assert observed["cmd"][-4:] == ["--n", "7", "--k", "1"]
    assert (tmp_path / "n_007_k_001.log").exists()


def test_worker_does_not_silently_accept_another_group(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(returncode=0, stdout=audit.WEB_SENTINEL +
                                        json.dumps({"n": 7, "k": 2}), stderr=""))
    row = audit.source_worker(tmp_path, 7, 1, 5, tmp_path)
    assert row["status"] == "WRONG_GROUP"


def test_write_report_does_not_promote_abstract_match(tmp_path: Path) -> None:
    report = {"matrix": {"n4_toda56": [{"group": "pi_10^4",
                 "abstract_structure_compatible": True,
                 "first_input_db_exists": True, "second_input_db_exists": True,
                 "existing_pi74_root_shape": False,
                 "generator_image_verified": False}]}, "source_workers": []}
    audit.write_report(tmp_path, report)
    data = json.loads((tmp_path / "audit.json").read_text(encoding="utf-8"))
    assert data["matrix"]["n4_toda56"][0]["generator_image_verified"] is False
    assert "NOT a verified derivation" in (tmp_path / "audit.md").read_text(encoding="utf-8")


def test_dryrun_does_not_import_proof_system_or_run_workers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda root, remote: {
        "branch": "develop", "head": audit.REVIEWED_HEAD,
        "source_guard": "PASS", "remote_checked": remote,
    })
    monkeypatch.setattr(audit, "analyze_groups", lambda: pytest.fail("no live analysis in dryrun"))
    monkeypatch.setattr(audit, "source_worker", lambda *a, **kw: pytest.fail("no workers in dryrun"))
    assert audit.run(tmp_path, dry_run=True, timeout=10, remote=False) == 0
    reports = list((tmp_path / "EHPProofTracerRecovery").glob("phase173_r4_r3_*/audit.json"))
    assert len(reports) == 1
    saved = json.loads(reports[0].read_text(encoding="utf-8"))
    assert saved["result"] == "DRY_RUN_PASS"
    assert saved["tracked_unchanged"] is True
