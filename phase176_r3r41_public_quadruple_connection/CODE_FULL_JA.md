# R3R41R1 配布コード全文

変更対象は apply.py と run.ps1、追加は tests/test_apply.py。他のコードは前回と同一です。

## `source.py`

```python
"""Source-screened backward candidates for the audited Toda (5.5) connection."""
from __future__ import annotations

from collections.abc import Callable

from expression import Composition, HomotopyElement, MapApplication, Multiple
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase176_r3r27r1_toda55_quadruple_isolated.source import canonical_quadruple_goal
from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan
from proof import Relation, RelationType


def public_quadruple_backward_plan(
    goal: object, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Derive a finite candidate from the goal and screened H(alpha) values.

    The existing audited planner validates both independent input obligations.
    Neither the source availability nor this plan certifies their truth.
    """
    if not isinstance(available, tuple):
        raise TypeError('available must be a tuple')
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.lhs.expression.right, Composition)
            or not isinstance(goal.rhs, Multiple)
            or not isinstance(goal.rhs.expression, HomotopyElement)
            or type(goal.rhs.coefficient) is not int
            or goal.rhs.coefficient != 4):
        return ()
    forward = canonical_quadruple_goal(goal.rhs.expression.dimension)
    if forward is None or forward.lhs != goal.rhs:
        return ()
    alpha = goal.lhs.expression.left
    gamma = goal.lhs.expression.right
    plans = []
    for item in available:
        if (not isinstance(item, Relation)
                or item.relation_type is not RelationType.EQUALITY
                or item.lhs != MapApplication(EHP_H_MAP, alpha)
                or not isinstance(item.rhs, HomotopyElement)
                or available.count(item) != 1):
            continue
        transported = Relation(goal.lhs, Composition(item.rhs, gamma))
        plan = connection_backward_plan(transported, forward, available)
        if plan and plan[-1][0] == goal:
            plans.append(plan)
    # Ambiguous routes are not silently selected by a notation heuristic.
    return plans[0] if len(plans) == 1 else ()


def build_public_quadruple_connection_provider(
    available: tuple[object, ...],
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Keep only candidate obligations in a single DFS context, not proofs."""
    if not isinstance(available, tuple):
        raise TypeError('available must be a tuple')
    stages: list[tuple[Relation, GoalExpansion]] = []

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if not isinstance(goal, Relation):
            return ()
        known = tuple(option for target, option in stages if target == goal)
        if known:
            return known
        plan = public_quadruple_backward_plan(goal, available)
        if not plan:
            return ()
        # Shared sub-obligations may recur across plans; keep identical ones.
        for target, option in plan:
            for previous, old in stages:
                if target == previous and (old.rule.name != option.rule.name
                                           or old.subgoals != option.subgoals):
                    return ()
        for target, option in plan:
            if not any(target == previous for previous, _ in stages):
                stages.append((target, option))
        return tuple(option for target, option in stages if target == goal)

    return expand
```

## `apply.py`

