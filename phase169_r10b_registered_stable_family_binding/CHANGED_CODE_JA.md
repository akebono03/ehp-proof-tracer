# Phase 169 R10B — 変更・追加コード全文

## 既存関数の置換全文（既存 import は変更しない）

```python
def _intermediate_typed_generator(source: object, target: object, step: int,
                                  exponent: int) -> object | None:
    """Build DB-identified typed candidates, never a proven image equality.

    The HyoujiGen kinds=0 row is identity metadata. The downstream R7 rule
    continues to demand independently proved GeneratorImage obligations.
    """
    if type(step) is not int or type(exponent) is not int or not 0 <= step <= exponent:
        return None
    if isinstance(source, HomotopyElement) and isinstance(target, HomotopyElement):
        from phase169_r10b_registered_stable_family_binding.family_registry import (
            registered_stable_family_pair,
        )
        family = registered_stable_family_pair(source, target)
        s, t = source.generator, target.generator
        if (family is None
                or not isinstance(s, GeneratorSymbol)
                or not isinstance(t, GeneratorSymbol)
                or type(s.index) is not int
                or type(t.index) is not int
                or t.index - s.index != exponent
                or target.dimension - source.dimension != exponent
                or target.source - source.source != exponent
                or target.target - source.target != exponent):
            return None
        if step == 0:
            return source
        if step == exponent:
            return target
        middle_index = s.index + step
        return replace(
            source,
            name=family.name_at(middle_index),
            dimension=source.dimension + step,
            source=source.source + step,
            target=source.target + step,
            generator=replace(s, index=middle_index),
        )
    if isinstance(source, Composition) and isinstance(target, Composition):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Composition(left, right) if left is not None and right is not None else None
    if isinstance(source, Sum) and isinstance(target, Sum):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Sum(left, right) if left is not None and right is not None else None
    if (isinstance(source, Multiple) and isinstance(target, Multiple)
            and source.coefficient == target.coefficient):
        inner = _intermediate_typed_generator(source.expression, target.expression,
                                              step, exponent)
        return Multiple(source.coefficient, inner) if inner is not None else None
    if step == 0:
        return source
    if step == exponent:
        return target
    if (isinstance(target, IteratedSuspension)
            and target.expression == source
            and type(target.exponent) is int
            and target.exponent == exponent):
        return IteratedSuspension(source, step)
    if (isinstance(source, IteratedSuspension)
            and isinstance(target, IteratedSuspension)
            and source.expression == target.expression
            and type(source.exponent) is int
            and type(target.exponent) is int
            and target.exponent - source.exponent == exponent):
        return IteratedSuspension(source.expression, source.exponent + step)
    return None
```

## 新規モジュール全文: family_registry.py

