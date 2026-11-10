# Phase 174 R59 — 新規コード全文

監査は既存コードを一切変更しません。以下はすべて新規追加ファイルです。

## audit.py（新規ディレクトリ配下に配置）

```python
"""Phase 174 R59: audit Toda (5.10)'s exact printed sign and typed signed witness.

Read only. A signed image of the unique nonzero element of Z/2 is the exact
same element. This observation must not be extended to a general Z/m codomain.
No inference rule, source assertion, ProofStep, or public narrative is created.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r59_toda510_signed_semantics_audit"
REVIEWED_DEVELOP_HEAD = "82d725d8649cd6307c2abd67024e3ef4f3cddfe2"
PINS = {
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py":
        "b90fe1fee5db04228ed986083b5214709045a7ea",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py":
        "01d200cd7fd8698cb34ac02fdffe1b01c6879d10",
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py":
        "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py":
        "67c3a78501bfb8b6be6a8a788e82a0927ece61d7",
}


def git_blob_sha(content: bytes) -> str:
    """Calculate a Git object ID for the exact supplied bytes."""
    header = b"blob " + str(len(content)).encode("ascii") + b"\x00"
    return sha1(header + content).hexdigest()


def signed_generator_is_identical(order: int, sign: int) -> bool:
    """Check whether +/- one generator coincide in Z/order, without proofs."""
    if type(order) is not int or order < 1:
        raise ValueError("order must be a positive integer")
    if type(sign) is not int or sign not in (-1, 1):
        raise ValueError("sign must be -1 or +1")
    return sign % order == 1 % order


def checked_git_files(root: Path) -> tuple[str, ...]:
    """Fail closed on changed R34/R35 source code or their reviewed tests."""
    verified: list[str] = []
    for relative, expected in PINS.items():
        path = root / relative
        data = path.read_bytes()
        normalized = data.replace(b"\r\n", b"\n")
        accepted = (
            git_blob_sha(data),
            git_blob_sha(normalized),
            git_blob_sha(normalized.replace(b"\n", b"\r\n")),
        )
        if expected not in accepted:
            raise RuntimeError("R59_SOURCE_GUARD_FAILED: " + relative)
        verified.append(relative)
    return tuple(verified)


def local_git_snapshot(root: Path) -> dict[str, str]:
    """Report local Git state without confusing it with the reviewed remote HEAD."""
    result: dict[str, str] = {}
    for label, arguments in (
        ("local_head", ("rev-parse", "HEAD")),
        ("local_status", ("status", "--short")),
    ):
        process = subprocess.run(
            ["git", *arguments], cwd=root, text=True,
            capture_output=True, check=False,
        )
        result[label] = process.stdout.strip() if process.returncode == 0 else "UNAVAILABLE"
    return result


def inspect_semantics(root: Path) -> dict[str, object]:
    """Check pinned printed equation, source citation, and R35's actual inputs."""
    from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring import source
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
        conditional_inputs, cyclic_delta_kernel_rule,
    )
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    verified = checked_git_files(root)
    printed = source.pinned_source_text(root)
    eq_start = printed.index(source.EQ510)
    eq_end = printed.index(r"\end{equation}", eq_start)
    displayed_equation = printed[eq_start:eq_end]
    if (displayed_equation.count(source.IMAGE_CLAUSE) != 1
            or r"\pm" in displayed_equation):
        raise RuntimeError("R59 source equation is not the exact sign-free (5.10)")

    group, image = source.checked_prior_statements(root)
    if (type(group) is not Relation
            or group.relation_type is not RelationType.EQUALITY
            or type(group.rhs) is not FiniteCyclicGroup
            or group.rhs.order != 2
            or type(image) is not TodaDeltaImageUpToSignStatement
            or image.positive_value != group.rhs.generator
            or image.map.target_group != group.lhs):
        raise RuntimeError("R59 source/group/signed-image structural mismatch")
    if not signed_generator_is_identical(2, -1):
        raise RuntimeError("R59 arithmetic sign check failed for the actual order two")
    if signed_generator_is_identical(3, -1):
        raise RuntimeError("R59 sign equality incorrectly generalized to order three")

    domain = Relation(
        image.map.source_group, FreeCyclicGroup(image.element),
        RelationType.EQUALITY,
    )
    goal = KernelMultipleStatement(
        image.map, image.map.source_group, image.element, 2,
    )
    actual_inputs = conditional_inputs(goal, domain, group, image)
    if actual_inputs != (domain, group, image):
        raise RuntimeError("R59 existing generic kernel rule no longer accepts exact inputs")
    rule = cyclic_delta_kernel_rule(goal, domain, group, image)
    if len(rule.premise_patterns) != 3:
        raise RuntimeError("R59 existing kernel rule antecedents changed")
    bridge = source.build_cited_lower_delta_sources(root)
    if len(bridge.proof_links) != 2:
        raise RuntimeError("R59 changed the count of cited source givens")
    for link in bridge.proof_links:
        if link.step.rule is not ProofRule.GIVEN or link.step.premises:
            raise RuntimeError("R59 unexpected source step type")
    references = tuple(
        bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).locator
        for link in bridge.proof_links
    )
    if references != ("Proposition 5.8", "(5.10)"):
        raise RuntimeError("R59 original sources or order changed")

    return {
        "source_guard": "PASS",
        "source_pins": len(verified),
        "toda_source_checked": True,
        "printed_equation_sign_free": True,
        "typed_image_remains_up_to_sign": True,
        "actual_codomain_generator_order": 2,
        "positive_equals_negative_in_actual_codomain": True,
        "no_general_sign_elimination": True,
        "existing_kernel_rule_premises": 3,
        "source_reference_locators": list(references),
        "source_given_count": 2,
        "production_changes": 0,
        "new_mathematical_rules": 0,
        "new_given": 0,
        "semantic_conclusion": (
            "Equivalent only under the independently cited Z/2 group presentation. "
            "The standalone up-to-sign type remains weaker than an exact equation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = inspect_semantics(root)
    result["reviewed_develop_head"] = REVIEWED_DEVELOP_HEAD
    result.update(local_git_snapshot(root))
    for key, value in result.items():
        if key not in ("local_status", "semantic_conclusion"):
            print("PHASE174_R59_" + key.upper() + "=" + str(value))
    if args.dry_run:
        print("PHASE174_R59_GATE=PASS_R59_READ_ONLY_DRYRUN")
        print("(END)")
        return 0

    from phase174_r3_r7_r57_narrative_source_cleanup.audit import inspect_public
    public = inspect_public()
    if not (public["pi11_6_complete"] and public["pi12_7_complete"]
            and public["pi11_6_hopf_delta_cited"]
            and public["pi12_7_prop27_absent"]):
        raise RuntimeError("R59 existing public proof regression failed")
    result["r57_public_proof_reverified"] = True
    result["r57_pi11_reference_count"] = public["pi11_reference_count"]
    result["r57_pi12_reference_count"] = public["pi12_reference_count"]
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    output = base / "EHPProofTracerAudit" / PACKAGE / "report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R59_R57_PUBLIC_PROOF_REVERIFIED=True")
    print("PHASE174_R59_REPORT=" + str(output))
    print("PHASE174_R59_GATE=PASS_R59_CITED_ORDER2_SEMANTICS_AND_PUBLIC")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_audit.py（新規ディレクトリ配下に配置）

```python
"""R59 focused, read-only source and conditional-sign audit."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r59_toda510_signed_semantics_audit.audit import (
    checked_git_files, inspect_semantics, signed_generator_is_identical,
)
from pathlib import Path


@pytest.mark.parametrize("sign", (-1, 1))
def test_toda510_order_two_identifies_both_signs(sign: int) -> None:
    assert signed_generator_is_identical(2, sign)


@pytest.mark.parametrize("order", (3, 4, 5, 8))
def test_not_a_general_sign_elimination(order: int) -> None:
    assert not signed_generator_is_identical(order, -1)


@pytest.mark.parametrize("order,sign", ((0, 1), (-2, 1), (2, 0), (2, 2)))
def test_invalid_signed_generator_parameters_rejected(order: int, sign: int) -> None:
    with pytest.raises(ValueError):
        signed_generator_is_identical(order, sign)


def test_existing_source_and_test_blobs_still_pinned() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(checked_git_files(root)) == 4


def test_real_toda_source_and_r35_premises_remain_coherent() -> None:
    root = Path(__file__).resolve().parents[2]
    report = inspect_semantics(root)
    assert report["printed_equation_sign_free"]
    assert report["actual_codomain_generator_order"] == 2
    assert report["positive_equals_negative_in_actual_codomain"]
    assert report["typed_image_remains_up_to_sign"]
    assert report["existing_kernel_rule_premises"] == 3
    assert report["source_given_count"] == 2
    assert report["source_reference_locators"] == ["Proposition 5.8", "(5.10)"]
    assert report["production_changes"] == 0
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
```

## run.ps1（新規ディレクトリ配下に配置）

```powershell
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r59_toda510_signed_semantics_audit.audit'
    if ($DryRun) {
        python -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R59 DryRun Source Guard failed' }
        exit 0
    }

    python -m $module
    if ($LASTEXITCODE -ne 0) { throw 'R59 cited semantic/public audit failed' }

    python -m pytest -q -o addopts= --import-mode=importlib `
        'phase174_r3_r7_r59_toda510_signed_semantics_audit/tests/test_audit.py' `
        'phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py' `
        'phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'
    if ($LASTEXITCODE -ne 0) { throw 'R59 focused pytest failed' }

    Write-Output 'PHASE174_R59_GATE=PASS_R59_FOCUSED_AND_PUBLIC'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
```

