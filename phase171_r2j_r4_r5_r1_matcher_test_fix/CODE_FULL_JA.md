# Phase 171 R2J-R4-R5-R1 — 新規コード・変更テスト全文

対象変更は `phase171_r2j_r4_r5_short_exact_sequence/tests/test_audit.py` のテスト1関数と `CODE_FULL_JA.md` の全文更新のみです。import の変更はありません。元の R4-R5 コード全文は `assets/CODE_FULL_JA.md` に収録しています。

## 修正後 `tests/test_audit.py` 全文

```python
"""Focused typed EHP short-exact rule and real provenance regression tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r2j_r4_r5_short_exact_sequence.audit import (
    _cited_prop42_source,
    _git,
    build_short_exact_proof,
)
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    EHPShortExactSequence,
    ehp_short_exact_rule,
    expand_ehp_short_exact,
    short_exact_from_ehp,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _premises():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    injection = MapInjective(TodaSuspensionMap(a, b))
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a, b, c, EHP_E_MAP, EHP_H_MAP,
    ))
    projection = MapSurjective(TodaHopfInvariantMap(b, c))
    return injection, exact, projection


def test_valid_ehp_window_and_maps_propose_one_short_exact_inference():
    inputs = _premises()
    assert prop42_exactness_indices(inputs[1]) == (2, 6, "e_h")
    goal = short_exact_from_ehp(*inputs)
    assert isinstance(goal, EHPShortExactSequence)
    assert goal.source_group == TodaPrimaryGroup(5, 2)
    assert goal.middle_group == TodaPrimaryGroup(6, 3)
    assert goal.target_group == TodaPrimaryGroup(6, 5)
    proposals = expand_ehp_short_exact(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == inputs


def test_rule_produces_checked_inference_from_three_inferred_steps():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    rules = ehp_short_exact_rule(goal)
    premises = tuple(ProofStep(value, (), ProofRule.INFERENCE) for value in inputs)
    matches = find_inference_matches_for_rule(rules, premises)
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == premises


def test_given_exactness_or_map_properties_are_not_admitted_as_inference():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    rule = ehp_short_exact_rule(goal)
    for index in range(3):
        steps = tuple(ProofStep(
            statement, (), ProofRule.GIVEN if position == index else ProofRule.INFERENCE,
        ) for position, statement in enumerate(inputs))
        assert find_inference_matches_for_rule(rule, steps) == ()


def test_wrong_suspension_or_hopf_endpoints_fail_closed():
    injection, exact, projection = _premises()
    wrong_e = replace(injection, map=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    wrong_h = replace(projection, map=TodaHopfInvariantMap(
        TodaPrimaryGroup(6, 4), TodaPrimaryGroup(6, 5),
    ))
    assert short_exact_from_ehp(wrong_e, exact, projection) is None
    assert short_exact_from_ehp(injection, exact, wrong_h) is None


def test_invalid_exactness_or_wrong_ehp_map_names_fail_closed():
    injection, exact, projection = _premises()
    wrong = replace(exact, window=replace(
        exact.window, first_map=EHP_DELTA_MAP,
    ))
    assert short_exact_from_ehp(injection, wrong, projection) is None
    bad_group = replace(exact, window=replace(
        exact.window, target_term=TodaPrimaryGroup(7, 5),
    ))
    assert short_exact_from_ehp(injection, bad_group, projection) is None
    assert short_exact_from_ehp(injection, exact, object()) is None


def test_unrelated_sequence_is_rejected_and_reordered_premises_are_matched():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    incorrect = replace(goal, middle_group=TodaPrimaryGroup(7, 3))
    assert expand_ehp_short_exact(incorrect) == ()

    rule = ehp_short_exact_rule(goal)
    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE) for item in inputs)
    reordered = (steps[2], steps[1], steps[0])
    matches = find_inference_matches_for_rule(rule, reordered)
    assert len(matches) == 1
    assert matches[0].premises == steps
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == steps

    wrong_injection = ProofStep(
        MapInjective(TodaSuspensionMap(
            TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
        )),
        (),
        ProofRule.INFERENCE,
    )
    assert find_inference_matches_for_rule(
        rule, (steps[2], steps[1], wrong_injection),
    ) == ()
    assert expand_ehp_short_exact(object()) == ()


def test_real_proposition42_source_is_screened_and_unique():
    screened, _, citing = _screened_context()
    link = _cited_prop42_source(screened, citing)
    assert link.step.rule is ProofRule.GIVEN
    assert not link.step.premises
    assert link.assertion_id.endswith("adopted:assertion:prop42:general")


def test_read_only_git_guard():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_real_short_exact_proof_has_full_inferred_parentage():
    root, nodes, report = build_short_exact_proof()
    assert root.rule is ProofRule.INFERENCE
    assert len(root.premises) == 3
    assert all(parent.rule is ProofRule.INFERENCE for parent in root.premises)
    assert report["status"] == "INFERRED"
    assert report["new_given_added"] == 0
    assert report["order_four_proven"] is False
    assert report["pi63_group_proven"] is False
    assert report["given_leaves"] >= 3
    assert sum(node.rule is ProofRule.INFERENCE for node in nodes) >= 3
```

