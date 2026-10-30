# Phase 171 R2J-R4-R9-R7 — コード・import・関数・テスト全文

変更対象は新規パッケージ全ファイルと `phase165_r52_r9_shared_math.py` 内の `shared_expansion_provider()` のみ。実行時に現行の既存関数全文を構造検査して置換し、`output/shared_expansion_provider_FULL.py` に完全な関数を出力する。既存トップレベル import は一切変更しない。

## source.py

```python
"""Source-anchored backward proposals for finite order-four cyclic presentations.

This proposer never derives an order or returns a ProofStep. It proposes two
subgoals only when a typed cited double relation identifies a candidate
for the generator of the requested group. All subgoals must be proved by the
normal recursive engine. No dimensions, generator names, or source IDs are
hard-coded in the rule.
"""
from __future__ import annotations

from expression import HomotopyElement, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10e5_composite_generator_image.rule import _endpoints
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase171_r2j_r4_r8_cyclic_structure.source import (
    expand_cyclic_group_from_full_element_order,
)
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def expand_cited_double_cyclic_root(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer a generic order-four root obligation, not an assumed group result.

    A screened fixed 2*x=... citation only identifies x; it does NOT prove
    2*x nonzero, order(x)=4, or cardinality of the group. Those are separate
    required inferences with their own registered source ancestry.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (
        not isinstance(goal, Relation)
        or goal.relation_type is not RelationType.EQUALITY
        or not isinstance(goal.lhs, TodaPrimaryGroup)
        or not isinstance(goal.rhs, FiniteCyclicGroup)
        or type(goal.rhs.order) is not int
        or goal.rhs.order != 4
    ):
        return ()
    dimensions = (goal.lhs.group_dimension, goal.lhs.sphere_dimension)
    candidates: list[GoalExpansion] = []
    for claim in available:
        if (
            not isinstance(claim, Relation)
            or claim.relation_type is not RelationType.EQUALITY
            or not isinstance(claim.lhs, Multiple)
            or type(claim.lhs.coefficient) is not int
            or claim.lhs.coefficient != 2
            or not isinstance(claim.lhs.expression, HomotopyElement)
            or _endpoints(claim.lhs.expression) != dimensions
            or claim.rhs is None
        ):
            continue
        candidate = FiniteCyclicGroup(4, claim.lhs.expression)
        if (
            candidate != goal.rhs
            and not same_registered_group_presentation(candidate, goal.rhs)
        ):
            continue
        cardinality = FiniteGroupCardinality(goal.lhs, 4)
        element_order = FiniteElementOrder(goal.lhs, claim.lhs.expression, 4)
        routes = expand_cyclic_group_from_full_element_order(
            goal, cardinality, element_order,
        )
        if len(routes) != 1:
            continue
        if not any(
            existing.subgoals == routes[0].subgoals
            and existing.rule.name == routes[0].rule.name
            for existing in candidates
        ):
            candidates.append(routes[0])
    # Multiple incompatible cited candidates must not be resolved by an
    # arbitrary source or by a database-presentation guess.
    return tuple(candidates) if len(candidates) == 1 else ()

```

## install.py

