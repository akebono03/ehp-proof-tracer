# Phase 171 R2J-R4-R9-R8 — 完全コード・import・テスト一覧

既存 `phase165_r52_r9_shared_math.py` のトップレベル import は変更しない。修正は既存 `shared_expansion_provider()` の内部関数 `expand()` に4行追加するのみ。
変更後の関数・ファイル全文はインストーラーが現行ソースを保ったまま `output/shared_expansion_provider_FULL.py` と `output/phase165_r52_r9_shared_math.FULL.py` に出力する。

## 既存関数に挿入する4行（R7 呼出しの直後）

```python
        from phase171_r2j_r4_r9_r8_public_cardinality.source import (
            expand_cited_ehp_middle_cardinality,
        )
        options.extend(expand_cited_ehp_middle_cardinality(goal, tuple(available)))
```

## source.py

```python
"""Source-anchored, generic EHP middle-cardinality backward expansion.

This module creates proof obligations, never mathematical GIVEN steps. Both
finite end-group candidates come from earlier screened fixed statements or
checked specialization of a screened symbolic statement; the short exact
sequence and all end-group claims must be independently proved by search.
"""
from __future__ import annotations

from homotopy_groups import (
    FiniteCyclicGroup,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    specialize_eta_group_relation,
)
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    EHPShortExactSequence,
    expand_ehp_short_exact,
)
from phase171_r2j_r4_r6_middle_cardinality.source import (
    FiniteGroupCardinality,
    expand_finite_cardinality_from_short_exact,
)
from proof import Relation, RelationType


def _unique_relations(candidates: tuple[object, ...]) -> tuple[Relation, ...]:
    """Keep different typed presentations distinct, dropping identical copies."""
    distinct: list[Relation] = []
    for candidate in candidates:
        if not (
            isinstance(candidate, Relation)
            and candidate.relation_type is RelationType.EQUALITY
            and isinstance(candidate.lhs, TodaPrimaryGroup)
            and isinstance(candidate.rhs, FiniteCyclicGroup)
            and type(candidate.rhs.order) is int
            and candidate.rhs.order > 0
        ):
            continue
        if candidate not in distinct:
            distinct.append(candidate)
    return tuple(distinct)


def _cited_finite_group_candidates(
    group: TodaPrimaryGroup, available: tuple[object, ...]
) -> tuple[Relation, ...]:
    """Select exact cited finite groups or an admissible cited eta schema.

    A specialized Relation is a search goal, not a proved conclusion. Its
    underlying source must still be admitted by the existing proof engine.
    """
    candidates: list[object] = []
    n = group.sphere_dimension
    for claim in available:
        if isinstance(claim, Relation) and claim.lhs == group:
            candidates.append(claim)
        if _is_generic_eta_group_relation(claim) and type(n) is int and n >= 4:
            specialized = specialize_eta_group_relation(claim, n)
            if specialized.lhs == group:
                candidates.append(specialized)
    return _unique_relations(tuple(candidates))


def expand_cited_ehp_middle_cardinality(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose |B|=|A||C| only with unique earlier typed end-group claims.

    Canonical EHP indices are derived from the goal group B=pi_q^n:
    A=pi_(q-1)^(n-1), C=pi_q^(2n-1). This is dimension-generic, not a
    special-case pi_6^3 proof or an import of a previously completed tree.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple of screened fixed claims")
    if not isinstance(goal, FiniteGroupCardinality):
        return ()
    middle = goal.group
    if not isinstance(middle, TodaPrimaryGroup):
        return ()
    q = middle.group_dimension
    n = middle.sphere_dimension
    if (
        type(q) is not int or type(n) is not int
        or type(goal.order) is not int or goal.order <= 0
        or n < 3 or q < max(n + 1, 2 * n - 1)
    ):
        return ()
    left_group = TodaPrimaryGroup(q - 1, n - 1)
    right_group = TodaPrimaryGroup(q, 2 * n - 1)
    sequence = EHPShortExactSequence(
        source_group=left_group,
        middle_group=middle,
        target_group=right_group,
        injection=TodaSuspensionMap(left_group, middle),
        projection=TodaHopfInvariantMap(middle, right_group),
    )
    # The existing typed EHP rule checks map indices and exactness shapes.
    if len(expand_ehp_short_exact(sequence)) != 1:
        return ()
    left = _cited_finite_group_candidates(left_group, available)
    right = _cited_finite_group_candidates(right_group, available)
    if len(left) != 1 or len(right) != 1:
        return ()
    options = expand_finite_cardinality_from_short_exact(
        goal, left[0], sequence, right[0],
    )
    if len(options) != 1 or options[0].subgoals != (left[0], sequence, right[0]):
        return ()
    return options
```

