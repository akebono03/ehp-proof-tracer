# Phase 176 R3R39 — 新規実装コード全文

以下は、新規ファイルの全文です。既存 `shared_expansion_provider()` の変更後全文は `run.ps1` 本実行時に `SHARED_FUNCTION_FULL_JA.md` に出力します。

## `source.py`

```python
"""Public backward plan for the six existing right-Hopf equality steps.

This registers no mathematical rule. Every node is a regular GoalExpansion
whose rule is one of the pre-existing equality/Hopf congruence rules.
The two input leaves remain independent proof-search obligations.
"""
from __future__ import annotations

from collections.abc import Callable

from expression import Composition, MapApplication, Suspension
from hopf_rules import ehp_h_preserves_equality_inference_rule
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r34_composite_suspension_isolated.source import (
    composite_suspension_equality_input,
)
from phase176_r3r38_equality_transport_isolated.source import (
    right_hopf_transport_inputs,
)
from proof import Relation, RelationType
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)


def right_hopf_transport_backward_plan(
    goal: object,
    available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Produce exact six ordinary inference nodes, without proving a leaf.

    The finite candidate beta = delta o gamma.left is merely a backward-search
    hypothesis. The ordinary suspension-image derivation must establish
    E(beta) = gamma; no inverse suspension equality is assumed. This choice
    is structural, not tied to eta/nu names or a particular group query.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)
            or not isinstance(goal.rhs.right, Composition)
            or goal.lhs.expression.right != goal.rhs.right):
        return ()

    alpha = goal.lhs.expression.left
    delta = goal.rhs.left
    gamma = goal.rhs.right
    beta = Composition(delta, gamma.left)
    inputs = right_hopf_transport_inputs(goal, beta)
    if inputs is None:
        return ()
    substituted, suspension = inputs
    if composite_suspension_equality_input(suspension) is None:
        return ()

    hopf_value = Relation(
        MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY,
    )
    if (available.count(TodaProp22RightFormula()) != 1
            or available.count(hopf_value) != 1):
        return ()

    suspended = Suspension(beta)
    alpha_composition = Relation(
        Composition(alpha, suspended), Composition(alpha, gamma),
        RelationType.EQUALITY,
    )
    hopf_composition = Relation(
        substituted.lhs, goal.lhs, RelationType.EQUALITY,
    )
    reversed_hopf_composition = Relation(
        goal.lhs, substituted.lhs, RelationType.EQUALITY,
    )
    delta_composition = Relation(
        substituted.rhs, goal.rhs, RelationType.EQUALITY,
    )
    intermediate = Relation(
        goal.lhs, substituted.rhs, RelationType.EQUALITY,
    )
    return (
        (alpha_composition, GoalExpansion(
            equality_preserved_under_left_composition_inference_rule(alpha),
            (suspension,),
        )),
        (hopf_composition, GoalExpansion(
            ehp_h_preserves_equality_inference_rule(),
            (alpha_composition,),
        )),
        (reversed_hopf_composition, GoalExpansion(
            equality_symmetry_inference_rule(),
            (hopf_composition,),
        )),
        (delta_composition, GoalExpansion(
            equality_preserved_under_left_composition_inference_rule(delta),
            (suspension,),
        )),
        (intermediate, GoalExpansion(
            equality_transitivity_inference_rule(),
            (reversed_hopf_composition, substituted),
        )),
        (goal, GoalExpansion(
            equality_transitivity_inference_rule(),
            (intermediate, delta_composition),
        )),
    )


def build_public_right_hopf_transport_provider(
    available: tuple[object, ...],
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Retain the exact intermediate stages within one source-screened DFS.

    A stage is cached only after its parent has been proposed. This avoids
    introducing global assumptions, pre-completed proofs, or out-of-context
    equality candidates. DFS must independently replay each of the six nodes.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    stages: dict[Relation, GoalExpansion] = {}

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if not isinstance(goal, Relation):
            return ()
        if goal in stages:
            return (stages[goal],)
        plan = right_hopf_transport_backward_plan(goal, available)
        if not plan:
            return ()
        # Two different goals must not inject conflicting backward steps.
        if any(target in stages for target, _proposal in plan):
            return ()
        stages.update(plan)
        return (stages[goal],)

    return expand
```

