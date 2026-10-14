from pathlib import Path
import ast
import shutil

root = Path.cwd()
old = root / 'web_group_proof.py'
common = root / 'web_group_proof_common.py'
adapter = root / 'phase165_r52_r3_web_adapter.py'
if not all(p.is_file() for p in (old, common, adapter)):
    raise SystemExit('R27-R10 prerequisite missing: common Web module and adapter required; no changes made')
common_tree = ast.parse(common.read_text(encoding='utf-8-sig'))
common_defs = {node.name for node in common_tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
needed = {'WebGroupProofView', 'WebGroupProofStepView', '_build_group_proof_rendered_lines', '_group_proof_rule_name', '_group_proof_statement_latex'}
if not needed.issubset(common_defs):
    raise SystemExit('R27-R10 common definitions incomplete; no changes made')
if 'from web_group_proof_common import' not in adapter.read_text(encoding='utf-8-sig'):
    raise SystemExit('R27-R10 adapter has not been migrated; no changes made')
source = old.read_text(encoding='utf-8-sig')
tree = ast.parse(source)
funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build_standard_web_group_proof_view']
if len(funcs) != 1:
    raise SystemExit('Legacy entry function not uniquely located; no changes made')
node = funcs[0]
lines = source.splitlines(keepends=True)
replacement = '''def build_standard_web_group_proof_view(
    n: int,
    k: int,
    max_depth: int = 2,
    mode: str = "narrative",
) -> WebGroupProofView:
    """Compatibility entry: use only the registered shared backward search."""
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")

    from phase165_r52_r5_auto_search import search_group_structure_automatically
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    result = search_group_structure_automatically(n=n, k=k)
    return build_partial_web_group_proof_view(
        result, max_depth=max_depth, mode=mode,
    )
'''
lines[node.lineno - 1:node.end_lineno] = [replacement + '\n']
updated = ''.join(lines)
# Remove old-only module imports only if none of their imported names have live uses.
obsolete = {
    'toda_calculation_facade', 'toda_calculation_result',
    'toda_group_query', 'toda_group_query_semantics',
    'toda_group_proof_narrative_renderer', 'toda_group_proof_outline_renderer',
    'toda_group_proof_presentation', 'toda_group_result_proof_replay',
}
tree2 = ast.parse(updated)
for n in sorted((x for x in tree2.body if isinstance(x, ast.ImportFrom) and x.module in obsolete), key=lambda x:x.lineno, reverse=True):
    names = {alias.asname or alias.name for alias in n.names}
    uses = {x.id for x in ast.walk(tree2) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)}
    if names.isdisjoint(uses):
        ls = updated.splitlines(keepends=True)
        ls[n.lineno-1:n.end_lineno] = []
        updated = ''.join(ls)
        tree2 = ast.parse(updated)
assert 'build_standard_toda_report' not in updated
assert 'build_phase164_r5_r2_common_replay' not in updated
compile(updated, str(old), 'exec')
backup = old.with_suffix('.py.phase165_r27_r11_backup')
if not backup.exists():
    shutil.copy2(old, backup)
old.write_text(updated, encoding='utf-8')
print('R27-R11 installed: legacy Web proof entry now uses canonical search; retained common presentation APIs')
