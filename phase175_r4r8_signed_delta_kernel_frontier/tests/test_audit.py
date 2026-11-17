"""R4R8 standalone, source-first, fail-closed tests (synthetic evidence)."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from phase175_r4r8_signed_delta_kernel_frontier import audit


def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R7",
        "mode": "ISOLATED_TYPED_CONDITIONAL_INFERENCE",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 1,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "preflight": {"head": audit.BASE_HEAD},
        "source_and_boundary": {
            "source_rechecked": True,
            "sign_retained": True,
            "public_search_unchanged": True,
            "source_is_proof": False,
        },
        "isolated": {
            "isolated_backward_proposals": 1,
            "unproved_parent_obligations": 2,
            "signed_goal_retained": True,
            "verified_parent_proof_steps_created": 0,
            "previous_proof_search_executed": False,
            "public_provider_connected": False,
            "pi95_completed": False,
        },
    }


def text_fixture() -> tuple[str, str]:
    chapter_two = (
        r"\begin{proposition}\label{prop:2.5}" + "\n"
        + r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)" + "\n"
        + r"j<3m-1" + " とき等号\n"
        + r"\end{proposition}"
    )
    chapter_five = (
        r"\begin{equation}\label{eq:5.8}" + "\n"
        + r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" + "\n"
        + r"\end{equation}" + "\n"
        + r"\begin{proposition}\label{prop:5.8}" + "\n"
        + r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}" + "\n"
        + r"\end{proposition}" + "\n"
        + r"\Delta(\eta_9)"
    )
    return chapter_two, chapter_five


def test_success_prior_is_not_a_proof_certificate() -> None:
    result = audit.validate_prior(prior_fixture())
    assert result["prior_is_not_proof_certificate"] is True
    assert result["historical_r4r7_head"] == audit.BASE_HEAD


@pytest.mark.parametrize("key,invalid", (
    ("gate", "PASS_UNRELATED"),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 0),
    ("production_changes", ["proof.py"]),
    ("rule_connected_to_public", True),
    ("pi95_proof_complete", True),
    ("full_pytest_executed", True),
))
def test_prior_scope_tampering_rejected(key: str, invalid: object) -> None:
    record = prior_fixture()
    record[key] = invalid
    with pytest.raises(RuntimeError, match="R4R8_PRIOR_SCOPE_INVALID"):
        audit.validate_prior(record)


@pytest.mark.parametrize("field,invalid", (
    ("head", "0" * 40),
))
def test_prior_historical_head_fail_closed(field: str, invalid: object) -> None:
    data = prior_fixture()
    data["preflight"][field] = invalid
    with pytest.raises(RuntimeError, match="HISTORICAL_HEAD_INVALID"):
        audit.validate_prior(data)


@pytest.mark.parametrize("section,key,invalid", (
    ("source_and_boundary", "source_rechecked", False),
    ("source_and_boundary", "sign_retained", False),
    ("source_and_boundary", "source_is_proof", True),
    ("isolated", "unproved_parent_obligations", 1),
    ("isolated", "verified_parent_proof_steps_created", 1),
    ("isolated", "previous_proof_search_executed", True),
    ("isolated", "public_provider_connected", True),
))
def test_prior_evidence_tampering_rejected(section: str, key: str, invalid: object) -> None:
    data = deepcopy(prior_fixture())
    data[section][key] = invalid
    with pytest.raises(RuntimeError, match="R4R8_PRIOR_"):
        audit.validate_prior(data)


def test_latest_prior_finds_real_pass_and_ignores_dryrun(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    earlier = folder / "20261117T085531_456222Z"
    newer = folder / "20261117T085540_456222Z"
    earlier.mkdir(parents=True)
    newer.mkdir(parents=True)
    (earlier / "report.json").write_text(json.dumps(prior_fixture()), encoding="utf-8")
    wrong = prior_fixture()
    wrong["dry_run"] = True
    (newer / "report.json").write_text(json.dumps(wrong), encoding="utf-8")
    assert audit.find_prior() == earlier / "report.json"
    assert audit.find_prior(earlier / "report.json") == (earlier / "report.json").resolve()
    with pytest.raises(RuntimeError, match="PRIOR_REPORT_NOT_FOUND"):
        audit.find_prior(folder / "missing.json")


def test_source_preserves_sign_and_is_not_a_step() -> None:
    result = audit.source_frontier(*text_fixture())
    assert result["source_sign"] == "±"
    assert result["source_not_a_verified_proof_step"] is True
    assert result["prop25_equality_condition_m4_j9"] is True


@pytest.mark.parametrize("part,token", (
    (0, r"\Delta\alpha"),
    (0, r"j<3m-1"),
    (1, r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')"),
    (1, r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"),
    (1, r"\Delta(\eta_9)"),
))
def test_malformed_source_rejected(part: int, token: str) -> None:
    sources = list(text_fixture())
    sources[part] = sources[part].replace(token, "REMOVED")
    with pytest.raises(RuntimeError, match="R4R8_"):
        audit.source_frontier(*sources)


@pytest.mark.parametrize("N,m", ((8, 4), (8, 2), (12, 3), (16, 8), (6, 2)))
def test_general_kernel_formula_and_enumeration(N: int, m: int) -> None:
    result = audit.cyclic_kernel_arithmetic(N, m)
    b = N // m
    assert result["kernel_generator_free_coefficient"] == b
    assert result["kernel_generator_torsion_coefficient"] == -1
    assert result["arithmetic_checked_not_a_proof_step"] is True
    for u in range(-2 * N, 2 * N + 1):
        for v in range(m):
            kernel_member = ((u + b * v) % N) == 0
            generated_member = (u % b == 0 and (v + u // b) % m == 0)
            assert kernel_member == generated_member


@pytest.mark.parametrize("N,m", ((0, 4), (8, 0), (8, 3), (4, 8), (True, 4), (8, False)))
def test_invalid_kernel_domain_fails_closed(N: object, m: object) -> None:
    with pytest.raises(ValueError, match="R4R8_INVALID_CYCLIC_KERNEL_PARAMETERS"):
        audit.cyclic_kernel_arithmetic(N, m)


def test_unresolved_evidence_is_never_labeled_proved() -> None:
    rows = audit.unresolved_obligations()
    assert len(rows) == 6
    assert [x["index"] for x in rows] == list(range(1, 7))
    assert all(x["verified_proof_step_in_r4r8"] is False for x in rows)
    assert any("surjection" in x["obligation"] for x in rows)


def g(root: Path, *parts: str) -> str:
    return subprocess.run(["git", *parts], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


def commit(root: Path, message: str) -> None:
    g(root, "add", ".")
    g(root, "-c", "user.name=Test", "-c", "user.email=t@example.com",
      "commit", "-qm", message)


def init_repo(tmp_path: Path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    g(root, "init", "-q")
    (root / "baseline.txt").write_text("baseline", encoding="utf-8")
    commit(root, "baseline")
    base = g(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "BASE_HEAD", base)
    return root, base


def test_reviewed_lineage_accepts_baseline_and_r4r7_commit(tmp_path: Path, monkeypatch) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    assert audit.reviewed_lineage(root, base)["reviewed_intervening_paths"] == []
    changed = root / audit.PRIOR_PACKAGE / "rule.py"
    changed.parent.mkdir(parents=True)
    changed.write_text("isolated rule", encoding="utf-8")
    commit(root, "r4r7")
    result = audit.reviewed_lineage(root, g(root, "rev-parse", "HEAD"))
    assert result["reviewed_intervening_paths"] == [audit.PRIOR_PACKAGE + "/rule.py"]


def test_reviewed_lineage_rejects_unrelated_change(tmp_path: Path, monkeypatch) -> None:
    root, _ = init_repo(tmp_path, monkeypatch)
    (root / "proof.py").write_text("unreviewed", encoding="utf-8")
    commit(root, "unauthorized")
    with pytest.raises(RuntimeError, match="R4R8_UNREVIEWED_COMMITTED_CHANGE"):
        audit.reviewed_lineage(root, g(root, "rev-parse", "HEAD"))


def test_reviewed_lineage_rejects_non_descendant(tmp_path: Path, monkeypatch) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(audit, "BASE_HEAD", "0" * 40)
    with pytest.raises(RuntimeError, match="R4R8_BASE_HEAD_NOT_ANCESTOR"):
        audit.reviewed_lineage(root, base)


def test_reviewed_lineage_rejects_false_exact_r4r7_successor(tmp_path: Path, monkeypatch) -> None:
    root, _ = init_repo(tmp_path, monkeypatch)
    fake_head = g(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "REVIEWED_R4R7_HEAD", fake_head)
    with pytest.raises(RuntimeError, match="R4R8_R4R7_COMMIT_CONTENT_MISSING"):
        audit.reviewed_lineage(root, fake_head)


def test_preflight_accepts_source_pinned_untracked_r4r7_at_base_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    g(root, "checkout", "-qb", "develop")
    fake_source = root / "phase165_r52_r9_shared_math.py"
    fake_source.write_text("def shared_expansion_provider():\n    return ()\n", encoding="utf-8")
    commit(root, "committed source")
    base = g(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "BASE_HEAD", base)
    p = root / audit.PRIOR_PACKAGE / "rule.py"
    p.parent.mkdir(parents=True)
    p.write_text("uncommitted, reviewed prior rule\n", encoding="utf-8")
    committed_blob = g(root, "rev-parse", "HEAD:phase165_r52_r9_shared_math.py")
    untracked_blob = g(root, "hash-object", "--", p.relative_to(root).as_posix())
    monkeypatch.setattr(audit, "PINNED_BLOBS", {
        "phase165_r52_r9_shared_math.py": committed_blob,
        audit.PRIOR_PACKAGE + "/rule.py": untracked_blob,
    })
    checked = audit.preflight(root)
    assert checked["head"] == base
    assert checked["pinned_source_blobs"] == 2
    assert checked["reviewed_intervening_paths"] == []


def test_preflight_rejects_untracked_r4r7_byte_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    g(root, "checkout", "-qb", "develop")
    fake_source = root / "phase165_r52_r9_shared_math.py"
    fake_source.write_text("no public R4R7 provider", encoding="utf-8")
    commit(root, "committed source")
    monkeypatch.setattr(audit, "BASE_HEAD", g(root, "rev-parse", "HEAD"))
    p = root / audit.PRIOR_PACKAGE / "rule.py"
    p.parent.mkdir(parents=True)
    p.write_text("tampered code", encoding="utf-8")
    monkeypatch.setattr(audit, "PINNED_BLOBS", {
        "phase165_r52_r9_shared_math.py": g(root, "rev-parse", "HEAD:phase165_r52_r9_shared_math.py"),
        audit.PRIOR_PACKAGE + "/rule.py": "0" * 40,
    })
    with pytest.raises(RuntimeError, match="R4R8_PINNED_SOURCE_BLOB_DRIFT"):
        audit.preflight(root)
