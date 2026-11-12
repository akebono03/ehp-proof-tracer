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


def test_r3r2_report_shows_independent_premises_without_claiming_completion(tmp_path: Path) -> None:
    worker = {
        "status": "INSPECTED",
        "data": {
            "screened_fixed_leaves_count": 9,
            "hopf_lift_candidate_count": 1,
            "cited_hopf_chain_count": 1,
            "exact_generator_spelling_matches": 0,
            "registered_generator_identity_matches": 1,
            "earlier_codomain_schema_count": 1,
            "source_pair_matches": 1,
            "isolated_search_status": "search_failed",
            "certified_hopf_lift_steps": 0,
            "isolated_trust_verified": False,
            "isolated_open_goals": ["CyclicStructureStatement"],
            "source_bound_codomain_candidate": True,
            "subgoal_observations": [
                {"name": "hopf_injectivity", "status": "UNRESOLVED",
                 "offered_routes": 1, "actual_proof_rule": None,
                 "diagnostic": "missing certified zero image"},
                {"name": "cyclic_codomain", "status": "DIRECT_GIVEN_NOT_ACCEPTABLE",
                 "offered_routes": 1, "actual_proof_rule": "given", "diagnostic": None},
                {"name": "source_bound_cyclic_codomain", "status": "INFERRED",
                 "offered_routes": 1, "actual_proof_rule": "inference", "diagnostic": None},
            ],
        },
    }
    audit.write_report(tmp_path, {"worker": worker})
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "hopf_injectivity: **UNRESOLVED**" in content
    assert "cyclic_codomain: **DIRECT_GIVEN_NOT_ACCEPTABLE**" in content
    assert "source_bound_cyclic_codomain: **INFERRED**" in content
    assert "Source-bound cyclic codomain offered: True" in content


def test_r3r2_pins_original_recursive_resolver() -> None:
    assert audit.EXTRA_PINS["phase165_r3_recursive_search.py"] == (
        "06009bfcf57f99cac58c229d99c53f16324692d0"
    )


def test_r3r2_code_does_not_change_public_provider_or_register_givens() -> None:
    pkg = Path(__file__).resolve().parents[1]
    code = (pkg / "frontier.py").read_text(encoding="utf-8")
    audit_code = (pkg / "audit.py").read_text(encoding="utf-8")
    assert "SourceBoundGoal(codomain, sources[0])" in code
    assert "reconstruct_registered_goal(" in code
    assert 'lookup_mode="typed_reference_publication"' in code
    assert '"new_given": 0' in audit_code
    assert '"public_search_modified": False' in audit_code
    assert '"public_web_complete_claimed": False' in audit_code


def r3r3_git_fixture(tmp_path: Path) -> tuple[Path, str]:
    """A real local Git index, with an independently committed R3 audit."""
    root = tmp_path

    def command(*arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments], cwd=root, check=True,
            capture_output=True, text=True, encoding="utf-8",
        ).stdout.strip()

    command("init", "-q", "-b", "develop")
    command("config", "user.email", "r3r3@example.invalid")
    command("config", "user.name", "R3R3 Audit")
    tracked = (
        "data/sphere.csv",
        "protected/r1.txt",
        "protected/r2.txt",
        "protected/r3.txt",
        "phase175_r3_pi73_hopf_lift/audit.py",
        "phase175_r3_pi73_hopf_lift/README.md",
        "phase175_r3_pi73_hopf_lift/rule.py",
    )
    for relative in tracked:
        file = root / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        if relative == "data/sphere.csv":
            file.write_text(
                "n,k,id,generator,orders\n"
                + "".join(f"{n},4,{n},x,2\n" for n in range(2, 8)),
                encoding="utf-8",
            )
        else:
            file.write_text("original " + relative + "\n", encoding="utf-8")
    command("add", ".")
    command("commit", "-qm", "phase175 R3 audit baseline")
    return root, command("rev-parse", "HEAD")


def test_r3r3_scoped_guard_accepts_unstaged_audit_edits_and_hashes(tmp_path: Path) -> None:
    from hashlib import sha256

    root, _ = r3r3_git_fixture(tmp_path)
    assert audit.audit_only_tracked_snapshot(root) == {}
    file = root / "phase175_r3_pi73_hopf_lift/audit.py"
    file.write_text("R3R2 audit replacement\n", encoding="utf-8")
    snapshot = audit.audit_only_tracked_snapshot(root)
    assert snapshot == {
        "phase175_r3_pi73_hopf_lift/audit.py": sha256(file.read_bytes()).hexdigest(),
    }
    file.write_text("R3R2 audit replacement modified during run\n", encoding="utf-8")
    assert audit.audit_only_tracked_snapshot(root) != snapshot