```python
"""Minimal byte-preserving connection to the reviewed shared provider."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
SETUP_ANCHOR = '    if not isinstance(prior_conclusions, tuple):\n'
SETUP = '''    # Phase 176 R3R41: audited source-screened quadruple connection.
    from phase176_r3r41_public_quadruple_connection.source import (
        build_public_quadruple_connection_provider,
    )
    public_quadruple_connection = build_public_quadruple_connection_provider(
        tuple(available),
    )
'''
DISPATCH_ANCHOR = ('        options = []\n'
                   '        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (\n'
                   '            expand_public_cited_prop27_goal,\n')
DISPATCH = '        options.extend(public_quadruple_connection(goal))\n'
PATCHED_DISPATCH_ANCHOR = '        options = []\n' + DISPATCH + DISPATCH_ANCHOR.split('\n', 1)[1]


def _unique_function(nodes, name: str) -> ast.FunctionDef:
    matches = [node for node in nodes
               if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError('SHARED_FUNCTION_NOT_UNIQUE:' + name)
    return matches[0]


def updated_source(source: str) -> str:
    """Edit only the reviewed function and its immediate nested expand."""
    if '\r' in source or source.startswith('\ufeff'):
        raise ValueError('EXPECTED_REPAIRED_LF_SOURCE')
    tree = ast.parse(source)
    function = _unique_function(tree.body, 'shared_expansion_provider')
    expand = _unique_function(function.body, 'expand')
    lines = source.splitlines(keepends=True)
    start, stop = function.lineno - 1, function.end_lineno
    body = ''.join(lines[start:stop])
    dispatch_body = ''.join(lines[expand.lineno - 1:expand.end_lineno])
    setup_body = ''.join(lines[start:expand.lineno - 1])
    if body.count(SETUP_ANCHOR) != 1 or setup_body.count(SETUP_ANCHOR) != 1:
        raise ValueError('SHARED_SETUP_ANCHOR_NOT_UNIQUE')
    if dispatch_body.count('options.extend(public_right_hopf_transport(goal))') != 1:
        raise ValueError('R3R39_HOOK_MISSING')
    if SETUP in setup_body and DISPATCH in dispatch_body:
        if (source.count(SETUP) != 1 or source.count(DISPATCH) != 1
                or source.count('public_quadruple_connection') != SETUP.count('public_quadruple_connection') + DISPATCH.count('public_quadruple_connection')
                or setup_body.count(SETUP + SETUP_ANCHOR) != 1
                or dispatch_body.count(PATCHED_DISPATCH_ANCHOR) != 1
                or DISPATCH_ANCHOR in dispatch_body):
            raise ValueError('DUPLICATE_OR_MOVED_R3R41_PATCH')
        return source
    if 'public_quadruple_connection' in source:
        raise ValueError('PARTIAL_OR_CHANGED_R3R41_PATCH')
    if dispatch_body.count(DISPATCH_ANCHOR) != 1 or body.count(DISPATCH_ANCHOR) != 1:
        raise ValueError('SHARED_DISPATCH_ANCHOR_NOT_UNIQUE')
    changed_body = body.replace(SETUP_ANCHOR, SETUP + SETUP_ANCHOR, 1)
    changed_body = changed_body.replace(DISPATCH_ANCHOR, PATCHED_DISPATCH_ANCHOR, 1)
    changed = ''.join(lines[:start]) + changed_body + ''.join(lines[stop:])
    ast.parse(changed)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    original = TARGET.read_bytes().decode('utf-8')
    changed = updated_source(original)
    if not args.dry_run:
        if changed != original:
            TARGET.write_bytes(changed.encode('utf-8'))
        tree = ast.parse(changed)
        function = _unique_function(tree.body, 'shared_expansion_provider')
        full = '\n'.join(changed.splitlines()[function.lineno-1:function.end_lineno])
        (Path(__file__).parent / 'SHARED_FUNCTION_FULL_JA.md').write_bytes(
            ('# 変更後の共有関数全文\n\n```python\n' + full + '\n```\n').encode('utf-8'))
    print('PHASE176_R3R41_PATCH=' + ('DRY_RUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## `audit.py`

```python
"""Verify the real default shared DFS, without an audit-only provider."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r41_public_quadruple_connection"
ROOT = Path(__file__).resolve().parent.parent


def source_guard() -> None:
    from phase176_r3r40_toda55_connection_audit.audit import source_guard as prior_guard
    prior_guard()
    from phase176_r3r41_public_quadruple_connection.apply import TARGET, updated_source
    current = TARGET.read_bytes().decode("utf-8")
    updated_source(current)
    for filename in (
        "phase165_r12_r21_eta_generator_chain.py",
        "phase165_r12_r28_presentation_connection.py",
        "phase171_r2i_eta_hopf_bridge/source.py",
        "phase176_r3r40r1_eta_notation_bridge/source.py",
    ):
        ast.parse((ROOT / filename).read_text(encoding="utf-8-sig"), filename=filename)


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase176_r3r41_public_quadruple_connection.source import public_quadruple_backward_plan
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r27r1_toda55_quadruple_isolated.source import (
        RULE_NAME, Toda55UniversalQuadrupleStatement, canonical_quadruple_goal, quadruple_inputs,
    )
    from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
    from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan, eta_notation_backward_plan
    from proof import ProofRule, Relation
    from unified_statement_registry import AssertionOrigin

    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    transported = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)), Composition(eta5, gamma))
    forward = canonical_quadruple_goal(5)
    if forward is None:
        raise RuntimeError("CANONICAL_QUADRUPLE_MISSING")
    print("PHASE176_R3R41_TRANSPORT_CUBE_REPR=" + repr(transported.rhs))
    print("PHASE176_R3R41_TODA55_CUBE_REPR=" + repr(forward.rhs))
    goal = Relation(transported.lhs, forward.lhs)
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    root = roots[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    links = tuple(link for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN
                  and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                  and screened.registry.assertion(link.assertion_id).content == link.step.conclusion)
    available = tuple(link.step.conclusion for link in links)
    sources = tuple(link for link in links if link.step.conclusion == Toda55UniversalQuadrupleStatement())
    if (len(sources) != 1 or available.count(TodaEtaFamilyGeneralDefinition()) != 1
            or available.count(TodaProp22RightFormula()) != 1):
        raise RuntimeError("SCREENED_SOURCES_MISSING_OR_AMBIGUOUS")
    notation = eta_notation_backward_plan(transported.rhs, forward.rhs, available)
    if transported.rhs != forward.rhs and not notation:
        raise RuntimeError("NO_TYPED_ETA_NOTATION_PLAN")
    plan = connection_backward_plan(transported, forward, available)
    transport_plan = right_hopf_transport_backward_plan(transported, available)
    if not plan or len(transport_plan) != 6:
        raise RuntimeError("CONNECTION_PLAN_MISSING")
    if any(item in available for item in (root, transported, forward, goal) + tuple(target for target, _ in plan)):
        raise RuntimeError("DERIVED_GOAL_PRESENT_AS_GIVEN")
    # No extra providers, wrapper, pre-completed proof, or injected proof steps.
    provider = shared_expansion_provider(screened, proof_target=root)
    public_plan = public_quadruple_backward_plan(goal, available)
    if tuple((target, option.rule.name, option.subgoals) for target, option in public_plan) != tuple(
            (target, option.rule.name, option.subgoals) for target, option in plan):
        raise RuntimeError("PUBLIC_PLAN_MISMATCH")
    if not any(option.rule.name == plan[-1][1].rule.name and option.subgoals == plan[-1][1].subgoals
               for option in provider(goal)):
        raise RuntimeError("DEFAULT_PROVIDER_FINAL_CANDIDATE_MISSING")

    events = []
    result = reconstruct_registered_goal(goal, screened, sources[0].assertion_id, provider,
        lookup_mode="typed_reference", progress_observer=lambda kind, target, step: events.append((kind, target)))
    visited = []

    def visit(step):
        if any(step is earlier for earlier in visited):
            return
        visited.append(step)
        for child in step.premises:
            visit(child)

    visit(result)
    if result.conclusion != goal or result.rule is not ProofRule.INFERENCE:
        raise RuntimeError("FINAL_GOAL_NOT_INFERRED")
    for target, expansion in tuple(transport_plan) + plan:
        if not any(step.conclusion == target and step.rule is ProofRule.INFERENCE
                   and step.inference_rule.name == expansion.rule.name
                   and tuple(child.conclusion for child in step.premises) == expansion.subgoals
                   for step in visited):
            raise RuntimeError("TREE_STAGE_MISSING:" + expansion.rule.name + ":" + repr(target))
    quad = next((step for step in visited if step.conclusion == forward), None)
    if (quad is None or quad.rule is not ProofRule.INFERENCE or quad.inference_rule.name != RULE_NAME
            or tuple(child.conclusion for child in quad.premises) != quadruple_inputs(forward)
            or quad.premises[0].rule is not ProofRule.INFERENCE
            or any(child.rule is not ProofRule.GIVEN for child in quad.premises[1:])):
        raise RuntimeError("TODA55_TREE_MISSING")
    witness_targets = tuple(dict.fromkeys(child for _, option in notation for child in option.subgoals
                                         if isinstance(child, GeneratorSuspension)))
    for witness in witness_targets:
        if not any(step.conclusion == witness and step.rule is ProofRule.INFERENCE for step in visited):
            raise RuntimeError("ETA_WITNESS_NOT_INFERRED")
    givens = tuple(step for step in visited if step.rule is ProofRule.GIVEN)
    if any(not any(step is link.step for link in links) for step in givens):
        raise RuntimeError("UNSCREENED_GIVEN")
    for required in (Toda55UniversalQuadrupleStatement(), TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula()):
        if not any(step.conclusion == required for step in givens):
            raise RuntimeError("CITED_ANCESTOR_MISSING:" + repr(required))
    if not any(kind == "proved" and target == goal for kind, target in events):
        raise RuntimeError("FINAL_DFS_EVENT_MISSING")
    generator = getattr(root.rhs, "generator", None)
    return {
        "gate": "PASS_R3R41_DEFAULT_SHARED_DFS_HOPF_QUADRUPLE",
        "raw_eta_cube_equal": transported.rhs == forward.rhs,
        "notation_steps": len(notation),
        "independently_inferred_eta_witnesses": len(witness_targets),
        "notation_connection_proved": True,
        "r3r39_six_steps_preserved": True,
        "toda55_inferred_with_cited_ancestors": True,
        "default_shared_dfs_hopf_quadruple_proved": True,
        "audit_only_provider_used": False,
        "registered_generator_matches_audit_expression": generator == goal.lhs.expression,
        "registered_generator_repr": repr(generator),
        "shared_default_provider_modified": True,
        "root_group_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        source_guard()
        result = {"gate": "PASS_R3R41_DRYRUN", "full_pytest": "NOT_RUN"} if args.dry_run else probe()
    except Exception as error:
        result = {"gate": "FAIL_R3R41", "error": type(error).__name__ + ": " + str(error), "full_pytest": "NOT_RUN"}
    destination = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE / "report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R41_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_public_connection.py`

```python
"""Focused public proposal and patch contracts."""
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, MapApplication, Multiple
from phase176_r3r40r1_eta_notation_bridge.tests.test_notation import example
from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan
from phase176_r3r41_public_quadruple_connection.source import (
    build_public_quadruple_connection_provider, public_quadruple_backward_plan,
)
from phase176_r3r41_public_quadruple_connection.apply import TARGET, SETUP, DISPATCH, updated_source
from proof import Relation


def test_public_plan_matches_audited_obligations():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    plan = public_quadruple_backward_plan(goal, available)
    expected = connection_backward_plan(transported, forward, available)
    assert len(plan) == 21
    assert [(t, x.rule.name, x.subgoals) for t, x in plan] == [
        (t, x.rule.name, x.subgoals) for t, x in expected]
    assert transported not in dict(plan) and forward not in dict(plan)


def test_source_gate_rejects_missing_and_duplicate_citations():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    for i in range(len(available)):
        assert public_quadruple_backward_plan(goal, available[:i] + available[i+1:]) == ()
        assert public_quadruple_backward_plan(goal, available + (available[i],)) == ()
    with pytest.raises(TypeError):
        public_quadruple_backward_plan(goal, list(available))


def test_provider_replays_all_stages_in_own_context():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    plan = public_quadruple_backward_plan(goal, available)
    provider = build_public_quadruple_connection_provider(available)
    assert provider(plan[0][0]) == ()
    assert len(provider(goal)) == 1
    for target, option in reversed(plan):
        actual, = provider(target)
        assert actual.rule.name == option.rule.name and actual.subgoals == option.subgoals
    assert provider(transported) == () and provider(forward) == ()
    assert build_public_quadruple_connection_provider(available)(plan[0][0]) == ()


def test_wrong_multiple_and_generator_are_rejected():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    assert public_quadruple_backward_plan(replace(goal, rhs=Multiple(2, forward.lhs.expression)), available) == ()
    wrong = replace(forward.lhs.expression, generator=GeneratorSymbol('η', index=5))
    assert public_quadruple_backward_plan(replace(goal, rhs=Multiple(4, wrong)), available) == ()
    lhs = goal.lhs
    alpha = replace(lhs.expression.left, name='not a cited generator')
    assert public_quadruple_backward_plan(replace(goal, lhs=MapApplication(lhs.map, Composition(alpha, lhs.expression.right))), available) == ()


def test_patch_is_lf_idempotent_and_minimal():
    current = TARGET.read_bytes().decode('utf-8')
    assert '\r' not in current
    assert updated_source(current) == current
    assert current.count(SETUP) == current.count(DISPATCH) == 1
    baseline = current.replace(SETUP, '').replace(DISPATCH, '')
    assert updated_source(baseline) == current
    with pytest.raises(ValueError):
        updated_source(current.replace(DISPATCH, ''))
    with pytest.raises(ValueError):
        updated_source(current.replace('\n', '\r\n'))
```

## `tests/test_apply.py`

```python
"""Regression tests for the two legitimate Prop. 2.7 imports."""
from __future__ import annotations

import difflib

import pytest

from phase176_r3r41_public_quadruple_connection.apply import (
    DISPATCH, DISPATCH_ANCHOR, PATCHED_DISPATCH_ANCHOR, SETUP, SETUP_ANCHOR,
    updated_source,
)


BASELINE = '''def build_shared_typed_bridge():
    if True:
        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
            register_positioned_prop27,
        )
    return register_positioned_prop27


def shared_expansion_provider(bridge, prior_conclusions=()):
    available = ()
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")

    def expand(goal):
        options = []
        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
            expand_public_cited_prop27_goal,
        )
        options.extend(public_right_hopf_transport(goal))
        return tuple(options)
    return expand


def following_function():
    return None
'''


def test_duplicate_module_import_is_legitimate_and_eight_lines_only():
    assert BASELINE.count(DISPATCH_ANCHOR.splitlines()[1]) == 2
    changed = updated_source(BASELINE)
    assert changed.replace(SETUP, '').replace(DISPATCH, '') == BASELINE
    assert PATCHED_DISPATCH_ANCHOR in changed
    delta = list(difflib.ndiff(BASELINE.splitlines(), changed.splitlines()))
    assert len([line for line in delta if line.startswith('+ ')]) == 8
    assert not any(line.startswith('- ') for line in delta)
    assert updated_source(changed) == changed


def test_same_setup_text_outside_target_function_does_not_conflict():
    extra = ('\ndef unrelated(prior_conclusions):\n' + SETUP_ANCHOR
             + '        raise TypeError("other function")\n')
    original = BASELINE + extra
    changed = updated_source(original)
    assert changed.endswith(extra)
    assert changed.replace(SETUP, '').replace(DISPATCH, '') == original


def test_missing_or_wrong_inner_dispatch_is_rejected():
    wrong = BASELINE.replace(DISPATCH_ANCHOR, DISPATCH_ANCHOR.replace(
        'expand_public_cited_prop27_goal', 'register_positioned_prop27'))
    with pytest.raises(ValueError, match='SHARED_DISPATCH_ANCHOR_NOT_UNIQUE'):
        updated_source(wrong)
    duplicate = BASELINE.replace(DISPATCH_ANCHOR, DISPATCH_ANCHOR +
        '        )\n' + DISPATCH_ANCHOR)
    with pytest.raises(ValueError, match='SHARED_DISPATCH_ANCHOR_NOT_UNIQUE'):
        updated_source(duplicate)


def test_partial_or_moved_patch_is_rejected():
    changed = updated_source(BASELINE)
    with pytest.raises(ValueError, match='PARTIAL_OR_CHANGED'):
        updated_source(changed.replace(DISPATCH, ''))
    moved = changed.replace(DISPATCH, '').replace(
        '        return tuple(options)\n', DISPATCH + '        return tuple(options)\n')
    with pytest.raises(ValueError, match='DUPLICATE_OR_MOVED'):
        updated_source(moved)


def test_missing_r3r39_or_crlf_is_rejected():
    with pytest.raises(ValueError, match='R3R39_HOOK_MISSING'):
        updated_source(BASELINE.replace('        options.extend(public_right_hopf_transport(goal))\n', ''))
    with pytest.raises(ValueError, match='EXPECTED_REPAIRED_LF_SOURCE'):
        updated_source(BASELINE.replace('\n', '\r\n'))
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $mode = @()
    if ($DryRun) { $mode += '--dry-run' }
    & python -B -m phase176_r3r41_public_quadruple_connection.apply @mode
    if ($LASTEXITCODE -ne 0) { throw 'R3R41 patch failed' }
    & python -B -m phase176_r3r41_public_quadruple_connection.audit @mode
    if ($LASTEXITCODE -ne 0) { throw 'R3R41 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r41_public_quadruple_connection\tests\test_apply.py `
            .\phase176_r3r41_public_quadruple_connection\tests\test_public_connection.py `
            .\phase176_r3r40r1_eta_notation_bridge\tests\test_notation.py `
            .\phase176_r3r40_toda55_connection_audit\tests\test_connection.py `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests\test_source.py `
            .\phase176_r3r28_toda55_quadruple_public\tests\test_public.py `
            .\phase176_r3r39_public_equality_transport\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R41 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R41 git diff check failed' }
        Write-Host 'PHASE176_R3R41_GATE=PASS_R3R41_PUBLIC_QUADRUPLE_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R41R1_GATE=PASS_R3R41R1_SCOPED_PATCH_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R41_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally { Pop-Location }
```
