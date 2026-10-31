# Phase 171 R20：新規コードとテスト全文

既存 `shared_expansion_provider()` の全文は、インストーラが元ファイルから抽出して `output/FULL_SHARED_PROVIDER_BEFORE.py` と `output/FULL_SHARED_PROVIDER_AFTER.py` に全行出力する。ここでは新規ファイルの import と関数を全文掲載する。

## `source.py`

```python
"""Prefer the typed η specialization over an identical generic scalar route.

Both source-to-conclusion inference rules remain callable independently.
This helper removes only a redundant backward proposal that uses the *same*
screened source and target as the existing, mathematically checked η route.
It never constructs ProofSteps, adds GIVEN sources, or weakens uniqueness.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization

ETA_RULE = "Toda Proposition 5.1 generic higher-eta specialization"
SCALAR_RULE = "generic cited typed scalar specialization"


def prefer_specific_cited_eta_specialization(
    goal: object, available: tuple[object, ...],
    expansions: tuple[GoalExpansion, ...],
) -> tuple[GoalExpansion, ...]:
    """Suppress only the generic route shadowing a vetted exact η route.

    Require both candidates in the same expansion tuple and verify the
    specialized rule against available screened source conclusions. A
    different source or a different conclusion never becomes interchangeable.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    if not all(isinstance(value, GoalExpansion) for value in expansions):
        raise TypeError("all proposals must be GoalExpansion instances")
    confirmed = expand_registered_eta_specialization(goal, available)
    concrete = tuple(
        item for item in expansions
        if getattr(item.rule, "name", None) == ETA_RULE
        and any(reference.subgoals == item.subgoals for reference in confirmed)
    )
    if not concrete:
        return expansions
    return tuple(
        item for item in expansions
        if not (
            getattr(item.rule, "name", None) == SCALAR_RULE
            and any(item.subgoals == specific.subgoals for specific in concrete)
        )
    )

```

## `install.py`

```python
"""Guarded single-function provider hook, preserving all unrelated bytes."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
REVIEWED_BLOB = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
ORIGINAL = "        return retain_ordered_root_expansions(proof_target, goal, merged)"
REPLACEMENT = """        from phase171_r2j_r4_r9_r20_eta_route_precedence.source import (
            prefer_specific_cited_eta_specialization,
        )
        preferred = prefer_specific_cited_eta_specialization(
            goal, tuple(available), merged,
        )
        return retain_ordered_root_expansions(proof_target, goal, preferred)"""


def git_read(*args: str) -> bytes:
    """Read-only Git access, never checkout, reset, pull, or stage."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", "HEAD:phase165_r52_r9_shared_math.py"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if args not in allowed:
        raise ValueError("mutating Git commands are not allowed")
    return subprocess.run(["git", *args], cwd=ROOT,
                          check=True, capture_output=True).stdout


def blob_sha(data: bytes) -> str:
    """Calculate the SHA-1 of a committed Git blob without writing files."""
    return hashlib.sha1(("blob %d\0" % len(data)).encode("ascii") + data).hexdigest()


def source_function(source: str, name: str = "shared_expansion_provider") -> str:
    """Extract the *complete* function via AST, without truncation."""
    tree = ast.parse(source)
    selected = [item for item in tree.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                and item.name == name]
    if len(selected) != 1:
        raise RuntimeError("expected one complete shared provider definition")
    node = selected[0]
    return "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def patch_text(original: str) -> str:
    """Only change the reviewed final return of the common provider."""
    if original.count(REPLACEMENT) == 1:
        source_function(original)
        return original
    if original.count(ORIGINAL) != 1:
        raise RuntimeError("reviewed provider return anchor is not unique")
    altered = original.replace(ORIGINAL, REPLACEMENT, 1)
    ast.parse(altered)
    before = source_function(original)
    after = source_function(altered)
    if before == after:
        raise RuntimeError("provider function was not updated")
    if altered.replace(REPLACEMENT, ORIGINAL, 1) != original:
        raise RuntimeError("nonlocal source modification detected")
    return altered


def preflight() -> dict[str, str]:
    branch = git_read("branch", "--show-current").decode("utf-8").strip()
    head = git_read("rev-parse", "HEAD").decode("utf-8").strip()
    committed = git_read("show", "HEAD:phase165_r52_r9_shared_math.py")
    if branch != "develop":
        raise RuntimeError("R20 requires develop")
    if blob_sha(committed) != REVIEWED_BLOB:
        raise RuntimeError("HEAD provider differs from the reviewed R19/R11 baseline")
    local = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in local else "\n"
    current = local.decode("utf-8-sig").replace("\r\n", "\n")
    expected = committed.decode("utf-8-sig").replace("\r\n", "\n")
    if current != expected and current != patch_text(expected):
        raise RuntimeError("working provider differs from HEAD and the R20 patch")
    return {"branch": branch, "head": head, "newline": newline}


def install(*, dry_run: bool = False) -> bool:
    """Apply one guarded patch; always write full-function evidence on success."""
    ready = preflight()
    before = TARGET.read_bytes()
    original = before.decode("utf-8-sig").replace("\r\n", "\n")
    after = patch_text(original)
    output = PACKAGE / "output"
    print("PHASE171_R20_BRANCH=" + ready["branch"], flush=True)
    print("PHASE171_R20_HEAD=" + ready["head"], flush=True)
    print("PHASE171_R20_REVIEWED_PROVIDER=PASS", flush=True)
    if dry_run:
        print("PHASE171_R20_RESULT=PASS_DRY_RUN", flush=True)
        return False
    output.mkdir(exist_ok=True)
    (output / "FULL_SHARED_PROVIDER_BEFORE.py").write_text(
        source_function(original), encoding="utf-8")
    (output / "FULL_SHARED_PROVIDER_AFTER.py").write_text(
        source_function(after), encoding="utf-8")
    (output / "BACKUP_phase165_r52_r9_shared_math.py").write_bytes(before)
    changed = after != original
    if changed:
        target_bytes = after.replace("\n", ready["newline"]).encode("utf-8")
        if before.startswith(b"\xef\xbb\xbf"):
            target_bytes = b"\xef\xbb\xbf" + target_bytes
        TARGET.write_bytes(target_bytes)
    print("PHASE171_R20_PATCHED=" + str(changed), flush=True)
    print("PHASE171_R20_FULL_FUNCTION=" + str(output / "FULL_SHARED_PROVIDER_AFTER.py"), flush=True)
    print("PHASE171_R20_BACKUP=" + str(output / "BACKUP_phase165_r52_r9_shared_math.py"), flush=True)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

```

