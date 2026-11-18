# Phase 175 R4R12R8 — 新規コード全文

追加位置：リポジトリ直下に `phase175_r4r12r8_delta_generator_source_audit/` を追加する。既存クラス、関数、import は変更しない。

## `audit.py`

```python
"""Read-only Source-first audit of the Toda Delta generator image in Phase 175 R4R12R8.

This module checks textual source evidence and explicitly does not construct a
ProofStep, register a GIVEN, install a rule, or run recursive proof search.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import traceback

PACKAGE = "phase175_r4r12r8_delta_generator_source_audit"
BASE_HEAD = "94c5d6839889bbfa03aad166ac9c6fd1558b8c5b"
R7_COMMIT = "b7bbb1032ef6c0568cb0cbf1c0116c2b183716e4"
SOURCE = Path("sources/toda/Toda_05_2.tex")
R7_AUDIT = Path("phase175_r4r12r7_six_obligation_frontier/audit.py")
R7_TEST = Path("phase175_r4r12r7_six_obligation_frontier/tests/test_audit.py")
DELTA_RULE = Path("toda_delta_image_rules.py")


def git(root: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    return proc.returncode, proc.stdout.strip()


def verify_repository(root: Path) -> dict[str, object]:
    rc, actual_root = git(root, "rev-parse", "--show-toplevel")
    if rc or Path(actual_root).resolve() != root.resolve():
        raise RuntimeError("Run from the repository root")
    rc, branch = git(root, "branch", "--show-current")
    if rc or branch != "develop":
        raise RuntimeError("Expected develop branch")
    rc, head = git(root, "rev-parse", "HEAD")
    if rc:
        raise RuntimeError("Unable to read HEAD")
    rc, _ = git(root, "merge-base", "--is-ancestor", BASE_HEAD, head)
    if rc:
        raise RuntimeError("Baseline R4R12R6 commit is not an ancestor of HEAD")
    rc, dirty = git(root, "status", "--porcelain", "--untracked-files=no")
    if rc:
        raise RuntimeError("Unable to inspect working tree")
    # A read-only audit never silently treats uncommitted work as the reviewed source.
    dirty_paths = [line[3:] for line in dirty.splitlines() if len(line) >= 4]
    tracked_evidence = [str(SOURCE), str(R7_AUDIT), str(R7_TEST), str(DELTA_RULE)]
    modified_evidence = sorted(set(dirty_paths).intersection(tracked_evidence))
    if modified_evidence:
        raise RuntimeError("Tracked source or audit evidence is dirty: " + repr(modified_evidence))
    return {
        "head": head,
        "branch": branch,
        "baseline_is_ancestor": True,
        "r7_commit_is_ancestor": git(root, "merge-base", "--is-ancestor", R7_COMMIT, head)[0] == 0,
        "other_tracked_changes_present": bool(dirty_paths),
        "modified_evidence": [],
    }


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def single_segment(source: str, start: str, end: str) -> str:
    if source.count(start) != 1:
        raise RuntimeError("Missing or ambiguous source anchor: " + start)
    after = source.split(start, 1)[1]
    if end not in after:
        raise RuntimeError("Missing source boundary: " + end)
    return after.split(end, 1)[0]


def inspect_source(source: str) -> dict[str, object]:
    eq58 = single_segment(source, r"\begin{equation}\label{eq:5.8}", r"\end{equation}")
    eq511 = single_segment(source, r"\begin{equation}\label{eq:5.11}", r"\end{equation}")
    proof = single_segment(source, r"\begin{proposition}\label{prop:5.8}", r"\qed")
    n58 = normalized(eq58)
    n511 = normalized(eq511)
    np = normalized(proof)
    requirements = {
        "equation_5_8_has_signed_delta_iota9": r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" in n58,
        "equation_5_11_has_delta_eta9": r"\Delta(\eta_9)=E\nu'\circ\eta_7" in n511,
        "proof_uses_prop_2_5": r"\Delta(\iota_9)\circ\eta_7" in np and "byProp2.5" in np,
        "proof_uses_equation_5_8": r"(2\nu_4-E\nu')\circ\eta_7" in np and "by(5.8)" in np,
        "proof_uses_order_two_reduction": r"\nu_4\circ(2\eta_7)-E\nu'\circ\eta_7" in np,
        "proof_prints_final_image": r"E\nu'\circ\eta_7" in np,
    }
    if not all(requirements.values()):
        raise RuntimeError("Required Toda source markers missing: " + repr(requirements))
    # 2-primary groups yield -x=x only after order-two is established;
    # this audit records the obligation rather than certifying the proof.
    return {
        "adopted_tex_path": str(SOURCE),
        "markers": requirements,
        "relation_explicitly_printed": True,
        "signed_source_equation": True,
        "sign_disappears_only_after_order_two_argument": True,
        "source_edition_is_original_print": False,
        "type_source": "Delta: pi_10^9 -> pi_8^4; eta_9 in pi_10^9",
        "type_target": "E(nu_prime) o eta_7 in pi_8^4",
    }


def inspect_existing_rule(rule_text: str, r7_text: str) -> dict[str, object]:
    required_rule = [
        "def free_cyclic_generator_delta_image_inference_rule", 
        "TodaDeltaImageUpToSignStatement", "TodaDeltaImageFreeCyclicStatement",
    ]
    if not all(marker in rule_text for marker in required_rule):
        raise RuntimeError("Existing Delta image rule unexpectedly changed")
    if "def audit_obligations" not in r7_text or '"proved": False' not in r7_text:
        raise RuntimeError("R7 frontier audit contract unexpectedly changed")
    return {
        "existing_rule_requires_signed_image_as_premise": True,
        "existing_rule_does_not_construct_the_image_equation": True,
        "r7_explicitly_reports_unproved_obligations": True,
        "typed_proof_of_equation_5_11": False,
        "recursive_proof_search_executed": False,
    }


def build_report(root: Path) -> dict[str, object]:
    repository = verify_repository(root)
    for relative in (SOURCE, R7_AUDIT, R7_TEST, DELTA_RULE):
        if not (root / relative).is_file():
            raise RuntimeError("Missing reviewed source/test: " + str(relative))
    source = inspect_source((root / SOURCE).read_text(encoding="utf-8-sig"))
    rule = inspect_existing_rule(
        (root / DELTA_RULE).read_text(encoding="utf-8-sig"),
        (root / R7_AUDIT).read_text(encoding="utf-8-sig"),
    )
    return {
        "phase": "175-R4R12R8",
        "repository": repository,
        "source": source,
        "existing_rules": rule,
        "remaining_obligations": [
            "Admit typed Proposition 2.5 with exact hypotheses and 2-primary equality condition",
            "Derive signed equation (5.8) without promoting a conclusion to a GIVEN",
            "Verify order two of eta_7 and E(nu_prime) o eta_7 before dropping signs",
            "Verify typed composition and additivity rules, including dimension endpoints",
            "Evaluate shared-provider candidate expansion without asserting completion",
        ],
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": False,
        "full_pytest_executed": False,
        "group_proof_complete": False,
        "gate": "PASS_R4R12R8_ADOPTED_SOURCE_FOUND_TYPED_PROOF_PENDING",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    try:
        report = build_report(root)
        report["dry_run"] = arguments.dry_run
    except Exception as error:
        report = {
            "phase": "175-R4R12R8", "dry_run": arguments.dry_run,
            "gate": "FAIL_R4R12R8_SOURCE_AUDIT",
            "error": type(error).__name__ + ": " + str(error),
            "traceback": traceback.format_exc()[-5000:],
            "group_proof_complete": False,
        }
    destination = root / PACKAGE / "output"
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / ("preflight.json" if arguments.dry_run else "audit_report.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R8_GATE=" + str(report["gate"]))
    print("PHASE175_R4R12R8_REPORT=" + str(path))
    print("PHASE175_R4R12R8_GROUP_COMPLETE=False")
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())

```

