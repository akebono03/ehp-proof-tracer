# R40R1 差し替え可能なコード全文

対象ファイル：`phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py`。変更対象関数：`test_direct_given_for_generator_zero_is_rejected()`。変更後のテストファイルはすべての import と全テスト関数を含む。

## 変更後のテストファイル全文 (replacement/test_rule.py)

```python
"""Focused real-adoption and fail-closed inference-contract tests for R40."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, exact_prior_database_result
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
    RULE_NAME, adopted_prior_zero_image_rule, expand_adopted_prior_zero_image,
    verified_prior_zero_image_inputs,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from homotopy_groups import FiniteCyclicGroup


def fixture():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    relation = exact_prior_database_result(5, 5)
    assert type(relation) is Relation
    assert relation.lhs == TodaPrimaryGroup(10, 5)
    delta = TodaSuspensionMap(relation.lhs, TodaPrimaryGroup(11, 6))
    goal = ImageZeroStatement(delta)
    db = admitted_db_step(relation, proof_target=root, bridge=bridge)
    assert isinstance(db, ProofStep)
    zero = GeneratorImage(delta, relation.rhs.generator, Zero())
    independent = ProofStep(
        conclusion=zero, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independent generator-zero fixture"),
    )
    return root, bridge, relation, goal, db, independent


def test_adopted_earlier_db_and_inferred_zero_have_one_general_candidate():
    root, bridge, relation, goal, db, independent = fixture()
    assert verified_prior_zero_image_inputs(goal, relation, proof_target=root, bridge=bridge) == (
        relation, independent.conclusion,
    )
    result = expand_adopted_prior_zero_image(goal, relation, proof_target=root, bridge=bridge)
    assert len(result) == 1
    assert result[0].rule.name == RULE_NAME
    assert result[0].subgoals == (relation, independent.conclusion)
    assert all(not isinstance(item, ProofStep) for item in result[0].subgoals)
    matches = find_inference_matches_for_rule(result[0].rule, (db, independent))
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (db, independent)
    assert db.rule is ProofRule.GIVEN
    assert db.note == "ADOPTED_DATABASE_PRIOR; independent reference not asserted"


def test_historical_r6_does_not_accept_db_given_and_remains_unchanged():
    root, bridge, relation, goal, db, independent = fixture()
    old = expand_zero_image_from_cyclic_generator(goal, relation)
    assert len(old) == 1
    assert find_inference_matches_for_rule(old[0].rule, (db, independent)) == ()


def test_forged_db_step_with_different_source_identity_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(db, inference_rule=InferenceRule(name="test-only forged DB citation"))
    assert find_inference_matches_for_rule(rule, (forged, independent)) == ()
    forged_note = replace(db, note="CITED_TODA_SOURCE")
    assert find_inference_matches_for_rule(rule, (forged_note, independent)) == ()


def test_direct_given_for_generator_zero_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(independent, rule=ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (db, forged)) == ()
    assert find_inference_matches_for_rule(rule, (forged, db)) == ()
    assert find_inference_matches_for_rule(rule, (db,)) == ()

    # The matcher is premise-pattern based: valid input order is immaterial.
    matches = find_inference_matches_for_rule(rule, (independent, db))
    assert len(matches) == 1
    assert matches[0].premises == (db, independent)


def test_self_citing_or_prior_root_fails_strict_order():
    root, bridge, relation, goal, db, independent = fixture()
    wrong_root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 5))
    assert verified_prior_zero_image_inputs(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) is None
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) == ()
    with pytest.raises(ValueError, match="earlier adopted"):
        adopted_prior_zero_image_rule(
            goal, relation, proof_target=wrong_root, bridge=bridge,
        )


def test_non_database_presentation_and_wrong_order_are_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    other = Relation(relation.lhs, FiniteCyclicGroup(4, relation.rhs.generator), RelationType.EQUALITY)
    assert expand_adopted_prior_zero_image(
        goal, other, proof_target=root, bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target="untyped root", bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        "not a zero image", relation, proof_target=root, bridge=bridge,
    ) == ()


def test_cross_map_and_wrong_target_zero_fail():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    wrong_map = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(12, 7))
    altered = replace(independent, conclusion=GeneratorImage(
        wrong_map, relation.rhs.generator, Zero(),
    ))
    assert find_inference_matches_for_rule(rule, (db, altered)) == ()
    altered_two = replace(independent, conclusion=GeneratorImage(
        goal.map, relation.rhs.generator, "zero",
    ))
    assert find_inference_matches_for_rule(rule, (db, altered_two)) == ()


def test_rule_is_not_registered_by_constructing_it():
    root, bridge, relation, goal, db, independent = fixture()
    before = tuple(bridge.proof_links)
    options = expand_adopted_prior_zero_image(
        goal, relation, proof_target=root, bridge=bridge,
    )
    assert len(options) == 1
    assert bridge.proof_links == before
    assert all(link.step is None or link.step.conclusion != goal for link in before)
```

