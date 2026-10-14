from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent


def replace_function(source: str, function_name: str, new_code: str) -> str:
    tree = ast.parse(source)
    functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == function_name]
    if len(functions) != 1:
        raise RuntimeError(f'Expected exactly one {function_name}; found {len(functions)}')
    lines = source.splitlines(keepends=True)
    node = functions[0]
    start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
    end = node.end_lineno
    return ''.join(lines[:start]) + new_code.rstrip() + '\n\n\n' + ''.join(lines[end:])


def ensure_source(path: Path) -> str:
    if not path.is_file():
        raise RuntimeError(f'Missing target: {path}')
    return path.read_text(encoding='utf-8-sig')


query_path = ROOT / 'web_group_query.py'
main_path = ROOT / 'main.py'
query = ensure_source(query_path)
main = ensure_source(main_path)
if 'def build_standard_web_group_query_view(' not in query:
    raise RuntimeError('Missing Group query API')
if 'def _run_group_proof_command(' not in main or 'def main(' not in main:
    raise RuntimeError('Missing CLI APIs')

new_query = replace_function(query, 'build_standard_web_group_query_view', (BUNDLE / 'web_query_function.txt').read_text(encoding='utf-8'))
# The old report import is no longer needed anywhere in this module.
old_import = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\n'
if old_import not in new_query:
    raise RuntimeError('Unexpected web_group_query import layout; refuse partial migration')
new_query = new_query.replace(old_import, '', 1)
new_main = replace_function(main, '_run_group_proof_command', (BUNDLE / 'cli_proof_function.txt').read_text(encoding='utf-8'))
# Preserve every other CLI subcommand exactly; replace only the normal query tail.
main_ast = ast.parse(new_main)
main_node = next(n for n in main_ast.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
original_lines = new_main.splitlines(keepends=True)
main_body = ''.join(original_lines[main_node.lineno - 1:main_node.end_lineno])
anchor = '  result = (\n    build_standard_toda_report(\n'
if main_body.count(anchor) != 1:
    raise RuntimeError('Expected one normal CLI group-report call')
main_body = main_body[:main_body.index(anchor)] + (BUNDLE / 'cli_normal_query_tail.txt').read_text(encoding='utf-8').rstrip() + '\n'
new_main = replace_function(new_main, 'main', main_body)

for name, content in [('web_group_query.py', new_query), ('main.py', new_main)]:
    compile(content, name, 'exec')

# Back up exact pre-install files, then write only after both transformations validate.
for name, old, new in [('web_group_query.py', query, new_query), ('main.py', main, new_main)]:
    path = ROOT / name
    if old == new:
        print(f'Already installed: {name}')
    else:
        backup = path.with_name(path.name + '.phase165_r27_r8_backup')
        if not backup.exists():
            backup.write_text(old, encoding='utf-8')
        path.write_text(new, encoding='utf-8')
        print(f'Updated: {name}')
print('R27-R8 installed; old proof building code preserved for later audit/removal')