```python
"""Bind typed indexed generators to kinds=0 HyoujiGen identities.

A DB row supplies candidate identity and degree metadata, NEVER a proof or a
claim that the suspension homomorphism is an isomorphism. R7 still requires
actual prior source, cited Toda (4.5), and proved GeneratorImage premises.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement


_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CSV = _ROOT / "data" / "HyoujiGen.csv"


@dataclass(frozen=True)
class RegisteredStableFamily:
    """A row of naming metadata, not an assertion of mathematical truth."""

    family_id: int
    display: str
    symbol_family: str
    stem: int
    minimum_n: int
    latex: str

    def name_at(self, n: int) -> str:
        return self.display + str(n).translate(_SUB)


@lru_cache(maxsize=8)
def read_registered_stable_families(csv_path: str | Path | None = None) -> tuple[RegisteredStableFamily, ...]:
    """Read all genuine kinds=0 generators; exclude the registered zero row."""
    path = Path(csv_path) if csv_path is not None else _DEFAULT_CSV
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = tuple(csv.DictReader(stream))
    result: list[RegisteredStableFamily] = []
    seen_ids: set[int] = set()
    for row in rows:
        if int(row["kinds"]) != 0:
            continue
        family_id = int(row["id"])
        if family_id == 0:
            continue
        if family_id in seen_ids:
            raise ValueError(f"duplicate HyoujiGen stable-family ID: {family_id}")
        seen_ids.add(family_id)
        stem = int(row["k"])
        minimum_n = int(row["n"])
        display = row["display"].strip()
        latex = row["latex"].strip()
        if stem < 0 or minimum_n < 1 or not display or not latex:
            raise ValueError(f"invalid registered stable-family metadata: {family_id}")
        symbol_family = display if display in {"η", "ν", "σ", "ι"} else latex
        result.append(RegisteredStableFamily(
            family_id=family_id,
            display=display,
            symbol_family=symbol_family,
            stem=stem,
            minimum_n=minimum_n,
            latex=latex,
        ))
    return tuple(result)


def registered_family_of(
    element: object, *, csv_path: str | Path | None = None,
) -> RegisteredStableFamily | None:
    """Match the complete typed member, not an untrusted display label alone."""
    if not isinstance(element, HomotopyElement):
        return None
    symbol = element.generator
    if not isinstance(symbol, GeneratorSymbol) or symbol.decoration is not None:
        return None
    n = symbol.index
    if type(n) is not int or not all(
        type(value) is int
        for value in (element.dimension, element.source, element.target)
    ):
        return None
    if element.dimension != n or element.target != n:
        return None
    matches = tuple(family for family in read_registered_stable_families(csv_path)
                    if n >= family.minimum_n
                    and element.source == n + family.stem
                    and symbol.family == family.symbol_family
                    and element.name in (
                        family.name_at(n), family.display + "_" + str(n),
                    ))
    return matches[0] if len(matches) == 1 else None


def registered_stable_family_pair(
    source: object, target: object, *, csv_path: str | Path | None = None,
) -> RegisteredStableFamily | None:
    """Same DB family ID and increasing indices, without asserting E(source)."""
    earlier = registered_family_of(source, csv_path=csv_path)
    later = registered_family_of(target, csv_path=csv_path)
    if earlier is None or later is None or earlier.family_id != later.family_id:
        return None
    if source.dimension >= target.dimension:
        return None
    return earlier
```

## 新規テスト関数と import の全文: tests/test_r10b_registered_family.py