## install.py

```python
"""Guarded single-function provider patch; preserve an uncommitted R9-R7 patch."""
from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
PATH_IN_GIT = "phase165_r52_r9_shared_math.py"
REVIEWED_ORIGINAL_BLOB_SHA = "68846671215c38e3e0a572932b8ed955a7880edc"
R7_HOOK = (
    "        from phase171_r2j_r4_r9_r7_public_cyclic_root.source import (\n"
    "            expand_cited_double_cyclic_root,\n"
    "        )\n"
    "        options.extend(expand_cited_double_cyclic_root(goal, tuple(available)))\n"
)
R8_HOOK = (
    "        from phase171_r2j_r4_r9_r8_public_cardinality.source import (\n"
    "            expand_cited_ehp_middle_cardinality,\n"
    "        )\n"
    "        options.extend(expand_cited_ehp_middle_cardinality(goal, tuple(available)))\n"
)


def _git(*args: str) -> bytes:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
        ("show", f"HEAD:{PATH_IN_GIT}"),
    }
    if args not in permitted:
        raise ValueError("only reviewed read-only Git commands are permitted")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def _clean_text(blob: bytes) -> str:
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _git_blob_sha(blob: bytes) -> str:
    header = f"blob {len(blob)}\0".encode("ascii")
    return hashlib.sha1(header + blob).hexdigest()


def _function_text(source: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one shared_expansion_provider function")
    node = matches[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def install(*, dry_run: bool) -> bool:
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("existing shared provider is missing")
    head_bytes = _git("show", f"HEAD:{PATH_IN_GIT}")
    head_text = _clean_text(head_bytes)
    # Ensure this is still the exact GitHub-reviewed module, whether the
    # previous four-line R7 patch was committed or remains uncommitted.
    if head_text.count(R7_HOOK) > 1 or R8_HOOK in head_text:
        raise RuntimeError("unknown previously committed provider hook")
    if R7_HOOK in head_text:
        newline = "\r\n" if b"\r\n" in head_bytes else "\n"
        reviewed_blob = head_bytes.replace(R7_HOOK.replace("\n", newline).encode(), b"")
    else:
        reviewed_blob = head_bytes
    if _git_blob_sha(reviewed_blob) != REVIEWED_ORIGINAL_BLOB_SHA:
        raise RuntimeError("Git HEAD provider differs from GitHub-reviewed baseline")
    original_bytes = TARGET.read_bytes()
    content = _clean_text(original_bytes)
    expected = head_text if R7_HOOK in head_text else head_text.replace(
        "        options.extend(expand_finite_cyclic_relation(goal))\n",
        "        options.extend(expand_finite_cyclic_relation(goal))\n" + R7_HOOK,
        1,
    )
    if R7_HOOK not in expected or expected.count(R7_HOOK) != 1:
        raise RuntimeError("reviewed R7 hook missing or ambiguous")
    if content == expected:
        state = "READY_TO_PATCH"
        next_text = content.replace(R7_HOOK, R7_HOOK + R8_HOOK, 1)
    elif content == expected.replace(R7_HOOK, R7_HOOK + R8_HOOK, 1):
        state = "ALREADY_INSTALLED"
        next_text = content
    else:
        raise RuntimeError("tracked provider has unknown changes; refusing overwrite")
    if next_text.count(R8_HOOK) != 1 or next_text.count(R7_HOOK) != 1:
        raise RuntimeError("R7/R8 hook duplicate or missing")
    function = _function_text(next_text)
    if R7_HOOK not in function or R8_HOOK not in function:
        raise RuntimeError("hook escaped the intended provider function")
    ast.parse(next_text)
    print("PHASE171_R2J_R4_R9_R8_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R8_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R8_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original_bytes)
        newline = "\r\n" if b"\r\n" in original_bytes else "\n"
        prefix = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(prefix + next_text.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R8_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(function + "\n", encoding="utf-8")
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R8_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R8_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    install(dry_run=arguments.dry_run)


if __name__ == "__main__":
    main()
```

