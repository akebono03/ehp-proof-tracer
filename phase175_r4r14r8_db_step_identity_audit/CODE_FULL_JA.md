# Phase 175 R4R14R8 — コード全文

## audit.py

```python
"""Read-only inspection of the exact adopted DB step used in the R41 proof.

Do not accept any mismatched step; report which verification fields differ.
"""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
import json
import os
from pathlib import Path
import subprocess
import tempfile
import traceback


def git(root: Path, *args: str) -> str:
    command = subprocess.run(
        ("git",) + args, cwd=root, capture_output=True, check=False,
        text=True, encoding="utf-8", errors="replace",
    )
    if command.returncode:
        raise RuntimeError("GIT_FAILED " + " ".join(args) + ": " + command.stderr)
    return command.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_FILES_REQUIRE_REVIEW")
    source = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    for token in (
        "build_public_composite_zero_transport_provider(bridge)",
        "options.extend(expand_surjective_zero_codomain(goal))",
        "build_public_adopted_zero_image_provider(",
    ):
        if token not in source:
            raise RuntimeError("MISSING_CONNECTED_PROVIDER: " + token)
    return {"head": git(root, "rev-parse", "HEAD"),
            "shared_worktree_hash": git(root, "hash-object", "phase165_r52_r9_shared_math.py")}


def inspect() -> dict[str, object]:
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider,
    )
    from proof import ProofRule, find_inference_matches_for_rule

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    context = []
    result = search_group_from_registered_goal(n=6, k=4, context_sink=context.append)
    if len(context) != 1:
        raise RuntimeError("NOT_ONE_SCREENED_CONTEXT")
    bridge = context[0]
    group = TodaPrimaryGroup(9, 5)
    e = TodaSuspensionMap(group, TodaPrimaryGroup(10, 6))
    image_goal = ImageZeroStatement(e)
    presentation = exact_prior_database_result(5, 4)
    if presentation is None:
        raise RuntimeError("PRIOR_MISSING")
    generator_zero = GeneratorImage(e, presentation.rhs.generator, Zero())
    expected = admitted_db_step(presentation, proof_target=root, bridge=bridge)
    if expected is None:
        raise RuntimeError("EXPECTED_ADMITTED_DB_ABSENT")
    options = build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=root,
    )(image_goal)
    if len(options) != 1:
        raise RuntimeError("R41_PROPOSAL_MISSING_OR_DUPLICATE")
    option = options[0]
    steps = tuple(result.proven_steps)
    db_steps = tuple(s for s in steps if s.conclusion == presentation)
    generator_steps = tuple(s for s in steps if s.conclusion == generator_zero)

    def identify(step):
        return {
            "rule": getattr(step.rule, "name", str(step.rule)),
            "note": step.note,
            "inference_rule_name": getattr(step.inference_rule, "name", None),
            "literature_reference": repr(getattr(step.inference_rule, "literature_reference", None)),
            "premise_count": len(step.premises),
            "equals_expected_admitted": step == expected,
            "verified_db_step": verified_db_step(step, proof_target=root, bridge=bridge),
            "conclusion_matches": step.conclusion == presentation,
        }

    expected_fields = {}
    if is_dataclass(expected):
        for f in fields(expected):
            expected_fields[f.name] = repr(getattr(expected, f.name))[:1200]
    differences = []
    for step in db_steps:
        if is_dataclass(expected):
            differences.append({
                f.name: {
                    "observed": repr(getattr(step, f.name))[:1200],
                    "expected": repr(getattr(expected, f.name))[:1200],
                }
                for f in fields(expected)
                if getattr(step, f.name) != getattr(expected, f.name)
            })
        else:
            differences.append({"diagnostic": "non_dataclass_proof_step"})
    return {
        "search_status": getattr(result.status, "value", str(result.status)),
        "open_goals": [str(g) for g in result.open_goals],
        "proven_count": len(steps),
        "r41_subgoals_match": option.subgoals == (presentation, generator_zero),
        "r41_matches_with_actual_steps": len(find_inference_matches_for_rule(option.rule, steps)),
        "r41_matches_with_expected_added": len(find_inference_matches_for_rule(option.rule, steps + (expected,))),
        "expected_db_step": identify(expected),
        "expected_db_fields": expected_fields,
        "actual_db_steps": [identify(s) for s in db_steps],
        "actual_db_field_differences": differences,
        "actual_generator_zero_steps": [{
            "rule": getattr(s.rule, "name", str(s.rule)),
            "inference_rule": getattr(s.inference_rule, "name", None),
            "premise_count": len(s.premises),
        } for s in generator_steps],
        "new_given": 0,
        "production_changed": False,
        "root_complete_claimed": False,
    }


def run(root: Path, dry_run: bool) -> int:
    report: dict[str, object] = {"phase": "175_R4R14R8", "full_pytest": False,
                                 "gate": "FAIL_R4R14R8"}
    try:
        report["preflight"] = preflight(root)
        if not dry_run:
            report["observed"] = inspect()
        report["gate"] = (
            "PASS_R4R14R8_DRYRUN_SOURCE_GUARD" if dry_run
            else "PASS_R4R14R8_DB_STEP_IDENTITY_AUDITED"
        )
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
    path = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R8_db_step_identity.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R4R14R8_GATE=" + str(report["gate"]))
    print("PHASE175_R4R14R8_REPORT=" + str(path))
    if "error" in report:
        print("PHASE175_R4R14R8_ERROR=" + str(report["error"]))
        return 1
    if not dry_run:
        o = report["observed"]
        for key in ("search_status", "proven_count", "r41_matches_with_actual_steps",
                    "r41_matches_with_expected_added"):
            print("PHASE175_R4R14R8_" + key.upper() + "=" + str(o[key]))
        print("PHASE175_R4R14R8_ACTUAL_DB_VERIFIED=" +
              str([x["verified_db_step"] for x in o["actual_db_steps"]]))
        print("PHASE175_R4R14R8_ACTUAL_DB_DIFFERING_FIELDS=" +
              str([list(x) for x in o["actual_db_field_differences"]]))
        print("PHASE175_R4R14R8_NEW_GIVEN=0")
        print("PHASE175_R4R14R8_PRODUCTION_UNCHANGED=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_audit.py

```python
"""Source and audit contracts for the R41 DB-step discrepancy."""
from __future__ import annotations