```python
"""R10B: DB family identity is a typed candidate guard, not a proof axiom."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
    registered_family_of,
    registered_stable_family_pair,
)
from phase169_r7_general_stable_transport.rule import (
    _consecutive_generator_image_goals,
    _intermediate_typed_generator,
)
from proof import Relation, RelationType


_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def member(family, n: int) -> HomotopyElement:
    return HomotopyElement(
        name=family.display + str(n).translate(_SUB),
        dimension=n,
        source=n + family.stem,
        target=n,
        generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def test_r10b_all_registered_kinds_zero_identified_without_zero():
    families = read_registered_stable_families()
    assert len(families) == 39
    assert len({item.family_id for item in families}) == 39
    assert not any(item.family_id == 0 for item in families)
    assert {2, 4, 9}.issubset({item.family_id for item in families})
    for family in families:
        initial = member(family, family.minimum_n)
        assert registered_family_of(initial) == family
        assert registered_family_of(member(family, family.minimum_n + 3)) == family
        assert registered_family_of(member(family, family.minimum_n - 1)) is None


@pytest.mark.parametrize("family_id", [2, 4, 9, 10, 23, 103])
@pytest.mark.parametrize("r", [1, 2, 4])
def test_r10b_registered_family_arbitrary_steps(family_id, r):
    families = read_registered_stable_families()
    family = next(row for row in families if row.family_id == family_id)
    source = member(family, max(family.minimum_n, family.stem + 2))
    target = member(family, source.dimension + r)
    assert registered_stable_family_pair(source, target) == family
    for step in range(1, r):
        assert _intermediate_typed_generator(source, target, step, r) == member(
            family, source.dimension + step
        )


def test_r10b_rejects_spoofed_family_stem_and_minimum():
    families = read_registered_stable_families()
    nu = next(row for row in families if row.family_id == 4)
    source = member(nu, 5)
    target = member(nu, 7)
    assert registered_stable_family_pair(source, target) == nu
    wrong_stem = replace(target, source=target.source + 1)
    wrong_symbol = replace(target, generator=replace(target.generator, family="η"))
    wrong_decoration = replace(target, generator=replace(target.generator, decoration="′"))
    wrong_name = replace(target, name="ν₉")
    unknown = replace(target, generator=replace(target.generator, family="UNKNOWN"))
    for invalid in (wrong_stem, wrong_symbol, wrong_decoration, wrong_name, unknown):
        assert registered_stable_family_pair(source, invalid) is None
        assert _intermediate_typed_generator(source, invalid, 1, 2) is None
    assert registered_family_of(member(nu, 3)) is None


def test_r10b_single_suspension_also_requires_registered_identity():
    families = read_registered_stable_families()
    nu = next(row for row in families if row.family_id == 4)
    original = member(nu, 5)
    last = member(nu, 6)
    assert _intermediate_typed_generator(original, last, 0, 1) == original
    assert _intermediate_typed_generator(original, last, 1, 1) == last
    bad = replace(last, source=last.source + 1)
    assert _intermediate_typed_generator(original, bad, 0, 1) is None
    from proof import Relation, RelationType
    source_group = Relation(TodaPrimaryGroup(8, 5), FiniteCyclicGroup(8, original),
                            RelationType.EQUALITY)
    target_group = Relation(TodaPrimaryGroup(9, 6), FiniteCyclicGroup(8, bad),
                            RelationType.EQUALITY)
    assert _consecutive_generator_image_goals(source_group, target_group) is None


def test_r10b_unequal_registry_id_does_not_count_as_same_family():
    families = read_registered_stable_families()
    eta = next(row for row in families if row.family_id == 2)
    nu = next(row for row in families if row.family_id == 4)
    assert registered_stable_family_pair(member(eta, 4), member(nu, 6)) is None


def test_r10b_mixed_composition_preserves_typed_names():
    families = read_registered_stable_families()
    eta = next(row for row in families if row.family_id == 2)
    start = Composition(member(eta, 4), member(eta, 5))
    finish = Composition(member(eta, 7), member(eta, 8))
    middle = _intermediate_typed_generator(start, finish, 2, 3)
    assert middle == Composition(member(eta, 6), member(eta, 7))


def test_r10b_registered_names_never_generate_proof_steps():
    families = read_registered_stable_families()
    nu = next(row for row in families if row.family_id == 4)
    original = member(nu, 5)
    last = member(nu, 7)
    source = Relation(TodaPrimaryGroup(8, 5), FiniteCyclicGroup(8, original),
                      RelationType.EQUALITY)
    target = Relation(TodaPrimaryGroup(10, 7), FiniteCyclicGroup(8, last),
                      RelationType.EQUALITY)
    images = _consecutive_generator_image_goals(source, target)
    assert images is not None and len(images) == 2
    assert images[0].source_generator == original
    assert images[-1].target_generator == last
    assert all(type(image).__name__ == "GeneratorImage" for image in images)
    assert all(type(image).__name__ != "ProofStep" for image in images)
    too_early = Relation(TodaPrimaryGroup(7, 4), FiniteCyclicGroup(8, member(nu, 4)),
                         RelationType.EQUALITY)
    assert _consecutive_generator_image_goals(too_early, target) is None


def test_r10b_patch_only_complete_function_and_preserves_other_source():
    from phase169_r10b_registered_stable_family_binding.patch import (
        BACKUP, replacement_content, _function_range,
    )
    before = BACKUP.read_bytes()
    after, function = replacement_content(before)
    previous = before.decode("utf-8").replace("\r\n", "\n")
    changed = after.decode("utf-8").replace("\r\n", "\n")
    start, end = _function_range(previous)
    assert "registered_stable_family_pair" in function
    assert previous[:start] == changed[:start]
    assert previous[end:].strip() == changed[start + len(function):].strip()
    with pytest.raises(RuntimeError):
        replacement_content(after)
```

## パッチ全体: patch.py

