# Phase 175 R4R12R13R3 — 追加・変更コード全文

このファイルは新規 Python ファイルと PowerShell ファイルの全文です。既存の `phase165_r52_r9_shared_math.py` の `shared_expansion_provider` 関数は現行 develop の実環境から `run.ps1` 実行時に `output/shared_expansion_provider_FULL.py` へ全文出力します。

## provider.py

```python
"""Public conditional bridge for R13R2 inference rules; no new proof leaves.

All literature and group premises remain backward subgoals to be resolved by
normal source-first proof search. The provider does not assert any goal.
"""
from __future__ import annotations

from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta,
    canonical_toda58,
)
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    expand_delta_injective_from_free_coordinate,
    expand_e_surjective_from_delta_injective,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def screened_toda58_available(bridge: object) -> bool:
    """Require an actual matching, citation-eligible GIVEN in the bridge."""
    registry = getattr(bridge, "registry", None)
    links = getattr(bridge, "proof_links", None)
    if registry is None or links is None:
        return False
    witnesses = []
    for link in links:
        step = getattr(link, "step", None)
        if step is None or step.rule is not ProofRule.GIVEN or step.premises:
            continue
        assertion = registry.assertion(link.assertion_id)
        claim = step.conclusion
        if (
            assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and assertion.content == claim
            and type(claim) is CitedToda58SignedDelta
            and claim.locator == "(5.8)"
            and claim.statement == canonical_toda58()
        ):
            witnesses.append(claim)
    return len(witnesses) == 1


def delta_free_coordinate_proposals(
    goal: object,
    *,
    cited58: bool,
    database_lookup=exact_prior_database_result,
) -> tuple[GoalExpansion, ...]:
    """Offer an unproved route only for a uniquely cited signed source formula.

    π₉⁹ is a *goal* to be proved from a separate citation, never a fabricated
    given. π₇⁴ is also a goal; its existing DB row is not promoted here.
    """
    if not cited58 or not isinstance(goal, MapInjective) or not isinstance(goal.map, TodaDeltaMap):
        return ()
    signed = canonical_toda58()
    if goal.map != signed.map:
        return ()
    source = Relation(
        lhs=goal.map.source_group,
        rhs=FreeCyclicGroup(signed.element),
        relation_type=RelationType.EQUALITY,
    )
    # DB n=4,k=3 is an earlier group, not the queried π₉⁵ target.
    target = database_lookup(4, 3)
    if not isinstance(target, Relation) or target.lhs != TodaPrimaryGroup(7, 4):
        return ()
    return expand_delta_injective_from_free_coordinate(goal, source, target, signed)


def build_public_delta_e_provider(bridge: object):
    """Connect existing R13R2 rules without introducing new mathematical rules."""
    has_source = screened_toda58_available(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return (
            delta_free_coordinate_proposals(goal, cited58=has_source)
            + expand_e_surjective_from_delta_injective(goal)
        )

    return expand
```

## installer.py

```python
"""Strict, reversible installation of a single shared-provider registration."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("phase165_r52_r9_shared_math.py")
ANCHOR = '    # Phase 175 R4R12R9: infer a generator image from a proved typed\n'
INSERT = '''    # Phase 175 R4R12R13R3: conditional Delta injectivity and E surjectivity.
    # Every parent is independently verified by recursive proof search.
    from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
        build_public_delta_e_provider,
    )
    extra_providers = (build_public_delta_e_provider(bridge),) + tuple(extra_providers)
'''


def render(text: str) -> tuple[str, bool]:
    """Fail closed for unknown source, duplicate hooks, or partial installation."""
    if text.count(INSERT) == 1:
        return text, False
    if "build_public_delta_e_provider" in text:
        raise RuntimeError("R13R3_PARTIAL_OR_UNREVIEWED_PROVIDER")
    if text.count(ANCHOR) != 1:
        raise RuntimeError("R13R3_UNREVIEWED_SHARED_PROVIDER_ANCHOR")
    return text.replace(ANCHOR, INSERT + ANCHOR, 1), True


def plan(root: Path) -> tuple[Path, str, str, bool]:
    target = root / TARGET
    before = target.read_text(encoding="utf-8")
    after, change = render(before)
    return target, before, after, change


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    target, before, after, required = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    # Full replacement function is automatically exported from actual local code.
    start = after.index("def shared_expansion_provider(")
    next_def = after.find("\ndef ", start + 5)
    body = after[start:] if next_def == -1 else after[start:next_def]
    (output / "shared_expansion_provider_FULL.py").write_text(body, encoding="utf-8")
    if not dry_run and required:
        # Only the exact anchored insertion is permitted; retain original EOL.
        raw = target.read_bytes()
        if b"\r\n" in raw:
            after_bytes = after.replace("\n", "\r\n").encode("utf-8")
        else:
            after_bytes = after.encode("utf-8")
        target.write_bytes(after_bytes)
    return {
        "target": str(TARGET), "change_required": required,
        "installed": not dry_run and required,
        "full_function_export": str(output / "shared_expansion_provider_FULL.py"),
    }
```

## audit.py

