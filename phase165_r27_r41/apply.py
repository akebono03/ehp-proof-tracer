"""Phase 165 R27-R41: isolate operation grammar and route legacy CLI element."""
import ast
import json
from pathlib import Path
import shutil
import sys

BASE = Path(__file__).resolve().parent.parent
BACKUP = BASE / 'phase165_r27_r41_backup'


def _function_span(source, name):
    tree = ast.parse(source)
    found = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(found) != 1:
        raise ValueError(f'expected exactly one {name}')
    node = found[0]
    lines = source.splitlines(keepends=True)
    return sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno]))


def prepare(base):
    cli = base / 'cli.py'
    lookup = base / 'phase165_r27_r34_typed_lookup.py'
    parser = base / 'repository_operation_query.py'
    target = base / 'toda_operation_query.py'
    for p in (cli, lookup, parser):
        if not p.is_file():
            raise FileNotFoundError(str(p))
    c = cli.read_text(encoding='utf-8-sig')
    l = lookup.read_text(encoding='utf-8-sig')
    p = parser.read_text(encoding='utf-8-sig')
    if target.exists() and target.read_text(encoding='utf-8-sig') != p:
        raise ValueError('existing toda_operation_query.py differs from source parser')
    ast.parse(p)
    old = 'from repository_operation_query import'
    new = 'from toda_operation_query import'
    if old in l:
        lnew = l.replace(old, new)
    elif new in l:
        lnew = l
    else:
        raise ValueError('typed lookup import anchor missing')
    fn_start, fn_end = _function_span(c, '_run_element_command')
    replacement = '''def _run_element_command(
  repository: ProofRepository,
  generator_input: str,
  stdout: TextIO,
  stderr: TextIO,
) -> int:
  """Explore typed generator statements without replaying the old repository."""
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex

  try:
    generator = resolve_generator_input(generator_input)
    result = search_typed_generator_statements(generator_input)
  except (TypeError, ValueError) as error:
    print(f"error: {error}", file=stderr)
    return 2

  _write_markdown(stdout, f"## Generator: {generator_input.strip()}")
  _write_markdown(stdout, f"Search status: {result.status.value}")
  for step in result.proven_steps:
    try:
      statement = render_toda_proof_statement_latex(step.conclusion)
    except (TypeError, ValueError):
      statement = repr(step.conclusion)
    _write_markdown(stdout, f"- ${statement}$")
  for diagnostic in result.diagnostics:
    _write_markdown(stdout, f"- {diagnostic}")
  if result.open_goals:
    _write_markdown(stdout, f"Open goals: {len(result.open_goals)}")
  return 0
'''
    cnew = c[:fn_start] + replacement + c[fn_end:]
    # remove only the now-unused direct legacy facade import
    tree = ast.parse(cnew)
    imports = [n for n in tree.body if isinstance(n, ast.ImportFrom) and n.module == 'repository_element_facade']
    for node in reversed(imports):
        if [x.name for x in node.names] != ['explore_repository_generator']:
            raise ValueError('legacy facade import structure changed')
        lines = cnew.splitlines(keepends=True)
        a = sum(map(len, lines[:node.lineno - 1]))
        b = sum(map(len, lines[:node.end_lineno]))
        cnew = cnew[:a] + cnew[b:]
    ast.parse(cnew)
    ast.parse(lnew)
    return {cli: cnew, lookup: lnew, target: p}


def install(base=BASE):
    updates = prepare(base)
    changed = [p for p, content in updates.items() if not p.exists() or p.read_text(encoding='utf-8-sig') != content]
    backup = base / 'phase165_r27_r41_backup'
    for p in changed:
        if p.exists() and (backup / p.name).exists() and (backup / p.name).read_bytes() != p.read_bytes():
            raise ValueError(f'backup collision: {p.name}')
    backup.mkdir(exist_ok=True)
    for p in changed:
        if p.exists():
            shutil.copy2(p, backup / p.name)
        p.write_text(updates[p], encoding='utf-8')
    report = {'phase':'165 R27-R41','status':'CHANGED' if changed else 'ALREADY_INSTALLED', 'modified_files':[p.name for p in changed], 'legacy_element_facade_removed':True, 'operation_parser_migrated':True, 'full_pytest_run':False}
    (base/'phase165_r27_r41_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    install()
