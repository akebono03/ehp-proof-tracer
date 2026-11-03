# Phase 173 R4-R15R3 — 変更コード・テスト全文

新規ファイルはすべて `phase173_r4_r15r3_formal_suspension_bridge/` 直下または `tests/` 以下に追加する。既存本番ファイルの import・クラス・関数の変更はない。各ファイルは省略せず全文掲載する。

## `__init__.py`

```python
"""Source-safe formal suspension proof frontier."""
```

## `bridge.py`

```python
"""Uniform, typed *formal* E images; no named generator identification.

This module never registers a public proof expansion or a new GIVEN source.
A formal E(g) is the definition of suspension. Splitting E(a o b) into
E(a) o E(b) is the functoriality of suspension. Neither statement implies
that a separately named database generator equals that formal expression.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from proof import InferenceRule


FORMAL_RULE_NAME = "canonical formal suspension of typed compositions"


def canonical_formal_suspension(expression: object) -> object | None:
    """Distribute one E over a typed composition without renaming atoms.

    An arbitrary atom becomes an explicit IteratedSuspension even in an
    unstable range. This is *not* a stable-family generator identity.
    """
    span = typed_element_span(expression)
    if span is None or span[1] < 2 or span[0] < span[1]:
        return None
    expected_span = (span[0] + 1, span[1] + 1)
    if isinstance(expression, HomotopyElement):
        result = IteratedSuspension(expression=expression, exponent=1)
    elif isinstance(expression, IteratedSuspension):
        if (type(expression.exponent) is not int
                or expression.exponent < 0):
            return None
        result = IteratedSuspension(
            expression=expression.expression,
            exponent=expression.exponent + 1,
        )
    elif isinstance(expression, Composition):
        left = canonical_formal_suspension(expression.left)
        right = canonical_formal_suspension(expression.right)
        if left is None or right is None:
            return None
        result = Composition(left=left, right=right)
    else:
        return None
    return result if typed_element_span(result) == expected_span else None


def formal_image_goal(expression: object) -> GeneratorImage | None:
    """Build a typed E-image goal for a canonical formal expression only."""
    span = typed_element_span(expression)
    image = canonical_formal_suspension(expression)
    if span is None or image is None:
        return None
    q, n = span
    return GeneratorImage(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(q, n),
            target_group=TodaPrimaryGroup(q + 1, n + 1),
        ),
        source_generator=expression,
        target_generator=image,
    )


def is_canonical_formal_image(statement: object) -> bool:
    """Reject forged endpoints and all named or noncanonical image claims."""
    if not isinstance(statement, GeneratorImage):
        return False
    expected = formal_image_goal(statement.source_generator)
    return expected is not None and statement == expected


def expand_canonical_formal_image(
    statement: object,
) -> tuple[GoalExpansion, ...]:
    """Offer an independently replayable definitional step, not DB equality."""
    if not is_canonical_formal_image(statement):
        return ()

    def guard(premises, bindings):
        return (
            len(premises) == 0
            and not bindings
            and is_canonical_formal_image(statement)
        )

    rule = InferenceRule(
        name=FORMAL_RULE_NAME,
        description=(
            "One formal suspension E of an explicitly typed representative; "
            "suspension preserves composition. No separately named generator "
            "is identified and no source theorem or DB claim is added."
        ),
        premise_patterns=(),
        match_guard=guard,
        conclusion_pattern=statement,
    )
    return (GoalExpansion(rule, ()),)
```

## `audit.py`