## `apply.py`（R3R39R1 修正版）

```python
"""Idempotent, anchored R3R39 minimal shared-provider patch."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
INSERT_AFTER_AVAILABLE = "    if not isinstance(prior_conclusions, tuple):\n"
INSERT_AFTER_HOPF = "        options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))\n"
NEW_SETUP = (
    "    # Phase 176 R3R39: source-screened, six existing equality inferences.\n"
    "    from phase176_r3r39_public_equality_transport.source import (\n"
    "        build_public_right_hopf_transport_provider,\n"
    "    )\n"
    "    public_right_hopf_transport = build_public_right_hopf_transport_provider(\n"
    "        tuple(available),\n"
    "    )\n"
)
NEW_DISPATCH = (
    "        # All six transport steps stay visible in the ordinary Proof Tree.\n"
    "        options.extend(public_right_hopf_transport(goal))\n"
)


def updated_source(source: str) -> str:
    """Produce one exact shared-function update; fail on missing/changed hooks."""
    setup_count = source.count(NEW_SETUP)
    dispatch_count = source.count(NEW_DISPATCH)
    if setup_count == 1 and dispatch_count == 1:
        return source
    if setup_count != 0 or dispatch_count != 0:
        raise ValueError("PARTIAL_R3R39_PATCH_REFUSED")
    if (source.count(INSERT_AFTER_AVAILABLE) != 1
            or source.count(INSERT_AFTER_HOPF) != 1
            or source.count("options.extend(expand_composite_suspension_equality(goal))") != 1):
        raise ValueError("SHARED_PROVIDER_ANCHORS_CHANGED")
    return source.replace(
        INSERT_AFTER_AVAILABLE, NEW_SETUP + INSERT_AFTER_AVAILABLE, 1,
    ).replace(
        INSERT_AFTER_HOPF, INSERT_AFTER_HOPF + NEW_DISPATCH, 1,
    )


def normalized_source(raw: bytes) -> str:
    """Decode UTF-8 without treating the byte representation as source code."""
    return raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def patched_bytes(baseline: bytes, current: bytes) -> bytes:
    """Only permit the exact R3R39 insertion; preserve baseline EOL and BOM."""
    original = normalized_source(baseline)
    proposed = updated_source(original)
    if normalized_source(current) not in (original, proposed):
        raise ValueError("UNRELATED_WORKTREE_CHANGE_REFUSED")
    without_crlf = baseline.replace(b"\r\n", b"")
    if b"\r" in without_crlf or (b"\r\n" in baseline and b"\n" in without_crlf):
        raise ValueError("MIXED_OR_UNSUPPORTED_BASELINE_EOL")
    eol = "\r\n" if b"\r\n" in baseline else "\n"
    encoding = "utf-8-sig" if baseline.startswith(b"\xef\xbb\xbf") else "utf-8"
    ast.parse(proposed, filename=str(TARGET))
    return proposed.replace("\n", eol).encode(encoding)


def tracked_baseline() -> bytes:
    """Reject staged changes; compare the index and HEAD as exact bytes."""
    relative = TARGET.relative_to(ROOT).as_posix()
    head = subprocess.check_output(["git", "show", "HEAD:" + relative], cwd=ROOT)
    index = subprocess.check_output(["git", "show", ":" + relative], cwd=ROOT)
    if head != index:
        raise ValueError("STAGED_TARGET_CHANGE_REFUSED")
    return index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    for required in (
        ROOT / "phase176_r3r38_equality_transport_isolated/source.py",
        ROOT / "phase176_r3r34_composite_suspension_isolated/source.py",
        ROOT / "phase176_r3r36_composite_right_hopf_isolated/source.py",
    ):
        if not required.is_file():
            raise ValueError("MISSING_BASELINE:" + str(required.relative_to(ROOT)))
    current = TARGET.read_bytes()
    proposed = patched_bytes(tracked_baseline(), current)
    if not args.dry_run:
        if current != proposed:
            TARGET.write_bytes(proposed)
        if TARGET.read_bytes() != proposed:
            raise ValueError("BYTE_VERIFICATION_FAILED")
        text = normalized_source(proposed)
        start = text.index("def shared_expansion_provider(")
        end = text.index("\ndef search_shared_group_goal(", start)
        documented = (
            "# Phase 176 R3R39 — shared_expansion_provider() 全文\n\n"
            "既存実装を維持し、R3R39 のセットアップと呼び出しのみを追加したものです。\n\n"
            "```python\n" + text[start:end].rstrip() + "\n```\n"
        )
        (Path(__file__).resolve().parent / "SHARED_FUNCTION_FULL_JA.md").write_bytes(
            documented.encode("utf-8"),
        )
    print("PHASE176_R3R39_PATCH=" + ("DRY_RUN_PASS" if args.dry_run else "APPLIED_OR_ALREADY_PRESENT"))
    print("PHASE176_R3R39R1_EOL=" + ("DRY_RUN_PASS" if args.dry_run else "BYTE_VERIFIED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `audit.py`

```python
"""Source-screened public DFS audit; fail closed when any step is missing."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

from phase176_r3r39_public_equality_transport.apply import ROOT, TARGET, updated_source

PACKAGE = "phase176_r3r39_public_equality_transport"


def source_guard(require_patch: bool) -> None:
    for filename in (
        "phase165_r52_r9_shared_math.py",
        "phase176_r3r38_equality_transport_isolated/source.py",
        "phase176_r3r34_composite_suspension_isolated/source.py",
        "phase176_r3r36_composite_right_hopf_isolated/source.py",
        "relation_rules.py",
        "hopf_rules.py",
    ):
        path = ROOT / filename
        if not path.is_file():
            raise ValueError("MISSING_SOURCE:" + filename)
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=filename)
    current = TARGET.read_text(encoding="utf-8-sig")
    proposed = updated_source(current)
    if require_patch and proposed != current:
        raise ValueError("PUBLIC_PATCH_NOT_APPLIED")
    if require_patch and current.count("options.extend(public_right_hopf_transport(goal))") != 1:
        raise ValueError("PUBLIC_DISPATCH_NOT_UNIQUE")


def probe() -> dict:
    """Run real shared DFS over the screened root context, not fake inputs."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r39_public_equality_transport.source import (
        right_hopf_transport_backward_plan,
    )
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    nu_prime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(nu_prime, gamma)),
        Composition(eta5, gamma), RelationType.EQUALITY,
    )

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in steps)
    if len(right_hopf_transport_backward_plan(goal, available)) != 6:
        raise RuntimeError("SOURCE_FIRST_TRANSPORT_PLAN_MISSING")
    if available.count(TodaProp22RightFormula()) != 1:
        raise RuntimeError("PROPOSITION_22_CITATION_MISSING")

    provider = shared_expansion_provider(screened, proof_target=roots[0])
    root_options = provider(goal)
    plan = right_hopf_transport_backward_plan(goal, available)
    if not any(option.rule.name == "equality transitivity"
               and option.subgoals == plan[-1][1].subgoals
               for option in root_options):
        raise RuntimeError("SHARED_ROOT_EXPANSION_MISSING")
    events: list[tuple[str, object]] = []
    ids = tuple(screened.registry._assertions)
    if not ids:
        raise RuntimeError("EMPTY_SCREENED_REGISTRY")

    inferred = reconstruct_registered_goal(
        goal,
        screened,
        ids[0],
        provider,
        lookup_mode="typed_reference",
        progress_observer=lambda kind, target, _step: events.append((kind, target)),
    )
    if inferred.conclusion != goal or inferred.rule is not ProofRule.INFERENCE:
        raise RuntimeError("SHARED_DFS_DID_NOT_PROVE_HOPF_TRANSPORT")

    visited: list = []
    def visit(step):
        for child in step.premises:
            visit(child)
        visited.append(step)
    visit(inferred)
    transport_names = [
        "equality preserved under left composition",
        "EHP H preserves equality",
        "equality symmetry",
        "equality preserved under left composition",
        "equality transitivity",
        "equality transitivity",
    ]
    for target, expansion in plan:
        step = next((item for item in reversed(visited)
                     if item.conclusion == target), None)
        if (step is None or step.rule is not ProofRule.INFERENCE
                or step.inference_rule.name != expansion.rule.name
                or tuple(child.conclusion for child in step.premises) != expansion.subgoals):
            raise RuntimeError("SIX_STEP_PROOF_TREE_MISMATCH:" + expansion.rule.name)
    if not any(kind == "proved" and target == goal for kind, target in events):
        raise RuntimeError("DFS_PROGRESS_NOT_RECORDED")
    if not any(step.conclusion == TodaProp22RightFormula()
               and step.rule is ProofRule.GIVEN for step in visited):
        raise RuntimeError("PROPOSITION_22_PROVENANCE_MISSING")

    return {
        "gate": "PASS_R3R39_PUBLIC_SOURCED_DFS_SIX_EXISTING_STEPS",
        "registered_root_candidates": len(roots),
        "cited_prop22_count": available.count(TodaProp22RightFormula()),
        "six_old_rules_in_shared_proof_tree": transport_names,
        "shared_dfs_intermediate_hopf_transport_proved": True,
        "screened_context_used": True,
        "root_order_gate_retained": True,
        "toda55_quadruple_connection_proved": False,
        "root_hopf_image_goal_proved": False,
        "group_structure_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        source_guard(require_patch=not args.dry_run)
        result = ({"gate": "PASS_R3R39_DRYRUN", "full_pytest": "NOT_RUN"}
                  if args.dry_run else probe())
    except Exception as error:
        result = {
            "gate": "FAIL_R3R39",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    destination = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                   / "EHPProofTracerAudit" / PACKAGE / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R39_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_source.py`

```python
"""Phase 176 R3R39: existing-rule expansion and source-gate tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r38_equality_transport_isolated.source import (
    right_hopf_transport_inputs,
)
from phase176_r3r39_public_equality_transport.source import (
    build_public_right_hopf_transport_provider,
    right_hopf_transport_backward_plan,
)
from proof import ProofRule, ProofStep, Relation, RelationType, apply_inference_match, find_inference_match


def _example():
    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    delta = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)),
                    Composition(delta, gamma), RelationType.EQUALITY)
    value = Relation(MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY)
    return goal, (TodaProp22RightFormula(), value)


def test_six_stages_use_only_the_existing_rules_in_order():
    goal, available = _example()
    plan = right_hopf_transport_backward_plan(goal, available)
    assert len(plan) == 6
    assert plan[-1][0] == goal
    assert [expansion.rule.name for _target, expansion in plan] == [
        "equality preserved under left composition",
        "EHP H preserves equality",
        "equality symmetry",
        "equality preserved under left composition",
        "equality transitivity",
        "equality transitivity",
    ]
    beta = Composition(goal.rhs.left, goal.rhs.right.left)
    substituted, suspension = right_hopf_transport_inputs(goal, beta)
    assert plan[0][1].subgoals == (suspension,)
    assert plan[3][1].subgoals == (suspension,)
    assert plan[4][1].subgoals[1] == substituted
    assert plan[5][1].subgoals == (plan[4][0], plan[3][0])


def test_provider_maintains_stages_in_one_dfs_and_is_deterministic():
    goal, available = _example()
    provider = build_public_right_hopf_transport_provider(available)
    assert provider(goal) == provider(goal)
    plan = right_hopf_transport_backward_plan(goal, available)
    for target, expansion in reversed(plan):
        chosen = provider(target)
        assert len(chosen) == 1
        assert chosen[0].rule.name == expansion.rule.name
        assert chosen[0].subgoals == expansion.subgoals
    assert provider("unrelated") == ()


def test_proof_tree_replays_six_existing_steps_with_two_input_obligations():
    goal, available = _example()
    plan = right_hopf_transport_backward_plan(goal, available)
    beta = Composition(goal.rhs.left, goal.rhs.right.left)
    substituted, suspension = right_hopf_transport_inputs(goal, beta)
    # Synthetic inputs are fixtures only, never production proof certificates.
    input_steps = {
        substituted: ProofStep(substituted, (), ProofRule.INFERENCE),
        suspension: ProofStep(suspension, (), ProofRule.INFERENCE),
    }
    for target, expansion in plan:
        premises = tuple(input_steps[subgoal] for subgoal in expansion.subgoals)
        match = find_inference_match(expansion.rule, premises)
        assert match is not None
        result = apply_inference_match(match)
        assert result.conclusion == target
        assert result.premises == premises
        assert result.rule is ProofRule.INFERENCE
        input_steps[target] = result
    assert input_steps[goal].premises == (
        input_steps[plan[4][0]], input_steps[plan[3][0]],
    )


def test_missing_or_ambiguous_screened_sources_fail_closed():
    goal, available = _example()
    for bad in ((), (available[0],), (available[1],),
                available + (available[0],), available + (available[1],)):
        assert right_hopf_transport_backward_plan(goal, bad) == ()
    with pytest.raises(TypeError, match="available must be a tuple"):
        right_hopf_transport_backward_plan(goal, list(available))
    with pytest.raises(TypeError, match="available must be a tuple"):
        build_public_right_hopf_transport_provider(list(available))


def test_invalid_shape_and_dimensions_fail_closed():
    goal, available = _example()
    assert right_hopf_transport_backward_plan(replace(goal, rhs=goal.rhs.left), available) == ()
    assert right_hopf_transport_backward_plan(replace(goal, lhs=goal.rhs), available) == ()
    assert right_hopf_transport_backward_plan(
        replace(goal, rhs=Composition(
            replace(goal.rhs.left, target=4), goal.rhs.right,
        )), available,
    ) == ()
    assert right_hopf_transport_backward_plan(
        replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(
            replace(goal.lhs.expression.left, source=100), goal.rhs.right,
        ))), available,
    ) == ()


def test_not_hardcoded_to_eta_or_nu_names():
    goal, _available = _example()
    alpha = replace(goal.lhs.expression.left, name="formal-alpha", generator=None)
    delta = replace(goal.rhs.left, name="formal-delta", generator=None)
    abstract_goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, goal.rhs.right)),
        Composition(delta, goal.rhs.right), RelationType.EQUALITY,
    )
    cited_value = Relation(MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY)
    plan = right_hopf_transport_backward_plan(
        abstract_goal, (TodaProp22RightFormula(), cited_value),
    )
    assert len(plan) == 6


def test_shared_patch_has_unique_anchors_and_is_idempotent():
    from phase176_r3r39_public_equality_transport.apply import (
        NEW_DISPATCH,
        NEW_SETUP,
        TARGET,
        updated_source,
    )
    original = TARGET.read_text(encoding="utf-8-sig")
    patched = updated_source(original)
    assert patched == original
    assert original.count(NEW_SETUP) == 1
    assert original.count(NEW_DISPATCH) == 1
    assert original.count("options.extend(expand_composite_suspension_equality(goal))") == 1
    assert original.count("options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))") == 1


def test_root_order_gate_does_not_discard_intermediate_transport_expansion():
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    goal, available = _example()
    root = Relation(TodaPrimaryGroup(8, 3),
                    FiniteCyclicGroup(2, goal.lhs.expression))
    candidate = build_public_right_hopf_transport_provider(available)(goal)
    assert len(candidate) == 1
    assert retain_ordered_root_expansions(root, goal, candidate) == candidate
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsForPatch = @()
    if ($DryRun) { $argsForPatch += '--dry-run' }
    & python -B -m phase176_r3r39_public_equality_transport.apply @argsForPatch
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 patch failed' }
    $argsForAudit = @()
    if ($DryRun) { $argsForAudit += '--dry-run' }
    & python -B -m phase176_r3r39_public_equality_transport.audit @argsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r39_public_equality_transport\tests\test_source.py `
            .\phase176_r3r38_equality_transport_isolated\tests\test_source.py `
            .\phase176_r3r34_composite_suspension_isolated\tests\test_source.py `
            .\phase176_r3r36_composite_right_hopf_isolated\tests\test_source.py `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R39 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R39 git diff check failed' }
        Write-Host 'PHASE176_R3R39_GATE=PASS_R3R39_PUBLIC_SOURCED_DFS_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R39_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```

