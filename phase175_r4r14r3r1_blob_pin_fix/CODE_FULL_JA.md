# R4R14R3R1 監査コード全文

## audit.py（修正済み全文）

```python
"""Phase 175 R4R14R3: read-only binary composition / zero relation audit.

This module does not modify shared rules, source assertions, or the renderer.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

SOURCE_BLOBS = {
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase173_r4_r15r3_formal_suspension_bridge/bridge.py": "3850d5747932a13558ed647745d3c85e1883d421",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
}

def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + " " + result.stderr.strip())
    return result.stdout.strip()


def source_guard(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("EXPECTED_DEVELOP")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_NEED_REVIEW")
    for path, expected in SOURCE_BLOBS.items():
        if not (root / path).is_file():
            raise RuntimeError("SOURCE_FILE_MISSING: " + path)
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("PINNED_COMMIT_BLOB_CHANGED: " + path)
        if git(root, "hash-object", path) != expected:
            raise RuntimeError("PINNED_WORKTREE_BLOB_CHANGED: " + path)
    return {"head": git(root, "rev-parse", "HEAD"), "source_blobs": SOURCE_BLOBS}


def inspect_live() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import canonical_annihilator_instance
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        lifted_stable_composition, left_associated, expand_source_bound_zero_image_chain,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import composite_zero_generator_inputs
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider,
    )
    from phase173_r4_r15r3_formal_suspension_bridge.bridge import canonical_formal_suspension
    from proof import ProofRule, Relation, RelationType

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    laws = tuple(link.step.conclusion for link in screened.proof_links
                 if link.step is not None and link.step.rule is ProofRule.GIVEN
                 and type(link.step.conclusion) is CitedFamilyAnnihilator)
    if len(laws) != 1:
        raise RuntimeError("TODA59_SOURCE_COUNT_NOT_ONE")
    law = laws[0]
    annihilator = canonical_annihilator_instance(law, 6)
    prior = exact_prior_database_result(5, 4)
    if prior is None or not hasattr(prior.rhs, "generator"):
        raise RuntimeError("PRIOR_GROUP_PRESENTATION_UNAVAILABLE")
    generator = prior.rhs.generator
    if type(generator) is not Composition:
        raise RuntimeError("EXPECTED_BINARY_COMPOSITION_GENERATOR")
    mapping = TodaSuspensionMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6))
    lifted = lifted_stable_composition(generator)
    if type(lifted) is not Composition:
        raise RuntimeError("STABLE_COMPOSITE_LIFT_MISSING")
    composite_image = GeneratorImage(mapping, generator, lifted)
    zero_image = GeneratorImage(mapping, generator, Zero())
    image_zero = ImageZeroStatement(mapping)
    factor_goals = component_image_obligations(composite_image)
    if factor_goals is None or len(factor_goals) != 2:
        raise RuntimeError("BINARY_SUSPENSION_RULE_NOT_AVAILABLE")
    if canonical_formal_suspension(generator) is None:
        raise RuntimeError("FORMAL_BINARY_SUSPENSION_UNAVAILABLE")
    # Compare Toda's zero *whole composition* with R7's zero *left factor*.
    r7_requirements = composite_zero_generator_inputs(zero_image, composite_image)
    if r7_requirements is None:
        raise RuntimeError("R7_RULE_INPUTS_UNAVAILABLE")
    r7_zero_relation = r7_requirements[1]
    direct_zero_relation = Relation(lifted, Zero(), RelationType.EQUALITY)
    if direct_zero_relation != annihilator:
        raise RuntimeError("TODA59_INSTANCE_DOES_NOT_MATCH_LIFTED_COMPOSITE")
    shared = shared_expansion_provider(screened, proof_target=root)
    options = tuple(shared(zero_image))
    r38 = expand_source_bound_zero_image_chain(zero_image, laws)
    r41 = build_public_adopted_zero_image_provider(bridge=screened, proof_target=root)
    r41_options = tuple(r41(image_zero))
    return {
        "root": "pi_10^6", "prior": "pi_9^5",
        "cited_toda59_source_count": len(laws),
        "binary_lift_exists": True,
        "binary_factor_proof_goals": len(factor_goals),
        "direct_toda59_zero_is_whole_composite": direct_zero_relation == annihilator,
        "r7_requires_left_factor_zero": r7_zero_relation.lhs == lifted.left,
        "r7_requirement_matches_toda59": r7_zero_relation == annihilator,
        "r38_generator_zero_proposals": [x.rule.name for x in r38],
        "shared_generator_zero_proposals": [x.rule.name for x in options],
        "r41_image_zero_proposals": [x.rule.name for x in r41_options],
        "left_associated_available": left_associated(lifted) is not None,
        "conclusion": "BINARY_COMPOSITION_ZERO_PROPAGATION_GAP" if
            (r7_zero_relation != annihilator and not r38 and not options) else "RECHECK_REQUIRED",
        "new_given": 0, "new_rules": 0,
    }


def run(root: Path, dry_run: bool = False) -> int:
    report = {"phase": "175_R4R14R3", "mode": "READ_ONLY_BINARY_RULE_AUDIT",
              "gate": "FAIL_R4R14R3", "full_pytest": False,
              "new_given": 0, "new_rules": 0}
    try:
        report["source_guard"] = source_guard(root)
        if dry_run:
            report["gate"] = "PASS_R4R14R3_DRYRUN_SOURCE_GUARD"
        else:
            row = inspect_live()
            report["observed"] = row
            if row["conclusion"] != "BINARY_COMPOSITION_ZERO_PROPAGATION_GAP":
                raise RuntimeError("UNEXPECTED_RULE_FRONTIER: " + row["conclusion"])
            if not row["r41_image_zero_proposals"]:
                raise RuntimeError("PREEXISTING_R41_IMAGE_ZERO_PATH_MISSING")
            report["gate"] = "PASS_R4R14R3_BINARY_RULE_GAP_AUDITED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
    output = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R3_binary_rule_audit.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R4R14R3_GATE=" + str(report["gate"]))
    print("PHASE175_R4R14R3_REPORT=" + str(output))
    if "error" in report:
        print("PHASE175_R4R14R3_ERROR=" + report["error"])
        return 1
    if not dry_run:
        row = report["observed"]
        for key in ("binary_factor_proof_goals", "direct_toda59_zero_is_whole_composite",
                    "r7_requires_left_factor_zero", "r7_requirement_matches_toda59",
                    "shared_generator_zero_proposals", "r41_image_zero_proposals", "conclusion"):
            print("PHASE175_R4R14R3_" + key.upper() + "=" + str(row[key]))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

## run.ps1（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $repo '.git'))) { throw 'Run from ehp_proof repository root' }
$source = Join-Path $PSScriptRoot 'audit.py'
$targetDir = Join-Path $repo 'phase175_r4r14r3_binary_composition_audit'
$target = Join-Path $targetDir 'audit.py'
if (-not (Test-Path $target)) { throw 'Extract R4R14R3_binary_composition_audit.zip first' }
$old = 'd98a7b45e08cd3b07c16e3f38e0a558ccebfc9b67a'
$new = 'd98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6'
$existing = [System.IO.File]::ReadAllText($target)
$expected = [System.IO.File]::ReadAllText($source)
if ($existing -ne $expected) {
    if (-not $existing.Contains($old)) { throw 'Unexpected audit script; refusing replacement' }
    if ($existing.Replace($old, $new) -ne $expected) { throw 'Changes beyond reviewed SHA correction; refusing replacement' }
    [System.IO.File]::WriteAllText($target, $expected, (New-Object System.Text.UTF8Encoding($false)))
}
$script = Join-Path $targetDir 'run.ps1'
if ($DryRun) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
} else {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $script
}
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3R1 delegated audit failed' }
if ($DryRun) { Write-Output 'PHASE175_R4R14R3R1_GATE=PASS_DRYRUN_PIN_CORRECTED' }
else { Write-Output 'PHASE175_R4R14R3R1_GATE=PASS_FOCUSED_AUDIT_PIN_CORRECTED' }

```
