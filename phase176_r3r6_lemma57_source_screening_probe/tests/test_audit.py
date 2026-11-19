"""R3R6 read-only source audit regression tests."""
from __future__ import annotations

import json

import pytest

from phase176_r3r6_lemma57_source_screening_probe import audit


def test_source_contract_accepts_fixture(tmp_path) -> None:
    for name, anchors in audit.REQUIRED.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(anchors), encoding="utf-8")
    assert set(audit.source_contract(tmp_path)) == set(audit.REQUIRED)


def test_missing_source_anchor_fails_closed(tmp_path) -> None:
    for name in audit.REQUIRED:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("unrelated", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHORS_MISSING"):
        audit.source_contract(tmp_path)


def test_expansion_is_not_proof() -> None:
    class Rule:
        name = "fixture rule"

    class Expansion:
        rule = Rule()
        subgoals = ("still open",)

    summary = audit.option_details((Expansion(),))
    assert summary["count"] == 1
    assert summary["status"] == "UNVERIFIED_PROPOSALS"
    assert summary["options"][0]["subgoals"] == ["'still open'"]


def test_empty_expansion_is_distinguished() -> None:
    assert audit.option_details(())["count"] == 0


def test_worker_rejects_false_proof_claim(monkeypatch) -> None:
    import subprocess

    class Process:
        returncode = 0
        stdout = audit.MARKER + json.dumps({"new_given": 0, "any_proof_claimed": True})
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: Process())
    with pytest.raises(RuntimeError, match="AUDIT_MUST_NOT_CLAIM_PROOF"):
        audit.worker(5)


def test_dry_run_has_no_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "test"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker must not run"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    path = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["full_pytest"] == "NOT_RUN"
    assert report["new_given"] == 0
