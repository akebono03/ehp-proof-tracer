# Phase 174 R3-R7-R29 新規コード全文

変更は新規ファイルのみです。既存クラス・関数・import に変更はありません。

## `provider.py`（新規追加）

```python
"""Source-bound Proposition 2.7 provider for the canonical backward search.

R29 intentionally does not register this provider in the ordinary Web route.
The checked universal literature leaf is the sole GIVEN in the isolated bridge;
every specialized result is produced by the canonical inference engine.
"""
from __future__ import annotations

from pathlib import Path

from phase165_r3_recursive_search import GoalExpansion, reconstruct_registered_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r6_2_unified_registry_r3_r3.provider_registry import (
    UnifiedExpansionProviderRegistry,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, Prop27TypedHopfDeltaStatement,
    prop27_typed_specialization_rule, typed_specialization,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID, Prop27UniversalLiteratureStatement,
    prop27_literature_to_premise_rule, register_universal_prop27,
)
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin

PROVIDER_ID = "phase174.r3.r7.r29.toda_prop27_source_bound_specialization"


def expand_cited_prop27_goal(goal: object) -> tuple[GoalExpansion, ...]:
    """Suggest two general source-bound rules; never create a proof step.

    The concrete n is read from the typed requested goal, not a hard-coded
    special case. Invalid domains and forged typed statements offer no rule.
    """
    if type(goal) is Prop27GeneralTheoremPremise:
        if goal != Prop27GeneralTheoremPremise():
            return ()
        return (GoalExpansion(
            prop27_literature_to_premise_rule(),
            (Prop27UniversalLiteratureStatement(),),
        ),)
    if type(goal) is Prop27TypedHopfDeltaStatement:
        try:
            if typed_specialization(goal.n) != goal:
                return ()
            rule = prop27_typed_specialization_rule(goal.n)
        except (ValueError, TypeError):
            return ()
        return (GoalExpansion(rule, (Prop27GeneralTheoremPremise(),)),)
    return ()


def build_canonical_prop27_context(root: Path):
    """Reuse the shared typed registry merger and common provider registry."""
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")
    literature = register_universal_prop27(root)
    bridge = build_shared_typed_bridge(sources=(literature,))
    matches = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT
        and type(assertion.content) is Prop27UniversalLiteratureStatement
    )
    if len(matches) != 1 or matches[0].assertion_id != "shared:0:" + ASSERTION_ID:
        raise RuntimeError("shared literature registration is not unique")
    links = tuple(link for link in bridge.proof_links
                  if link.assertion_id == matches[0].assertion_id)
    if (len(links) != 1 or not isinstance(links[0].step, ProofStep)
            or links[0].step.rule is not ProofRule.GIVEN
            or links[0].step.conclusion != matches[0].content):
        raise RuntimeError("typed source ProofStepLink is absent or invalid")
    providers = UnifiedExpansionProviderRegistry()
    providers.register(
        PROVIDER_ID, expand_cited_prop27_goal, origin="SHARED_CITED_CONTEXT",
    )
    return bridge, providers


def search_canonical_prop27_instance(root: Path, n: int) -> ProofStep:
    """Run the actual shared backward-proof engine on the cited typed instance."""
    target = typed_specialization(n)
    bridge, providers = build_canonical_prop27_context(root)
    return reconstruct_registered_goal(
        target, bridge, "shared:0:" + ASSERTION_ID,
        providers.providers()[0], lookup_mode="typed_reference",
    )

```

## `audit.py`（新規追加）