## audit.py

```python
"""Audit real public cardinality expansion against independent R4-R6 evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r8_public_cardinality.source import (
    expand_cited_ehp_middle_cardinality,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
    }
    if args not in allowed:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()


def has_exact_proposal(options: tuple, reference: object) -> bool:
    """Check one existing inferred rule and its ordered typed subgoals."""
    return sum(
        option.rule.name == reference.inference_rule.name
        and option.subgoals == tuple(item.conclusion for item in reference.premises)
        for option in options
    ) == 1


def inspect_public_cardinality() -> dict:
    screened, target, _ = _screened_context()
    original_root, _, original_report = build_cyclic_pi63_proof()
    if (
        original_root.rule is not ProofRule.INFERENCE
        or original_root.conclusion != target
        or original_report["new_given_added"] != 0
    ):
        raise RuntimeError("original R4-R8 proof must be independently inferred")
    cardinality_step = original_root.premises[0]
    if cardinality_step.rule is not ProofRule.INFERENCE:
        raise RuntimeError("original middle-group cardinality was not inferred")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    derived_options = expand_cited_ehp_middle_cardinality(
        cardinality_step.conclusion, available,
    )
    if not has_exact_proposal(derived_options, cardinality_step):
        raise RuntimeError("generic end-group source candidates do not match R4-R6")
    shared = shared_expansion_provider(screened, proof_target=target)
    production_options = shared(cardinality_step.conclusion)
    if not has_exact_proposal(production_options, cardinality_step):
        raise RuntimeError("cardinality obligation is absent from the shared provider")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    return {
        "phase": "171-R2J-R4-R9-R8",
        "mode": "GENERIC_PUBLIC_CARDINALITY_CONNECTION_ONLY",
        "registered_group_goal": repr(target),
        "cardinality_goal": repr(cardinality_step.conclusion),
        "source_anchored_cardinality_routes": len(derived_options),
        "shared_cardinality_routes": len(production_options),
        "shared_cardinality_connected": True,
        "short_exact_subgoal": repr(derived_options[0].subgoals[1]),
        "left_end_group": repr(derived_options[0].subgoals[0]),
        "right_end_group": repr(derived_options[0].subgoals[2]),
        "public_search_status": public.status.value,
        "public_complete": public.status.value == "complete" and public.conclusion == target,
        "public_open_goals": [repr(item)[:1200] for item in public.open_goals[:15]],
        "public_diagnostics": list(public.diagnostics[:15]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "web_modified": False,
        "trust_boundary_modified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    print("PHASE171_R2J_R4_R9_R8_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R8_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R8_RESULT=PASS_DRY_RUN", flush=True)
        return
    result = inspect_public_cardinality()
    result["git_head"] = head
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R8_SOURCE_ANCHORED_CARDINALITY=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R8_SHARED_CARDINALITY_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R8_PUBLIC_SEARCH=" + result["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R8_PUBLIC_COMPLETE=" + str(result["public_complete"]), flush=True)
    if result["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R8_FIRST_OPEN_GOAL=" + result["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R8_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R8_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R8_RESULT=PASS_CARDINALITY_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
```

## tests/test_audit.py

