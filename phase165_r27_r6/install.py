"""Phase 165 R27-R6: disconnect legacy proof construction from two public entries."""
from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path.cwd()

def replace_function(text: str, name: str, new_source: str) -> str:
    parsed = ast.parse(text)
    funcs = [n for n in parsed.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    if len(funcs) != 1:
        raise RuntimeError(f"Expected one top-level function {name}")
    old = funcs[0]
    lines = text.splitlines(keepends=True)
    return ''.join(lines[:old.lineno-1]) + new_source.rstrip() + '\n' + ''.join(lines[old.end_lineno:])

AUTO_FUNCTION = '''def search_group_structure_automatically(
    *, n: int, k: int,
    discovery=None,
) -> PartialProofResult:
    """Search registered typed group propositions without legacy calculation/replay.

    Never infer an expected group answer from the old repository.
    Unregistered structures remain open goals instead of becoming proofs.
    """
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    group = TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
    if discovery is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs
        discovery = discover_goal_search_inputs()

    bridge = discovery.bridge
    provider = discovery.expansion_provider
    assertions = tuple(bridge.registry._assertions.values())
    structural_candidates = _typed_structure_candidates(bridge, group)
    if not assertions:
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=(GroupStructureSearchGoal(group),),
            diagnostics=("命題台帳に登録主張がなく、型付き探索を開始できない",),
        )

    context_id = assertions[0].assertion_id
    goals = structural_candidates or (GroupStructureSearchGoal(group),)
    attempts = tuple(
        search_registered_partial_proof(
            n=n, k=k, goal=goal, bridge=bridge,
            citing_assertion_id=context_id,
            expansion_provider=provider,
            lookup_mode="typed_reference",
        )
        for goal in goals
    )
    unique_steps = []
    open_goals = []
    diagnostics = []
    complete = []
    for attempt in attempts:
        for step in attempt.proven_steps:
            if not any(step is found for found in unique_steps):
                unique_steps.append(step)
        for goal in attempt.open_goals:
            if not any(_same(goal, earlier) for earlier in open_goals):
                open_goals.append(goal)
        diagnostics.extend(attempt.diagnostics)
        if attempt.status is ProofSearchStatus.COMPLETE:
            complete.append(attempt)

    if len(complete) == 1 and len(structural_candidates) == 1:
        result = complete[0]
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.COMPLETE,
            structure_status=GroupStructureStatus.KNOWN,
            references=result.references,
            proven_steps=tuple(unique_steps),
            conclusion=result.conclusion,
        )
    if complete:
        diagnostics.append(
            "群構造の候補が複数あるため、一意の最終結論は認定しない"
        )
    if not structural_candidates:
        diagnostics.append(
            "群構造について型付きの具体的候補命題が未登録。"
            "SOURCE_ARCHIVE の文字列は証明前提に昇格させない"
        )
    return make_partial_proof_result(
        n=n, k=k,
        status=ProofSearchStatus.PARTIAL if unique_steps else ProofSearchStatus.SEARCH_FAILED,
        proven_steps=tuple(unique_steps),
        open_goals=tuple(open_goals) or (GroupStructureSearchGoal(group),),
        diagnostics=tuple(dict.fromkeys(diagnostics)),
    )
'''

OLD_WEB = '''          view = (
            build_standard_web_group_query_view(
              n=n,
              k=k,
            )
          )
          try:
            group_proof_view = (
              build_standard_web_group_proof_view(
                n,
                k,
                max_depth=group_proof_depth,
                mode=group_proof_mode_value,
              )
            )
          except GoalSearchIncompleteError:
            group_proof_view = build_group_proof_progress_view(
              n=n,
              k=k,
              max_depth=group_proof_depth,
            )'''
NEW_WEB = '''          group_proof_view = build_group_proof_progress_view(
            n=n,
            k=k,
            max_depth=group_proof_depth,
          )'''

def main():
    target_auto = ROOT / 'phase165_r52_r5_auto_search.py'
    target_web = ROOT / 'web_app.py'
    if not all(p.is_file() for p in (target_auto, target_web)):
        raise SystemExit('Run from ehp-proof-tracer repository root')
    auto = target_auto.read_text(encoding='utf-8-sig')
    web = target_web.read_text(encoding='utf-8-sig')
    if 'from toda_calculation_facade import build_standard_toda_report' in auto:
        new_auto = replace_function(auto, 'search_group_structure_automatically', AUTO_FUNCTION)
    elif 'legacy calculation/replay' in auto:
        new_auto = auto
    else:
        raise RuntimeError('Unexpected auto-search baseline; no files changed')
    if OLD_WEB in web:
        new_web = web.replace(OLD_WEB, NEW_WEB, 1)
    elif NEW_WEB in web and 'except GoalSearchIncompleteError:' not in web:
        new_web = web
    else:
        raise RuntimeError('Unexpected Flask route baseline; no files changed')
    if 'from phase165_goal_only_search import GoalSearchIncompleteError\n' in new_web:
        new_web = new_web.replace('from phase165_goal_only_search import GoalSearchIncompleteError\n', '', 1)
    if '  build_standard_web_group_proof_view,\n' in new_web:
        new_web = new_web.replace('  build_standard_web_group_proof_view,\n', '', 1)
    for target, old, new in ((target_auto, auto, new_auto), (target_web, web, new_web)):
        if old != new:
            target.with_name(target.name + '.phase165_r27_r6_backup').write_text(old, encoding='utf-8')
            target.write_text(new, encoding='utf-8')
            print('Updated', target.name)
        else:
            print('Already installed', target.name)
    print('R27-R6 installed; legacy group-query route and legacy implementation remain for later removal')

if __name__ == '__main__':
    main()