## 新規 `install.py` 全文

```python
"""Guarded read-only preflight and one-test-function fix for R2J-R4-R5.

The installer refuses unrelated local edits and modifies only the two
explicitly listed, known baseline files inside the existing audit package.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET_PACKAGE = ROOT / "phase171_r2j_r4_r5_short_exact_sequence"
TARGETS = (
    (
        TARGET_PACKAGE / "tests" / "test_audit.py",
        HERE / "assets" / "test_audit.py",
        "d1d4419054ecbfa015045833c768c8ccda5fcbc7565dfc21435a58aa516a98d9",
        "56d1b18d3ceb5ba430a07fbd700a43aa09cb788ba6dbd5d5f73a7dc3a780b257",
    ),
    (
        TARGET_PACKAGE / "CODE_FULL_JA.md",
        HERE / "assets" / "CODE_FULL_JA.md",
        "9945b629e86ad0764d2598a4ff3ab3cec6e6935945b3ea629b633d91e2b50cb1",
        "f01feab468bc127a8a7275a04f025e4ac5ddba3f89330f889a28672dad4b9b87",
    ),
)


def _digest(content: bytes) -> str:
    return sha256(content).hexdigest()


def preflight() -> tuple:
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R4-R5-R1 requires the develop branch")
    print("PHASE171_R2J_R4_R5_R1_BRANCH=" + branch, flush=True)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    print("PHASE171_R2J_R4_R5_R1_HEAD=" + head, flush=True)
    planned = []
    for target, replacement, old_hash, new_hash in TARGETS:
        if not target.is_file() or not replacement.is_file():
            raise RuntimeError("required local file absent: " + str(target))
        current = target.read_bytes()
        payload = replacement.read_bytes()
        if _digest(payload) != new_hash:
            raise RuntimeError("fix asset integrity mismatch: " + str(replacement))
        current_hash = _digest(current)
        if current_hash not in (old_hash, new_hash):
            raise RuntimeError("unrecognized local modification; refusing overwrite: " + str(target))
        planned.append((target, payload, current_hash != new_hash))
    return tuple(planned)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    plan = preflight()
    print("PHASE171_R2J_R4_R5_R1_TARGETS=" + str(len(plan)), flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R5_R1_RESULT=PASS_DRY_RUN", flush=True)
        return
    for target, payload, changed in plan:
        if changed:
            target.write_bytes(payload)
            print("PHASE171_R2J_R4_R5_R1_PATCHED=" + str(target), flush=True)
    if any(target.read_bytes() != payload for target, payload, _ in plan):
        raise RuntimeError("fix file verification failed")
    print("PHASE171_R2J_R4_R5_R1_PATCH=PASS", flush=True)


if __name__ == "__main__":
    main()
```

## 新規 `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Installer = Join-Path $PSScriptRoot "install.py"
$OriginalRunner = Join-Path $Repo "phase171_r2j_r4_r5_short_exact_sequence\run.ps1"
Push-Location $Repo
try {
    if (-not (Test-Path $OriginalRunner)) {
        throw "The existing R4-R5 package run.ps1 is required"
    }
    if ($DryRun) {
        python -B $Installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R4-R5-R1 guard preflight failed" }
        powershell -NoProfile -ExecutionPolicy Bypass -File $OriginalRunner -DryRun
        if ($LASTEXITCODE -ne 0) { throw "R4-R5 original dry-run failed" }
        Write-Output "PHASE171_R2J_R4_R5_R1_RESULT=PASS_DRY_RUN"
    }
    else {
        python -B $Installer
        if ($LASTEXITCODE -ne 0) { throw "R4-R5-R1 guarded patch failed" }
        powershell -NoProfile -ExecutionPolicy Bypass -File $OriginalRunner
        if ($LASTEXITCODE -ne 0) { throw "R4-R5 focused pytest or proof replay failed" }
        Write-Output "PHASE171_R2J_R4_R5_R1_RESULT=PASS"
    }
}
finally {
    Pop-Location
}
```