```python
"""Inspect canonical image claims and unresolved target-generator identifications."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
from phase173_r4_r4_typed_generator_audit.audit import _group_components
from phase173_r4_r15r2_generator_obligation_audit.audit import inspect_k as inspect_r15r2
from phase173_r4_r15r3_formal_suspension_bridge.bridge import (
    canonical_formal_suspension,
    expand_canonical_formal_image,
    formal_image_goal,
)


def _component_kind(component: object) -> tuple[str, int] | None:
    if isinstance(component, FreeCyclicGroup):
        return ("free", 0)
    if isinstance(component, FiniteCyclicGroup) and type(component.order) is int:
        return ("finite", component.order)
    return None


def inspect_k(k: int) -> dict[str, object]:
    """Do not choose a named target when equal-order matches are ambiguous."""
    base = inspect_r15r2(k)
    goal = exact_prior_database_result(4, k)
    pair = checked_abstract_inputs(goal) if goal is not None else None
    row: dict[str, object] = {
        "k": k,
        "abstract_compatible": pair is not None,
        "canonical_formal_images": [],
        "named_generator_identifications_proved": 0,
        "group_proof_completed": False,
        "new_given_assertions": 0,
        "public_route_modified": False,
    }
    if pair is None:
        row["state"] = "ABSTRACT_PRIOR_UNAVAILABLE"
        return row
    left, _ = pair
    lparts = _group_components(left)
    targets = _group_components(goal)
    if lparts is None or targets is None:
        raise RuntimeError("Previously checked abstract group lost typed components")
    if base["right_pending_indices"]:
        row["state"] = "RIGHT_MATCH_PENDING"
        return row
    residual = tuple(base["residual_target_indices"])
    rows: list[dict[str, object]] = []
    all_valid = True
    for j, source in enumerate(lparts):
        formal_goal = formal_image_goal(source.generator)
        available = (
            expand_canonical_formal_image(formal_goal)
            if formal_goal is not None else ()
        )
        admissible = bool(
            len(available) == 1
            and available[0].subgoals == ()
            and available[0].rule.match_guard((), {})
        )
        all_valid = all_valid and admissible
        kind = _component_kind(source)
        possible = tuple(
            index for index in residual
            if _component_kind(targets[index]) == kind
        )
        if not possible:
            all_valid = False
        rows.append({
            "source_index": j,
            "source_generator": str(source.generator),
            "formal_target_generator": (
                str(canonical_formal_suspension(source.generator))
                if formal_goal is not None else None
            ),
            "formal_rule_admissible": admissible,
            "source_component_order": list(kind) if kind else None,
            "possible_named_target_indices_by_order_only": list(possible),
            "named_target_identification_proved": False,
        })
    row["canonical_formal_images"] = rows
    row["all_formal_rules_admissible"] = all_valid
    row["residual_target_count"] = len(residual)
    row["state"] = (
        "FORMAL_IMAGES_AVAILABLE_NAMED_IDENTITIES_PENDING"
        if all_valid and rows else
        "NO_LEFT_GENERATOR_IMAGE_OBLIGATIONS"
        if all_valid else
        "FORMAL_IMAGE_OR_COMPONENT_CHECK_PENDING"
    )
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected repository root")
    result = tuple(inspect_k(k) for k in (4, 7, 8, 31))
    report = {
        "phase": "173-R4-R15R3",
        "mode": "FORMAL_TYPED_SUSPENSION_IMAGE_ONLY",
        "rows": result,
        "public_completion": False,
        "named_equalities_are_not_derived": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for row in result:
        count = len(row["canonical_formal_images"])
        print(
            f"PHASE173_R4_R15R3_K={row['k']} "
            f"FORMAL_IMAGES={count} "
            f"RULES={row.get('all_formal_rules_admissible', False)} "
            f"NAMED_PROVED={row['named_generator_identifications_proved']} "
            f"STATE={row['state']}",
            flush=True,
        )
    k31 = result[-1]
    passed = (
        k31["abstract_compatible"] is True
        and len(k31["canonical_formal_images"]) == 4
        and k31.get("all_formal_rules_admissible") is True
        and k31["named_generator_identifications_proved"] == 0
        and all(
            len(item["possible_named_target_indices_by_order_only"]) == 4
            for item in k31["canonical_formal_images"]
        )
    )
    print("PHASE173_R4_R15R3_K31_FORMAL_IMAGES=" + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R3_NO_NAMED_IMAGE_ASSUMPTION=True", flush=True)
    print("PHASE173_R4_R15R3_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R3_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `preflight.py`

```python
"""Exact source and reviewed commit-lineage guard for R15R3 read-only work."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess


REVIEWED_HEAD = "c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5"
REVIEWED_BLOBS = {
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
    "phase173_r4_r15r1_unbounded_abstract_frontier/frontier.py": "efba543568e46e5b8303ee3ee794508213e2ee27",
}
AUDIT_PATH = "phase173_r4_r15r2_generator_obligation_audit/audit.py"
AUDIT_SHA256 = "9fbf9af9c4218a8ba019ce8fd131890e83a1392e6f0b9cd5f93d383d68305884"
ALLOWED_COMMITTED_PREFIX = "phase173_r4_r15r2_generator_obligation_audit/"
ALLOWED_DIRTY_FILES = {".pytest_cache/v/cache/nodeids"}


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", *arguments), cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + ": " + result.stderr[:500]
        )
    return result.stdout.strip()


def normalized(value: bytes) -> bytes:
    """Permit Windows CRLF without loosening substantive source guards."""
    return value.replace(b"\r\n", b"\n")


def git_bytes(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ("git", *arguments), cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("Cannot read reviewed Git bytes: " + " ".join(arguments))
    return result.stdout


def guarded_descendant_paths(paths: tuple[str, ...]) -> bool:
    """Permit only the prior audit package and harmless test-cache history."""
    return all(
        item == ".pytest_cache/v/cache/nodeids"
        or item.startswith(ALLOWED_COMMITTED_PREFIX)
        for item in paths
    )


def preflight(root: Path) -> None:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Not the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local/remote develop differs")
    # A later audit-only commit must not invalidate a source-reviewed phase.
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed_paths = tuple(filter(
        None, git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()
    ))
    if not guarded_descendant_paths(committed_paths):
        raise RuntimeError("Unreviewed committed changes: " + str(committed_paths))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    if dirty - ALLOWED_DIRTY_FILES:
        raise RuntimeError("Tracked source modifications require review")
    for name, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("Committed dependency changed: " + name)
        if not (root / name).is_file():
            raise RuntimeError("Missing dependency: " + name)
        if normalized((root / name).read_bytes()) != normalized(
            git_bytes(root, "show", "HEAD:" + name)
        ):
            raise RuntimeError("Local dependency modified: " + name)
    previous_audit = root / AUDIT_PATH
    if not previous_audit.is_file():
        raise RuntimeError("R15R2 audit is required")
    digest = hashlib.sha256(normalized(previous_audit.read_bytes())).hexdigest()
    if digest != AUDIT_SHA256:
        raise RuntimeError("R15R2 audit changed: " + digest)
    print("PHASE173_R4_R15R3_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R3_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R3_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R3_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    preflight(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 Git fetch failed' }
    python -m phase173_r4_r15r3_formal_suspension_bridge.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 Preflight failed' }
    python -m pytest -q `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_static.py `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R3_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R3_PRODUCTION_EDIT=NONE'
        exit 0
    }
    python -m pytest -q `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R3_FOCUSED_PYTEST=PASS'
    python -m phase173_r4_r15r3_formal_suspension_bridge.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'formal_image_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R3 audit failed' }
    Write-Output 'PHASE173_R4_R15R3_PUBLIC_COMPLETION=False'
    Write-Output 'PHASE173_R4_R15R3_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
```

## `tests/__init__.py`

```python
"""Focused tests for R15R3."""
```

## `tests/test_bridge.py`

```python
"""Focused typed tests; canonical formal images are not named identities."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from phase173_r4_r15r3_formal_suspension_bridge.bridge import (
    canonical_formal_suspension,
    expand_canonical_formal_image,
    formal_image_goal,
    is_canonical_formal_image,
)
from phase173_r4_r15r3_formal_suspension_bridge.audit import inspect_k