```python
"""Replace one complete R7 generator-candidate function with DB-bound version."""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase169_r7_general_stable_transport" / "rule.py"
OUTPUT = HERE / "output"
BACKUP = OUTPUT / "phase169_r7_general_stable_transport.rule.py.before"

# The exact reviewed R7 function body is the only allowed patch anchor.
OLD_FUNCTION_START = "def _intermediate_typed_generator(source: object, target: object, step: int,"


NEW_FUNCTION = '''def _intermediate_typed_generator(source: object, target: object, step: int,
                                  exponent: int) -> object | None:
    """Build DB-identified typed candidates, never a proven image equality.

    The HyoujiGen kinds=0 row is identity metadata. The downstream R7 rule
    continues to demand independently proved GeneratorImage obligations.
    """
    if type(step) is not int or type(exponent) is not int or not 0 <= step <= exponent:
        return None
    if isinstance(source, HomotopyElement) and isinstance(target, HomotopyElement):
        from phase169_r10b_registered_stable_family_binding.family_registry import (
            registered_stable_family_pair,
        )
        family = registered_stable_family_pair(source, target)
        s, t = source.generator, target.generator
        if (family is None
                or not isinstance(s, GeneratorSymbol)
                or not isinstance(t, GeneratorSymbol)
                or type(s.index) is not int
                or type(t.index) is not int
                or t.index - s.index != exponent
                or target.dimension - source.dimension != exponent
                or target.source - source.source != exponent
                or target.target - source.target != exponent):
            return None
        if step == 0:
            return source
        if step == exponent:
            return target
        middle_index = s.index + step
        return replace(
            source,
            name=family.name_at(middle_index),
            dimension=source.dimension + step,
            source=source.source + step,
            target=source.target + step,
            generator=replace(s, index=middle_index),
        )
    if isinstance(source, Composition) and isinstance(target, Composition):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Composition(left, right) if left is not None and right is not None else None
    if isinstance(source, Sum) and isinstance(target, Sum):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Sum(left, right) if left is not None and right is not None else None
    if (isinstance(source, Multiple) and isinstance(target, Multiple)
            and source.coefficient == target.coefficient):
        inner = _intermediate_typed_generator(source.expression, target.expression,
                                              step, exponent)
        return Multiple(source.coefficient, inner) if inner is not None else None
    if step == 0:
        return source
    if step == exponent:
        return target
    if (isinstance(target, IteratedSuspension)
            and target.expression == source
            and type(target.exponent) is int
            and target.exponent == exponent):
        return IteratedSuspension(source, step)
    if (isinstance(source, IteratedSuspension)
            and isinstance(target, IteratedSuspension)
            and source.expression == target.expression
            and type(source.exponent) is int
            and type(target.exponent) is int
            and target.exponent - source.exponent == exponent):
        return IteratedSuspension(source.expression, source.exponent + step)
    return None
'''


def _function_range(code: str) -> tuple[int, int]:
    lines = code.splitlines(keepends=True)
    tree = ast.parse(code)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "_intermediate_typed_generator"]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one R7 generator candidate function")
    node = matches[0]
    if not lines[node.lineno - 1].startswith(OLD_FUNCTION_START):
        raise RuntimeError("R7 generator function signature drifted")
    return sum(len(line) for line in lines[:node.lineno - 1]), sum(
        len(line) for line in lines[:node.end_lineno]
    )


def replacement_content(original: bytes) -> tuple[bytes, str]:
    """Only change the function; preserve all other R7 source bytes and EOLs."""
    windows = b"\r\n" in original
    code = original.decode("utf-8").replace("\r\n", "\n")
    start, end = _function_range(code)
    original_function = code[start:end]
    if ("Every index/dimension change is checked structurally" not in original_function
            or "_indexed_display(source)" not in original_function
            or "_indexed_display(target)" not in original_function):
        raise RuntimeError("R7 baseline function has changed; no patch applied")
    replacement = NEW_FUNCTION + ("\n" if code[end:end + 1] == "\n" else "")
    updated = code[:start] + replacement + code[end:]
    ast.parse(updated)
    if updated.count("def _intermediate_typed_generator(") != 1:
        raise RuntimeError("duplicate generator-candidate function")
    new_content = updated.replace("\n", "\r\n") if windows else updated
    return new_content.encode("utf-8"), NEW_FUNCTION


def main() -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R10B requires the develop branch")
    original = TARGET.read_bytes()
    changed, function = replacement_content(original)
    OUTPUT.mkdir(exist_ok=True)
    if BACKUP.exists():
        if BACKUP.read_bytes() != original:
            raise RuntimeError("existing R10B restore point does not match production")
    else:
        BACKUP.write_bytes(original)
    (OUTPUT / "_intermediate_typed_generator_FULL.py").write_text(
        function, encoding="utf-8"
    )
    (OUTPUT / "phase169_r7_general_stable_transport.rule.py.FULL").write_bytes(changed)
    tmp = TARGET.with_name(TARGET.name + ".r10b-tmp")
    try:
        tmp.write_bytes(changed)
        tmp.replace(TARGET)
    finally:
        if tmp.exists():
            tmp.unlink()
    print("R10B_PATCHED=" + str(TARGET))
    print("R10B_BACKUP=" + str(BACKUP))
    print("R10B_FULL_FUNCTION=" + str(OUTPUT / "_intermediate_typed_generator_FULL.py"))
    print("R10B_FULL_FILE=" + str(OUTPUT / "phase169_r7_general_stable_transport.rule.py.FULL"))


if __name__ == "__main__":
    main()
```