```python
"""Focused regression tests for screened finite-cardinality backward goals."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r5_short_exact_sequence.source import EHPShortExactSequence
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r9_r8_public_cardinality.source import (
    _cited_finite_group_candidates,
    expand_cited_ehp_middle_cardinality,
)
from proof import ProofStep, Relation, RelationType


def _case():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    left = Relation(
        a,
        FiniteCyclicGroup(2, HomotopyElement(
            name="left", dimension=2, source=5, target=2,
            generator=GeneratorSymbol(family="η", index=2),
        )),
        RelationType.EQUALITY,
    )
    right = Relation(
        c,
        FiniteCyclicGroup(2, HomotopyElement(
            name="right", dimension=5, source=6, target=5,
            generator=GeneratorSymbol(family="η", index=5),
        )),
        RelationType.EQUALITY,
    )
    return FiniteGroupCardinality(b, 4), left, right


def test_end_groups_yield_only_one_typed_backward_obligation():
    goal, left, right = _case()
    proposals = expand_cited_ehp_middle_cardinality(goal, (left, right))
    assert len(proposals) == 1
    option = proposals[0]
    assert isinstance(option, GoalExpansion)
    assert option.rule.name == "finite middle-group cardinality from short exact sequence"
    assert option.subgoals[0] == left
    assert isinstance(option.subgoals[1], EHPShortExactSequence)
    assert option.subgoals[2] == right
    assert not any(isinstance(item, ProofStep) for item in option.subgoals)


def test_missing_or_wrong_group_source_fails_closed():
    goal, left, right = _case()
    assert expand_cited_ehp_middle_cardinality(goal, (left,)) == ()
    assert expand_cited_ehp_middle_cardinality(goal, (right,)) == ()
    wrong = replace(left, lhs=TodaPrimaryGroup(5, 3))
    assert expand_cited_ehp_middle_cardinality(goal, (wrong, right)) == ()


def test_product_order_must_be_proved_not_assumed():
    goal, left, right = _case()
    assert expand_cited_ehp_middle_cardinality(replace(goal, order=8), (left, right)) == ()
    wrong = replace(right, rhs=FiniteCyclicGroup(3, right.rhs.generator))
    assert expand_cited_ehp_middle_cardinality(goal, (left, wrong)) == ()


def test_ambiguous_end_group_presentations_fail_closed():
    goal, left, right = _case()
    ambiguous = replace(right, rhs=FiniteCyclicGroup(
        2, replace(right.rhs.generator, name="different"),
    ))
    assert expand_cited_ehp_middle_cardinality(goal, (left, right, ambiguous)) == ()


def test_duplicate_exact_sources_are_deduplicated():
    goal, left, right = _case()
    assert len(expand_cited_ehp_middle_cardinality(goal, (left, left, right, right))) == 1
    assert _cited_finite_group_candidates(left.lhs, (left, left)) == (left,)


def test_non_ehp_dimensions_and_bad_input_are_rejected():
    goal, left, right = _case()
    with pytest.raises(TypeError):
        expand_cited_ehp_middle_cardinality(goal, [left, right])
    assert expand_cited_ehp_middle_cardinality("not a cardinality", (left, right)) == ()
    assert expand_cited_ehp_middle_cardinality(
        FiniteGroupCardinality(TodaPrimaryGroup(6, 4), 4), (left, right),
    ) == ()
    assert expand_cited_ehp_middle_cardinality(
        FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 0), (left, right),
    ) == ()


def test_public_provider_matches_actual_verified_r4_r6_cardinality():
    from phase171_r2j_r4_r9_r8_public_cardinality.audit import inspect_public_cardinality
    report = inspect_public_cardinality()
    assert report["shared_cardinality_connected"] is True
    assert report["source_anchored_cardinality_routes"] == 1
    assert report["new_given_added"] == 0
    assert report["completed_proof_imported"] is False


def test_scoped_canonical_search_is_still_complete_and_trusted():
    from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit import (
        audit_second_source_bound_hopf,
    )
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
    if (-not (Test-Path '.git')) { throw 'EHP Git repository root required' }
    python -B -m phase171_r2j_r4_r9_r8_public_cardinality.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R8 guarded preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R8_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r8_public_cardinality.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R8 guarded patch failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r8_public_cardinality\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r7_public_cyclic_root\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R8 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R8_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r8_public_cardinality.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R8 cardinality audit failed' }
} finally {
    Pop-Location
}
```

## README.md

```markdown
# EHP Proof Tracer — Phase 171 R2J-R4-R9-R8

This package connects the **existing generic finite-middle-group cardinality inference rule** to the shared backward expansion provider. It deliberately does not add a fixed group result, a proof step, a new mathematical theorem, a Web shortcut, or a special-case completed proof.

## Scope and prerequisites

The verified R9-R7 root hook must be present in `phase165_r52_r9_shared_math.py`. The R9-R8 installer accepts either its uncommitted exact four-line patch or an identical committed revision. It verifies the reviewed pre-R7 Git blob (`68846671215c38e3e0a572932b8ed955a7880edc`), rejects all unknown changes in that provider, and never calls Git reset, checkout, pull, or commit.

Only `shared_expansion_provider()` changes in that existing module. The new module `phase171_r2j_r4_r9_r8_public_cardinality/source.py` offers a `GoalExpansion` for a typed `FiniteGroupCardinality` goal when both EHP end-group candidates are uniquely determined from already screened fixed statements or a checked eta specialization. The general short-exact inference and group-order inference rules are reused; search must prove every premise.

This is one incremental production-provider connection. The complete public proof and Web presentation may remain unavailable. The audit records the actual status and unresolved goals rather than upgrading status.

## PowerShell

Unpack the ZIP at the repository root and execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r8_public_cardinality\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r8_public_cardinality\run.ps1"
git status -sb
git diff --stat
```