def test_r3r3_guard_rejects_production_or_unlisted_r3_changes(tmp_path: Path) -> None:
    root, _ = r3r3_git_fixture(tmp_path)
    file = root / "phase175_r3_pi73_hopf_lift/audit.py"
    file.write_text("R3R2 audit replacement\n", encoding="utf-8")
    (root / "protected/r1.txt").write_text("unreviewed protected change", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3_PROTECTED_TRACKED_CHANGE"):
        audit.audit_only_tracked_snapshot(root)
    subprocess.run(
        ["git", "checkout", "--", "protected/r1.txt"],
        cwd=root, check=True, capture_output=True,
    )
    (root / "phase175_r3_pi73_hopf_lift/rule.py").write_text(
        "unreviewed rule replacement", encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="R3_PROTECTED_TRACKED_CHANGE"):
        audit.audit_only_tracked_snapshot(root)


def test_r3r3_guard_rejects_index_staging_even_inside_r3(tmp_path: Path) -> None:
    root, _ = r3r3_git_fixture(tmp_path)
    file = root / "phase175_r3_pi73_hopf_lift/audit.py"
    file.write_text("audited replacement\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "phase175_r3_pi73_hopf_lift/audit.py"],
        cwd=root, check=True, capture_output=True,
    )
    with pytest.raises(RuntimeError, match="R3_STAGED_OR_OTHER_TRACKED_CHANGE"):
        audit.audit_only_tracked_snapshot(root)


def test_r3r3_guard_rejects_deletion_and_unknown_rename(tmp_path: Path) -> None:
    root, _ = r3r3_git_fixture(tmp_path)
    (root / "phase175_r3_pi73_hopf_lift/README.md").unlink()
    with pytest.raises(RuntimeError, match="R3_STAGED_OR_OTHER_TRACKED_CHANGE"):
        audit.audit_only_tracked_snapshot(root)


def test_r3r3_scoped_preflight_rechecks_r1_r2_r3_pins(
    tmp_path: Path, monkeypatch,
) -> None:
    from phase175_r1_k4_audit import audit as r1
    from phase175_r2_k4_frontier_audit import audit as r2

    root, baseline = r3r3_git_fixture(tmp_path)

    def blob(relative: str) -> str:
        return audit.git(root, "rev-parse", "HEAD:" + relative)

    monkeypatch.setattr(r1, "REVIEWED_MAIN_MERGE", baseline)
    monkeypatch.setattr(r1, "SOURCE_BLOBS", {
        "data/sphere.csv": blob("data/sphere.csv"),
        "protected/r1.txt": blob("protected/r1.txt"),
    })
    monkeypatch.setattr(r2, "EXTRA_PINS", {
        "protected/r2.txt": blob("protected/r2.txt"),
    })
    monkeypatch.setattr(audit, "EXTRA_PINS", {
        "protected/r3.txt": blob("protected/r3.txt"),
    })

    audit_file = root / "phase175_r3_pi73_hopf_lift/audit.py"
    audit_file.write_text("R3R2 audit replacement\n", encoding="utf-8")
    checked = audit.preflight(root)
    assert checked["branch"] == "develop"
    assert checked["head"] == baseline
    assert checked["tracked_clean"] is False
    assert checked["r3_scoped_source_guard"] == "R3_ONLY_UNSTAGED_AUDIT_EDITS"
    assert checked["r3_registered_groups"] == 6
    assert set(checked["r3_scoped_audit_modified"]) == {
        "phase175_r3_pi73_hopf_lift/audit.py",
    }
    assert audit.preflight(root) == checked

    (root / "protected/r2.txt").unlink()
    with pytest.raises(RuntimeError, match="R3_STAGED_OR_OTHER_TRACKED_CHANGE"):
        audit.preflight(root)


def test_r3r3_clean_path_retains_unmodified_r2_preflight(
    tmp_path: Path, monkeypatch,
) -> None:
    root, baseline = r3r3_git_fixture(tmp_path)
    calls = []

    def original_guard(candidate: Path):
        calls.append(candidate)
        return {"head": baseline, "branch": "develop", "tracked_clean": True}

    monkeypatch.setattr(audit, "r2_preflight", original_guard)
    monkeypatch.setattr(audit, "EXTRA_PINS", {
        "protected/r3.txt": audit.git(root, "rev-parse", "HEAD:protected/r3.txt"),
    })
    checked = audit.preflight(root)
    assert calls == [root]
    assert checked["tracked_clean"] is True
    assert checked["r3_scoped_source_guard"] == "CLEAN_WORKTREE"
    assert checked["r3_scoped_audit_modified"] == {}


def test_r3r4_lineage_accepts_r2_and_named_r3_additions(tmp_path: Path) -> None:
    """A real Git DAG reproduces R2 commit followed by R3 package commit."""
    root, before = prepare_git_repository(tmp_path)
    for relative in (
        audit.R2_PACKAGE + "/audit.py",
        audit.PACKAGE + "/__init__.py",
        audit.PACKAGE + "/audit.py",
        audit.PACKAGE + "/rule.py",
        audit.PACKAGE + "/README.md",
    ):
        file = root / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("audited package file\n", encoding="utf-8")
    subprocess.run(["git", "add", audit.R2_PACKAGE], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "R2 audit package"], cwd=root, check=True)
    subprocess.run(["git", "add", audit.PACKAGE], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "R3 isolated audit package"], cwd=root, check=True)
    after = audit.git(root, "rev-parse", "HEAD")
    result = audit.verify_lineage(root, {"preflight": {"head": before}}, {"head": after})
    assert result["mode"] == "AUDIT_ONLY_DESCENDANT"
    assert result["r3_added_paths"] == [
        audit.PACKAGE + "/README.md",
        audit.PACKAGE + "/__init__.py",
        audit.PACKAGE + "/audit.py",
        audit.PACKAGE + "/rule.py",
    ]
    assert audit.R2_PACKAGE + "/audit.py" in result["audit_only_paths"]


