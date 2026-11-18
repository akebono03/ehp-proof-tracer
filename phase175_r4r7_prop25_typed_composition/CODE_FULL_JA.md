# Phase 175 R4R7R1 — 置換・追加コード全文

既存本番コードは変更しない。`audit.py` の `reviewed_head_lineage()` は `git()` と `preflight()` の間に追加する。`preflight()` 全体を置換し、定数2件を既存の `REVIEWED_HEAD` の直後に置く。`tests/test_audit.py` は import を更新し、テスト・ヘルパー9件を末尾に追加する。

## 変更後の import 部分

### `audit.py`

```python
"""Phase 175 R4R7: isolated and source-guarded conditional Prop 2.5 rule audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
```

### `tests/test_audit.py`

```python
"""Fail-closed R4R7 audit contracts; the reports below are synthetic fixtures."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import hashlib
import subprocess

import pytest

from phase175_r4r7_prop25_typed_composition import audit
```

## ファイル全文

### `audit.py`

```python
"""Phase 175 R4R7: isolated and source-guarded conditional Prop 2.5 rule audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

PACKAGE = "phase175_r4r7_prop25_typed_composition"
PRIOR_PACKAGE = "phase175_r4r6_prop25_eq58_source_frontier"
PRIOR_GATE = "PASS_R4R6_PROP25_EQ58_SOURCE_FRONTIER_RECORDED_NOT_PUBLIC"
DRY_GATE = "PASS_R4R7_PROP25_TYPED_INFERENCE_DRYRUN"
FINAL_GATE = "PASS_R4R7_PROP25_TYPED_INFERENCE_ISOLATED_NOT_PUBLIC"
REVIEWED_HEAD = "c48fdc307ba67a5e21b0ef49d57953468f7b47e2"
REVIEWED_R4R6_HEAD = "11968d23724cee147520b5fa3fd5a6e89989003e"
REVIEWED_R4R6_PATHS = (
    "phase175_r4r6_prop25_eq58_source_frontier/AUDIT_PLAN_JA.md",
    "phase175_r4r6_prop25_eq58_source_frontier/CODE_FULL_JA.md",
    "phase175_r4r6_prop25_eq58_source_frontier/README.md",
    "phase175_r4r6_prop25_eq58_source_frontier/TEST_RESULTS_JA.md",
    "phase175_r4r6_prop25_eq58_source_frontier/__init__.py",
    "phase175_r4r6_prop25_eq58_source_frontier/audit.py",
    "phase175_r4r6_prop25_eq58_source_frontier/run.ps1",
    "phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py",
)
PRIOR_HISTORICAL_HEAD = "bc1a9eff9c1d051764ff817bb1948f55a1479961"
PRIOR_AUDIT_SHA256 = "cedcfc994d4ccf6989bc9025a82741e51105708da0d1305fb3282e5ae41f9b7d"
PINNED_GIT_BLOBS = {
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "df4e0f834e9bc321f338ec10b363c79d82623457",
    "phase175_r4r5r3_public_order_zero/provider.py": "9a736418a2f191cfe485e3777c8bbb2143f2a9f3",
}


def git(root: Path, *parts: str) -> str:
    result = subprocess.run(
        ["git", *parts], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R7_GIT_ERROR: " + " ".join(parts) + " " + result.stderr.strip())
    return result.stdout.strip()


def reviewed_head_lineage(root: Path, head: str) -> list[str]:
    """Accept only the reviewed R4R6 successor with its exact committed paths.

    The original R4R7 baseline is also supported. Any unrelated or later
    commit is rejected; individual source blobs and R4R6 audit bytes are
    independently checked in preflight().
    """
    if head == REVIEWED_HEAD:
        return []
    if head != REVIEWED_R4R6_HEAD:
        raise RuntimeError("R4R7_UNREVIEWED_HEAD: " + head)
    git(root, "merge-base", "--is-ancestor", REVIEWED_HEAD, head)
    changed = sorted(set(git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()))
    if changed != sorted(REVIEWED_R4R6_PATHS):
        raise RuntimeError("R4R7_UNREVIEWED_R4R6_LINEAGE: " + repr(changed))
    return changed


def preflight(root: Path) -> dict[str, object]:
    """Guard the reviewed Git lineage, source blobs and inherited R4R6 code."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R7_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R7_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")
    reviewed_changes = reviewed_head_lineage(root, head)
    tracked = sorted(set(
        git(root, "diff", "--name-only").splitlines()
        + git(root, "diff", "--cached", "--name-only").splitlines()
    ))
    if [path for path in tracked if path != ".pytest_cache/v/cache/nodeids"]:
        raise RuntimeError("R4R7_UNREVIEWED_TRACKED_CHANGES: " + repr(tracked))
    for path, expected in PINNED_GIT_BLOBS.items():
        if not (root / path).is_file():
            raise RuntimeError("R4R7_SOURCE_FILE_MISSING: " + path)
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("R4R7_SOURCE_BLOB_DRIFT: " + path)
    prior_audit = root / PRIOR_PACKAGE / "audit.py"
    if (not prior_audit.is_file()
            or hashlib.sha256(prior_audit.read_bytes()).hexdigest() != PRIOR_AUDIT_SHA256):
        raise RuntimeError("R4R7_REVIEWED_R4R6_AUDIT_DRIFT")
    return {
        "head": head,
        "reviewed_r4r7_base_head": REVIEWED_HEAD,
        "reviewed_r4r6_successor_head": REVIEWED_R4R6_HEAD,
        "reviewed_intervening_paths": reviewed_changes,
        "pinned_blobs": len(PINNED_GIT_BLOBS),
        "prior_audit_sha256": PRIOR_AUDIT_SHA256,
        "tracked_changed": tracked,
    }


def validate_prior(data: object) -> dict[str, object]:
    """Only an actual completed R4R6 audit, not a mathematical proof."""
    if not isinstance(data, dict):
        raise RuntimeError("R4R7_R4R6_REPORT_INVALID")
    expected = {
        "phase": "175-R4R6",
        "mode": "READ_ONLY_SOURCE_TYPE_BOUNDARY_AUDIT",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
    }
    if any(data.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R7_R4R6_SCOPE_OR_GATE_INVALID")
    pre = data.get("preflight")
    history = data.get("prior_history")
    printed = data.get("source_evidence")
    typed = data.get("typed_frontier")
    boundary = data.get("order_and_implementation_boundary")
    if (not isinstance(pre, dict) or pre.get("head") != REVIEWED_HEAD
            or not isinstance(history, dict)
            or history.get("historical_reviewed_head") != PRIOR_HISTORICAL_HEAD
            or history.get("historical_production_blob_checked") is not True
            or history.get("historical_rule_sha256_checked") is not True
            or not isinstance(printed, dict)
            or printed.get("proposition_2_5_inclusion_and_conditions") is not True
            or printed.get("equation_5_8_signed_identity") is not True
            or printed.get("source_sign_preserved") != "±"
            or printed.get("printed_relation_is_a_verified_proof_step") is not False
            or not isinstance(typed, dict)
            or (typed.get("m"), typed.get("i"), typed.get("j")) != (4, 8, 9)
            or typed.get("j_less_than_3m_minus_1") is not True
            or typed.get("typed_endpoints_are_verified_proof_steps") is not False
            or not isinstance(boundary, dict)
            or boundary.get("new_prop25_provider_connected") is not False
            or boundary.get("signed_reduction_executed_as_proof_step") is not False
            or boundary.get("prior_proof_search_executed") is not False):
        raise RuntimeError("R4R7_R4R6_EVIDENCE_INVALID")
    return {
        "r4r6_head": pre["head"],
        "r4r5r3_historical_head": history["historical_reviewed_head"],
        "printed_source_is_not_proof": True,
        "r4r6_public_proof_completed": False,
    }


def latest_real_prior(explicit: Path | None = None) -> Path:
    if explicit is not None:
        candidate = explicit.expanduser().resolve()
        if not candidate.is_file():
            raise RuntimeError("R4R7_R4R6_REPORT_MISSING: " + str(candidate))
        return candidate
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    rejected: list[str] = []
    for path in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, UnicodeError, RuntimeError) as error:
            rejected.append(path.name + ": " + str(error))
            continue
        return path
    raise RuntimeError(
        "R4R7_SUCCESSFUL_R4R6_REPORT_NOT_FOUND: " + str(folder)
        + " rejected=" + repr(rejected[:5])
    )


def check_source_and_boundaries(root: Path) -> dict[str, object]:
    """Revalidate Toda wording and verify public provider wasn't wired to R4R7."""
    from phase175_r4r6_prop25_eq58_source_frontier import audit as prior_audit

    printed = prior_audit.source_evidence(
        (root / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8"),
        (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8"),
    )
    if (printed["printed_relation_is_a_verified_proof_step"] is not False
            or printed["source_sign_preserved"] != "±"):
        raise RuntimeError("R4R7_PRINTED_SOURCE_PROMOTED_TO_PROOF")
    typed = prior_audit.typed_frontier()
    if (typed["m"], typed["i"], typed["j"]) != (4, 8, 9):
        raise RuntimeError("R4R7_SPECIALIZATION_CHANGED")
    shared = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    if ("phase175_r4r7_prop25_typed_composition" in shared
            or "expand_prop25_signed_composition" in shared):
        raise RuntimeError("R4R7_PREMATURE_PUBLIC_CONNECTION")
    return {
        "source_rechecked": True,
        "m_i_j": [4, 8, 9],
        "numeric_equality_condition": True,
        "sign_retained": True,
        "primary_branch_not_assumed": True,
        "public_search_unchanged": True,
        "source_is_proof": False,
    }


def audit_isolated_rule() -> dict[str, object]:
    """Create a typed backward obligation only; not a verified parent step."""
    from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from proof import Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement
    from phase175_r4r7_prop25_typed_composition.rule import expand_prop25_signed_composition

    alpha = HomotopyElement("iota", 9, source=9, target=9)
    beta = HomotopyElement("eta", 7, source=8, target=7)
    gamma = HomotopyElement("eta", 9, source=10, target=9)
    nu = HomotopyElement("nu", 4, source=7, target=4)
    other = HomotopyElement("E_nu_prime", 4, source=7, target=4)
    representative = Sum(Multiple(2, nu), Multiple(-1, other))
    signed = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)),
        alpha, representative,
    )
    identity = Relation(Composition(alpha, IteratedSuspension(beta, 2)),
                        gamma, RelationType.EQUALITY)
    goal = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(representative, beta),
    )
    results = expand_prop25_signed_composition(goal, signed, identity)
    if (len(results) != 1 or results[0].subgoals != (signed, identity)
            or results[0].rule.conclusion_pattern != goal):
        raise RuntimeError("R4R7_ISOLATED_TYPED_GOAL_INVALID")
    return {
        "isolated_backward_proposals": 1,
        "unproved_parent_obligations": 2,
        "signed_goal_retained": True,
        "verified_parent_proof_steps_created": 0,
        "previous_proof_search_executed": False,
        "public_provider_connected": False,
        "pi95_completed": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run(root: Path, *, dry_run: bool, prior_path: Path | None) -> int:
    output = report_folder()
    result: dict[str, object] = {
        "phase": "175-R4R7", "mode": "ISOLATED_TYPED_CONDITIONAL_INFERENCE",
        "dry_run": dry_run,
        "new_given": 0, "new_mathematical_rules": 1,
        "production_changes": [], "rule_connected_to_public": False,
        "pi95_proof_complete": False, "full_pytest_executed": False,
        "gate": "FAIL_R4R7_PROP25_TYPED_INFERENCE",
    }
    try:
        result["preflight"] = preflight(root)
        path = latest_real_prior(prior_path)
        result["prior_report"] = str(path)
        result["prior"] = validate_prior(json.loads(path.read_text(encoding="utf-8")))
        result["source_and_boundary"] = check_source_and_boundaries(root)
        result["isolated"] = audit_isolated_rule()
        result["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        result["error"] = type(error).__name__ + ": " + str(error)
        result["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "report.md").write_text(
        "# Phase 175 R4R7 — Toda Proposition 2.5 型付き一般推論\n\n"
        + "Gate: `" + str(result["gate"]) + "`\n\n"
        + "一般規則は独立した証明済み前提2件を必要とする。\n"
        + "符号 ± は保存し、m が奇数または j<3m−1 の場合だけ扱う。\n"
        + "2-primary の条件を無証明で仮定しない。\n"
        + "公開 Proof Search は未接続。π₉⁵ の証明は未完成。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R7_HEAD=" + str(result.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R7_NEW_GIVEN=0")
    print("PHASE175_R4R7_NEW_MATHEMATICAL_RULES=1")
    print("PHASE175_R4R7_PRODUCTION_CHANGES=0")
    print("PHASE175_R4R7_PUBLIC_RULE=NOT_CONNECTED")
    print("PHASE175_R4R7_PI95=NOT_COMPLETE")
    print("PHASE175_R4R7_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R7_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R7_GATE=" + str(result["gate"]))
    if "error" in result:
        print("PHASE175_R4R7_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r6-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_path=args.r4r6_report)


if __name__ == "__main__":
    sys.exit(main())
```

