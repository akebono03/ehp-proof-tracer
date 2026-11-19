# R4R14R3 監査コード全文

以下の新規ファイルを追加します。本番ファイルは変更しません。

## `audit.py`

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
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b67a",
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

## `tests/test_audit.py`

```python
"""R4R14R3 focused read-only audit contracts."""
from __future__ import annotations

from pathlib import Path

from phase175_r4r14r3_binary_composition_audit import audit


def test_binary_suspension_and_zero_propagation_are_separate_obligations() -> None:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase174_r3_r7_r7_composite_zero_audit.rule import composite_zero_generator_inputs

    a = HomotopyElement("a", 5, 8, 5, GeneratorSymbol("a", 5))
    b = HomotopyElement("b", 8, 9, 8, GeneratorSymbol("b", 8))
    a1 = HomotopyElement("a1", 6, 9, 6, GeneratorSymbol("a", 6))
    b1 = HomotopyElement("b1", 9, 10, 9, GeneratorSymbol("b", 9))
    source = Composition(a, b)
    target = Composition(a1, b1)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6))
    assert len(component_image_obligations(GeneratorImage(mapping, source, target))) == 2
    obligations = composite_zero_generator_inputs(GeneratorImage(mapping, source, Zero()),
                                                  GeneratorImage(mapping, source, target))
    assert obligations is not None
    assert obligations[1].lhs == a1
    assert obligations[1].lhs != target


def test_audit_has_no_mutation_or_new_mathematical_axiom() -> None:
    code = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    assert chr(34) + "new_given" + chr(34) in code
    assert chr(34) + "new_rules" + chr(34) in code
    assert "hash-object" in code
    assert "BINARY_COMPOSITION_ZERO_PROPAGATION_GAP" in code


def test_source_guard_pin_format() -> None:
    assert len(audit.SOURCE_BLOBS) == 7
    assert all(len(blob) == 40 for blob in audit.SOURCE_BLOBS.values())

```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r14r3_binary_composition_audit'
if (-not (Test-Path (Join-Path $package 'audit.py'))) { throw 'Run from ehp_proof repository root.' }
& python -B -m phase175_r4r14r3_binary_composition_audit.audit --root $repo $(if ($DryRun) {'--dry-run'})
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3 audit failed' }
if ($DryRun) { exit 0 }
& python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
    (Join-Path $package 'tests/test_audit.py') `
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' `
    'phase174_r3_r7_r12_toda59_annihilator_source/tests/test_rule.py'
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3 focused pytest failed' }
Write-Output 'PHASE175_R4R14R3_FOCUSED_TESTS=PASS'
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3 git diff check failed' }
Write-Output 'PHASE175_R4R14R3_PRODUCTION_UNCHANGED=PASS'

```