## `audit.py`

```python
"""Audit unique η proof and finite cardinality after the guarded R20 patch."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase171_r2j_r4_r9_r20_eta_route_precedence.install import git_read, preflight

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output" / "audit.json"


def probe_right_and_cardinality() -> dict:
    """Independently reconstruct goals in actual public and R2I source contexts."""
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit import (
        cardinality_route, probe_premise,
    )
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from phase171_r2j_r4_r9_r20_eta_route_precedence.source import (
        ETA_RULE, SCALAR_RULE,
    )

    screened, group_goal, citing = _screened_context()
    contexts: list[object] = []
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=group_goal,
        context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("expected one public proof context")
    records = {}
    for label, context in (("screened", screened), ("public", contexts[0])):
        provider = shared_expansion_provider(context, proof_target=group_goal)
        cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
        route = cardinality_route(provider, cardinality)
        right = route.subgoals[2]
        candidates = provider(right)
        rule_names = [getattr(item.rule, "name", "") for item in candidates]
        right_result, _ = probe_premise(right, provider, context, citing, group_goal)
        cardinality_result, _ = probe_premise(cardinality, provider, context, citing, group_goal)
        records[label] = {
            "rule_names": rule_names,
            "eta_routes": rule_names.count(ETA_RULE),
            "redundant_scalar_routes": rule_names.count(SCALAR_RULE),
            "right_status": right_result["status"],
            "right_error": right_result["error"],
            "cardinality_status": cardinality_result["status"],
            "cardinality_error": cardinality_result["error"],
            "given_source_ids": right_result.get("source_ids"),
        }
    return {
        "phase": "171-R2J-R4-R9-R20",
        "mode": "GUARDED_ETA_SPECIALIZATION_ROUTE_PRECEDENCE",
        "public_root_status": public.status.value,
        "contexts": records,
        "new_given": 0,
        "trust_boundary_modified": False,
        "completed_proof_imported": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    ready = preflight()
    before = git_read("status", "--porcelain", "--untracked-files=no")
    report = probe_right_and_cardinality()
    after = git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked working files changed during R20 read-only audit")
    report["head"] = ready["head"]
    report["tracked_source_status_unchanged"] = True
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20_PUBLIC_ROOT=" + report["public_root_status"], flush=True)
    for name, value in report["contexts"].items():
        print("PHASE171_R20_" + name.upper() + "_RIGHT=" + value["right_status"], flush=True)
        print("PHASE171_R20_" + name.upper() + "_CARDINALITY=" + value["cardinality_status"], flush=True)
        print("PHASE171_R20_" + name.upper() + "_ETA_ROUTES=" + str(value["eta_routes"]), flush=True)
        print("PHASE171_R20_" + name.upper() + "_SCALAR_ROUTES=" + str(value["redundant_scalar_routes"]), flush=True)
    assert all(x["eta_routes"] == 1 and x["redundant_scalar_routes"] == 0
               and x["right_status"] == "proved" for x in report["contexts"].values()), (
        "R20 did not uniquely reconstruct the cited right group")
    print("PHASE171_R20_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20_RESULT=PASS_GUARDED_PATCH_AUDIT", flush=True)


if __name__ == "__main__":
    main()

```

