"""Focused R4R4 fail-closed contracts; all report and source fixtures are synthetic."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json

import pytest

from phase175_r4r4_pi95_premise_frontier import audit


def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R3",
        "mode": "ISOLATED_GENERIC_INFERENCE",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "production_changes": [],
        "new_given": 0,
        "new_mathematical_rules": 1,
        "rule_connected_to_public": False,
        "complete_proof": False,
        "full_pytest_executed": False,
        "preflight": {
            "head": audit.EXPECTED_HEAD_AT_PRIOR_AUDIT,
            "pinned_source_count": 18,
        },
        "r4_observation": {
            "target_group": "pi_9^5",
            "prior_group": "pi_8^4",
            "open_goals_count": 3,
            "target_proven_steps": 0,
            "prior_verified": True,
            "proof_complete": False,
        },
    }


def printed_fixture() -> tuple[str, str]:
    chapter_two = (
        r"\begin{proposition}\label{prop:2.5}" + "\n"
        + r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)." + "\n"
        + r"\Delta(E^2\gamma)\ \ni\ \pm\,[\iota_m,\iota_m]\circ\gamma" + "\n"
        + "等号の条件: 2-primary" + "\n"
        + r"\end{proposition}"
    )
    chapter_five = (
        r"\begin{equation}\label{eq:5.8}" + "\n"
        + r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" + "\n"
        + r"\end{equation}" + "\n"
        + r"\begin{proposition}\label{prop:5.8}" + "\n"
        + r"\pi^{4}_{8}=\mathbb Z_2" + "\n"
        + r"\pi^{5}_{9}=\mathbb Z_2" + "\n"
        + r"\end{proposition}" + "\n"
        + r"\Delta:\pi_9^9\to\pi_7^4" + "\n"
        + r"\Delta(\eta_9)" + "\n"
        + r"\Delta(\iota_9)\circ \eta_7" + "\n"
        + r"\pi_9^5=E\pi_8^4" + "\n"
        + r"\begin{equation}\label{eq:5.9}"
    )
    return chapter_two, chapter_five


def test_prior_success_is_not_promoted_to_public_proof() -> None:
    found = audit.validate_prior_report(prior_fixture())
    assert found["open_goals_count"] == 3
    assert found["target_proven_steps"] == 0
    assert found["proof_complete"] is False
    assert found["prior_verified"] is True


@pytest.mark.parametrize("key,value", [
    ("phase", "175-R4R2"),
    ("mode", "PUBLIC_PROOF"),
    ("gate", audit.DRY_GATE),
    ("dry_run", True),
    ("production_changes", ["proof.py"]),
    ("new_given", 1),
    ("new_mathematical_rules", 2),
    ("rule_connected_to_public", True),
    ("complete_proof", True),
    ("full_pytest_executed", True),
])
def test_prior_scope_tampering_rejected(key: str, value: object) -> None:
    report = prior_fixture()
    report[key] = value
    with pytest.raises(RuntimeError, match="R4R4_PRIOR_GATE_OR_SCOPE_INVALID"):
        audit.validate_prior_report(report)


@pytest.mark.parametrize("section,key,value", [
    ("preflight", "head", "bad"),
    ("preflight", "pinned_source_count", 17),
    ("r4_observation", "target_group", "pi_10^6"),
    ("r4_observation", "open_goals_count", 2),
    ("r4_observation", "target_proven_steps", 1),
    ("r4_observation", "prior_verified", False),
    ("r4_observation", "proof_complete", True),
])
def test_prior_evidence_tampering_rejected(
    section: str, key: str, value: object,
) -> None:
    report = deepcopy(prior_fixture())
    report[section][key] = value
    with pytest.raises(RuntimeError, match="R4R4_PRIOR_OBSERVATION_CHANGED"):
        audit.validate_prior_report(report)


def test_latest_passed_real_report_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    passed = folder / "20261117T051200Z"
    later = folder / "20261117T053000Z"
    passed.mkdir(parents=True)
    later.mkdir(parents=True)
    (passed / "report.json").write_text(json.dumps(prior_fixture()), encoding="utf-8")
    failure = prior_fixture()
    failure["gate"] = "FAIL_R4R3_ISOLATED_RULE"
    (later / "report.json").write_text(json.dumps(failure), encoding="utf-8")
    assert audit.latest_prior_report() == passed / "report.json"
    assert audit.latest_prior_report(passed / "report.json") == (passed / "report.json").resolve()
    with pytest.raises(RuntimeError, match="R4R4_R4R3_REPORT_MISSING"):
        audit.latest_prior_report(folder / "missing.json")


def fake_git(root: Path, *args: str, allow_failure: bool = False) -> tuple[int, str]:
    if args == ("rev-parse", "HEAD"):
        return 0, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT
    if args[:2] == ("merge-base", "--is-ancestor"):
        return 0, ""
    if args[:2] == ("diff", "--name-only"):
        return 0, ""
    raise AssertionError(f"unexpected git args: {args}")


def test_lineage_accepts_same_reviewed_head(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit, "git", fake_git)
    found = audit.validate_prior_lineage(
        tmp_path, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT,
        audit.EXPECTED_HEAD_AT_PRIOR_AUDIT,
    )
    assert found["reviewed_intervening_paths"] == []


def test_lineage_accepts_only_isolated_package_descendant(tmp_path: Path, monkeypatch) -> None:
    descendant = "4" * 40

    def git_approved(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, descendant
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase175_r4r3_two_summand_quotient/README.md\n.pytest_cache/v/cache/nodeids"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", git_approved)
    found = audit.validate_prior_lineage(tmp_path, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, descendant)
    assert len(found["reviewed_intervening_paths"]) == 2


def test_lineage_rejects_unaudited_production_change(tmp_path: Path, monkeypatch) -> None:
    descendant = "4" * 40

    def git_dirty(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, descendant
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase165_r52_r9_shared_math.py"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", git_dirty)
    with pytest.raises(RuntimeError, match="R4R4_UNREVIEWED_INTERVENING_FILES"):
        audit.validate_prior_lineage(tmp_path, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, descendant)


@pytest.mark.parametrize("prior,current,code", [
    ("f" * 40, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, "R4R4_UNREVIEWED_PRIOR_HEAD"),
    (audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, "a" * 40, "R4R4_CURRENT_HEAD_MISMATCH"),
])
def test_lineage_rejects_wrong_ref(
    tmp_path: Path, monkeypatch, prior: str, current: str, code: str,
) -> None:
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match=code):
        audit.validate_prior_lineage(tmp_path, prior, current)


def test_reviewed_source_and_printed_evidence() -> None:
    evidence = audit.read_printed_source_evidence(*printed_fixture())
    assert evidence["proposition58_delta_eta9_formula_printed"] is True
    assert evidence["printed_text_counts_as_verified_inference_step"] is False


@pytest.mark.parametrize("marker", [
    r"\Delta\alpha", r"\subset", r"\ni", "等号",
])
def test_prop25_conditions_fail_closed(marker: str) -> None:
    chapter_two, chapter_five = printed_fixture()
    with pytest.raises(RuntimeError, match="R4R4_PROPOSITION25_HYPOTHESES_MISSING"):
        audit.read_printed_source_evidence(chapter_two.replace(marker, "REMOVED"), chapter_five)


@pytest.mark.parametrize("marker", [
    r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')",
    r"\Delta(\eta_9)",
    r"\Delta(\iota_9)\circ \eta_7",
    r"\Delta:\pi_9^9\to\pi_7^4",
    r"\pi_9^5=E\pi_8^4",
    r"\pi^{5}_{9}=\mathbb Z_2",
    r"\pi^{4}_{8}=\mathbb Z_2",
])
def test_prop58_source_clause_fail_closed(marker: str) -> None:
    chapter_two, chapter_five = printed_fixture()
    with pytest.raises(RuntimeError, match="R4R4_TODA58"):
        audit.read_printed_source_evidence(chapter_two, chapter_five.replace(marker, "REMOVED"))


def test_exact_six_premises_never_claim_verified_parents() -> None:
    prior = audit.validate_prior_report(prior_fixture())
    evidence = audit.read_printed_source_evidence(*printed_fixture())
    window = {"valid_window_is_a_verified_proof_step": False}
    rows = audit.premise_frontier(prior, evidence, window)
    assert [r["index"] for r in rows] == list(range(1, 7))
    assert all(r["verified_parent_step_in_r4r4"] is False for r in rows)
    assert rows[2]["status"] == "PRINTED_FORMULA_TYPED_INFERENCE_PENDING"
    assert rows[4]["status"] == "PRINTED_ARGUMENT_TYPED_INFERENCE_PENDING"


@pytest.mark.parametrize("which", ["prior", "evidence", "window"])
def test_premise_boundary_fails_closed(which: str) -> None:
    prior = audit.validate_prior_report(prior_fixture())
    evidence = audit.read_printed_source_evidence(*printed_fixture())
    window = {"valid_window_is_a_verified_proof_step": False}
    if which == "prior":
        prior["target_proven_steps"] = 1
    elif which == "evidence":
        evidence["printed_text_counts_as_verified_inference_step"] = True
    else:
        window["valid_window_is_a_verified_proof_step"] = True
    with pytest.raises(RuntimeError, match="R4R4_PREMISE_EVIDENCE_BOUNDARY_CHANGED"):
        audit.premise_frontier(prior, evidence, window)


def test_rule_file_sha_is_pinned(tmp_path: Path, monkeypatch) -> None:
    rule = tmp_path / audit.PRIOR_PACKAGE / "rule.py"
    rule.parent.mkdir()
    rule.write_bytes(b"synthetic rule content")
    for path in audit.EXTRA_SOURCE_PINS:
        current = tmp_path / path
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_text("synthetic test source", encoding="utf-8")

    def git_expected(root, *args, allow_failure=False):
        assert args[0] == "rev-parse" and args[1].startswith("HEAD:")
        path = args[1][5:]
        return 0, audit.EXTRA_SOURCE_PINS[path]

    monkeypatch.setattr(audit, "git", git_expected)
    with pytest.raises(RuntimeError, match="R4R4_R4R3_RULE_CONTENT_CHANGED"):
        audit.verify_code_and_source_pins(tmp_path)


def test_changed_extra_source_pin_rejected(tmp_path: Path, monkeypatch) -> None:
    for path in audit.EXTRA_SOURCE_PINS:
        current = tmp_path / path
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_text("synthetic test source", encoding="utf-8")

    def git_bad(root, *args, allow_failure=False):
        return 0, "0" * 40

    monkeypatch.setattr(audit, "git", git_bad)
    with pytest.raises(RuntimeError, match="R4R4_EXTRA_SOURCE_PIN_DRIFT"):
        audit.verify_code_and_source_pins(tmp_path)


def test_real_typed_delta_e_window_is_schema_only() -> None:
    """When the actual project types are installed, exercise them directly."""
    pytest.importorskip("homotopy_groups")
    found = audit.verify_ehp_shape()
    assert found["exactness_indices"] == [4, 9, "delta_e"]
    assert found["valid_window_is_a_verified_proof_step"] is False
