from __future__ import annotations
import ast
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'phase165_r55_nk_only_goal.py'

HELPER = '''def _r3q_publication_boundary(bridge, candidate):
    """Locate a printed target without confusing a goal with a citation leaf.

    Return no boundary when the registered publication claim is not unique.
    Unlocated and specialized goals must not receive invented positions.
    """
    from phase166_r3c_publication_order import precedes_citing_assertion

    def contains_relation(content):
        if isinstance(content, Relation):
            return type(content) is type(candidate) and content == candidate
        if is_dataclass(content) and not isinstance(content, type):
            return any(contains_relation(getattr(content, field.name))
                       for field in fields(content))
        if isinstance(content, (tuple, list)):
            return any(contains_relation(item) for item in content)
        return False

    matches = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if not contains_relation(assertion.content):
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None or assertion.component_position is None:
            continue
        matches.append(assertion.assertion_id)
    if len(matches) != 1:
        return None
    target_id = matches[0]
    # A target is a boundary, not a usable premise. Check that this is a
    # meaningful position, through the already-adopted common comparator.
    if not any(precedes_citing_assertion(bridge, previous.assertion_id, target_id)
               for previous in bridge.registry._assertions.values()):
        return None
    return target_id
'''

FUNCTION = '''def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None):
    """Search typed goals, using publication order only for located targets.

    Selecting the target and authorizing cited premises are separate actions.
    When the registered target has no unique printed location, do not invent
    one or reject an otherwise valid ordinary Web query.
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
    boundary_id = _r3q_publication_boundary(bridge, candidate)
    result = search_shared_group_goal(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
        **({"citing_assertion_id": boundary_id} if boundary_id is not None else {}),
    )
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
'''

def get_span(src, name):
    tree = ast.parse(src)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f'expected one function: {name}, found {len(nodes)}')
    lines = src.splitlines(keepends=True)
    node = nodes[0]
    return (sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno])))

def main():
    if not TARGET.is_file():
        raise SystemExit('Missing source file; run from project root')
    original = TARGET.read_text(encoding='utf-8')
    if '_r3q_publication_boundary' in original:
        raise SystemExit('R3-Q implementation already present; refusing duplicate install')
    start, end = get_span(original, 'search_group_from_registered_goal')
    current = original[start:end]
    required = ('registered_group_goal_candidates(bridge, n=n, k=k)', 'search_shared_group_goal(', 'proof_order_catalog=proof_order_catalog')
    if any(token not in current for token in required):
        raise SystemExit('Unexpected local function: no changes made')
    updated = original[:start] + HELPER + '\n\n' + FUNCTION + original[end:]
    ast.parse(updated)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT / 'phase166_r3q_reimplementation_backups' / stamp
    folder.mkdir(parents=True)
    shutil.copy2(TARGET, folder / TARGET.name)
    TARGET.write_text(updated, encoding='utf-8')
    (folder / 'NEW_FUNCTIONS.py.txt').write_text(HELPER + '\n\n' + FUNCTION, encoding='utf-8')
    print('PATCHED:', TARGET)
    print('BACKUP:', folder)
    print('FUNCTIONS: _r3q_publication_boundary, search_group_from_registered_goal')
    print('SHA256:', hashlib.sha256(updated.encode('utf-8')).hexdigest())

if __name__ == '__main__':
    main()