The runner executes eight new and eight R9-R7 focused regression tests; repository-wide pytest is deferred until Phase closeout. The installer writes the **full post-change** provider function, full production module, and pre-change backup into `output/`. Re-running the package after a successful installation is idempotent.
```

## 監査仕様.md

```markdown
# Phase 171 R2J-R4-R9-R8 監査仕様

## 目的

R4-R9-R7 で接続した巡回群の最終 Root Expansion（根の推論候補）の前提 `FiniteGroupCardinality`（有限群の位数に関する命題）について、既存の短完全列からの一般推論規則を共通 Provider（探索候補生成器）へ接続する。

数学的に使用するのは、短完全列 $0\to A\to B\to C\to0$ ならば $|B|=|A||C|$ という既存規則である。$B=\pi_q^n$ に対し、EHP の添字から $A=\pi_{q-1}^{n-1}$、$C=\pi_q^{2n-1}$ を構成する。群の位数および短完全列は **Goal（証明目標）** にとどまり、証明済みの事実として注入しない。

## 変更対象と位置

- 既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` の内部 `expand()`、R4-R9-R7 の `expand_cited_double_cyclic_root()` 呼出し直後に4行追加する。トップレベル import は変更しない。他の関数とクラスは変更しない。
- 新規 `phase171_r2j_r4_r9_r8_public_cardinality/source.py`：`_unique_relations()`、`_cited_finite_group_candidates()`、`expand_cited_ehp_middle_cardinality()` を追加する。
- 新規 `install.py`：`_git()`、`_clean_text()`、`_git_blob_sha()`、`_function_text()`、`install()`、`main()` を追加する。
- 新規 `audit.py`：`_git()`、`has_exact_proposal()`、`inspect_public_cardinality()`、`main()` を追加する。
- 新規 `tests/test_audit.py`：8個の独立テスト関数と必要な import を追加する。
- 新規 `run.ps1`、`README.md`、`CODE_FULL_JA.md`、`監査仕様.md` を追加する。

## 監査条件

1. 現行 GitHub `develop` の `phase165_r52_r9_shared_math.py` と関連テストを確認済み。R7 導入前の Git Blob は `68846671215c38e3e0a572932b8ed955a7880edc`。R7 の未コミット差分のみ許可し、それ以外を上書きしない。
2. 先行文献から選別済みの同じ群の有限巡回群候補が一意であることを要求する。`Proposition 5.1` の $\eta$ 群の一般形は既存の添字検証関数で特殊化するが、証明は共通探索に委ねる。
3. 双方の位数の積が目標の位数と一致すること、および EHP の短完全列候補が既存の型付き規則の添字検証を通過することを要求する。
4. 目標群そのものの DB レコードや過去の完成済み `ProofStep` を `GIVEN` に昇格させない。出典候補の重複は除去し、異なる候補が複数ある場合は接続を拒否する。
5. 限定 pytest は新規8件と R7 既存8件のみ。全体 pytest は Phase 終了時にのみ実行する。
6. 完了条件は、独立して推論済みの R4-R6 の位数証明と共通 Provider の GoalExpansion が一致し、既存の R4-R9-R6 限定探索が引き続き完成・検証されること。Web 完成証明の表示は本 Phase の対象外。

## 次 Phase との境界

残る `EHPShortExactSequence`（EHP 短完全列）などの前提目標は次の R4-R9-R9 以降に必要なら接続する。実測 `public_search_status` が `complete` にならない限り公開完成証明とは判定しない。

変更後の `shared_expansion_provider()` 全文は実行時に `output/shared_expansion_provider_FULL.py`、変更後の既存ファイル全文は `output/phase165_r52_r9_shared_math.FULL.py` に出力する。省略された関数断片で既存 API を置き換えることはしない。
```

