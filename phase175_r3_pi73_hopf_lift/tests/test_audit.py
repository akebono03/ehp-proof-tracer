"""Focused R3 provenance, source guard and no-premature-completion tests."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from phase175_r3_pi73_hopf_lift import audit


def r2_fixture() -> dict[str, object]:
    """Synthetic JSON contract only, never evidence for a production proof."""
    return {
        "phase": "175-R2", "mode": "READ_ONLY_FRONTIER_AUDIT",
        "dry_run": False, "result": "PASS_R2_SOURCE_FRONTIER_RECORDED",
        "tracked_unchanged": True, "production_changes": [],
        "new_given": 0, "new_mathematical_rules": 0,
        "full_pytest_executed": False,
        "preflight": {"head": "a" * 40, "branch": "develop"},
        "r1_root_status": [
            {"group": "pi_7^3", "status": "search_failed", "proven_steps": 0},
            {"group": "pi_9^5", "status": "search_failed", "proven_steps": 0},
            {"group": "pi_10^6", "status": "search_failed", "proven_steps": 0},
        ],
        "source_worker": {
            "status": "PASS_SOURCE_INVENTORY",
            "data": {"pi_7_3": {
                "printed_prop58_checked": True,
                "typed_relation_matches_db": True,
                "source_is_independent_complete_proof": False,
            }},
        },
    }


def test_r2_real_normal_contract() -> None:
    audit.validate_r2(r2_fixture())


@pytest.mark.parametrize("key,value", [
    ("dry_run", True),
    ("result", "PASS_R2_READ_ONLY_DRYRUN"),
    ("tracked_unchanged", False),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("full_pytest_executed", True),
    ("production_changes", ["phase165_r52_r9_shared_math.py"]),
])
def test_r2_unverified_or_mutating_report_rejected(key: str, value: object) -> None:
    row = r2_fixture()
    row[key] = value
    with pytest.raises(RuntimeError, match="R3_R2_EVIDENCE_REJECTED"):
        audit.validate_r2(row)


def test_r2_source_must_not_be_premature_root_proof() -> None:
    row = r2_fixture()
    row["source_worker"]["data"]["pi_7_3"]["source_is_independent_complete_proof"] = True
    with pytest.raises(RuntimeError, match="R3_R2_PI73_SOURCE_OR_GAP_CHANGED"):
        audit.validate_r2(row)


def test_r2_actual_original_gap_must_be_preserved() -> None:
    row = r2_fixture()
    row["r1_root_status"][0]["proven_steps"] = 10
    with pytest.raises(RuntimeError, match="R3_R2_PI73_SOURCE_OR_GAP_CHANGED"):
        audit.validate_r2(row)


def test_r2_report_selection_excludes_newer_dry_run(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    base = tmp_path / "EHPProofTracerAudit" / audit.R2_PACKAGE
    early, late = base / "20261111T083044_657453Z", base / "20261111T083100_000000Z"
    early.mkdir(parents=True)
    late.mkdir(parents=True)
    (early / "report.json").write_text(json.dumps(r2_fixture()), encoding="utf-8")
    invalid = r2_fixture()
    invalid["dry_run"] = True
    (late / "report.json").write_text(json.dumps(invalid), encoding="utf-8")
    assert audit.select_r2_report(None) == early / "report.json"


def prepare_git_repository(tmp_path: Path) -> tuple[Path, str]:
    """Actual local Git DAG with dummy files, not a fabricated source result."""
    def command(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=tmp_path, capture_output=True,
            check=True, text=True, encoding="utf-8",
        ).stdout.strip()

    command("init", "-q", "-b", "develop")
    command("config", "user.email", "phase175-test@example.invalid")
    command("config", "user.name", "Phase175 Test")
    (tmp_path / "production.txt").write_text("protected", encoding="utf-8")
    command("add", "production.txt")
    command("commit", "-qm", "baseline")
    return tmp_path, command("rev-parse", "HEAD")


def test_lineage_identical_head(tmp_path: Path) -> None:
    root, before = prepare_git_repository(tmp_path)
    assert audit.verify_lineage(root, {"preflight": {"head": before}}, {"head": before})["mode"] == "SAME_HEAD"


def test_lineage_audit_only_addition_is_allowed(tmp_path: Path) -> None:
    root, before = prepare_git_repository(tmp_path)
    folder = root / audit.R2_PACKAGE
    folder.mkdir()
    (folder / "audit.py").write_text("# audit", encoding="utf-8")
    subprocess.run(["git", "add", audit.R2_PACKAGE + "/audit.py"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "R2 audit only"], cwd=root, check=True)
    after = audit.git(root, "rev-parse", "HEAD")
    result = audit.verify_lineage(root, {"preflight": {"head": before}}, {"head": after})
    assert result["mode"] == "AUDIT_ONLY_DESCENDANT"
    assert result["audit_only_paths"] == [audit.R2_PACKAGE + "/audit.py"]


def test_lineage_production_change_is_rejected(tmp_path: Path) -> None:
    root, before = prepare_git_repository(tmp_path)
    (root / "production.txt").write_text("changed", encoding="utf-8")
    subprocess.run(["git", "add", "production.txt"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "unreviewed math source"], cwd=root, check=True)
    after = audit.git(root, "rev-parse", "HEAD")
    with pytest.raises(RuntimeError, match="R3_R2_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_lineage(root, {"preflight": {"head": before}}, {"head": after})


def test_lineage_reverse_history_is_rejected(tmp_path: Path) -> None:
    root, before = prepare_git_repository(tmp_path)
    folder = root / audit.R2_PACKAGE
    folder.mkdir()
    (folder / "README.md").write_text("audit", encoding="utf-8")
    subprocess.run(["git", "add", audit.R2_PACKAGE + "/README.md"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "audit"], cwd=root, check=True)
    after = audit.git(root, "rev-parse", "HEAD")
    with pytest.raises(RuntimeError, match="R3_R2_HEAD_NOT_ANCESTOR"):
        audit.verify_lineage(root, {"preflight": {"head": after}}, {"head": before})


def test_no_python_source_patching_or_given_in_worker() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert "shared_expansion_provider(screened, proof_target=target)" in source
    assert '"public_provider_changed": False' in source
    assert '"new_given": 0' in source
    assert "verify_proof_tree_for_narrative" in source


def test_report_only_claims_isolated_completion_after_trust(monkeypatch, tmp_path: Path) -> None:
    sample = {
        "preflight": {"head": "a" * 40},
        "worker": {"status": "INSPECTED", "data": {
            "screened_fixed_leaves_count": 8,
            "hopf_lift_candidate_count": 1,
            "cited_hopf_chain_count": 1,
            "exact_generator_spelling_matches": 0,
            "registered_generator_identity_matches": 1,
            "earlier_codomain_schema_count": 1,
            "source_pair_matches": 1,
            "isolated_search_status": "partial",
            "certified_hopf_lift_steps": 0,
            "isolated_trust_verified": False,
            "isolated_open_goals": ["MapInjective(...)"],
        }},
    }
    audit.write_report(tmp_path, sample)
    markdown = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "MapInjective" in markdown
    assert "Public provider: unchanged" in markdown


def test_audit_report_records_identity_filter_stage(monkeypatch, tmp_path: Path) -> None:
    sample = {
        "preflight": {"head": "a" * 40},
        "worker": {"status": "INSPECTED", "data": {
            "screened_fixed_leaves_count": 12,
            "hopf_lift_candidate_count": 1,
            "cited_hopf_chain_count": 1,
            "exact_generator_spelling_matches": 0,
            "registered_generator_identity_matches": 1,
            "earlier_codomain_schema_count": 1,
            "source_pair_matches": 1,
            "isolated_search_status": "partial",
            "certified_hopf_lift_steps": 0,
            "isolated_trust_verified": False,
            "isolated_open_goals": ["MapInjective(...)"],
        }},
    }
    audit.write_report(tmp_path, sample)
    displayed = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "HyoujiGen ID matches: 1" in displayed
    assert "Exact generator spelling matches: 0" in displayed
    assert "Earlier cyclic codomain schemas: 1" in displayed
    assert "Complete source-pair matches: 1" in displayed


def test_no_silent_trust_or_new_given_added_for_identity_fix() -> None:
    rule_file = Path(__file__).resolve().parents[1] / "rule.py"
    source = rule_file.read_text(encoding="utf-8")
    assert "not _same_generator(goal.generator, image.lhs.expression, goal.order)" in source
    assert "len(premises) == 3" in source
    assert "all(step.rule is ProofRule.INFERENCE" in source
    assert "proof_rule=ProofRule.INFERENCE" in source
    assert "ProofRule.GIVEN" not in source