def element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(
        name=name, dimension=target, source=source, target=target,
        generator=GeneratorSymbol(family=name),
    )


def test_nested_compositions_have_unbounded_formal_suspension() -> None:
    first = element("a", 28, 3)
    second = element("b", 32, 28)
    third = element("c", 34, 32)
    source = Composition(first, Composition(second, third))
    image = canonical_formal_suspension(source)
    assert image == Composition(
        IteratedSuspension(first, 1),
        Composition(IteratedSuspension(second, 1), IteratedSuspension(third, 1)),
    )
    assert typed_element_span(source) == (34, 3)
    assert typed_element_span(image) == (35, 4)
    goal = formal_image_goal(source)
    assert goal == GeneratorImage(
        map=TodaSuspensionMap(TodaPrimaryGroup(34, 3), TodaPrimaryGroup(35, 4)),
        source_generator=source, target_generator=image,
    )
    assert is_canonical_formal_image(goal)
    options = expand_canonical_formal_image(goal)
    assert len(options) == 1
    assert options[0].subgoals == ()
    assert options[0].rule.match_guard((), {}) is True
    assert options[0].rule.literature_reference is None


def test_formal_rule_rejects_forged_named_generator_and_wrong_map() -> None:
    source = element("unstable", 34, 3)
    goal = formal_image_goal(source)
    assert goal is not None
    forged = replace(goal, target_generator=element("unrelated", 35, 4))
    assert not is_canonical_formal_image(forged)
    assert expand_canonical_formal_image(forged) == ()
    wrong = replace(goal, map=TodaSuspensionMap(
        TodaPrimaryGroup(34, 3), TodaPrimaryGroup(36, 4),
    ))
    assert not is_canonical_formal_image(wrong)
    assert expand_canonical_formal_image(wrong) == ()


