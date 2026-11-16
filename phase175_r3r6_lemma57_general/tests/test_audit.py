"""Source guard ancestry and report shape tests, independent of the user checkout."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase175_r3r6_lemma57_general import audit


def valid_r3r5_report() -> dict:
    return {
        "phase": "175-R3R5",
        "dry_run": False,
        "result": "PASS_R3R5_LEMMA57_FRONTIER_RECORDED",
        "tracked_unchanged": True,
        "new_given": 0,
        "new_math_rules": 0,
        "worker": {
            "data": {
                "obligations": [
                    {"name": "ehp_exactness", "status": "INFERRED"},
                    {"name": "lower_pi62_group", "status": "INFERRED"},
                    {"name": "zero_generator_image", "status": "UNRESOLVED"},
                    {"name": "zero_suspension_image", "status": "UNRESOLVED"},
                    {"name": "hopf_injectivity", "status": "UNRESOLVED"},
                ],
            },
        },
    }


def write_prior(tmp_path: Path, document: dict) -> None:
    path = tmp_path / "EHPProofTracerAudit" / "phase175_r3r5_pi73_lemma57_frontier" / "20261116T011655_428931Z"
    path.mkdir(parents=True)
    (path / "report.json").write_text(json.dumps(document), encoding="utf-8")


def test_latest_r3r5_requires_real_verified_normal_run(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    write_prior(tmp_path, valid_r3r5_report())
    assert audit.latest_r3r5_report().name == "report.json"


@pytest.mark.parametrize("mutation", ["dry_run", "bad_gate", "inferred_zero", "new_given", "changed"])
def test_latest_r3r5_fails_closed(monkeypatch, tmp_path, mutation: str) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    value = valid_r3r5_report()
    if mutation == "dry_run":
        value["dry_run"] = True
    elif mutation == "bad_gate":
        value["result"] = "PASS_R3R5_READ_ONLY_DRYRUN"
    elif mutation == "inferred_zero":
        value["worker"]["data"]["obligations"][2]["status"] = "INFERRED"
    elif mutation == "new_given":
        value["new_given"] = 1
    elif mutation == "changed":
        value["tracked_unchanged"] = False
    write_prior(tmp_path, value)
    with pytest.raises(RuntimeError, match="R3R6_NO_VERIFIED_R3R5_FRONTIER_REPORT"):
        audit.latest_r3r5_report()


def test_report_preserves_full_obligations(tmp_path) -> None:
    report = {
        "result": "PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED",
        "worker": {"data": {"observations": [
            {"name": "double_suspension_membership", "status": "UNRESOLVED", "offered_routes": 0,
             "observed_unresolved": ["unproved E2 membership"]},
        ]}},
    }
    audit.write_report(tmp_path, report)
    content = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert content["worker"]["data"]["observations"][0]["status"] == "UNRESOLVED"
    markdown = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "double_suspension_membership" in markdown
    assert "unproved E2 membership" in markdown
