"""R4R11 provenance, reviewed local history, and prior-report contracts."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase175_r4r11_signed_eta_torsion_public import audit, installer


def passed_r4r10_report() -> dict[str, object]:
    return {
        "phase": "175-R4R10", "dry_run": False, "gate": audit.PRIOR_GATE,
        "new_given": 2, "new_mathematical_rules": 0,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
        "preflight": {"head": audit.BASE_HEAD},
        "delta_composition_replay": {
            "conclusion_is_signed": True,
            "proposition_2_5_citation_present": True,
            "equation_5_8_citation_present": True,
            "eta_family_citation_present": True,
            "signed_parent_inferred": True,
            "composition_identity_parent_inferred": True,
            "root_group_conclusion_inferred": False,
        },
        "public": {
            "public_prop25_candidate_found": True,
            "public_signed_parent_candidate_found": True,
            "public_identity_parent_candidate_found": True,
            "public_root_pi95_proof_complete": False,
        },
        "install": {
            "production_path": installer.TARGET.as_posix(),
            "after_git_blob": installer.BASE_WORKING_BLOB,
            "two_full_functions_exported": True,
        },
    }


def test_valid_real_report_shape_is_accepted_not_promoted() -> None:
    result = audit.validate_prior(passed_r4r10_report())
    assert result["successful_prior"] is True
    assert result["pi95_not_yet_complete"] is True


@pytest.mark.parametrize("key,change", (
    ("dry_run", True), ("phase", "175-R4R8"),
    ("gate", audit.DRY_GATE), ("new_given", 0),
    ("new_mathematical_rules", 1), ("pi95_proof_complete", True),
    ("full_pytest_executed", True), ("prior_proof_search_executed", True),
))
def test_prior_scope_tamper_rejected(key: str, change: object) -> None:
    report = passed_r4r10_report()
    report[key] = change
    with pytest.raises(RuntimeError, match="GATE_OR_SCOPE_CHANGED"):
        audit.validate_prior(report)


@pytest.mark.parametrize("section,key,change", (
    ("preflight", "head", "0" * 40),
    ("delta_composition_replay", "conclusion_is_signed", False),
    ("delta_composition_replay", "signed_parent_inferred", False),
    ("delta_composition_replay", "eta_family_citation_present", False),
    ("delta_composition_replay", "root_group_conclusion_inferred", True),
    ("public", "public_prop25_candidate_found", False),
    ("public", "public_signed_parent_candidate_found", False),
    ("public", "public_identity_parent_candidate_found", False),
    ("public", "public_root_pi95_proof_complete", True),
    ("install", "production_path", "proof.py"),
    ("install", "two_full_functions_exported", False),
))
def test_prior_evidence_tamper_rejected(
    section: str, key: str, change: object,
) -> None:
    report = deepcopy(passed_r4r10_report())
    report[section][key] = change
    with pytest.raises(RuntimeError, match="EVIDENCE_INVALID"):
        audit.validate_prior(report)


def test_latest_successful_report_is_selected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    older = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE / "old" / "report.json"
    newer = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE / "new" / "report.json"
    older.parent.mkdir(parents=True)
    newer.parent.mkdir(parents=True)
    older.write_text(json.dumps(passed_r4r10_report()), encoding="utf-8")
    tampered = passed_r4r10_report()
    tampered["gate"] = "FAIL"
    newer.write_text(json.dumps(tampered), encoding="utf-8")
    assert audit.find_prior(None) == older
    assert audit.find_prior(older) == older.resolve()


def fake_git_factory(root: Path, head: str, changed: str = ""):
    def fake_git(repository: Path, *args: str, allow_failure: bool = False):
        if args == ("rev-parse", "--show-toplevel"):
            return 0, str(root)
        if args == ("branch", "--show-current"):
            return 0, "develop"
        if args == ("rev-parse", "HEAD"):
            return 0, head
        if args == ("diff", "--name-only"):
            return 0, changed
        if args == ("diff", "--cached", "--name-only"):
            return 0, ""
        if args == ("merge-base", "--is-ancestor", audit.BASE_HEAD, head):
            return 0, ""
        if args == ("diff", "--name-only", audit.BASE_HEAD, head):
            return 0, audit.PRIOR_PACKAGE + "/source.py\n" + installer.TARGET.as_posix()
        raise AssertionError(args)
    return fake_git


def test_reviewed_eol_blob_matches_crlf_and_lf_without_accepting_drift() -> None:
    """Regression: expression.py/Toda sources are committed with CRLF."""
    source_lf = b"alpha\nbeta\n"
    source_crlf = b"alpha\r\nbeta\r\n"
    expected_crlf = installer.git_blob_sha(source_crlf)
    expected_lf = installer.git_blob_sha(source_lf)

    assert audit.reviewed_eol_blob_matches(source_crlf, expected_crlf)
    assert audit.reviewed_eol_blob_matches(source_lf, expected_crlf)
    assert audit.reviewed_eol_blob_matches(source_lf, expected_lf)
    assert audit.reviewed_eol_blob_matches(source_crlf, expected_lf)
    assert not audit.reviewed_eol_blob_matches(b"alpha\nbetampered\n", expected_crlf)
    assert not audit.reviewed_eol_blob_matches(b"alpha\rbet a\n", expected_crlf)
    assert not audit.reviewed_eol_blob_matches(source_crlf, "0" * 40)


def test_reviewed_heads_are_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(audit, "PINNED_WORKING_BLOBS", {})
    monkeypatch.setattr(installer, "plan", lambda root: (
        root / installer.TARGET, b"old", b"new", "full function",
    ))
    for head in (audit.BASE_HEAD, audit.REVIEWED_R4R10_HEAD):
        monkeypatch.setattr(audit, "git", fake_git_factory(tmp_path, head))
        found = audit.preflight(tmp_path)
        assert found["head"] == head


def test_unknown_head_or_dirty_unrelated_change_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(audit, "PINNED_WORKING_BLOBS", {})
    monkeypatch.setattr(installer, "plan", lambda root: (
        root / installer.TARGET, b"old", b"new", "full function",
    ))
    monkeypatch.setattr(audit, "git", fake_git_factory(tmp_path, "0" * 40))
    with pytest.raises(RuntimeError, match="UNREVIEWED_HEAD"):
        audit.preflight(tmp_path)
    monkeypatch.setattr(audit, "git", fake_git_factory(tmp_path, audit.BASE_HEAD, "proof.py"))
    with pytest.raises(RuntimeError, match="UNREVIEWED_TRACKED_CHANGE"):
        audit.preflight(tmp_path)
