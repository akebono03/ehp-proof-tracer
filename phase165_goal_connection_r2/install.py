from pathlib import Path
import ast
import json
import shutil

root = Path.cwd()

def replace_function(path, name, replacement):
    text = path.read_text(encoding='utf-8-sig')
    tree = ast.parse(text)
    node = next((x for x in tree.body if isinstance(x, (ast.FunctionDef,ast.AsyncFunctionDef)) and x.name == name), None)
    if node is None:
        raise RuntimeError(f'{name} not found in {path.name}')
    lines = text.splitlines(keepends=True)
    new = ''.join(lines[:node.lineno-1]) + replacement.rstrip() + '\n\n' + ''.join(lines[node.end_lineno:])
    ast.parse(new)
    if new == text:
        return False
    backup = path.with_name(path.name + '.goal_connection_r2_before.bak')
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(new, encoding='utf-8')
    return True

search = '''def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None):
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
web = '''def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
  *,
  goal=None,
) -> WebGroupProofView:
  """Render a shared search for an optional caller-supplied typed proof goal."""
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    raise ValueError("group proof is available only for positive-dimensional group queries")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")

  from phase165_r55_nk_only_goal import search_group_from_registered_goal
  from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

  result = search_group_from_registered_goal(n=n, k=k, goal=goal)
  return build_partial_web_group_proof_view(
    result,
    max_depth=max_depth,
    mode=mode,
  )
'''
changes = [
    ('phase165_r55_nk_only_goal.py','search_group_from_registered_goal',search),
    ('web_group_proof.py','build_standard_web_group_proof_view',web),
]
output={}
for filename,name,source in changes:
    path=root/filename
    if not path.is_file():
        raise FileNotFoundError(path)
    output[filename]='MODIFIED' if replace_function(path,name,source) else 'UNCHANGED'
print(json.dumps({'status':'INSTALLED','changes':output,'full_pytest_run':False},ensure_ascii=False))