```python
"""One-function guarded shared-provider patch and full-code export."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
ANCHOR = "        options.extend(expand_finite_cyclic_relation(goal))\n"
ADDITION = (
    "        from phase171_r2j_r4_r9_r7_public_cyclic_root.source import (\n"
    "            expand_cited_double_cyclic_root,\n"
    "        )\n"
    "        options.extend(expand_cited_double_cyclic_root(goal, tuple(available)))\n"
)


def _git(*args: str) -> str:
    if args not in {
        ("branch", "--show-current"),
        ("status", "--porcelain", "--untracked-files=no"),
        ("rev-parse", "HEAD"),
    }:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()


def _function_text(source: str) -> str:
    tree = ast.parse(source)
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise RuntimeError("expected one shared_expansion_provider function")
    node = functions[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def install(*, dry_run: bool) -> bool:
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared math provider missing")
    original_bytes = TARGET.read_bytes()
    prefix = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
    raw = original_bytes[len(prefix):]
    if b"\r\n" in raw:
        newline = "\r\n"
    else:
        newline = "\n"
    content = raw.decode("utf-8").replace("\r\n", "\n")
    if content.count(ANCHOR) != 1:
        raise RuntimeError("shared provider hook anchor missing or ambiguous")
    already = ADDITION in content
    if already:
        proposed = content
        state = "ALREADY_INSTALLED"
    else:
        if "phase171_r2j_r4_r9_r7_public_cyclic_root.source" in content:
            raise RuntimeError("partial/unknown prior hook detected")
        # Refuse to overlay pre-existing tracked changes.
        if _git("status", "--porcelain", "--untracked-files=no"):
            raise RuntimeError("tracked worktree must be clean before patch")
        proposed = content.replace(ANCHOR, ANCHOR + ADDITION, 1)
        state = "READY_TO_PATCH"
    # Confirm the generated hook is INSIDE the intended function.
    function = _function_text(proposed)
    if ADDITION not in function:
        raise RuntimeError("insertion escaped shared_expansion_provider")
    if proposed.count(ADDITION) != 1:
        raise RuntimeError("duplicate provider hook")
    ast.parse(proposed)
    print("PHASE171_R2J_R4_R9_R7_HEAD=" + _git("rev-parse", "HEAD"), flush=True)
    print("PHASE171_R2J_R4_R9_R7_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R7_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if not already:
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original_bytes)
        TARGET.write_bytes(prefix + proposed.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R7_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    # Full replacement units as requested by the project development rules.
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        function + "\n", encoding="utf-8",
    )
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R7_FULL_FUNCTION=" + str(
        OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R7_FULL_FILE=" + str(
        OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return not already


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

```

## audit.py

```python
"""Measure real shared-provider root integration and public search state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r1_public_path_audit.audit import has_exact_root_route
from phase171_r2j_r4_r9_r7_public_cyclic_root.source import expand_cited_double_cyclic_root
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
    }
    if args not in permitted:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()


def inspect_public_root() -> dict:
    screened, goal, _ = _screened_context()
    root, _, report = build_cyclic_pi63_proof()
    if root.rule is not ProofRule.INFERENCE or report["new_given_added"] != 0:
        raise RuntimeError("R4-R8 original root is not independently proved")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    candidates = expand_cited_double_cyclic_root(goal, available)
    if not has_exact_root_route(candidates, root):
        raise RuntimeError("source-anchored generic root did not match R4-R8")
    public = shared_expansion_provider(screened, proof_target=goal)(goal)
    if not has_exact_root_route(public, root):
        raise RuntimeError("new generic root is absent from shared provider")
    # Observe the real public engine; no results or inferred ProofSteps injected.
    actual = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=goal,
    )
    return {
        "phase": "171-R2J-R4-R9-R7",
        "mode": "GENERIC_PUBLIC_ROOT_CONNECTION_ONLY",
        "source_anchored_root_options": len(candidates),
        "shared_root_expansion_count": len(public),
        "shared_root_connected": True,
        "target": repr(goal),
        "root_rule_name": root.inference_rule.name,
        "canonical_public_status": actual.status.value,
        "public_complete": actual.status.value == "complete" and actual.conclusion == goal,
        "open_goals": [repr(x)[:900] for x in actual.open_goals[:15]],
        "diagnostics": list(actual.diagnostics[:15]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "trust_boundary_modified": False,
        "web_modified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print("PHASE171_R2J_R4_R9_R7_BRANCH=" + _git("branch", "--show-current"), flush=True)
    print("PHASE171_R2J_R4_R9_R7_HEAD=" + _git("rev-parse", "HEAD"), flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R7_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_root()
    OUTPUT.mkdir(exist_ok=True)
    dest = OUTPUT / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R7_SOURCE_ANCHORED_ROOT=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R7_SHARED_ROOT_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R7_PUBLIC_SEARCH=" + report["canonical_public_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R7_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    print("PHASE171_R2J_R4_R9_R7_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R7_REPORT=" + str(dest), flush=True)
    print("PHASE171_R2J_R4_R9_R7_RESULT=PASS_ROOT_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()

```

