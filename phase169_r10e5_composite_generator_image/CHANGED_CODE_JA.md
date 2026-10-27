# Phase 169 R10E5 — 全コードおよび変更単位

## 変更ファイル・関数

- `phase165_r52_r9_shared_math.py` : `shared_expansion_provider()` の関数全体を置換。既存の import は変更なし。
- `phase169_r10e5_composite_generator_image/rule.py` : 新規ファイル全文。既存関数が使用する新規モジュール。
- `phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py` : 新規テスト全文。
- `phase169_r10e5_composite_generator_image/audit.py` : 限定監査全文。
- `run.ps1`、`patch.py` : 実行・バックアップ・全文出力。

変更後の既存関数の全文は `run.ps1` 実行時に `output/shared_expansion_provider_FULL.py` に、既存ファイル全文は `output/phase165_r52_r9_shared_math.py.FULL` に生成される。旧コードの構文と単一の置換位置を検証してから適用する。

## 新規モジュール全文

### `rule.py`

```python
"""A typed suspension-of-composition inference, with no new source axioms.

The equality E(f o g) = E(f) o E(g) is used only when both component
GeneratorImage obligations have independently replayable INFERENCE proofs.
A source/target generator name or a database row is never proof evidence.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule


def _endpoints(element: object) -> tuple[int, int] | None:
    """For a typed map S^source -> S^target return (source, target)."""
    if isinstance(element, HomotopyElement):
        if not all(type(x) is int for x in (
            element.dimension, element.source, element.target,
        )):
            return None
        if (element.dimension != element.target or element.target < 2
                or element.source <= element.target):
            return None
        return (element.source, element.target)
    if isinstance(element, Composition):
        left = _endpoints(element.left)
        right = _endpoints(element.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return (right[0], left[1])
    return None


def component_image_obligations(
    goal: object,
) -> tuple[GeneratorImage, GeneratorImage] | None:
    """Decompose a valid E(f o g) obligation into E(f) and E(g) goals.

    This checks source/target dimensions and the composability at both ends.
    It does not claim that either factor image has been proved.
    """
    if (not isinstance(goal, GeneratorImage)
            or not isinstance(goal.map, TodaSuspensionMap)
            or not isinstance(goal.source_generator, Composition)
            or not isinstance(goal.target_generator, Composition)):
        return None
    source = goal.source_generator
    target = goal.target_generator
    source_end = _endpoints(source)
    target_end = _endpoints(target)
    if source_end is None or target_end is None:
        return None
    if (target_end != (source_end[0] + 1, source_end[1] + 1)
            or goal.map.source_group != TodaPrimaryGroup(*source_end)
            or goal.map.target_group != TodaPrimaryGroup(*target_end)):
        return None
    parts: list[GeneratorImage] = []
    for earlier, later in (
        (source.left, target.left),
        (source.right, target.right),
    ):
        source_part = _endpoints(earlier)
        target_part = _endpoints(later)
        if (source_part is None or target_part is None
                or target_part != (source_part[0] + 1, source_part[1] + 1)):
            return None
        parts.append(GeneratorImage(
            map=TodaSuspensionMap(
                TodaPrimaryGroup(*source_part),
                TodaPrimaryGroup(*target_part),
            ),
            source_generator=earlier,
            target_generator=later,
        ))
    return parts[0], parts[1]


def composite_generator_image_rule(goal: GeneratorImage) -> InferenceRule:
    """Require two independently inferred and typed suspension images."""
    expected = component_image_obligations(goal)
    if expected is None:
        raise ValueError("not a well-typed suspension of a composite")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == expected
            and component_image_obligations(goal) == expected
        )

    return InferenceRule(
        name="suspension preserves composition of separately proved maps",
        description=(
            "A composite generator image follows from two typed, "
            "independently inferred factor suspension images."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=expected[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=expected[1],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_composite_generator_image(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Propose only two typed proof obligations, never a GIVEN or direct fact."""
    expected = component_image_obligations(goal)
    if expected is None:
        return ()
    return (GoalExpansion(
        composite_generator_image_rule(goal), expected,
    ),)
```