## 変更前のテストファイル全文 (baseline/test_rule.py)

```python
"""Focused real-adoption and fail-closed inference-contract tests for R40."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, exact_prior_database_result
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
    RULE_NAME, adopted_prior_zero_image_rule, expand_adopted_prior_zero_image,
    verified_prior_zero_image_inputs,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from homotopy_groups import FiniteCyclicGroup


def fixture():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    relation = exact_prior_database_result(5, 5)
    assert type(relation) is Relation
    assert relation.lhs == TodaPrimaryGroup(10, 5)
    delta = TodaSuspensionMap(relation.lhs, TodaPrimaryGroup(11, 6))
    goal = ImageZeroStatement(delta)
    db = admitted_db_step(relation, proof_target=root, bridge=bridge)
    assert isinstance(db, ProofStep)
    zero = GeneratorImage(delta, relation.rhs.generator, Zero())
    independent = ProofStep(
        conclusion=zero, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independent generator-zero fixture"),
    )
    return root, bridge, relation, goal, db, independent


def test_adopted_earlier_db_and_inferred_zero_have_one_general_candidate():
    root, bridge, relation, goal, db, independent = fixture()
    assert verified_prior_zero_image_inputs(goal, relation, proof_target=root, bridge=bridge) == (
        relation, independent.conclusion,
    )
    result = expand_adopted_prior_zero_image(goal, relation, proof_target=root, bridge=bridge)
    assert len(result) == 1
    assert result[0].rule.name == RULE_NAME
    assert result[0].subgoals == (relation, independent.conclusion)
    assert all(not isinstance(item, ProofStep) for item in result[0].subgoals)
    matches = find_inference_matches_for_rule(result[0].rule, (db, independent))
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (db, independent)
    assert db.rule is ProofRule.GIVEN
    assert db.note == "ADOPTED_DATABASE_PRIOR; independent reference not asserted"


def test_historical_r6_does_not_accept_db_given_and_remains_unchanged():
    root, bridge, relation, goal, db, independent = fixture()
    old = expand_zero_image_from_cyclic_generator(goal, relation)
    assert len(old) == 1
    assert find_inference_matches_for_rule(old[0].rule, (db, independent)) == ()


def test_forged_db_step_with_different_source_identity_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(db, inference_rule=InferenceRule(name="test-only forged DB citation"))
    assert find_inference_matches_for_rule(rule, (forged, independent)) == ()
    forged_note = replace(db, note="CITED_TODA_SOURCE")
    assert find_inference_matches_for_rule(rule, (forged_note, independent)) == ()


def test_direct_given_for_generator_zero_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(independent, rule=ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (db, forged)) == ()
    assert find_inference_matches_for_rule(rule, (independent, db)) == ()
    assert find_inference_matches_for_rule(rule, (db,)) == ()


def test_self_citing_or_prior_root_fails_strict_order():
    root, bridge, relation, goal, db, independent = fixture()
    wrong_root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 5))
    assert verified_prior_zero_image_inputs(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) is None
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) == ()
    with pytest.raises(ValueError, match="earlier adopted"):
        adopted_prior_zero_image_rule(
            goal, relation, proof_target=wrong_root, bridge=bridge,
        )


def test_non_database_presentation_and_wrong_order_are_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    other = Relation(relation.lhs, FiniteCyclicGroup(4, relation.rhs.generator), RelationType.EQUALITY)
    assert expand_adopted_prior_zero_image(
        goal, other, proof_target=root, bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target="untyped root", bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        "not a zero image", relation, proof_target=root, bridge=bridge,
    ) == ()


def test_cross_map_and_wrong_target_zero_fail():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    wrong_map = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(12, 7))
    altered = replace(independent, conclusion=GeneratorImage(
        wrong_map, relation.rhs.generator, Zero(),
    ))
    assert find_inference_matches_for_rule(rule, (db, altered)) == ()
    altered_two = replace(independent, conclusion=GeneratorImage(
        goal.map, relation.rhs.generator, "zero",
    ))
    assert find_inference_matches_for_rule(rule, (db, altered_two)) == ()


def test_rule_is_not_registered_by_constructing_it():
    root, bridge, relation, goal, db, independent = fixture()
    before = tuple(bridge.proof_links)
    options = expand_adopted_prior_zero_image(
        goal, relation, proof_target=root, bridge=bridge,
    )
    assert len(options) == 1
    assert bridge.proof_links == before
    assert all(link.step is None or link.step.conclusion != goal for link in before)
```