## `tests/test_r20.py`

```python
"""Focused R20 tests: provider precedence, provenance and canonical proof."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit import cardinality_route, probe_premise
from phase171_r2j_r4_r9_r20_eta_route_precedence.install import (
    ORIGINAL, REPLACEMENT, git_read, patch_text, source_function,
)
from phase171_r2j_r4_r9_r20_eta_route_precedence.source import (
    ETA_RULE, SCALAR_RULE, prefer_specific_cited_eta_specialization,
)
from homotopy_groups import TodaPrimaryGroup
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from proof import ProofRule


@dataclass(frozen=True)
class FakeRule:
    name: str


def test_does_not_suppress_unverified_or_different_source():
    generic = GoalExpansion(FakeRule(SCALAR_RULE), ("unverified",))
    specific = GoalExpansion(FakeRule(ETA_RULE), ("unverified",))
    assert prefer_specific_cited_eta_specialization(object(), (), (generic, specific)) == (generic, specific)
    with pytest.raises(TypeError):
        prefer_specific_cited_eta_specialization(object(), [], (generic,))
    with pytest.raises(TypeError):
        prefer_specific_cited_eta_specialization(object(), (), [generic])


def test_source_bounded_eta_precedence_on_real_registered_general_source():
    screened, root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    order = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    right = cardinality_route(provider, order).subgoals[2]
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    specific = expand_registered_eta_specialization(right, available)
    generic = expand_cited_general_specialization(right, available)
    assert len(specific) == len(generic) == 1
    assert specific[0].subgoals == generic[0].subgoals
    output = prefer_specific_cited_eta_specialization(
        right, available, generic + specific,
    )
    assert output == specific


def test_unrelated_scalar_specialization_not_suppressed():
    screened, root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    right = cardinality_route(provider, FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)).subgoals[2]
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    specific, = expand_registered_eta_specialization(right, available)
    generic, = expand_cited_general_specialization(right, available)
    unrelated = GoalExpansion(generic.rule, (object(),))
    observed = prefer_specific_cited_eta_specialization(right, available, (generic, specific, unrelated))
    assert observed == (specific, unrelated)


def test_shared_provider_keeps_only_unique_specific_eta_route():
    screened, root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    right = cardinality_route(provider, FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)).subgoals[2]
    names = [item.rule.name for item in provider(right)]
    assert names.count(ETA_RULE) == 1
    assert names.count(SCALAR_RULE) == 0


def test_right_group_is_inferred_with_real_cited_source():
    screened, root, citing = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    right = cardinality_route(provider, FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)).subgoals[2]
    observed, step = probe_premise(right, provider, screened, citing, root)
    assert observed["status"] == "proved"
    assert step.rule is ProofRule.INFERENCE
    assert observed["source_ids"]


def test_cardinality_is_inferred_without_importing_completed_proof():
    screened, root, citing = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    observed, step = probe_premise(cardinality, provider, screened, citing, root)
    assert observed["status"] == "proved", observed["error"]
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == cardinality
    assert observed["source_ids"]


def test_guarded_installation_changes_exactly_one_complete_function():
    original = git_read("show", "HEAD:phase165_r52_r9_shared_math.py").decode("utf-8-sig").replace("\r\n", "\n")
    altered = patch_text(original)
    assert altered != original
    assert altered.count(REPLACEMENT) == 1
    assert altered.replace(REPLACEMENT, ORIGINAL) == original
    assert "def shared_expansion_provider(" in source_function(altered)
    assert "prefer_specific_cited_eta_specialization(" in source_function(altered)
    assert patch_text(altered) == altered

```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    if ($DryRun) {
        python -m phase171_r2j_r4_r9_r20_eta_route_precedence.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20_DRY_RUN_FAILED' }
        Write-Output 'PHASE171_R20_DRY_RUN=PASS'
        return
    }
    python -m phase171_r2j_r4_r9_r20_eta_route_precedence.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20_PREFLIGHT_FAILED' }
    python -m phase171_r2j_r4_r9_r20_eta_route_precedence.install
    if ($LASTEXITCODE -ne 0) { throw 'R20_INSTALL_FAILED' }
    Write-Output 'PHASE171_R20_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        .\phase171_r2j_r4_r9_r20_eta_route_precedence\tests\test_r20.py `
        .\phase171_r2j_r4_r9_r8_public_cardinality\tests\test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R20_FOCUSED_PYTEST_FAILED' }
    Write-Output 'PHASE171_R20_FOCUSED_PYTEST=PASS'
    python -m phase171_r2j_r4_r9_r20_eta_route_precedence.audit
    if ($LASTEXITCODE -ne 0) { throw 'R20_AUDIT_FAILED' }
    Write-Output 'PHASE171_R20_RESULT=PASS'
}
finally { Pop-Location }

```