## tests/test_audit.py

```python
"""Focused generic root and production-connection checks."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase171_r2j_r4_r9_r7_public_cyclic_root.source import expand_cited_double_cyclic_root
from proof import Relation, RelationType


def _case():
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    registered = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family=r"\nu'"),
    )
    source = Relation(Multiple(2, nu), "cited typed RHS", RelationType.EQUALITY)
    goal = Relation(TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, registered), RelationType.EQUALITY)
    return source, goal


def test_generic_source_anchored_root_is_a_premise_proposal_only():
    source, goal = _case()
    proposals = expand_cited_double_cyclic_root(goal, (source,))
    assert len(proposals) == 1
    route = proposals[0]
    assert route.rule.name == "finite group generated by an element of full order"
    assert len(route.subgoals) == 2
    assert route.subgoals[0].group == goal.lhs
    assert route.subgoals[0].order == 4
    assert route.subgoals[1].element == source.lhs.expression
    assert route.subgoals[1].order == 4


def test_missing_source_or_mismatching_generator_does_not_offer_route():
    source, goal = _case()
    assert expand_cited_double_cyclic_root(goal, ()) == ()
    wrong = replace(source.lhs.expression, generator=GeneratorSymbol(family="σ", index=8))
    assert expand_cited_double_cyclic_root(goal, (replace(source, lhs=Multiple(2, wrong)),)) == ()


def test_wrong_domain_and_wrong_coefficient_are_rejected():
    source, goal = _case()
    wrong = replace(source.lhs.expression, source=7)
    assert expand_cited_double_cyclic_root(goal, (replace(source, lhs=Multiple(2, wrong)),)) == ()
    assert expand_cited_double_cyclic_root(goal, (replace(source, lhs=Multiple(3, source.lhs.expression)),)) == ()


def test_no_alias_order_guess_or_other_cardinality():
    source, goal = _case()
    alt = replace(goal, rhs=FiniteCyclicGroup(8, goal.rhs.generator))
    assert expand_cited_double_cyclic_root(alt, (source,)) == ()
    assert expand_cited_double_cyclic_root(replace(goal, relation_type=RelationType.INEQUALITY), (source,)) == ()


def test_rejects_invalid_source_container():
    _, goal = _case()
    with pytest.raises(TypeError):
        expand_cited_double_cyclic_root(goal, [])


def test_duplicate_equivalent_sources_do_not_duplicate_options():
    source, goal = _case()
    assert len(expand_cited_double_cyclic_root(goal, (source, source))) == 1


def test_real_shared_provider_has_exact_inferred_root():
    from phase171_r2j_r4_r9_r7_public_cyclic_root.audit import inspect_public_root
    report = inspect_public_root()
    assert report["shared_root_connected"] is True
    assert report["new_given_added"] == 0
    assert report["completed_proof_imported"] is False
    assert report["trust_boundary_modified"] is False


def test_existing_scoped_search_still_certifies_full_result():
    from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit import audit_second_source_bound_hopf
    report = audit_second_source_bound_hopf()
    assert report["scoped_search_complete"] is True
    assert report["trust_boundary_accepted"] is True
    assert report["new_given_added"] == 0

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'EHP Git root required' }
    python -B -m phase171_r2j_r4_r9_r7_public_cyclic_root.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R7 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R7_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r7_public_cyclic_root.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R7 guarded patch failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r7_public_cyclic_root\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r6_source_bound_cited_hopf\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R7 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R7_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r7_public_cyclic_root.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R7 public root audit failed' }
} finally {
    Pop-Location
}

```

## README.md