## R40R1 install.py 全文

```python
"""R40R1: correct one reviewed R40 test expectation without changing math."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r40_adopted_db_zero_image_isolated.source_guard import (
    verify_checkout,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py"
BASELINE = PACKAGE / "baseline/test_rule.py"
REPLACEMENT = PACKAGE / "replacement/test_rule.py"
REVIEWED_PINS = {
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py":
        "2df41f2787b76d8d35852c7de2300b90b5391cf9cadbc27b15bc62b122907a83",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/audit.py":
        "a838e53ca442a523c48a891a071b1860547d418e3c49476de545b6d84f13e0d5",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/source_guard.py":
        "60c4ab69bf70680a0585f7193962699eb28a53cc1a81949d8f9873cf289fa8d9",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/run.ps1":
        "e24f0464a285c00a24e4a510e5a59e7b1fb85f62e5ff421b23dea42631bfe397",
}
BASELINE_SHA256 = "1e7952be77c1569d211ed16f8e610c9e20183b5dc22a56d0fd4e46c2b1719f2a"
REPLACEMENT_SHA256 = "dabd332aa0cbf036e55e9aacfe992d2a87ef50db9e296780246d3c3d066d4cf8"


def normalized(data: bytes) -> bytes:
    """Ignore Windows CRLF differences, not mathematical or code changes."""
    return data.replace(b"\r\n", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(normalized(data)).hexdigest()


def verified_mode() -> str:
    """Require reviewed Git/source state and the exact old or new R40 test."""
    verify_checkout()
    for name, expected in REVIEWED_PINS.items():
        file = ROOT / name
        if not file.is_file() or digest(file.read_bytes()) != expected:
            raise RuntimeError("R40R1 reviewed source differs: " + name)
    if not BASELINE.is_file() or digest(BASELINE.read_bytes()) != BASELINE_SHA256:
        raise RuntimeError("R40R1 baseline test has changed")
    if not REPLACEMENT.is_file() or digest(REPLACEMENT.read_bytes()) != REPLACEMENT_SHA256:
        raise RuntimeError("R40R1 replacement test has changed")
    if not TARGET.is_file():
        raise RuntimeError("R40 test target not present")
    current = digest(TARGET.read_bytes())
    if current == BASELINE_SHA256:
        return "BASELINE"
    if current == REPLACEMENT_SHA256:
        return "CORRECTED"
    raise RuntimeError("R40 test changed outside reviewed R40R1 scope")


def install(dry_run: bool) -> dict[str, object]:
    """On non-dry-run install a single test-file replacement atomically."""
    mode = verified_mode()
    result = {
        "source_guard": "PASS",
        "test_mode": mode,
        "production_files_changed": 0,
        "changed_test_files": 0 if dry_run or mode == "CORRECTED" else 1,
        "rule_or_api_changed": False,
        "full_pytest": False,
    }
    if dry_run:
        result["mode"] = "DRYRUN"
        return result
    if mode == "BASELINE":
        previous = TARGET.read_bytes()
        style = b"\r\n" if b"\r\n" in previous else b"\n"
        updated = normalized(REPLACEMENT.read_bytes())
        if style == b"\r\n":
            updated = updated.replace(b"\n", b"\r\n")
        temporary_name = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix="r40r1_", suffix=".tmp", dir=TARGET.parent,
                delete=False,
            ) as stream:
                temporary_name = stream.name
                stream.write(updated)
            os.replace(temporary_name, TARGET)
        finally:
            if temporary_name is not None and os.path.exists(temporary_name):
                os.unlink(temporary_name)
    if verified_mode() != "CORRECTED":
        raise RuntimeError("R40R1 test replacement failed post-installation check")
    result["mode"] = "INSTALLED"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = install(dry_run=args.dry_run)
    for key, value in report.items():
        print("PHASE174_R3R7R40R1_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R40R1_GATE=PASS_R40R1_MATCHER_ORDER_TEST_CONTRACT_FIXED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## R40R1 tests/test_patch.py 全文

```python
"""Standalone guard for the sole changed R40 test function."""
from __future__ import annotations