def test_reject_ill_typed_compositions_and_unrelated_objects() -> None:
    a = element("a", 28, 3)
    b = element("b", 34, 4)
    assert canonical_formal_suspension(Composition(a, b)) is None
    assert formal_image_goal(Composition(a, b)) is None
    assert expand_canonical_formal_image("not a typed generator image") == ()


@pytest.mark.parametrize("k,expected_count", ((4, 1), (7, 0), (8, 1), (31, 4)))
def test_real_database_formal_frontier_is_not_named_proof(
    k: int, expected_count: int,
) -> None:
    row = inspect_k(k)
    assert row["abstract_compatible"] is True
    assert row["group_proof_completed"] is False
    assert row["new_given_assertions"] == 0
    assert row["public_route_modified"] is False
    assert row["named_generator_identifications_proved"] == 0
    assert len(row["canonical_formal_images"]) == expected_count
    assert row["all_formal_rules_admissible"] is True


def test_k31_does_not_guess_permutation_of_four_equal_order_targets() -> None:
    row = inspect_k(31)
    assert row["state"] == "FORMAL_IMAGES_AVAILABLE_NAMED_IDENTITIES_PENDING"
    assert row["residual_target_count"] == 4
    assert len(row["canonical_formal_images"]) == 4
    for item in row["canonical_formal_images"]:
        assert item["formal_rule_admissible"] is True
        assert item["possible_named_target_indices_by_order_only"]
        assert len(item["possible_named_target_indices_by_order_only"]) == 4
        assert item["named_target_identification_proved"] is False
```

## `tests/test_bridge_isolated.py`

```python
"""Executable pure-rule tests with substitute types, not substitute evidence."""
from __future__ import annotations

from dataclasses import dataclass, replace
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest


