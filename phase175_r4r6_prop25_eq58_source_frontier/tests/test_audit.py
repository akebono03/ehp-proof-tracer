"""R4R6 fail-closed source and type contracts; synthetic data only."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import subprocess

import pytest

from phase175_r4r6_prop25_eq58_source_frontier import audit


def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R5R3", "gate": audit.PRIOR_GATE,
        "dry_run": False, "new_given": 0, "new_mathematical_rules": 0,
        "public_pi95_complete": False, "full_pytest_executed": False,
        "connected_previously_isolated_general_rules": 1,
        "source_guard": {
            "reviewed_head": audit.PRIOR_REVIEWED_BASE_HEAD,
            "reviewed_base_head": audit.PRIOR_REVIEWED_BASE_HEAD,
            "reviewed_intervening_paths": [],
            "production_blob": audit.PRIOR_PRODUCTION_BLOB,
            "isolated_rule_sha256": audit.PRIOR_RULE_SHA256,
        },
        "general_rule": {
            "public_provider_proposals_with_verified_parent": 3,
            "source_groups": ["pi_8^7", "pi_8^4", "pi_8^4"],
            "new_given": 0, "previous_proof_search_executed": False,
            "target_pi95_completed": False,
        },
        "real_integration_pytest": {"exit_code": 0},
    }


def source_fixture() -> tuple[str, str]:
    chapter2 = (
        r"\begin{proposition}\label{prop:2.5}" + "\n"
        + r"\alpha\in\pi_{i+1}(S^{2m+1})" + "\n"
        + r"\beta\in \pi_{j-1}(S^{i-1})" + "\n"
        + r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)" + "\n"
        + r"j<3m-1" + "\n" + r"2\)-primary" + " 等号\n"
        + r"\end{proposition}"
    )
    chapter5 = (
        r"\begin{equation}\label{eq:5.8}" + "\n"
        + r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" + "\n"
        + r"\end{equation}" + "\n"
        + r"\begin{proposition}\label{prop:5.8}" + "\n"
        + r"\pi^{4}_{8}=\mathbb Z_2" + "\n"
        + r"\end{proposition}" + "\n"
        + r"\Delta(\eta_9)" + "\n"
        + r"\Delta(\iota_9)\circ \eta_7" + "\n"
        + r"\nu_4\circ (2\eta_7)" + "\n"
        + r"E\nu'\circ \eta_7" + "\n"
        + r"\begin{equation}\label{eq:5.9}"
    )
    return chapter2, chapter5


def test_r4r5r3_real_report_accepted_as_audit_only() -> None:
    found = audit.validate_prior(prior_fixture())
    assert found["verified_provider_examples"] == 3
    assert found["prior_report_is_not_mathematical_proof"] is True


@pytest.mark.parametrize("key,bad", [
    ("phase", "175-R4R5R2"),
    ("gate", audit.DRY_GATE),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("public_pi95_complete", True),
    ("full_pytest_executed", True),
])
def test_prior_scope_tampering_rejected(key: str, bad: object) -> None:
    row = prior_fixture()
    row[key] = bad
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_GATE_OR_SCOPE_INVALID"):
        audit.validate_prior(row)


@pytest.mark.parametrize("path,bad", [
    (("source_guard", "reviewed_head"), "0" * 40),
    (("general_rule", "public_provider_proposals_with_verified_parent"), 2),
    (("general_rule", "previous_proof_search_executed"), True),
    (("general_rule", "target_pi95_completed"), True),
    (("real_integration_pytest", "exit_code"), 1),
])
def test_prior_evidence_tampering_rejected(path: tuple[str, str], bad: object) -> None:
    row = deepcopy(prior_fixture())
    row[path[0]][path[1]] = bad
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_EVIDENCE_INVALID"):
        audit.validate_prior(row)


def test_find_only_valid_prior_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    good = folder / "01"
    newer = folder / "02"
    good.mkdir(parents=True)
    newer.mkdir(parents=True)
    (good / "report.json").write_text(json.dumps(prior_fixture()), encoding="utf-8")
    bad = prior_fixture()
    bad["gate"] = "FAIL"
    (newer / "report.json").write_text(json.dumps(bad), encoding="utf-8")
    assert audit.find_real_prior() == good / "report.json"
    assert audit.find_real_prior(good / "report.json") == (good / "report.json").resolve()


def test_source_chain_signed_not_proof() -> None:
    found = audit.source_evidence(*source_fixture())
    assert found["source_sign_preserved"] == "±"
    assert found["printed_relation_is_a_verified_proof_step"] is False


@pytest.mark.parametrize("marker", [
    r"\alpha\in\pi_{i+1}(S^{2m+1})",
    r"\beta\in \pi_{j-1}(S^{i-1})",
    r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)",
    r"j<3m-1", r"2\)-primary", "等号",
])
def test_prop25_missing_condition_rejected(marker: str) -> None:
    c2, c5 = source_fixture()
    with pytest.raises(RuntimeError, match="R4R6_PROP25_SOURCE_DRIFT"):
        audit.source_evidence(c2.replace(marker, "REMOVED"), c5)


@pytest.mark.parametrize("marker,code", [
    (r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')", "R4R6_EQ58_SIGNED_FORMULA_DRIFT"),
    (r"\Delta(\eta_9)", "R4R6_PROP58_PROOF_CHAIN_DRIFT"),
    (r"\Delta(\iota_9)\circ \eta_7", "R4R6_PROP58_PROOF_CHAIN_DRIFT"),
    (r"\nu_4\circ (2\eta_7)", "R4R6_PROP58_PROOF_CHAIN_DRIFT"),
    (r"E\nu'\circ \eta_7", "R4R6_PROP58_PROOF_CHAIN_DRIFT"),
])
def test_signed_formula_or_proof_missing_rejected(marker: str, code: str) -> None:
    c2, c5 = source_fixture()
    with pytest.raises(RuntimeError, match=code):
        audit.source_evidence(c2, c5.replace(marker, "REMOVED"))


def test_typed_specialization_and_equality_condition() -> None:
    row = audit.typed_frontier()
    assert row["j_less_than_3m_minus_1"] is True
    assert row["delta_alpha_composed_beta"] == "pi_8^4"
    assert row["typed_endpoints_are_verified_proof_steps"] is False


@pytest.mark.parametrize("values", [(4, 8, 11), (4, 7, 9), (5, 10, 9), (4, 8, True)])
def test_wrong_typed_specialization_rejected(values: tuple) -> None:
    with pytest.raises(RuntimeError, match="R4R6_"):
        audit.typed_frontier(*values)


@pytest.mark.parametrize("dirty", ["proof.py", "phase165_r52_r9_shared_math.py", "unrelated/README.md"])
def test_unreviewed_tracked_change_rejected(dirty: str) -> None:
    with pytest.raises(RuntimeError, match="R4R6_UNREVIEWED_TRACKED_CHANGES"):
        audit.validate_tracked_changes([dirty])


def test_only_unrelated_cache_can_be_tracked_dirty() -> None:
    assert audit.validate_tracked_changes([".pytest_cache/v/cache/nodeids"]) == [
        ".pytest_cache/v/cache/nodeids"
    ]


def test_audit_scope_is_not_inference_registration() -> None:
    assert audit.FINAL_GATE.endswith("NOT_PUBLIC")
    assert "phase165_r52_r9_shared_math.py" in audit.PINNED_BLOBS
    assert "sources/toda/Toda_02_2.tex" in audit.PINNED_BLOBS


def test_prior_missing_reports_search_path_is_explicit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    expected = str(tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE)
    with pytest.raises(RuntimeError, match="R4R6_SUCCESSFUL_R4R5R3_REAL_REPORT_MISSING") as error:
        audit.find_real_prior()
    assert expected in str(error.value)


def test_prior_present_but_invalid_reports_reason_not_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    failed = folder / "20261117T073430_001276Z"
    failed.mkdir(parents=True)
    record = prior_fixture()
    record["source_guard"]["reviewed_head"] = "0" * 40
    (failed / "report.json").write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_REPORTS_FOUND_BUT_REJECTED") as error:
        audit.find_real_prior()
    assert "R4R6_PRIOR_EVIDENCE_INVALID" in str(error.value)
    assert "report.json" in str(error.value)


def test_explicit_success_report_path_is_preserved_for_strict_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "unused"))
    candidate = tmp_path / "explicit" / "report.json"
    candidate.parent.mkdir()
    candidate.write_text(json.dumps(prior_fixture()), encoding="utf-8")
    assert audit.find_real_prior(candidate) == candidate.resolve()
    assert audit.validate_prior(json.loads(candidate.read_text(encoding="utf-8")))[
        "verified_provider_examples"
    ] == 3


def test_historical_source_head_not_forced_to_later_checkout_head() -> None:
    record = prior_fixture()
    assert record["source_guard"]["reviewed_head"] not in audit.REVIEWED_HEADS
    assert audit.validate_prior(record)["r4r5r3_head"] == audit.PRIOR_REVIEWED_BASE_HEAD


@pytest.mark.parametrize("field,bad", [
    ("reviewed_base_head", "0" * 40),
    ("production_blob", "0" * 40),
    ("isolated_rule_sha256", "0" * 64),
    ("reviewed_intervening_paths", ["proof.py"]),
    ("reviewed_intervening_paths", ["phase175_r4r5_eta7_annihilator_isolated/../../proof.py"]),
])
def test_historical_source_guard_tampering_rejected(field: str, bad: object) -> None:
    record = prior_fixture()
    record["source_guard"][field] = bad
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_EVIDENCE_INVALID"):
        audit.validate_prior(record)


def test_historical_genuine_commit_range_is_accepted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=tmp_path, text=True,
                              capture_output=True, check=True).stdout.strip()

    def commit(message: str) -> str:
        git("add", ".")
        git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", message)
        return git("rev-parse", "HEAD")

    git("init", "-q")
    source_file = tmp_path / "phase165_r52_r9_shared_math.py"
    source_file.write_text("original shared provider\n", encoding="utf-8")
    base = commit("pre R4R5R2")
    monkeypatch.setattr(audit, "PRIOR_REVIEWED_BASE_HEAD", base)
    original_blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py")
    monkeypatch.setattr(audit, "PRIOR_PRODUCTION_BLOB", original_blob)

    rule_path = tmp_path / "phase175_r4r5_eta7_annihilator_isolated" / "rule.py"
    rule_path.parent.mkdir(parents=True)
    rule_path.write_bytes(b"source guarded order zero inference\n")
    import hashlib
    rule_hash = hashlib.sha256(rule_path.read_bytes()).hexdigest()
    monkeypatch.setattr(audit, "PRIOR_RULE_SHA256", rule_hash)
    historical_head = commit("R4R5R2 committed")
    source_file.write_text("new shared provider\n", encoding="utf-8")
    commit("R4R5R3 production wiring committed")
    record = prior_fixture()
    record["source_guard"].update({
        "reviewed_head": historical_head,
        "reviewed_base_head": base,
        "reviewed_intervening_paths": ["phase175_r4r5_eta7_annihilator_isolated/rule.py"],
        "production_blob": original_blob,
        "isolated_rule_sha256": rule_hash,
    })
    assert audit.validate_prior(record)["r4r5r3_head"] == historical_head
    checked = audit.validate_prior_history(tmp_path, record["source_guard"])
    assert checked["historical_reviewed_head"] == historical_head
    assert checked["historical_production_blob_checked"] is True

    forged = deepcopy(record)
    forged["source_guard"]["reviewed_intervening_paths"] = []
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_HISTORY_INVALID"):
        audit.validate_prior_history(tmp_path, forged["source_guard"])

    # The actual rule bytes are a separately verified source of the prior audit.
    rule_path.write_bytes(b"tampered source\n")
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_HISTORY_INVALID"):
        audit.validate_prior_history(tmp_path, record["source_guard"])


def test_historical_unrelated_commit_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=tmp_path, text=True,
                              capture_output=True, check=True).stdout.strip()
    def commit(message: str) -> str:
        git("add", ".")
        git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", message)
        return git("rev-parse", "HEAD")

    git("init", "-q")
    source = tmp_path / "phase165_r52_r9_shared_math.py"
    source.write_text("original\n", encoding="utf-8")
    base = commit("original")
    monkeypatch.setattr(audit, "PRIOR_REVIEWED_BASE_HEAD", base)
    monkeypatch.setattr(audit, "PRIOR_PRODUCTION_BLOB", git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py"))
    (tmp_path / "proof.py").write_text("unrelated change\n", encoding="utf-8")
    unreviewed_head = commit("unrelated")
    record = prior_fixture()
    record["source_guard"].update({
        "reviewed_head": unreviewed_head,
        "reviewed_base_head": base,
        "reviewed_intervening_paths": [],
    })
    assert audit.validate_prior(record)["verified_provider_examples"] == 3
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_HISTORY_INVALID"):
        audit.validate_prior_history(tmp_path, record["source_guard"])