```python
"""R29 source-guarded canonical provider integration audit."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

from phase174_r3_r7_r29_prop27_canonical_provider.provider import (
    build_canonical_prop27_context, expand_cited_prop27_goal,
    search_canonical_prop27_instance,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    Prop27UniversalLiteratureStatement,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parents[1]
BASE = "9dad1fb060f3bcc507626c980b767a0a52d2e923"
ALLOWED = (
    "phase174_r3_r7_r28_prop27_typed_literature_registration/",
    "phase174_r3_r7_r29_prop27_canonical_provider/",
)
CACHE = ".pytest_cache/v/cache/nodeids"
PROTECTED = (
    "sources/toda/Toda_02_2.tex",
    "proof.py",
    "homotopy_groups.py",
    "unified_statement_registry.py",
    "phase163_r4_registry_bridge.py",
    "phase165_r3_recursive_search.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r6_2_unified_registry_r3_r3/provider_registry.py",
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py",
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          check=True).stdout.strip()


def allow_paths(paths: tuple[str, ...]) -> bool:
    bad = tuple(path for path in paths
                if path != CACHE and not any(path.startswith(p) for p in ALLOWED))
    if bad:
        raise RuntimeError("Unreviewed committed/staged paths: " + repr(bad))
    return True


def source_guard() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("unexpected repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("expected develop branch")
    head = git("rev-parse", "HEAD")
    line = git("ls-remote", "origin", "refs/heads/develop")
    if not line or head != line.split()[0]:
        raise RuntimeError("local and remote develop differ")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", BASE, head),
                              cwd=ROOT, capture_output=True)
    if ancestor.returncode:
        raise RuntimeError("R28 reviewed HEAD is not an ancestor")
    allow_paths(tuple(git("diff", "--name-only", BASE, head).splitlines()))
    allow_paths(tuple(git("diff", "--name-only").splitlines()))
    allow_paths(tuple(git("diff", "--cached", "--name-only").splitlines()))
    # R28 is not necessarily committed at BASE; verify its distributed bytes.
    r28 = ROOT / "phase174_r3_r7_r28_prop27_typed_literature_registration" / "registration.py"
    r28_data = r28.read_bytes()
    normalized_r28 = r28_data.replace(b"\r\n", b"\n")
    if hashlib.sha256(normalized_r28).hexdigest() != (
        "a117a00aee6dd6e54ecce578eff2cd1038f6b3a691e0b60592c7f5b5267ea17c"
    ):
        raise RuntimeError("R28 registration source differs from reviewed package")
    for file in PROTECTED:
        baseline = subprocess.run(("git", "show", BASE + ":" + file),
                                  cwd=ROOT, capture_output=True, check=True).stdout
        working = (ROOT / file).read_bytes()
        normalized = baseline.replace(b"\r\n", b"\n")
        if working not in (baseline, normalized, normalized.replace(b"\n", b"\r\n")):
            raise RuntimeError("reviewed source changed: " + file)
    return head


def audit_canonical_search() -> dict[str, object]:
    bridge, providers = build_canonical_prop27_context(ROOT)
    if len(providers.entries()) != 1:
        raise RuntimeError("expected exactly one explicit provider")
    target = typed_specialization(6)
    candidates = expand_cited_prop27_goal(target)
    if len(candidates) != 1:
        raise RuntimeError("typed reverse search candidate missing")
    result = search_canonical_prop27_instance(ROOT, 6)
    if (result.conclusion != target or result.rule is not ProofRule.INFERENCE
            or len(result.premises) != 1
            or result.premises[0].rule is not ProofRule.INFERENCE
            or len(result.premises[0].premises) != 1
            or result.premises[0].premises[0].rule is not ProofRule.GIVEN
            or type(result.premises[0].premises[0].conclusion)
            is not Prop27UniversalLiteratureStatement):
        raise RuntimeError("canonical proof chain failed provenance verification")
    return {
        "shared_registry_reference_count": len(bridge.registry._references),
        "explicit_provider_count": len(providers.entries()),
        "n6_backward_candidates": len(candidates),
        "verified_n6_inference": True,
        "parent_depth": 2,
        "n6_direct_given_count": 0,
        "web_default_route_modified": False,
        "root_complete": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head = source_guard()
    print("PHASE174_R3R7R29_HEAD=" + head)
    print("PHASE174_R3R7R29_SOURCE_GUARD=PASS")
    if not args.dry_run:
        for key, value in audit_canonical_search().items():
            print("PHASE174_R3R7R29_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R29_PUBLIC_WEB_REGISTRATION=False")
    print("PHASE174_R3R7R29_FULL_PYTEST=False")
    print("PHASE174_R3R7R29_GATE=" + (
        "PASS_R29_SOURCE_PREFLIGHT_ONLY" if args.dry_run
        else "PASS_R29_CANONICAL_PROVIDER_VERIFIED_WEB_WIRING_PENDING"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_provider.py`（新規追加）

