"""Phase 165 R27-R38: replace legacy operation entry points and sweep dead modules."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASE = '165 R27-R38'
TARGETS = ('main.py', 'web_operation_query_proof.py')

QUERY = '''def _run_query_command(query_input: str) -> int:
  from phase165_r27_r34_typed_lookup import search_typed_operation_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  try:
    result = search_typed_operation_statements(query_input)
  except (TypeError, ValueError) as error:
    build_query_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  for step in result.proven_steps:
    print(render_toda_proof_statement_latex(step.conclusion))
  for message in result.diagnostics:
    print(message)
  if result.open_goals:
    print(f"Unresolved goals: {len(result.open_goals)}")
  return 0 if result.proven_steps else 1
'''
QUERY_PROOF = '''def _run_query_proof_command(
  query_input: str,
  fact_number: int | None = None,
  max_depth: int | None = None,
) -> int:
  from phase165_r27_r34_typed_lookup import search_typed_operation_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  if fact_number is not None and (type(fact_number) is not int or fact_number < 1):
    build_query_proof_argument_parser().error("fact_number must be positive")
  if max_depth is not None and (type(max_depth) is not int or max_depth < 0):
    build_query_proof_argument_parser().error("max_depth must be nonnegative")
  try:
    result = search_typed_operation_statements(query_input)
  except (TypeError, ValueError) as error:
    build_query_proof_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  if not result.proven_steps:
    for message in result.diagnostics:
      print(message)
    print(f"Unresolved goals: {len(result.open_goals)}")
    return 1
  if fact_number is None and len(result.proven_steps) > 1:
    for index, step in enumerate(result.proven_steps, start=1):
      print(f"{index}: {render_toda_proof_statement_latex(step.conclusion)}")
    print("Specify --fact N to select one proven statement.")
    return 1
  selected = fact_number if fact_number is not None else 1
  if selected > len(result.proven_steps):
    print("Requested fact is not among proven statements.")
    return 1
  step = result.proven_steps[selected - 1]
  print(render_toda_proof_statement_latex(step.conclusion))
  if result.open_goals:
    print(f"Unresolved goals: {len(result.open_goals)}")
  return 0
'''
WEB_PROOF = '''def build_standard_web_operation_query_proof_view(
  query_input: str,
  fact_number: int,
  max_depth: int = 1,
) -> WebOperationQueryProofView:
  """Display only steps proved by the canonical typed search, without replay."""
  from phase165_r27_r34_typed_lookup import search_typed_operation_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  if not isinstance(query_input, str):
    raise TypeError("query_input must be a str")
  query_input = query_input.strip()
  if not query_input:
    raise ValueError("operation query is required")
  if type(fact_number) is not int:
    raise TypeError("fact_number must be an int")
  if fact_number <= 0:
    raise ValueError("fact_number must be positive")
  if type(max_depth) is not int:
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  result = search_typed_operation_statements(query_input)
  if fact_number > len(result.proven_steps):
    raise ValueError(
      "requested fact is not proved by typed backward search; "
      f"status={result.status.value}; open_goals={len(result.open_goals)}"
    )
  step = result.proven_steps[fact_number - 1]
  statement_latex = render_toda_proof_statement_latex(step.conclusion)
  if not isinstance(statement_latex, str) or not statement_latex:
    raise ValueError("typed proof conclusion is not renderable")
  rule_name = (
    step.inference_rule.name if step.inference_rule is not None
    else step.rule.value
  )
  return WebOperationQueryProofView(
    query_input=query_input,
    fact_number=fact_number,
    conclusion_latex=statement_latex,
    provenance=WebOperationQueryProofProvenanceView(
      theorem=None,
      phase=None,
      key="typed-backward-search",
      depth=0,
    ),
    steps=(WebOperationQueryProofStepView(
      depth=0,
      statement_latex=statement_latex,
      fallback_type_name=None,
      rule_name=rule_name,
    ),),
    max_depth=max_depth,
  )
'''

def replace_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    matches = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    if len(matches) != 1:
        raise RuntimeError(f'expected exactly one {name}, got {len(matches)}')
    node = matches[0]
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [replacement.rstrip() + '\n']
    result = ''.join(lines)
    ast.parse(result)
    return result

def prune_unused_repository_imports(source: str) -> tuple[str, list[str]]:
    tree = ast.parse(source)
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    changes = []
    removed = []
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or not (node.module or '').startswith('repository_'):
            continue
        if any(alias.name == '*' for alias in node.names):
            continue
        keep = [alias for alias in node.names if (alias.asname or alias.name) in used]
        if len(keep) == len(node.names):
            continue
        removed.extend(f'{node.module}.{alias.name}' for alias in node.names if alias not in keep)
        statement = ''
        if keep:
            symbols = ', '.join(alias.name + (' as ' + alias.asname if alias.asname else '') for alias in keep)
            statement = f'from {node.module} import {symbols}\n'
        changes.append((node.lineno - 1, node.end_lineno, statement))
    lines = source.splitlines(keepends=True)
    for start, end, value in reversed(changes):
        lines[start:end] = [value] if value else []
    result = ''.join(lines)
    ast.parse(result)
    return result, removed

def dependency_graph(root: Path, overrides: dict[str, str]) -> dict:
    sources = {}
    for path in sorted(root.glob('*.py')):
        if path.name.startswith(('test_', 'audit_')) or '.phase' in path.stem or path.stem.endswith(('_backup', '_pre_cleanup')):
            continue
        sources[path.stem] = overrides.get(path.name, path.read_text(encoding='utf-8-sig'))
    edges = {}
    for name, source in sources.items():
        imports = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split('.')[0])
        edges[name] = imports & sources.keys()
    candidates = {name for name in sources if name.startswith('repository_')}
    protected = set(sources) - candidates
    queue = list(protected)
    while queue:
        for dep in edges[queue.pop()]:
            if dep not in protected:
                protected.add(dep)
                queue.append(dep)
    return {'deletable': sorted(candidates - protected),
            'retained_repository_modules': sorted(candidates & protected),
            'reachable_from_non_repository': {k: sorted(edges[k] & candidates) for k in sorted(sources.keys() - candidates) if edges[k] & candidates}}

def prepare(root: Path) -> tuple[dict[str, str], dict]:
    sources = {name: (root / name).read_text(encoding='utf-8-sig') for name in TARGETS}
    replacements = {
        'main.py': [('_run_query_command', QUERY), ('_run_query_proof_command', QUERY_PROOF)],
        'web_operation_query_proof.py': [('build_standard_web_operation_query_proof_view', WEB_PROOF)],
    }
    changes = {}
    removed_imports = {}
    for name, funcs in replacements.items():
        after = sources[name]
        for fname, new in funcs:
            after = replace_function(after, fname, new)
        after, removed = prune_unused_repository_imports(after)
        removed_imports[name] = removed
        if after != sources[name]:
            changes[name] = after
    report = dependency_graph(root, changes)
    report.update(phase=PHASE, modified_files=sorted(changes), imports_removed=removed_imports, full_pytest_run=False)
    return changes, report

def apply(root: Path = ROOT) -> dict:
    changes, report = prepare(root)
    backup_dir = root / 'phase165_r27_r38_backup'
    archive = {name: root / name for name in changes}
    archive.update({name + '.py': root / (name + '.py') for name in report['deletable']})
    for original in archive.values():
        target = backup_dir / original.name
        if target.exists() and target.read_bytes() != original.read_bytes():
            raise RuntimeError(f'conflicting prior backup: {target}')
    backup_dir.mkdir(exist_ok=True)
    for original in archive.values():
        target = backup_dir / original.name
        if not target.exists():
            shutil.copy2(original, target)
    for name, contents in changes.items():
        (root / name).write_text(contents, encoding='utf-8')
    for name in report['deletable']:
        (root / (name + '.py')).unlink()
    report['status'] = 'CHANGED' if changes or report['deletable'] else 'NO_SAFE_CHANGES'
    (root / 'phase165_r27_r38_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report

if __name__ == '__main__':
    print(json.dumps(apply(), ensure_ascii=False, indent=2))