### `tests/test_r10e5_composite_generator_image.py`

```python
"""Typed composition-image obligations; no result may be inserted as GIVEN."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
    composite_generator_image_rule,
    expand_composite_generator_image,
)
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from proof import (
    ProofRule, ProofStep, apply_inference_match,
    find_inference_matches_for_rule,
)


def _nu(n: int) -> HomotopyElement:
    family = next(x for x in read_registered_stable_families()
                  if x.family_id == 4)
    return HomotopyElement(
        name=family.name_at(n), dimension=n,
        source=n + family.stem, target=n,
        generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def _square(n: int) -> Composition:
    return Composition(_nu(n), _nu(n + 3))


def _cube(n: int) -> Composition:
    return Composition(_nu(n), Composition(_nu(n + 3), _nu(n + 6)))


def _image(n: int, stem: int, earlier: object, later: object) -> GeneratorImage:
    return GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + stem, n),
            TodaPrimaryGroup(n + stem + 1, n + 1),
        ),
        earlier, later,
    )


def test_r10e5_nu_squared_creates_two_independent_factor_images():
    goal = _image(8, 6, _square(8), _square(9))
    obligations = component_image_obligations(goal)
    assert obligations == (
        _image(8, 3, _nu(8), _nu(9)),
        _image(11, 3, _nu(11), _nu(12)),
    )
    options = expand_composite_generator_image(goal)
    assert len(options) == 1
    assert options[0].subgoals == obligations
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)


def test_r10e5_two_inferred_images_are_required_to_prove_composition():
    goal = _image(8, 6, _square(8), _square(9))
    obligations = component_image_obligations(goal)
    assert obligations is not None
    rule = composite_generator_image_rule(goal)
    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE)
                  for item in obligations)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal
    assert find_inference_matches_for_rule(rule, steps[:1]) == ()
    assert find_inference_matches_for_rule(
        rule, (replace(steps[0], rule=ProofRule.GIVEN), steps[1]),
    ) == ()
    assert find_inference_matches_for_rule(rule, tuple(reversed(steps))) == ()


def test_r10e5_nested_nu_cube_recurses_without_family_specific_code():
    goal = _image(9, 9, _cube(9), _cube(10))
    obligations = component_image_obligations(goal)
    assert obligations is not None and len(obligations) == 2
    assert obligations[0] == _image(9, 3, _nu(9), _nu(10))
    second_level = component_image_obligations(obligations[1])
    assert second_level is not None and len(second_level) == 2
    assert all(expand_composite_generator_image(item)
               for item in (goal, obligations[1]))


def test_r10e5_refuses_inconsistent_factor_suspension_and_composition():
    valid = _image(8, 6, _square(8), _square(9))
    bad_generator = Composition(_nu(9), _nu(13))
    assert expand_composite_generator_image(replace(
        valid, target_generator=bad_generator,
    )) == ()
    unchanged = replace(valid, target_generator=valid.source_generator)
    assert expand_composite_generator_image(unchanged) == ()
    wrong_map = replace(valid, map=TodaSuspensionMap(
        TodaPrimaryGroup(15, 9), TodaPrimaryGroup(16, 10),
    ))
    assert expand_composite_generator_image(wrong_map) == ()
    with pytest.raises(ValueError):
        composite_generator_image_rule(unchanged)


def test_r10e5_simple_member_remains_for_cited_family_path():
    goal = _image(8, 3, _nu(8), _nu(9))
    assert expand_composite_generator_image(goal) == ()
    from phase169_r10d2_general_family_definition.family_citation import (
        expand_cited_stable_family, CitedStableFamilyDefinition,
    )
    source = CitedStableFamilyDefinition(4, 4, 3)
    assert len(expand_cited_stable_family(goal, (source,))) == 1


def test_r10e5_composite_without_proved_component_cannot_complete():
    goal = _image(8, 6, _square(8), _square(9))
    options = expand_composite_generator_image(goal)
    assert len(options) == 1
    # The provider supplies candidate Goal objects, never a leaf or a proof.
    assert all(isinstance(item, GeneratorImage) for item in options[0].subgoals)
    assert find_inference_matches_for_rule(options[0].rule, ()) == ()


def test_r10e5_patch_guarded_and_full_function_retained():
    from phase169_r10e5_composite_generator_image.patch import OLD, NEW, transform
    sample = (
        'def shared_expansion_provider():\n'
        '    def expand(goal):\n'
        + OLD + '\n'
        '        return ()\n'
        '    return expand\n'
    ).encode('utf-8')
    modified, full = transform(sample)
    assert NEW in modified.decode('utf-8')
    assert full.startswith('def shared_expansion_provider():')
    with pytest.raises(RuntimeError, match='source anchor'):
        transform(modified)
```

