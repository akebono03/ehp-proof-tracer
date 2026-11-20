# Phase 176 R3R27R1R1 コード全文

## 修正対象のテスト関数全体と必要な import

```python
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition, canonical_member
from phase176_r3r27r1_toda55_quadruple_isolated.source import Toda55UniversalQuadrupleStatement, canonical_quadruple_goal, cited_quadruple_rule
from proof import InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule

def test_only_independently_inferred_family_member_can_close() -> None:
    goal = canonical_quadruple_goal(5)
    rule = cited_quadruple_rule(goal)
    family = CitedStableFamilyDefinition(4, 4, 3)
    member = canonical_member(family, 5)
    premise = ProofStep(member, (), ProofRule.INFERENCE,
                        inference_rule=InferenceRule(name="test independent family member"))
    cited = ProofStep(Toda55UniversalQuadrupleStatement(), (), ProofRule.GIVEN)
    eta = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(rule, (premise, cited, eta))
    assert len(matches) == 1
    assert find_inference_matches_for_rule(rule, (
        ProofStep(member, (), ProofRule.GIVEN), cited, eta)) == ()
    assert find_inference_matches_for_rule(rule, (premise, cited)) == ()
    reordered = find_inference_matches_for_rule(rule, (premise, eta, cited))
    assert len(reordered) == 1
    assert reordered[0].premises == (premise, cited, eta)
```

## 新規 install.py（全文）

```python
"""Fail-closed test-only patch for Phase 176 R3R27R1."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase176_r3r27r1_toda55_quadruple_isolated" / "tests" / "test_source.py"
PAYLOAD = PACKAGE / "test_source_FULL.py"
OLD = "    assert find_inference_matches_for_rule(rule, (premise, eta, cited)) == ()"
NEW = (
    "    reordered = find_inference_matches_for_rule(rule, (premise, eta, cited))\n"
    "    assert len(reordered) == 1\n"
    "    assert reordered[0].premises == (premise, cited, eta)"
)


def apply(dry_run: bool) -> int:
    if not TARGET.is_file():
        raise RuntimeError("R3R27R1_TEST_FILE_MISSING")
    baseline = TARGET.read_text(encoding="utf-8")
    intended = PAYLOAD.read_text(encoding="utf-8")
    if baseline == intended:
        print("PHASE176_R3R27R1R1_GATE=PASS_ALREADY_PATCHED")
        return 0
    if baseline.count(OLD) != 1:
        raise RuntimeError("BASELINE_ASSERTION_NOT_UNIQUE")
    if baseline.replace(OLD, NEW) != intended:
        raise RuntimeError("TEST_BASELINE_DIFFERS_FROM_REVIEWED_SOURCE")
    if not dry_run:
        with TARGET.open("w", encoding="utf-8", newline="") as output:
            output.write(intended)
    print("PHASE176_R3R27R1R1_GATE=" +
          ("PASS_DRYRUN" if dry_run else "PASS_TEST_EXPECTATION_FIXED"))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return apply(args.dry_run)
    except (OSError, RuntimeError) as error:
        print("PHASE176_R3R27R1R1_GATE=FAIL")
        print("PHASE176_R3R27R1R1_ERROR=" + str(error))
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

## 新規 run.ps1（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r27r1r1_premise_order_test_fix.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1R1 DryRun failed' }
        Write-Host 'PHASE176_R3R27R1R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    } else {
        python -B -m phase176_r3r27r1r1_premise_order_test_fix.install
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1R1 installation failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests `
            .\phase174_r3_r6_source_extension\tests\test_source.py `
            .\phase171_r2e_toda53_double_source\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1R1 focused pytest failed' }
        Write-Host 'PHASE176_R3R27R1R1_GATE=PASS_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R27R1R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```

## 置換後の test_source.py（全文）

```python
"""Focused source and guarded inference contracts for the second Toda (5.5) clause."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, Multiple, Zero
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, canonical_member,
)
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    build_cited_toda55_quadruple_source,
    canonical_quadruple_goal,
    cited_quadruple_rule,
    expand_cited_quadruple,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def available_sources():
    return (
        Toda55UniversalQuadrupleStatement(),
        CitedStableFamilyDefinition(4, 4, 3),
        TodaEtaFamilyGeneralDefinition(),
    )


def test_source_adopts_only_second_clause() -> None:
    bridge = build_cited_toda55_quadruple_source()
    assert len(bridge.proof_links) == 1
    step = bridge.proof_links[0].step
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == Toda55UniversalQuadrupleStatement()
    assertion = bridge.registry.assertion(bridge.proof_links[0].assertion_id)
    assert assertion.content == step.conclusion
    assert bridge.registry.reference(assertion.reference_id).publication_position == 8600


@pytest.mark.parametrize("n", (5, 6, 12))
def test_canonical_nu_quadruple_goal_is_typed(n: int) -> None:
    goal = canonical_quadruple_goal(n)
    assert isinstance(goal, Relation)
    assert goal.relation_type is RelationType.EQUALITY
    assert goal.lhs.coefficient == 4
    assert goal.lhs.expression.dimension == n
    assert isinstance(goal.rhs, Composition)
    assert tuple(x.generator.index for x in
                 (goal.rhs.left, goal.rhs.right.left, goal.rhs.right.right)) == (n, n + 1, n + 2)
    assert len(expand_cited_quadruple(goal, available_sources())) == 1


def test_unsupported_indices_and_sources_fail_closed() -> None:
    assert canonical_quadruple_goal(4) is None
    assert canonical_quadruple_goal(True) is None
    goal = canonical_quadruple_goal(5)
    assert expand_cited_quadruple(goal, ()) == ()
    assert expand_cited_quadruple(goal, available_sources()[:-1]) == ()
    assert expand_cited_quadruple(goal, available_sources() + (available_sources()[0],)) == ()
    assert expand_cited_quadruple(replace(goal, rhs=Zero()), available_sources()) == ()
    assert expand_cited_quadruple(Relation(Multiple(2, goal.lhs.expression), goal.rhs,
                                           RelationType.EQUALITY), available_sources()) == ()


def test_only_independently_inferred_family_member_can_close() -> None:
    goal = canonical_quadruple_goal(5)
    rule = cited_quadruple_rule(goal)
    family = CitedStableFamilyDefinition(4, 4, 3)
    member = canonical_member(family, 5)
    premise = ProofStep(member, (), ProofRule.INFERENCE,
                        inference_rule=InferenceRule(name="test independent family member"))
    cited = ProofStep(Toda55UniversalQuadrupleStatement(), (), ProofRule.GIVEN)
    eta = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(rule, (premise, cited, eta))
    assert len(matches) == 1
    assert find_inference_matches_for_rule(rule, (
        ProofStep(member, (), ProofRule.GIVEN), cited, eta)) == ()
    assert find_inference_matches_for_rule(rule, (premise, cited)) == ()
    reordered = find_inference_matches_for_rule(rule, (premise, eta, cited))
    assert len(reordered) == 1
    assert reordered[0].premises == (premise, cited, eta)
```
