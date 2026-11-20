"""Focused tests for the R3R13 read-only audit infrastructure."""
from __future__ import annotations

import json

import pytest

from phase176_r3r13_two_boundary_audit import audit


def test_static_wiring_check_detects_unregistered_provider(tmp_path):
    path = tmp_path / "phase165_r52_r9_shared_math.py"
    path.write_text("def shared_expansion_provider():\n    pass\n", encoding="utf-8")
    result = audit.static_wiring_check(tmp_path)
    assert result["no_direct_registration_detected"] is True
    path.write_text("expand_right_zero_transport\n", encoding="utf-8")
    assert audit.static_wiring_check(tmp_path)["no_direct_registration_detected"] is False


def test_source_preflight_fails_closed(tmp_path):
    for name, anchors in audit.REQUIRED.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("\n".join(anchors), encoding="utf-8")
    assert len(audit.source_preflight(tmp_path)) == len(audit.REQUIRED)
    (tmp_path / next(iter(audit.REQUIRED))).write_text("bad", encoding="utf-8")
    with pytest.raises(RuntimeError, match="REQUIRED_ANCHOR_MISSING"):
        audit.source_preflight(tmp_path)


def test_previous_report_rejects_unproved_claim(tmp_path):
    path = tmp_path / "EHPProofTracerAudit" / "phase176_r3r10_right_zero_transport_isolated" / "report.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"gate": "PASS_R3R10_ISOLATED_RIGHT_ZERO_TRANSPORT", "observed": {
        "base_step_inferred": True, "isolated_composite_zero_step_inferred": True,
        "shared_composite_zero_candidates": 0, "root_proof_complete": True}}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R10_EVIDENCE_NOT_VALIDATED"):
        audit.get_previous(tmp_path)


def test_previous_report_accepts_exact_isolated_boundary(tmp_path):
    path = tmp_path / "EHPProofTracerAudit" / "phase176_r3r10_right_zero_transport_isolated" / "report.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"gate": "PASS_R3R10_ISOLATED_RIGHT_ZERO_TRANSPORT", "observed": {
        "base_step_inferred": True, "isolated_composite_zero_step_inferred": True,
        "shared_composite_zero_candidates": 0, "root_proof_complete": False}}), encoding="utf-8")
    assert audit.get_previous(tmp_path)["observed"]["root_proof_complete"] is False