import ast
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1]
BASELINE = FOLDER / "baseline/test_rule.py"
REPLACEMENT = FOLDER / "replacement/test_rule.py"
TEST_NAME = "test_direct_given_for_generator_zero_is_rejected"


def test_only_one_test_function_changes() -> None:
    before = ast.parse(BASELINE.read_text(encoding="utf-8"))
    after = ast.parse(REPLACEMENT.read_text(encoding="utf-8"))
    assert len(before.body) == len(after.body)
    changed = []
    for old, new in zip(before.body, after.body):
        if ast.dump(old, include_attributes=False) != ast.dump(new, include_attributes=False):
            assert isinstance(old, ast.FunctionDef)
            assert isinstance(new, ast.FunctionDef)
            assert old.name == new.name
            changed.append(old.name)
    assert changed == [TEST_NAME]


def test_forged_given_rejection_is_preserved() -> None:
    changed = REPLACEMENT.read_text(encoding="utf-8")
    assert "find_inference_matches_for_rule(rule, (db, forged)) == ()" in changed
    assert "find_inference_matches_for_rule(rule, (forged, db)) == ()" in changed
    assert "find_inference_matches_for_rule(rule, (db,)) == ()" in changed


def test_reversed_valid_order_requires_canonical_premise_match() -> None:
    changed = REPLACEMENT.read_text(encoding="utf-8")
    assert "matches = find_inference_matches_for_rule(rule, (independent, db))" in changed
    assert "assert len(matches) == 1" in changed
    assert "assert matches[0].premises == (db, independent)" in changed
    assert "assert find_inference_matches_for_rule(rule, (independent, db)) == ()" not in changed


def test_full_file_parse_and_original_import_section_preserved() -> None:
    before = ast.parse(BASELINE.read_text(encoding="utf-8"))
    after = ast.parse(REPLACEMENT.read_text(encoding="utf-8"))
    imports_before = tuple(ast.dump(s, include_attributes=False) for s in before.body
                           if isinstance(s, (ast.Import, ast.ImportFrom)))
    imports_after = tuple(ast.dump(s, include_attributes=False) for s in after.body
                          if isinstance(s, (ast.Import, ast.ImportFrom)))
    assert imports_before == imports_after
    assert imports_before
```

## R40R1 run.ps1 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r40r1_matcher_order_test_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R40R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R40R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r40r1_matcher_order_test_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R40R1 focused test correction failed' }
    Write-Output 'PHASE174_R3R7R40R1_TEST_GROUP=R40R1_PATCH_CONTRACT'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r40r1_matcher_order_test_fix/tests/test_patch.py
    if ($LASTEXITCODE -ne 0) { throw 'R40R1 patch contract failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r40_adopted_db_zero_image_isolated\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R40 original focused audit failed after correction' }
    Write-Output 'PHASE174_R3R7R40R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R40R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