@pytest.fixture
def isolated_bridge(monkeypatch: pytest.MonkeyPatch):
    @dataclass(frozen=True)
    class HomotopyElement:
        name: str
        dimension: int
        source: int
        target: int

    @dataclass(frozen=True)
    class IteratedSuspension:
        expression: object
        exponent: int

    @dataclass(frozen=True)
    class Composition:
        left: object
        right: object

    @dataclass(frozen=True)
    class TodaPrimaryGroup:
        group_dimension: int
        sphere_dimension: int

    @dataclass(frozen=True)
    class TodaSuspensionMap:
        source_group: TodaPrimaryGroup
        target_group: TodaPrimaryGroup

    @dataclass(frozen=True)
    class GeneratorImage:
        map: TodaSuspensionMap
        source_generator: object
        target_generator: object

    @dataclass(frozen=True)
    class InferenceRule:
        name: str
        description: str
        premise_patterns: tuple
        match_guard: object
        conclusion_pattern: object

    @dataclass(frozen=True)
    class GoalExpansion:
        rule: InferenceRule
        subgoals: tuple

    def typed_element_span(value: object):
        if isinstance(value, HomotopyElement):
            return (value.source, value.target) if (
                type(value.dimension) is int and value.dimension == value.target
                and value.source >= value.target >= 2
            ) else None
        if isinstance(value, IteratedSuspension):
            span = typed_element_span(value.expression)
            return ((span[0] + value.exponent, span[1] + value.exponent)
                    if span and type(value.exponent) is int and value.exponent >= 0
                    else None)
        if isinstance(value, Composition):
            left, right = typed_element_span(value.left), typed_element_span(value.right)
            return (right[0], left[1]) if (
                left is not None and right is not None and left[0] == right[1]
            ) else None
        return None

    mapping = {
        "expression": (Composition, HomotopyElement, IteratedSuspension),
        "homotopy_groups": (TodaPrimaryGroup, TodaSuspensionMap),
        "phase165_r14_r6_generic_iso": (GeneratorImage,),
        "phase165_r3_recursive_search": (GoalExpansion,),
        "phase169_r10eq_r1_universal_stable_definition.definition": (typed_element_span,),
        "proof": (InferenceRule,),
    }
    parent = ModuleType("phase169_r10eq_r1_universal_stable_definition")
    parent.__path__ = []
    monkeypatch.setitem(sys.modules, parent.__name__, parent)
    for name, items in mapping.items():
        module = ModuleType(name)
        for item in items:
            setattr(module, item.__name__, item)
        monkeypatch.setitem(sys.modules, name, module)
    path = Path(__file__).resolve().parents[1] / "bridge.py"
    spec = importlib.util.spec_from_file_location("_phase173_r4_r15r3_isolated_bridge", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return SimpleNamespace(
        module=module,
        HomotopyElement=HomotopyElement,
        Composition=Composition,
        IteratedSuspension=IteratedSuspension,
        TodaSuspensionMap=TodaSuspensionMap,
        TodaPrimaryGroup=TodaPrimaryGroup,
        GeneratorImage=GeneratorImage,
        span=typed_element_span,
    )


def test_arbitrary_unstable_composition_formal_images(isolated_bridge) -> None:
    t = isolated_bridge
    a = t.HomotopyElement("delta_3", 3, 27, 3)
    b = t.HomotopyElement("sigma_27", 27, 34, 27)
    source = t.Composition(a, b)
    formal = t.module.canonical_formal_suspension(source)
    assert formal == t.Composition(t.IteratedSuspension(a, 1), t.IteratedSuspension(b, 1))
    assert t.span(formal) == (35, 4)
    goal = t.module.formal_image_goal(source)
    assert goal.map == t.TodaSuspensionMap(
        t.TodaPrimaryGroup(34, 3), t.TodaPrimaryGroup(35, 4)
    )
    assert t.module.is_canonical_formal_image(goal)
    options = t.module.expand_canonical_formal_image(goal)
    assert len(options) == 1
    assert options[0].subgoals == ()
    assert options[0].rule.match_guard((), {}) is True


def test_wrong_named_image_and_map_are_refused(isolated_bridge) -> None:
    t = isolated_bridge
    a = t.HomotopyElement("phi_prime", 3, 28, 3)
    goal = t.module.formal_image_goal(a)
    named = t.HomotopyElement("unrelated", 4, 29, 4)
    forged = replace(goal, target_generator=named)
    assert t.module.expand_canonical_formal_image(forged) == ()
    wrong_map = replace(goal, map=t.TodaSuspensionMap(
        t.TodaPrimaryGroup(28, 3), t.TodaPrimaryGroup(30, 4)
    ))
    assert t.module.expand_canonical_formal_image(wrong_map) == ()


def test_ill_typed_composition_not_accepted(isolated_bridge) -> None:
    t = isolated_bridge
    a = t.HomotopyElement("a", 3, 27, 3)
    b = t.HomotopyElement("b", 4, 34, 4)
    invalid = t.Composition(a, b)
    assert t.module.canonical_formal_suspension(invalid) is None
    assert t.module.formal_image_goal(invalid) is None
```

## `tests/test_static.py`

```python
"""Standalone structural guard tests; runnable without the project repository."""
from __future__ import annotations

import ast
from pathlib import Path

from phase173_r4_r15r3_formal_suspension_bridge import preflight


PACKAGE = Path(__file__).resolve().parents[1]


def test_source_syntax_and_no_production_patch() -> None:
    for name in ("bridge.py", "audit.py", "preflight.py"):
        ast.parse((PACKAGE / name).read_text(encoding="utf-8"))
    assert not (PACKAGE / "install.py").exists()


def test_stable_family_identity_is_not_assumed() -> None:
    source = (PACKAGE / "bridge.py").read_text(encoding="utf-8")
    assert "IteratedSuspension(expression=expression, exponent=1)" in source
    assert "is_canonical_formal_image(statement)" in source
    assert "source and target are definitionally" not in source
    assert "literature_reference=" not in source


def test_named_generator_identifications_never_promoted() -> None:
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert '"named_generator_identifications_proved": 0' in source
    assert '"group_proof_completed": False' in source
    assert '"new_given_assertions": 0' in source
    assert '"public_completion": False' in source


def test_only_audit_package_is_allowed_in_new_commits() -> None:
    assert preflight.guarded_descendant_paths(())
    assert preflight.guarded_descendant_paths((
        "phase173_r4_r15r2_generator_obligation_audit/audit.py",
        ".pytest_cache/v/cache/nodeids",
    ))
    assert not preflight.guarded_descendant_paths((
        "phase173_r4_r10_general_toda56_core/core.py",
    ))
    assert not preflight.guarded_descendant_paths((
        "phase173_r4_r15r2_generator_obligation_audit/audit.py",
        "proof.py",
    ))


def test_dependencies_are_pinned_to_reviewed_r15r1_core() -> None:
    assert preflight.REVIEWED_HEAD == "c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5"
    assert preflight.REVIEWED_BLOBS["phase173_r4_r10_general_toda56_core/core.py"] == (
        "d35600804ecbbc5f8566d52e45a2f6ecf8816347"
    )
    assert preflight.AUDIT_SHA256 == (
        "9fbf9af9c4218a8ba019ce8fd131890e83a1392e6f0b9cd5f93d383d68305884"
    )
```