```markdown
# EHP Proof Tracer — Phase 171 R2J-R4-R9-R7

## Scope

Introduce exactly one source-anchored, generic root backward proposal for finite order-four cyclic goals. A screened typed double relation identifies a possible generator, but the proposed `FiniteGroupCardinality` and `FiniteElementOrder` remain **unproved subgoals**. They must be reconstructed by the existing canonical engine and cannot be supplied as completed `ProofStep`s. No proof result, `GIVEN` leaf, or purported citation is added.

This phase modifies only the existing function `shared_expansion_provider()` in `phase165_r52_r9_shared_math.py` and introduces `phase171_r2j_r4_r9_r7_public_cyclic_root/` containing the proposer, guarded installer, audit and tests. The existing root rule and all existing Hopf, EHP, proof trust, renderer and Web APIs are unchanged.

## Before applying

The reference repository was reviewed on GitHub `akebono03/ehp-proof-tracer` `develop` at `54a372a9370404d65d42a5b8d8693c8f64de2b03`. An installer checks the branch, unchanged tracked files, a unique existing hook anchor, parses the entire resulting module, and refuses a partial prior installation. It preserves the original line-ending convention. Dry-run does not mutate files.

## Run (Windows PowerShell)

Unzip the package at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r7_public_cyclic_root\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r7_public_cyclic_root\run.ps1"
git status -sb
git diff --stat
```

The installer writes the **complete** post-change `shared_expansion_provider` function to `output/shared_expansion_provider_FULL.py` and the full amended source file to `output/phase165_r52_r9_shared_math.FULL.py`; it also saves a complete pre-change backup. Focused tests only; full pytest is deferred until Phase closeout.

## Completion criteria and phase boundary

The newly registered public root proposal must match R4-R8's inferred root, must be backed by a screened typed double relation, and must not contain a precompleted proof step. The real public search status and unresolved subgoals are reported, without claiming complete Web output. Later phases must connect missing subgoal expansions (if any), the two source-bound Hopf obligations, and independently verify public Web provenance before a public-complete claim.

```

## 監査仕様.md

```markdown
# Phase 171 R2J-R4-R9-R7 — 公開 Root Expansion の最小接続

## 現状と目的

R4-R9-R6 の独立した限定探索は `complete` となり、Trust Boundary（信頼境界）も受理された。しかし本番の `shared_expansion_provider()` は、R4-R8 の最終巡回群規則を公開候補として生成できない。本パッケージはその最初の候補を、既存の型付き数学規則と先行する出典だけから生成する。

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` 関数だけ。関数内の `expand()` に候補生成の2文を追加。トップレベル import、他関数、クラスは不変。
- 新規 `phase171_r2j_r4_r9_r7_public_cyclic_root/source.py`：`expand_cited_double_cyclic_root()` を新設。`Relation`, `Multiple`, `FiniteCyclicGroup` の型検査・次数検査・既存の HyoujiGen 同一性照合を行う。位数4は候補の対象であり数学的証明とは扱わない。
- 新規 `install.py`：`install()`、`main()`、ヘルパーを新設。ガード付き置換と関数全文の書き出し。
- 新規 `audit.py`：`inspect_public_root()`、`main()`、Git 読み取り処理を新設。
- 新規 `tests/test_audit.py`：8件の限定テスト。
- 新規 README（英語）、本監査仕様、全文コード文書、実行スクリプト。

## 信頼条件

1. `GIVEN` と `INFERENCE` を追加・偽装しない。生の二倍関係から群構造の証明を飛躍させない。
2. 完成済みの R4-R8 `ProofStep` を本番 Provider に取り込まない。監査での比較用途にのみ既存の独立した証明木を利用する。
3. 本番 Provider の公開変更は Root Expansion 追加のみ。Hopf の出典拘束などは未接続とみなす。
4. 既存の出典選別と Trust Boundary を変更しない。
5. `pytest` は限定テストのみ。全体テストは Phase 終了時に実施。

## 実行後の全文

`output/shared_expansion_provider_FULL.py` に変更後の**関数全体**、`output/phase165_r52_r9_shared_math.FULL.py` に変更後の**ファイル全体**、`output/phase165_r52_r9_shared_math.BEFORE.py` に変更前の**ファイル全体**が出力される。省略表現は使用しない。

## 完了条件

`SOURCE_ANCHORED_ROOT=PASS`、`SHARED_ROOT_CONNECTED=True`、`NEW_GIVEN=0`。`PUBLIC_SEARCH` は実測値として扱い、`partial` の場合に完成を宣言しない。次段階は他の推論前提の一般的な逆方向探索接続であり、Web への完成判定を先取りしない。

```