### `audit.py`

```python
"""Targeted, read-only search audit for newly composed generator images."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
)
from phase165_r14_r6_generic_iso import GeneratorImage


OUTPUT = Path(__file__).resolve().parent / "output"
CASES = (
    (14, 6),
    (15, 8),
    (15, 9),
    (14, 7),
    (8, 4),
    (13, 3),
)


def main() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    bridge = build_shared_typed_bridge()
    results = []
    for n, k in CASES:
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        composite_inferences = tuple(
            step for step in result.proven_steps
            if (step.rule.value == "inference"
                and isinstance(step.conclusion, GeneratorImage)
                and component_image_obligations(step.conclusion) is not None)
        )
        info = {
            "n": n,
            "k": k,
            "status": result.status.value,
            "composite_image_inferences": len(composite_inferences),
            "diagnostics": list(result.diagnostics),
            "unresolved_goal_types": [type(x).__name__ for x in result.open_goals],
        }
        results.append(info)
        print(f"R10E5_pi_{n+k}^{n}_STATUS={info['status']}")
        print(f"R10E5_pi_{n+k}^{n}_COMPOSITE_IMAGES={info['composite_image_inferences']}")
        print(f"R10E5_pi_{n+k}^{n}_OPEN_GOALS={','.join(info['unresolved_goal_types'])}")
    OUTPUT.mkdir(exist_ok=True)
    file = OUTPUT / "audit.json"
    file.write_text(json.dumps({
        "phase": "169 R10E5",
        "cases": results,
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2) + '\n', encoding="utf-8")
    print("R10E5_AUDIT=" + str(file))
    print("R10E5_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
```

### `patch.py`

```python
"""Guarded one-function edit of the common backward expansion provider."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OLD = (
    "        options.extend(expand_cited_eta_generator(goal))\n"
    "        options.extend(expand_cited_stable_family(goal))"
)
NEW = (
    "        eta_generator_options = expand_cited_eta_generator(goal)\n"
    "        options.extend(eta_generator_options)\n"
    "        options.extend(expand_cited_stable_family(goal))\n"
    "        if not eta_generator_options:\n"
    "            from phase169_r10e5_composite_generator_image.rule import (\n"
    "                expand_composite_generator_image,\n"
    "            )\n"
    "            options.extend(expand_composite_generator_image(goal))"
)


def full_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    found = tuple(n for n in tree.body
                  if isinstance(n, ast.FunctionDef) and n.name == name)
    if len(found) != 1:
        raise RuntimeError("expected exactly one full function: " + name)
    node = found[0]
    return "".join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])


def transform(raw: bytes) -> tuple[bytes, str]:
    crlf = b"\r\n" in raw
    source = raw.decode("utf-8-sig").replace("\r\n", "\n")
    if source.count(OLD) != 1 or NEW in source:
        raise RuntimeError("R10E5 source anchor missing or already applied")
    updated = source.replace(OLD, NEW, 1)
    ast.parse(updated)
    full = full_function(updated, "shared_expansion_provider")
    encoded = updated.encode("utf-8")
    if crlf:
        encoded = encoded.replace(b"\n", b"\r\n")
    return encoded, full


def main() -> None:
    raw = TARGET.read_bytes()
    updated, fn = transform(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "phase165_r52_r9_shared_math.py.before").write_bytes(raw)
    (OUTPUT / "phase165_r52_r9_shared_math.py.FULL").write_bytes(updated)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(fn, encoding="utf-8")
    TARGET.write_bytes(updated)
    print("R10E5_PATCHED=" + str(TARGET))
    print("R10E5_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"))
    print("R10E5_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.py.FULL"))


if __name__ == "__main__":
    main()
```

