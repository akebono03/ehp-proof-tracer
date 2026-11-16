"""R3R5 audit-only evidence gates and no-forged-proof contracts."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase175_r3r5_pi73_lemma57_frontier import audit


def prior_report() -> dict:
    return {
        "phase": "175-R3",
        "dry_run": False,
        "result": "PASS_R3_PI73_HOPF_FRONTIER_RECORDED",
        "tracked_unchanged": True,
        "new_given": 0,
        "worker": {"data": {
            "target_direct_given_excluded": True,
            "hopf_lift_candidate_count": 1,
            "subgoal_observations": [
                {"name": "hopf_injectivity", "status": "UNRESOLVED"},
                {"name": "cyclic_codomain", "status": "INFERRED"},
                {"name": "hopf_generator_image", "status": "INFERRED"},
                {"name": "source_bound_cyclic_codomain", "status": "INFERRED"},
            ],
        }},
    }


def write_report(root: Path, result: dict, stamp: str = "20261112T001000_123456Z") -> Path:
    location = root / "EHPProofTracerAudit" / "phase175_r3_pi73_hopf_lift" / stamp
    location.mkdir(parents=True, exist_ok=True)
    target = location / "report.json"
    target.write_text(json.dumps(result), encoding="utf-8")
    return target


def test_latest_real_r3r4_report_is_admitted(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    path = write_report(tmp_path, prior_report())
    assert audit.latest_verified_r3_report() == path


@pytest.mark.parametrize("changes", [
    {"dry_run": True},
    {"result": "PASS_R3_READ_ONLY_DRYRUN"},
    {"tracked_unchanged": False},
    {"new_given": 1},
])
def test_invalid_r3r4_evidence_refused(tmp_path: Path, monkeypatch, changes: dict) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    write_report(tmp_path, {**prior_report(), **changes})
    with pytest.raises(RuntimeError, match="NO_VERIFIED_R3R4"):
        audit.latest_verified_r3_report()


def test_unproved_hopf_injectivity_required(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    entry = prior_report()
    entry["worker"]["data"]["subgoal_observations"][0]["status"] = "INFERRED"
    write_report(tmp_path, entry)
    with pytest.raises(RuntimeError):
        audit.latest_verified_r3_report()


def test_direct_given_codomain_not_counted_as_success(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    entry = prior_report()
    entry["worker"]["data"]["subgoal_observations"][1]["status"] = "DIRECT_GIVEN_NOT_ACCEPTABLE"
    write_report(tmp_path, entry)
    with pytest.raises(RuntimeError):
        audit.latest_verified_r3_report()


def test_report_written_outside_source_tree(tmp_path: Path) -> None:
    folder = tmp_path / "evidence"
    folder.mkdir()
    payload = {
        "result": "PASS_R3R5_READ_ONLY_DRYRUN",
        "preflight": {"toda_lemma57_source": {"locator": "Lemma 5.7", "source_blob": "a" * 40}},
    }
    audit.write_report(folder, payload)
    assert json.loads((folder / "report.json").read_text()) == payload
    assert "Lemma 5.7" in (folder / "report.md").read_text()


def test_audit_package_never_writes_to_production_paths() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert '"new_given": 0' in source
    assert '"production_changes": []' in source
    assert "--worker" in source
    assert "git reset" not in source
    assert "git add" not in source
