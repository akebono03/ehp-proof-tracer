"""Phase 165 R27-R35 minimal AST-based cutover, rollback before each change."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

GENERATOR_FUNC = '''def build_standard_web_generator_exploration_view(
  generator_input: str,
) -> WebGeneratorExplorationView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  symbol = resolve_generator_input(generator_input)
  lookup = search_typed_generator_statements(generator_input)
  occurrences = tuple(
    WebGeneratorExplorationOccurrenceView(
      conclusion_latex=render_toda_proof_statement_latex(step.conclusion),
      role_labels=("proved",),
      phase="165 R27-R35",
      theorem="Typed Backward Search",
    )
    for step in lookup.proven_steps
  )
  return WebGeneratorExplorationView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    occurrence_count=len(occurrences),
    toda_bracket_occurrences=(),
    map_input_occurrences=(),
    group_generator_occurrences=(),
    composition_left_occurrences=(),
    composition_right_occurrences=(),
    other_occurrences=occurrences,
    search_status=lookup.status.value,
    diagnostics=lookup.diagnostics,
    open_goal_count=len(lookup.open_goals),
  )
'''

CLI_FUNC = '''def _run_explore_command(generator_input: str) -> int:
  from phase165_r27_r34_typed_lookup import (
    TypedLookupStatus,
    search_typed_generator_statements,
  )
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  try:
    result = search_typed_generator_statements(generator_input)
  except (TypeError, ValueError) as error:
    build_explore_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  for step in result.proven_steps:
    print(f"- ${render_toda_proof_statement_latex(step.conclusion)}$")
  for diagnostic in result.diagnostics:
    print(diagnostic)
  if result.open_goals:
    print(f"Open goals: {len(result.open_goals)}")
  return 0 if result.status is TypedLookupStatus.COMPLETE else 1
'''

# Add optional search metadata; existing callers and dataclass invariants remain.
GENERATOR_FIELDS = '''  search_status: str = "not_searched"
  diagnostics: tuple[str, ...] = ()
  open_goal_count: int = 0
'''
OPERATION_FIELDS = '''  search_status: str = "not_searched"
  diagnostics: tuple[str, ...] = ()
  open_goal_count: int = 0
'''
OPERATION_FUNC = '''def build_standard_web_operation_query_view(query_input: str) -> WebOperationQueryView:
  if not isinstance(query_input, str):
    raise TypeError("query_input must be a str")
  query_input = query_input.strip()
  if not query_input:
    raise ValueError("operation query is required")
  from phase165_r27_r34_typed_lookup import search_typed_operation_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  result = search_typed_operation_statements(query_input)
  items = []
  for step in result.proven_steps:
    statement_latex = render_toda_proof_statement_latex(step.conclusion)
    if not isinstance(statement_latex, str) or not statement_latex:
      continue
    items.append(WebOperationQueryItemView(statement_latex=statement_latex, provenance_count=1))
  return WebOperationQueryView(
    query_input=query_input, found=bool(items), items=tuple(items),
    search_status=result.status.value, diagnostics=result.diagnostics,
    open_goal_count=len(result.open_goals),
  )
'''

def replace_function(source, name, replacement):
    nodes = [x for x in ast.parse(source).body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f"Expected one function {name}, found {len(nodes)}")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1]) + replacement + ''.join(lines[node.end_lineno:])

def ensure_dataclass_fields(source, classname, fields):
    matches = [x for x in ast.parse(source).body if isinstance(x, ast.ClassDef) and x.name == classname]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one class: {classname}")
    node = matches[0]
    existing = {x.target.id for x in node.body if isinstance(x, ast.AnnAssign) and isinstance(x.target, ast.Name)}
    names = {x.target.id for x in ast.parse('class C:\n'+''.join('    '+line for line in fields.splitlines(True))).body[0].body if isinstance(x, ast.AnnAssign)}
    if names <= existing:
        return source
    if existing & names:
        raise RuntimeError('Partially installed optional search status fields')
    lines = source.splitlines(keepends=True)
    # Add fields just before first method; method is after all existing dataclass field declarations.
    methods = [x for x in node.body if isinstance(x, ast.FunctionDef)]
    if not methods:
        raise RuntimeError('Dataclass method boundary missing')
    at = methods[0].lineno - 1
    return ''.join(lines[:at]) + fields + '\n' + ''.join(lines[at:])

def transform_generator(source):
    source = ensure_dataclass_fields(source, 'WebGeneratorExplorationView', GENERATOR_FIELDS)
    source = replace_function(source, 'build_standard_web_generator_exploration_view', GENERATOR_FUNC)
    ast.parse(source)
    return source

def transform_operation(source):
    source = ensure_dataclass_fields(source, 'WebOperationQueryView', OPERATION_FIELDS)
    source = replace_function(source, 'build_standard_web_operation_query_view', OPERATION_FUNC)
    ast.parse(source)
    return source

def transform_main(source):
    source = replace_function(source, '_run_explore_command', CLI_FUNC)
    ast.parse(source)
    return source

def apply():
    changes = {
        'web_generator_exploration.py': transform_generator,
        'web_operation_query.py': transform_operation,
        'main.py': transform_main,
    }
    planned = {}
    for name, transform in changes.items():
        path = ROOT / name
        if not path.is_file():
            raise RuntimeError(f'Missing file {name}')
        before = path.read_text(encoding='utf-8')
        planned[name] = (before, transform(before))
    backups = HERE / 'backup'
    backups.mkdir(exist_ok=True)
    for name,(before, after) in planned.items():
        if before == after:
            continue
        backup = backups / name
        if not backup.exists():
            backup.write_text(before, encoding='utf-8')
        (ROOT / name).write_text(after, encoding='utf-8')
        print(f'R27-R35 installed: {name}')
    print('R27-R35 ready; targeted pytest follows; full pytest NOT run.')

if __name__ == '__main__':
    apply()
