from __future__ import annotations
import ast
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'main.py'

IMPORTS = '''from phase165_r52_partial_proof import (
    ProofSearchStatus,
    render_partial_proof_markdown,
)
from phase165_r52_r5_auto_search import (
    search_group_structure_automatically,
)
'''
GROUP_PROOF = '''def _run_group_proof_command(
  n: int,
  k: int,
  max_depth: int | None = 2,
  mode: str = "narrative",
) -> int:
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")
  if max_depth is not None and (
    isinstance(max_depth, bool)
    or not isinstance(max_depth, int)
    or max_depth < 0
  ):
    raise ValueError("max_depth must be nonnegative")

  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    print(render_toda_group_query_domain_cli_message(domain))
    return 1

  result = search_group_structure_automatically(n=n, k=k)
  print(render_partial_proof_markdown(result), end="")
  return 0 if result.status is ProofSearchStatus.COMPLETE else 1
'''
GROUP_QUERY = '''def _run_group_query_command(
  n: int,
  k: int,
) -> int:
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    print(render_toda_group_query_domain_cli_message(domain))
    return 0

  result = search_group_structure_automatically(n=n, k=k)
  print(render_partial_proof_markdown(result), end="")
  return 0 if result.status is ProofSearchStatus.COMPLETE else 1
'''

def transform(source: str) -> str:
    if (
        'build_standard_toda_report(' not in source
        and 'def _run_group_query_command(' in source
        and 'from phase165_r52_r5_auto_search import' in source
    ):
        ast.parse(source)
        return source
    tree = ast.parse(source)
    defs = {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    for name in ('main','_run_group_proof_command'):
        if name not in defs: raise RuntimeError('Missing expected function: '+name)
    lines = source.splitlines(keepends=True)
    main_node = defs['main']
    main_text = ''.join(lines[main_node.lineno-1:main_node.end_lineno])
    if 'build_standard_toda_report' in main_text:
        # Preserve all CLI command routing and replace only the terminal group branch.
        start = main_text.index('  query = TodaGroupQuery(',main_text.index('  args = parser.parse_args('))
        main_text = main_text[:start] + '''  return _run_group_query_command(\n    args.n,\n    args.k,\n  )\n'''
    elif 'return _run_group_query_command(' not in main_text:
        raise RuntimeError('Unexpected main group-query layout')
    modifications = [(main_node.lineno,main_node.end_lineno,main_text)]
    group_node = defs['_run_group_proof_command']
    group_text = ''.join(lines[group_node.lineno-1:group_node.end_lineno])
    if 'build_standard_toda_report' in group_text:
        modifications.append((group_node.lineno,group_node.end_lineno,GROUP_PROOF))
    elif 'search_group_structure_automatically' not in group_text:
        raise RuntimeError('Unexpected group-proof function')
    for first,last,repl in sorted(modifications,reverse=True):
        lines[first-1:last]=[repl+'\n']
    result=''.join(lines)
    if not any(isinstance(n,ast.FunctionDef) and n.name=='_run_group_query_command' for n in ast.parse(result).body):
        marker='def _run_group_proof_command('
        if result.count(marker)!=1: raise RuntimeError('Group proof function placement ambiguous')
        result=result.replace(marker,GROUP_QUERY+'\n\n'+marker,1)
    # Delete old calculation imports, but retain unrelated imports for compatibility.
    tree=ast.parse(result)
    rows=result.splitlines(keepends=True)
    old_modules={'toda_calculation_facade','toda_calculation_result'}
    deletions=[]
    for node in tree.body:
        if isinstance(node,ast.ImportFrom) and node.module in old_modules:
            deletions.append((node.lineno,node.end_lineno))
    for first,last in sorted(deletions,reverse=True): rows[first-1:last]=[]
    result=''.join(rows)
    if 'from phase165_r52_r5_auto_search import' not in result:
        result=IMPORTS+'\n'+result
    ast.parse(result)
    if 'build_standard_toda_report(' in result:
        raise RuntimeError('Legacy calculation call remains in CLI')
    return result

def apply() -> None:
    before=TARGET.read_text(encoding='utf-8-sig')
    after=transform(before)
    if after==before:
        print('R27-R23 already installed')
        return
    backup=Path(__file__).resolve().parent/'main_before_r23.py'
    if not backup.exists(): backup.write_text(before,encoding='utf-8')
    TARGET.write_text(after,encoding='utf-8')
    print('R27-R23 installed: CLI group query/proof now use typed Backward Search')

if __name__=='__main__': apply()
