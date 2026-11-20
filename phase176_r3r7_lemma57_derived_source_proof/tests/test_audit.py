"""Focused regression tests for Phase 176 R3R7."""
from __future__ import annotations

import json

import pytest

from phase176_r3r7_lemma57_derived_source_proof import audit


def test_source_contract_matches_fixture(tmp_path) -> None:
    for name, anchors in audit.REQUIRED.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("\n".join(anchors), encoding="utf-8")
    assert set(audit.check_sources(tmp_path)) == set(audit.REQUIRED)


def test_missing_source_text_rejected(tmp_path) -> None:
    for name in audit.REQUIRED:
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("unrelated", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.check_sources(tmp_path)


def test_lemma57_anchor_preserves_nu_prime() -> None:
    anchors = audit.REQUIRED["sources/toda/Toda_05_2.tex"]
    assert r"E(\eta_2\circ\nu')=0" in anchors
    assert r"\nu\'" not in "".join(anchors)


def fake_proof_modules(monkeypatch):
    import sys
    from enum import Enum
    from types import ModuleType

    class ProofRule(Enum):
        GIVEN = "given"
        INFERENCE = "inference"

    class ProofStep:
        def __init__(self, conclusion, premises, rule):
            self.conclusion = conclusion
            self.premises = premises
            self.rule = rule

    proof = ModuleType("proof")
    proof.ProofRule = ProofRule
    proof.ProofStep = ProofStep
    proof.find_inference_matches_for_rule = lambda rule, premises: ()
    factory = ModuleType("phase164_r8_proofstep_factory")
    factory.derive_inference_proof_step = lambda match: None
    monkeypatch.setitem(sys.modules, "proof", proof)
    monkeypatch.setitem(sys.modules, "phase164_r8_proofstep_factory", factory)
    return ProofRule, ProofStep


def test_derived_step_rejects_nonproof_source(monkeypatch) -> None:
    fake_proof_modules(monkeypatch)

    class Expansion:
        subgoals = ("cited",)

    with pytest.raises(RuntimeError, match="SCREENED_GIVEN_REQUIRED"):
        audit.derive_from_existing_source(Expansion(), "cited")


def test_derived_step_rejects_unrelated_source(monkeypatch) -> None:
    ProofRule, ProofStep = fake_proof_modules(monkeypatch)

    class Expansion:
        subgoals = ("correct",)

    with pytest.raises(RuntimeError, match="EXACT_SOURCE_PREMISE_REQUIRED"):
        audit.derive_from_existing_source(
            Expansion(), ProofStep("wrong", (), ProofRule.GIVEN)
        )


def test_worker_rejects_false_completion(monkeypatch) -> None:
    class Completed:
        returncode = 0
        stdout = audit.MARKER + json.dumps({
            "base_step_inferred_in_isolation": True,
            "root_proof_complete": True,
            "new_given": 0,
            "source_installed_into_production": False,
        }) + "\n"
        stderr = ""

    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: Completed())
    with pytest.raises(RuntimeError, match="WORKER_FALSE_PROOF_OR_SOURCE_CLAIM"):
        audit.worker(5)


def test_dry_run_does_not_call_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "fixture"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker launched"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text())
    assert report["gate"] == "PASS_R3R7_READ_ONLY_DRYRUN"
    assert report["new_given"] == 0
    assert report["root_proof_complete"] is False
    assert report["full_pytest"] == "NOT_RUN"