### `tests/test_audit.py`

```python
"""Fail-closed R4R7 audit contracts; the reports below are synthetic fixtures."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import hashlib
import subprocess

import pytest

from phase175_r4r7_prop25_typed_composition import audit


def passed_r4r6_report() -> dict[str, object]:
    return {
        "phase": "175-R4R6",
        "mode": "READ_ONLY_SOURCE_TYPE_BOUNDARY_AUDIT",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "preflight": {"head": audit.REVIEWED_HEAD},
        "prior_history": {
            "historical_reviewed_head": audit.PRIOR_HISTORICAL_HEAD,
            "historical_production_blob_checked": True,
            "historical_rule_sha256_checked": True,
        },
        "source_evidence": {
            "proposition_2_5_inclusion_and_conditions": True,
            "equation_5_8_signed_identity": True,
            "source_sign_preserved": "±",
            "printed_relation_is_a_verified_proof_step": False,
        },
        "typed_frontier": {
            "m": 4, "i": 8, "j": 9,
            "j_less_than_3m_minus_1": True,
            "typed_endpoints_are_verified_proof_steps": False,
        },
        "order_and_implementation_boundary": {
            "new_prop25_provider_connected": False,
            "signed_reduction_executed_as_proof_step": False,
            "prior_proof_search_executed": False,
        },
    }


def test_r4r6_real_success_shape_validated_without_proof_upgrade() -> None:
    found = audit.validate_prior(passed_r4r6_report())
    assert found["r4r6_head"] == audit.REVIEWED_HEAD
    assert found["printed_source_is_not_proof"] is True
    assert found["r4r6_public_proof_completed"] is False


@pytest.mark.parametrize("name,value", (
    ("phase", "175-R4R5R3"),
    ("gate", audit.DRY_GATE),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("production_changes", ["proof.py"]),
    ("rule_connected_to_public", True),
    ("pi95_proof_complete", True),
    ("full_pytest_executed", True),
))
def test_wrong_gate_or_scope_rejected(name: str, value: object) -> None:
    report = passed_r4r6_report()
    report[name] = value
    with pytest.raises(RuntimeError, match="R4R7_R4R6_SCOPE_OR_GATE_INVALID"):
        audit.validate_prior(report)


@pytest.mark.parametrize("section,name,value", (
    ("preflight", "head", "0" * 40),
    ("prior_history", "historical_reviewed_head", "0" * 40),
    ("prior_history", "historical_production_blob_checked", False),
    ("prior_history", "historical_rule_sha256_checked", False),
    ("source_evidence", "equation_5_8_signed_identity", False),
    ("source_evidence", "source_sign_preserved", "+"),
    ("source_evidence", "printed_relation_is_a_verified_proof_step", True),
    ("typed_frontier", "m", 5),
    ("typed_frontier", "j_less_than_3m_minus_1", False),
    ("typed_frontier", "typed_endpoints_are_verified_proof_steps", True),
    ("order_and_implementation_boundary", "new_prop25_provider_connected", True),
    ("order_and_implementation_boundary", "signed_reduction_executed_as_proof_step", True),
    ("order_and_implementation_boundary", "prior_proof_search_executed", True),
))
def test_prior_evidence_change_rejected(section: str, name: str, value: object) -> None:
    report = deepcopy(passed_r4r6_report())
    report[section][name] = value
    with pytest.raises(RuntimeError, match="R4R7_R4R6_EVIDENCE_INVALID"):
        audit.validate_prior(report)


def test_only_latest_valid_real_report_chosen(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    base = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    prior = base / "20261117T083246_831773Z"
    later = base / "20261117T083247_831773Z"
    prior.mkdir(parents=True)
    later.mkdir(parents=True)
    (prior / "report.json").write_text(json.dumps(passed_r4r6_report()), encoding="utf-8")
    rejected = passed_r4r6_report()
    rejected["gate"] = "FAIL_R4R6"
    (later / "report.json").write_text(json.dumps(rejected), encoding="utf-8")
    assert audit.latest_real_prior() == prior / "report.json"
    assert audit.latest_real_prior(prior / "report.json") == (prior / "report.json").resolve()
    with pytest.raises(RuntimeError, match="R4R7_R4R6_REPORT_MISSING"):
        audit.latest_real_prior(prior / "missing.json")


def test_missing_or_rejected_reports_fail_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    with pytest.raises(RuntimeError, match="R4R7_SUCCESSFUL_R4R6_REPORT_NOT_FOUND"):
        audit.latest_real_prior()
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE / "20261117"
    folder.mkdir(parents=True)
    (folder / "report.json").write_text('{"gate":"FAIL"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="R4R7_SUCCESSFUL_R4R6_REPORT_NOT_FOUND"):
        audit.latest_real_prior()


def test_source_guard_rejects_wrong_head(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audit, "git", lambda root, *args: (
        str(root) if args == ("rev-parse", "--show-toplevel")
        else "develop" if args == ("branch", "--show-current")
        else "0" * 40
    ))
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_HEAD"):
        audit.preflight(tmp_path)


def test_source_guard_rejects_dirty_unrelated_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("rev-parse", "--show-toplevel"):
            return str(root)
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return audit.REVIEWED_HEAD
        if args == ("diff", "--name-only"):
            return "proof.py"
        if args == ("diff", "--cached", "--name-only"):
            return ""
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_TRACKED_CHANGES"):
        audit.preflight(tmp_path)


def test_report_is_not_proof_certificate() -> None:
    report = passed_r4r6_report()
    result = audit.validate_prior(report)
    assert "verified_proof_step" not in result
    assert result["printed_source_is_not_proof"] is True


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True,
    )
    return result.stdout.strip()


def commit_fixture(root: Path, message: str) -> str:
    run_git(root, "add", ".")
    run_git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com",
            "commit", "-qm", message)
    return run_git(root, "rev-parse", "HEAD")


def synthetic_reviewed_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    *, extra_path: str | None = None,
) -> tuple[Path, str, str]:
    """Construct two real Git commits; no synthetic HEAD values are trusted."""
    root = tmp_path / "repo"
    root.mkdir()
    run_git(root, "init", "-q")
    run_git(root, "checkout", "-qb", "develop")
    pinned = root / "proof.py"
    pinned.write_text("reviewed proof source\n", encoding="utf-8")
    old = commit_fixture(root, "reviewed R4R7 base")
    for name in audit.REVIEWED_R4R6_PATHS:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("reviewed R4R6 file: " + name + "\n", encoding="utf-8")
    if extra_path is not None:
        path = root / extra_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("not reviewed\n", encoding="utf-8")
    successor = commit_fixture(root, "175-4-6")
    monkeypatch.setattr(audit, "REVIEWED_HEAD", old)
    monkeypatch.setattr(audit, "REVIEWED_R4R6_HEAD", successor)
    monkeypatch.setattr(audit, "PINNED_GIT_BLOBS", {
        "proof.py": run_git(root, "rev-parse", "HEAD:proof.py"),
    })
    sha = hashlib.sha256((root / audit.PRIOR_PACKAGE / "audit.py").read_bytes()).hexdigest()
    monkeypatch.setattr(audit, "PRIOR_AUDIT_SHA256", sha)
    return root, old, successor


def test_reviewed_r4r6_successor_with_exact_paths_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old, successor = synthetic_reviewed_history(tmp_path, monkeypatch)
    result = audit.preflight(root)
    assert result["head"] == successor
    assert result["reviewed_r4r7_base_head"] == old
    assert result["reviewed_intervening_paths"] == sorted(audit.REVIEWED_R4R6_PATHS)
    assert result["pinned_blobs"] == 1


def test_unreviewed_extra_file_in_r4r6_commit_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(
        tmp_path, monkeypatch, extra_path="unreviewed_source.py",
    )
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_R4R6_LINEAGE"):
        audit.preflight(root)


def test_later_unreviewed_head_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    (root / "new_file.txt").write_text("later commit\n", encoding="utf-8")
    next_head = commit_fixture(root, "unaudited later commit")
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_HEAD: " + next_head):
        audit.preflight(root)


def test_reviewed_successor_source_blob_drift_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    monkeypatch.setattr(audit, "PINNED_GIT_BLOBS", {"proof.py": "0" * 40})
    with pytest.raises(RuntimeError, match="R4R7_SOURCE_BLOB_DRIFT"):
        audit.preflight(root)


def test_reviewed_successor_r4r6_audit_bytes_drift_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    audit_file = root / audit.PRIOR_PACKAGE / "audit.py"
    audit_file.write_text("modified source\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_TRACKED_CHANGES"):
        audit.preflight(root)
    run_git(root, "restore", "--", audit.PRIOR_PACKAGE + "/audit.py")
    monkeypatch.setattr(audit, "PRIOR_AUDIT_SHA256", "0" * 64)
    with pytest.raises(RuntimeError, match="R4R7_REVIEWED_R4R6_AUDIT_DRIFT"):
        audit.preflight(root)


def test_wrong_ancestry_in_reviewed_successor_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    monkeypatch.setattr(audit, "REVIEWED_HEAD", "0" * 40)
    with pytest.raises(RuntimeError, match="R4R7_GIT_ERROR"):
        audit.preflight(root)
```