## 監査全体: audit.py

```python
"""Read-only post-patch audit of typed family and canonical 1/2-stem proofs."""
from __future__ import annotations

import json
from pathlib import Path

from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative


HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = read_registered_stable_families()
    assert len(rows) == 39
    bridge = build_shared_typed_bridge()
    cases = []
    for n, k in ((8, 1), (5, 2), (6, 2), (7, 2), (8, 2)):
        contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        if result.status is not ProofSearchStatus.COMPLETE:
            raise AssertionError(f"pi_{n+k}^{n} lost its complete proof")
        from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
        from web_group_proof import build_standard_web_group_proof_view
        if len(contexts) != 1 or result.open_goals:
            raise AssertionError("completed proof missing screened context")
        citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        if citing_id is None:
            raise AssertionError("completed group has no citation binding")
        verify_proof_tree_for_narrative(
            result, contexts[0], citing_assertion_id=citing_id,
        )
        view = build_standard_web_group_proof_view(n, k, mode="narrative")
        if view.key != "generic-complete-proof" or view.partial_result:
            raise AssertionError("Web canonical proof regressed")
        cases.append({"n": n, "k": k, "status": result.status.value,
                      "steps": len(result.proven_steps),
                      "proof_tree_verified": True, "web_key": view.key})
        print(f"R10B_pi_{n+k}^{n}_STATUS=complete")
    output = HERE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(json.dumps({
        "phase": "169-R10B", "family_rows": len(rows), "cases": cases,
        "claim": "typed candidate registry; no source proof from DB",
        "full_pytest": False,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("R10B_STABLE_FAMILY_RECORDS=" + str(len(rows)))
    print("R10B_AUDIT=" + str(output / "audit.json"))
    print("R10B_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
```

## Windows PowerShell 実行スクリプト全文: run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$target = Join-Path $root 'phase169_r7_general_stable_transport\rule.py'
$backup = Join-Path $folder 'output\phase169_r7_general_stable_transport.rule.py.before'
$patched = $false
$passed = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10B requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect HEAD.' }
    Write-Host "R10B_BRANCH=$branch"
    Write-Host "R10B_GIT_HEAD=$head"
    $beforeOther = @(git diff --name-only -- . ':!phase169_r7_general_stable_transport/rule.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect existing tracked changes.' }
    python -m phase169_r10b_registered_stable_family_binding.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10B source patch failed.' }
    $patched = $true
    python -m pytest -q `
      (Join-Path $folder 'tests\test_r10b_registered_family.py') `
      (Join-Path $root 'phase169_r7_general_stable_transport\tests\test_r7_general_stable_transport.py') `
      (Join-Path $root 'phase169_r10a2_unified_one_stem\tests\test_r10a2_one_stem_projection.py') `
      (Join-Path $root 'phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10B focused pytest failed.' }
    python -m phase169_r10b_registered_stable_family_binding.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10B proof audit failed.' }
    $afterOther = @(git diff --name-only -- . ':!phase169_r7_general_stable_transport/rule.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0 -or ($beforeOther -join "`n") -ne ($afterOther -join "`n")) {
        throw 'An unrelated tracked file changed.'
    }
    $passed = $true
    Write-Host 'R10B_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10B_PRODUCTION_FILES_CHANGED=phase169_r7_general_stable_transport/rule.py'
    Write-Host 'R10B_FULL_PYTEST_RUN=False'
} finally {
    if ($patched -and -not $passed -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10B_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
```
