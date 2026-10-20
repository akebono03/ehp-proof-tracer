"""Restore the pre-R3-J Web dispatcher; leave registry and ordering intact."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

FILE = Path('phase165_r55_nk_only_goal.py')
FUNCTION = '''def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None):
    """Search an explicitly supplied typed goal, without treating it as evidence.

    The optional goal is a Relation carrying the asserted structure and generator.
    Legacy n,k-only calls preserve the existing registered-goal selection path.
    """
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    if goal is not None:
        if (not isinstance(goal, Relation)
                or goal.relation_type is not RelationType.EQUALITY
                or goal.lhs != TodaPrimaryGroup(n + k, n)
                or not isinstance(goal.rhs, _GROUP_STRUCTURES)):
            raise ValueError("goal must be a typed equality for the requested n,k")
    if bridge is None:
        bridge = build_shared_typed_bridge()
    if goal is None:
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        if len(candidates) != 1:
            explanation = (
                "群構造・生成元の型付き証明目標を指定してください"
                if not candidates else
                "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
            )
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(TodaPrimaryGroup(n + k, n),),
                diagnostics=(explanation,),
            )
        candidate = candidates[0]
    else:
        candidate = goal
    if proof_order_catalog is None:
        from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
        proof_order_catalog, order_diagnostic = resolve_reviewed_order_catalog(
            bridge, n=n, k=k,
        )
        if order_diagnostic is not None:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
    result = search_shared_group_goal(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
    )
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
'''

def main() -> None:
    if not FILE.is_file():
        raise SystemExit('Repository root not found: ' + str(FILE))
    src = FILE.read_text(encoding='utf-8')
    tree = ast.parse(src)
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name == 'search_group_from_registered_goal']
    if len(matches) != 1:
        raise SystemExit('Expected exactly one Web dispatch function')
    node = matches[0]
    lines = src.splitlines(keepends=True)
    original = ''.join(lines[node.lineno - 1:node.end_lineno])
    if 'Phase 166 R3-I: select the exact registered source assertion' not in original:
        if original.strip() == FUNCTION.strip():
            print('ALREADY RESTORED; no change')
            return
        raise SystemExit('Unexpected function revision; refusing to overwrite')
    changed = ''.join(lines[:node.lineno - 1]) + FUNCTION + ''.join(lines[node.end_lineno:])
    ast.parse(changed)
    backup_dir = Path('phase166_r3j_pi32_regression_recovery_backup') / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup_dir.mkdir(parents=True, exist_ok=False)
    shutil.copy2(FILE, backup_dir / FILE.name)
    FILE.write_text(changed, encoding='utf-8')
    print('RESTORED FUNCTION:', FILE, 'search_group_from_registered_goal')
    print('BACKUP:', backup_dir)
    print(FUNCTION)
    print('Other files unchanged; full pytest NOT run')

if __name__ == '__main__':
    main()