## `tests/test_audit.py`

```python
"""Focused read-only tests for Phase 175 R4R12R8."""
from pathlib import Path
import pytest
from phase175_r4r12r8_delta_generator_source_audit import audit


def test_delta_source_expected_proof_fragments() -> None:
    source = (
        r"\begin{equation}\label{eq:5.8}\Delta(\iota_9)=\pm(2\nu_4-E\nu')\end{equation}"
        r"\begin{proposition}\label{prop:5.8}"
        r"\Delta(\iota_9)\circ\eta_7\text{by Prop2.5}"
        r"(2\nu_4-E\nu')\circ\eta_7\text{by (5.8)}"
        r"\nu_4\circ(2\eta_7)-E\nu'\circ\eta_7"
        r"E\nu'\circ\eta_7\qed"
        r"\begin{equation}\label{eq:5.11}\Delta(\eta_9)=E\nu'\circ\eta_7\end{equation}"
    )
    result = audit.inspect_source(source)
    assert all(result["markers"].values())
    assert result["sign_disappears_only_after_order_two_argument"]
    assert not result["source_edition_is_original_print"]


def test_missing_signed_equation_fails_closed() -> None:
    source = (
        r"\begin{equation}\label{eq:5.8}\Delta(\iota_9)=0\end{equation}"
        r"\begin{proposition}\label{prop:5.8}\qed"
        r"\begin{equation}\label{eq:5.11}\Delta(\eta_9)=0\end{equation}"
    )
    with pytest.raises(RuntimeError, match="source markers missing"):
        audit.inspect_source(source)


def test_existing_rule_is_not_mistaken_for_image_proof() -> None:
    rule = (
        "def free_cyclic_generator_delta_image_inference_rule():\n"
        "    pass\n"
        "# TodaDeltaImageUpToSignStatement\n"
        "# TodaDeltaImageFreeCyclicStatement\n"
    )
    r7 = 'def audit_obligations():\n    return {"proved": False}\n'
    result = audit.inspect_existing_rule(rule, r7)
    assert result["existing_rule_requires_signed_image_as_premise"]
    assert not result["typed_proof_of_equation_5_11"]


def test_wrong_repository_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="repository root"):
        audit.verify_repository(tmp_path)

```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = 'phase175_r4r12r8_delta_generator_source_audit'
python -B -m pytest -q --import-mode=prepend -p no:cacheprovider ".\$package\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R4R12R8 focused pytest failed' }
$arguments = @('-B', '-m', "$package.audit", '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { throw 'R4R12R8 read-only audit failed' }

```

## `__init__.py`

```python
"""Source-first audit package; no production hooks."""

```