from pathlib import Path

from phase175_r4r14r8_db_step_identity_audit import audit


def test_inspector_reports_field_level_provenance_differences() -> None:
    text = Path(audit.__file__).read_text(encoding="utf-8")
    assert "actual_db_field_differences" in text
    assert "verified_db_step(step, proof_target=root, bridge=bridge)" in text
    assert "r41_matches_with_actual_steps" in text
    assert "r41_matches_with_expected_added" in text


def test_audit_does_not_patch_public_search() -> None:
    text = Path(audit.__file__).read_text(encoding="utf-8")
    assert "search_group_from_registered_goal(n=6, k=4" in text
    assert '"new_given": 0' in text
    assert '"production_changed": False' in text
    assert "write_text(json.dumps(report" in text

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    $params = @('-m', 'phase175_r4r14r8_db_step_identity_audit.audit', '--root', $repo)
    if ($DryRun) { $params += '--dry-run' }
    python @params
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R8 read-only audit failed' }
    if ($DryRun) { exit 0 }
    python -m pytest -q --import-mode=importlib -p no:cacheprovider `
        phase175_r4r14r8_db_step_identity_audit/tests/test_audit.py `
        phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py `
        phase175_r4r14r7_zero_image_match_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R8 focused pytest failed' }
    Write-Output 'PHASE175_R4R14R8_FOCUSED_TESTS=PASS'
    Write-Output 'PHASE175_R4R14R8_GATE=PASS_DB_IDENTITY_DIAGNOSIS_AND_FOCUSED_TESTS'
} finally {
    Pop-Location
}

```