def test_r3r4_lineage_rejects_unlisted_r3_added_file(tmp_path: Path) -> None:
    root, before = prepare_git_repository(tmp_path)
    unlisted = root / audit.PACKAGE / "unexpected_source.py"
    unlisted.parent.mkdir(parents=True, exist_ok=True)
    unlisted.write_text("# not part of the audited R3 ZIP\n", encoding="utf-8")
    subprocess.run(["git", "add", audit.PACKAGE], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "unexpected R3 addition"], cwd=root, check=True)
    after = audit.git(root, "rev-parse", "HEAD")
    with pytest.raises(RuntimeError, match="R3_R2_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_lineage(root, {"preflight": {"head": before}}, {"head": after})


def test_r3r4_lineage_rejects_prior_committed_r3_modification(tmp_path: Path) -> None:
    root, _ = prepare_git_repository(tmp_path)
    tracked = root / audit.PACKAGE / "audit.py"
    tracked.parent.mkdir(parents=True, exist_ok=True)
    tracked.write_text("initial R3 audit", encoding="utf-8")
    subprocess.run(["git", "add", audit.PACKAGE], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "first R3 audit"], cwd=root, check=True)
    before = audit.git(root, "rev-parse", "HEAD")
    tracked.write_text("unreviewed committed change", encoding="utf-8")
    subprocess.run(["git", "add", audit.PACKAGE], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "unreviewed R3 edit"], cwd=root, check=True)
    after = audit.git(root, "rev-parse", "HEAD")
    with pytest.raises(RuntimeError, match="R3_R2_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_lineage(root, {"preflight": {"head": before}}, {"head": after})


def test_r3r4_lineage_rejects_production_change_even_with_valid_audit_additions(
    tmp_path: Path,
) -> None:
    root, before = prepare_git_repository(tmp_path)
    file = root / audit.PACKAGE / "rule.py"
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("isolated R3 rule", encoding="utf-8")
    (root / "production.txt").write_text("modified", encoding="utf-8")
    subprocess.run(["git", "add", "production.txt", audit.PACKAGE], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "audit plus unreviewed production"], cwd=root, check=True)
    after = audit.git(root, "rev-parse", "HEAD")
    with pytest.raises(RuntimeError, match="R3_R2_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_lineage(root, {"preflight": {"head": before}}, {"head": after})
