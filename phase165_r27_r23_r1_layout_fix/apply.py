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

def _has_import(tree: ast.Module, module: str, name: str) -> bool:
    return any(
        isinstance(node, ast.ImportFrom)
        and node.module == module
        and any(alias.name == name for alias in node.names)
        for node in tree.body
    )


def _replace_terminal_main_branch(main_node: ast.FunctionDef, source_lines: list[str]) -> str:
    """Keep all CLI subcommand dispatch; replace only the default n/k branch."""
    parser_assignments = [
        node for node in main_node.body
        if isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == 'build_argument_parser'
    ]
    if len(parser_assignments) != 1:
        raise RuntimeError('Default group parser boundary is not unique')
    boundary = parser_assignments[0]
    if not any(
        isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and node.value.func.attr == 'parse_args'
        for node in main_node.body
        if node.lineno > boundary.lineno
    ):
        raise RuntimeError('Default parser does not parse arguments')
    if not all(
        isinstance(node, (ast.Assign, ast.If, ast.Expr, ast.Return))
        for node in main_node.body
        if node.lineno >= boundary.lineno
    ):
        raise RuntimeError('Unexpected default group command statements')
    start = boundary.lineno
    indent = source_lines[start - 1][:len(source_lines[start - 1]) - len(source_lines[start - 1].lstrip())]
    return ''.join(source_lines[main_node.lineno - 1:start - 1]) + (
        indent + 'parser = build_argument_parser()\n'
        + indent + 'args = parser.parse_args(raw_argv)\n'
        + indent + 'return _run_group_query_command(\n'
        + indent + '    args.n,\n'
        + indent + '    args.k,\n'
        + indent + ')\n'
    )


def transform(source: str) -> str:
    tree = ast.parse(source)
    defs = {
        node.name: node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    for name in ('main', '_run_group_proof_command'):
        if name not in defs:
            raise RuntimeError('Missing required CLI function: ' + name)

    lines = source.splitlines(keepends=True)
    modifications = []
    main_node = defs['main']
    main_text = _replace_terminal_main_branch(main_node, lines)
    modifications.append((main_node.lineno, main_node.end_lineno, main_text))
    proof_node = defs['_run_group_proof_command']
    modifications.append((proof_node.lineno, proof_node.end_lineno, GROUP_PROOF))
    for first, last, replacement in sorted(modifications, reverse=True):
        lines[first - 1:last] = [replacement.rstrip('\n') + '\n']
    result = ''.join(lines)
    if '_run_group_query_command' not in defs:
        marker = 'def _run_group_proof_command('
        if result.count(marker) != 1:
            raise RuntimeError('Cannot locate group proof function insertion point')
        result = result.replace(marker, GROUP_QUERY + '\n\n' + marker, 1)

    # Add each missing import once; preserve unrelated imports and formatting.
    required = {
        'phase165_r52_partial_proof': ('ProofSearchStatus', 'render_partial_proof_markdown'),
        'phase165_r52_r5_auto_search': ('search_group_structure_automatically',),
    }
    tree = ast.parse(result)
    missing = []
    for module, names in required.items():
        absent = [name for name in names if not _has_import(tree, module, name)]
        if absent:
            missing.append('from ' + module + ' import (\n' + ''.join('    ' + name + ',\n' for name in absent) + ')\n')
    if missing:
        result = ''.join(missing) + '\n' + result

    # Delete legacy builder import only if no remaining reference uses it.
    tree = ast.parse(result)
    has_legacy_call = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == 'build_standard_toda_report'
        for node in ast.walk(tree)
    )
    if has_legacy_call:
        raise RuntimeError('Unexpected legacy builder call remains after CLI migration')
    lines = result.splitlines(keepends=True)
    for node in reversed(tree.body):
        if isinstance(node, ast.ImportFrom) and node.module == 'toda_calculation_facade':
            if len(node.names) == 1 and node.names[0].name == 'build_standard_toda_report':
                lines[node.lineno-1:node.end_lineno] = []
    result = ''.join(lines)
    ast.parse(result)
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