```python
"""R29 canonical backward provider and source-bound ancestry tests."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase174_r3_r7_r29_prop27_canonical_provider.provider import (
    PROVIDER_ID, build_canonical_prop27_context,
    expand_cited_prop27_goal, search_canonical_prop27_instance,
)
from phase174_r3_r7_r29_prop27_canonical_provider.audit import allow_paths
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, typed_specialization,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    Prop27UniversalLiteratureStatement,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parents[2]


def test_context_uses_canonical_shared_bridge_and_registry():
    bridge, providers = build_canonical_prop27_context(ROOT)
    assert len(bridge.proof_links) == 1
    assert len(providers.entries()) == 1
    assert providers.entries()[0].provider_id == PROVIDER_ID
    assert providers.entries()[0].origin == "SHARED_CITED_CONTEXT"


def test_registered_general_goal_has_exact_universal_premise():
    proposals = expand_cited_prop27_goal(Prop27GeneralTheoremPremise())
    assert len(proposals) == 1
    assert proposals[0].subgoals == (Prop27UniversalLiteratureStatement(),)


def test_cited_specialization_proposal_is_general_not_given():
    proposals = expand_cited_prop27_goal(typed_specialization(6))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (Prop27GeneralTheoremPremise(),)


@pytest.mark.parametrize("n", [2, 4, 6, 8])
def test_canonical_backward_inference_keeps_provenance(n):
    step = search_canonical_prop27_instance(ROOT, n)
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == typed_specialization(n)
    assert len(step.premises) == 1
    general = step.premises[0]
    assert general.rule is ProofRule.INFERENCE
    assert general.premises[0].rule is ProofRule.GIVEN
    assert type(general.premises[0].conclusion) is Prop27UniversalLiteratureStatement
    assert step.inference_rule.literature_reference.locator == "Proposition 2.7"


def test_forged_signed_instance_has_no_candidate():
    forged = replace(typed_specialization(6), sign_undetermined=False)
    assert expand_cited_prop27_goal(forged) == ()


def test_no_unrelated_goal_candidate():
    assert expand_cited_prop27_goal("pi_12^7=0") == ()
    assert expand_cited_prop27_goal(Prop27GeneralTheoremPremise(only_even_n=False)) == ()


def test_odd_dimensions_are_not_admitted():
    with pytest.raises(ValueError):
        search_canonical_prop27_instance(ROOT, 5)


def test_source_guard_rejects_unreviewed_paths():
    assert allow_paths(("phase174_r3_r7_r28_prop27_typed_literature_registration/README.md",))
    assert allow_paths(("phase174_r3_r7_r29_prop27_canonical_provider/provider.py",))
    for path in ("proof.py", "phase165_r52_r9_shared_math.py", ".pytest_cache/v/cache/lastfailed"):
        with pytest.raises(RuntimeError):
            allow_paths((path,))

```

## `run.ps1`（新規追加）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& python -B -m phase174_r3_r7_r29_prop27_canonical_provider.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R29 Source Guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R29_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}
& python -B -m phase174_r3_r7_r29_prop27_canonical_provider.audit
if ($LASTEXITCODE -ne 0) { throw 'R29 canonical proof audit failed' }
& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r29_prop27_canonical_provider/tests/test_provider.py `
  phase174_r3_r7_r28_prop27_typed_literature_registration/tests/test_registration.py `
  phase174_r3_r7_r27_certified_premise_registry_audit/tests/test_audit.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_bridge.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_audit.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_run_import_mode.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_rule.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_lineage.py `
  phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py `
  tests/test_phase50_prop27_theorem_semantics.py
if ($LASTEXITCODE -ne 0) { throw 'R29 focused pytest failed' }
Write-Output 'PHASE174_R3R7R29_RUN=PASS'
Write-Output '(END)'

```

## `__init__.py`（新規追加）

```python
"""R29 source-bound canonical provider package."""

```