```python
"""Phase 175 R13R3 conditional public wiring with fail-closed evidence audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase175_r4r12r13r3_public_delta_e_bridge import installer

PACKAGE = "phase175_r4r12r13r3_public_delta_e_bridge"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R13R3_GIT_ERROR: " + " ".join(args) + " " + process.stderr.strip())
    return process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R13R3_WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R13R3_WRONG_BRANCH")
    dirty = set(git(root, "diff", "--name-only").splitlines())
    dirty.update(git(root, "diff", "--cached", "--name-only").splitlines())
    if dirty - {".pytest_cache/v/cache/nodeids", str(installer.TARGET)}:
        raise RuntimeError("R13R3_UNREVIEWED_TRACKED_CHANGES: " + repr(sorted(dirty)))
    if str(installer.TARGET) in dirty:
        _, _, _, change = installer.plan(root)
        if change:
            raise RuntimeError("R13R3_PREEXISTING_SHARED_PROVIDER_DIRTY")
    return {"head": git(root, "rev-parse", "HEAD"), "dirty": sorted(dirty)}


def inspect() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
    from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
        build_public_delta_e_provider, screened_toda58_available,
    )
    bridge = build_shared_typed_bridge()
    has_citation = screened_toda58_available(bridge)
    provider = build_public_delta_e_provider(bridge)
    delta = MapInjective(canonical_toda58().map)
    emap = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    delta_branches = provider(delta)
    e_branches = provider(emap)
    return {
        "toda58_cited_given_present": has_citation,
        "delta_injective_candidates": len(delta_branches),
        "delta_input_goal_types": [type(x).__name__ for branch in delta_branches for x in branch.subgoals],
        "e_surjective_candidates": len(e_branches),
        "e_input_goal_types": [type(x).__name__ for branch in e_branches for x in branch.subgoals],
        "parent_proofs_dispatched": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "proof_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"phase": "175-R4R12R13R3", "dry_run": dry_run,
        "gate": "FAIL_R13R3", "full_pytest_executed": False}
    try:
        report["preflight"] = preflight(root)
        report["installation"] = installer.install(root, dry_run=dry_run, output=output)
        report["frontier"] = inspect()
        if report["frontier"]["e_surjective_candidates"] != 1:
            raise RuntimeError("R13R3_MISSING_E_SURJECTIVE_RULE")
        if report["frontier"]["delta_injective_candidates"] != 1:
            report["gate"] = "PASS_R13R3_E_CONNECTED_DELTA_TYPED_MATCH_PENDING"
        else:
            report["gate"] = "PASS_R13R3_CONDITIONAL_PROVIDER_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    filename = output / ("dry_run_report.json" if dry_run else "report.json")
    filename.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R13R3_GATE=" + str(report["gate"]))
    print("PHASE175_R13R3_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    front = report.get("frontier", {})
    print("PHASE175_R13R3_TODA58_CITED=" + str(front.get("toda58_cited_given_present", "NOT_CHECKED")))
    print("PHASE175_R13R3_DELTA_CANDIDATES=" + str(front.get("delta_injective_candidates", "NOT_CHECKED")))
    print("PHASE175_R13R3_E_CANDIDATES=" + str(front.get("e_surjective_candidates", "NOT_CHECKED")))
    print("PHASE175_R13R3_NEW_GIVEN=0")
    print("PHASE175_R13R3_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R3_REPORT=" + str(filename))
    if "error" in report:
        print("PHASE175_R13R3_ERROR=" + report["error"])
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    return run(options.root.resolve(), dry_run=options.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_provider.py

```python
"""Focused source-first tests of conditional R13R3 public proposals."""
from __future__ import annotations

from dataclasses import replace

from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
    TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r3_public_delta_e_bridge import installer
from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
    delta_free_coordinate_proposals,
)
from proof import Relation, RelationType


def target_fixture():
    signed = canonical_toda58()
    return Relation(
        lhs=TodaPrimaryGroup(7, 4),
        rhs=DirectSumGroup((
            FreeCyclicGroup(signed.positive_value.left.expression),
            FiniteCyclicGroup(4, signed.positive_value.right.expression),
        )),
        relation_type=RelationType.EQUALITY,
    )


def test_cited_toda58_conditional_branch_has_three_unproved_parents():
    signed = canonical_toda58()
    options = delta_free_coordinate_proposals(
        MapInjective(signed.map), cited58=True,
        database_lookup=lambda n, k: target_fixture() if (n, k) == (4, 3) else None,
    )
    assert len(options) == 1
    source, target, image = options[0].subgoals
    assert source.rhs == FreeCyclicGroup(signed.element)
    assert target == target_fixture()
    assert image == signed


def test_missing_citation_and_incorrect_target_fail_closed():
    signed = canonical_toda58()
    goal = MapInjective(signed.map)
    assert delta_free_coordinate_proposals(goal, cited58=False,
        database_lookup=lambda n, k: target_fixture()) == ()
    wrong = replace(target_fixture(), lhs=TodaPrimaryGroup(8, 4))
    assert delta_free_coordinate_proposals(goal, cited58=True,
        database_lookup=lambda n, k: wrong) == ()


def test_installer_idempotent_and_anchor_required():
    text = "def shared_expansion_provider(bridge, extra_providers=()):\n" + installer.ANCHOR + "    return extra_providers\n"
    updated, required = installer.render(text)
    assert required
    assert updated.count("build_public_delta_e_provider") == 2
    assert installer.render(updated) == (updated, False)


def test_installer_rejects_unreviewed_source():
    import pytest
    with pytest.raises(RuntimeError, match="ANCHOR"):
        installer.render("def other_provider(): pass\n")


def test_e_surjective_backward_route_has_three_obligations():
    from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
        expand_e_surjective_from_delta_injective,
    )
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    expansion = expand_e_surjective_from_delta_injective(goal)
    assert len(expansion) == 1
    assert len(expansion[0].subgoals) == 3
    assert expansion[0].subgoals[0] == MapInjective(canonical_toda58().map)
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$argsPython = @('-m', 'phase175_r4r12r13r3_public_delta_e_bridge.audit', '--root', $root)
if ($DryRun) { $argsPython += '--dry-run' }
python @argsPython
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
```

## __init__.py

```python
"""Conditional public connection of audited R13R2 rules."""
```