### `rule.py`

```python
"""Conditional, dimension-checked Toda Proposition 2.5 equality inference.

For alpha in pi_(i+1)^(2m+1) and beta in pi_(j-1)^(i-1), the
source proves Delta(alpha) o beta is contained in Delta(alpha o E^2 beta).
Under m odd OR j < 3m-1 the inclusion is equality. Given separately
proved signed Delta(alpha)=+/-x and alpha o E^2 beta=gamma, derive
Delta(gamma)=+/-(x o beta), keeping the sign unresolved.

The alternative 2-primary equality branch is deliberately NOT inferred from
an unproved flag. This isolated rule registers no source statements or GIVEN
and is not connected to public proof search in R4R7.
"""
from __future__ import annotations

from expression import (
    Composition,
    HomotopyElement,
    IteratedSuspension,
    Multiple,
    Sum,
    Suspension,
)
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from toda_rules import TodaDeltaImageUpToSignStatement


RULE_NAME = "Toda Proposition 2.5 conditional signed Delta composition equality"


def typed_endpoints(expression: object) -> tuple[int, int] | None:
    """Check the actual sphere source and target, including identity maps."""
    if isinstance(expression, HomotopyElement):
        values = (expression.dimension, expression.source, expression.target)
        if (any(type(value) is not int for value in values)
                or expression.dimension != expression.target
                or expression.target < 2
                or expression.source < expression.target):
            return None
        return expression.source, expression.target
    if isinstance(expression, Composition):
        left = typed_endpoints(expression.left)
        right = typed_endpoints(expression.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    if isinstance(expression, (Suspension, IteratedSuspension)):
        exponent = 1 if isinstance(expression, Suspension) else expression.exponent
        if type(exponent) is not int or exponent < 0:
            return None
        endpoints = typed_endpoints(expression.expression)
        if endpoints is None:
            return None
        return endpoints[0] + exponent, endpoints[1] + exponent
    if isinstance(expression, Multiple):
        if type(expression.coefficient) is not int:
            return None
        return typed_endpoints(expression.expression)
    if isinstance(expression, Sum):
        left = typed_endpoints(expression.left)
        right = typed_endpoints(expression.right)
        if left is None or left != right:
            return None
        return left
    return None


def prop25_inputs(
    goal: object,
    signed_delta: object,
    composition_identity: object,
) -> tuple[TodaDeltaImageUpToSignStatement, Relation] | None:
    """Return the two independently proved obligations or reject the goal.

    Dimensions are reconstructed from the actual typed alpha/beta/gamma and
    Delta maps. Neither a familiar symbol name nor a stated index is trusted.
    This branch uses only the explicitly checkable arithmetic hypotheses of
    Prop 2.5 (m odd or j < 3m-1), not presumed 2-primary membership.
    """
    if (type(goal) is not TodaDeltaImageUpToSignStatement
            or type(signed_delta) is not TodaDeltaImageUpToSignStatement
            or type(composition_identity) is not Relation
            or composition_identity.relation_type is not RelationType.EQUALITY
            or not isinstance(composition_identity.lhs, Composition)
            or not isinstance(composition_identity.lhs.right, IteratedSuspension)
            or type(composition_identity.lhs.right.exponent) is not int
            or composition_identity.lhs.right.exponent != 2):
        return None

    alpha = composition_identity.lhs.left
    beta = composition_identity.lhs.right.expression
    gamma = composition_identity.rhs
    alpha_pair = typed_endpoints(alpha)
    beta_pair = typed_endpoints(beta)
    gamma_pair = typed_endpoints(gamma)
    value_pair = typed_endpoints(signed_delta.positive_value)
    if (alpha_pair is None or beta_pair is None
            or gamma_pair is None or value_pair is None
            or signed_delta.element != alpha):
        return None

    i = alpha_pair[0] - 1
    j = beta_pair[0] + 1
    if ((alpha_pair[1] - 1) % 2 != 0):
        return None
    m = (alpha_pair[1] - 1) // 2
    if (m < 2 or i < 2 * m or j < i
            or beta_pair != (j - 1, i - 1)
            or gamma_pair != (j + 1, 2 * m + 1)
            or value_pair != (i - 1, m)):
        return None
    if not (m % 2 == 1 or j < 3 * m - 1):
        return None

    source_delta = TodaDeltaMap(
        TodaPrimaryGroup(i + 1, 2 * m + 1),
        TodaPrimaryGroup(i - 1, m),
    )
    target_delta = TodaDeltaMap(
        TodaPrimaryGroup(j + 1, 2 * m + 1),
        TodaPrimaryGroup(j - 1, m),
    )
    if (signed_delta.map != source_delta
            or goal.map != target_delta
            or goal.element != gamma
            or goal.positive_value != Composition(signed_delta.positive_value, beta)
            or typed_endpoints(composition_identity.lhs) != gamma_pair
            or typed_endpoints(goal.positive_value) != (j - 1, m)):
        return None
    return signed_delta, composition_identity


def prop25_signed_composition_rule(
    goal: TodaDeltaImageUpToSignStatement,
    signed_delta: TodaDeltaImageUpToSignStatement,
    composition_identity: Relation,
) -> InferenceRule:
    """Require two INFERENCE ProofSteps before concluding a signed image."""
    required = prop25_inputs(goal, signed_delta, composition_identity)
    if required is None:
        raise ValueError("not a typed conditional Proposition 2.5 goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and prop25_inputs(goal, signed_delta, composition_identity) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "With m odd or j<3m-1, Toda Proposition 2.5 turns the "
            "Delta-composition inclusion into equality. A proved signed "
            "Delta(alpha) and independently proved alpha o E^2(beta)=gamma "
            "give Delta(gamma)=+/-(Delta(alpha) representative o beta). "
            "Do not choose the sign or assume 2-primary membership."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaDeltaImageUpToSignStatement,
                statement_pattern=required[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[1],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_prop25_signed_composition(
    goal: object,
    signed_delta: object,
    composition_identity: object,
) -> tuple[GoalExpansion, ...]:
    """An isolated backward proposal, not a source or proof certificate."""
    required = prop25_inputs(goal, signed_delta, composition_identity)
    if required is None:
        return ()
    return (GoalExpansion(
        prop25_signed_composition_rule(goal, signed_delta, composition_identity),
        required,
    ),)
```

### `run.ps1`

```powershell
param(
    [switch] $DryRun,
    [string] $R4R6Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_audit.py',
        'phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py',
        'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
        'phase175_r4r5r3_public_order_zero/tests/test_real_integration.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R7 focused pytest failed' }
    Write-Output 'PHASE175_R4R7_FOCUSED_PYTEST=PASS'

    $argsForAudit = @(
        '-B', '-m', 'phase175_r4r7_prop25_typed_composition.audit', '--root', $root
    )
    if ($DryRun) { $argsForAudit += '--dry-run' }
    if ($R4R6Report -ne '') { $argsForAudit += @('--r4r6-report', $R4R6Report) }
    & python @argsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R4R7 isolated typed/source audit failed' }
    Write-Output 'PHASE175_R4R7_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R7_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R7_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
```

### `__init__.py`

```python
"""Phase 175 R4R7: isolated conditional Toda Proposition 2.5 inference."""
```