### `run.ps1`

```powershell
$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$root = (Resolve-Path (Join-Path $here '..')).Path
$targetRel = 'phase165_r52_r9_shared_math.py'
$target = Join-Path $root $targetRel
$backup = Join-Path $here 'output/phase165_r52_r9_shared_math.py.before'
$success = $false
$patchAttempted = $false
$oldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    $head = (git rev-parse HEAD).Trim()
    Write-Host "R10E5_BRANCH=$branch"
    Write-Host "R10E5_HEAD=$head"
    if ($branch -ne 'develop' -or $head -ne '7a687a58443d1cfe40ba03923dd9be60fa462788') {
        throw 'R10E5 requires the reviewed develop HEAD 7a687a5.'
    }
    if (-not (Test-Path (Join-Path $root 'phase169_r10e4_ordered_db_prior/db_prior.py'))) {
        throw 'R10E5 requires previously installed R10E4 database prior policy.'
    }
    if (-not (Test-Path (Join-Path $root 'phase169_r10e4r4_db_prior_test_alignment/tests'))) {
        throw 'R10E5 requires completed R10E4-R4 regression tests.'
    }
    $trackBefore = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    $otherBefore = @($trackBefore | Where-Object { $_ -ne $targetRel })
    Write-Host ('R10E5_EXISTING_TRACKED=' + ($trackBefore -join '|'))
    $patchAttempted = $true
    python -m phase169_r10e5_composite_generator_image.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E5 guarded patch failed.' }
    $focused = @(
        'phase169_r10e5_composite_generator_image/tests',
        'phase169_r10e4_ordered_db_prior/tests',
        'phase169_r10e4r2_explicit_db_row_parser/tests',
        'phase169_r10e4r4_db_prior_test_alignment/tests',
        'phase169_r10e1_general_group_transport/tests',
        'phase169_r10e2_unpositioned_citation/tests',
        'phase169_r10d2_general_family_definition/tests',
        'phase169_r10b_registered_stable_family_binding/tests',
        'phase169_r7_general_stable_transport/tests',
        'phase168_r3_41p13_trust_boundary/tests',
        'phase168_r3_41p19_phase_closeout/tests'
    )
    python -m pytest -q @focused
    if ($LASTEXITCODE -ne 0) { throw 'R10E5 focused pytest failed.' }
    python -m phase169_r10e5_composite_generator_image.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E5 audit failed.' }
    $trackAfter = @(git -c core.quotepath=false diff --name-only HEAD -- . | Where-Object { $_ -ne '' } | ForEach-Object { $_.Replace('\','/') } | Sort-Object -Unique)
    $otherAfter = @($trackAfter | Where-Object { $_ -ne $targetRel })
    $added = @($otherAfter | Where-Object { $otherBefore -notcontains $_ })
    $removed = @($otherBefore | Where-Object { $otherAfter -notcontains $_ })
    Write-Host ('R10E5_UNRELATED_ADDED=' + ($added -join '|'))
    Write-Host ('R10E5_UNRELATED_REMOVED=' + ($removed -join '|'))
    if ($added.Count -gt 0 -or $removed.Count -gt 0) {
        throw 'R10E5 unrelated tracked changes detected.'
    }
    if ((-not (Test-Path $backup)) -or
        ((Get-FileHash -Path $backup -Algorithm SHA256).Hash -eq
         (Get-FileHash -Path $target -Algorithm SHA256).Hash)) {
        throw 'R10E5 production target was not modified.'
    }
    $success = $true
    Write-Host 'R10E5_INTEGRITY_RESULT=PASS'
    Write-Host 'R10E5_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host ('R10E5_PRODUCTION_FILES_CHANGED=' + $targetRel)
    Write-Host 'R10E5_FULL_PYTEST_RUN=False'
} finally {
    if ($patchAttempted -and -not $success -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10E5_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
```

