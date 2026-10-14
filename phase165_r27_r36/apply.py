"""R27-R36: typed Generator Web entry migration; all edits staged before writing."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

REPLACEMENTS = {
'web_generator_proof.py': ("build_standard_web_generator_proof_view", '''def build_standard_web_generator_proof_view(generator_input: str, max_depth: int = 1) -> WebGeneratorProofView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  symbol = resolve_generator_input(generator_input)
  result = search_typed_generator_statements(generator_input)
  steps = tuple(WebGeneratorProofStepView(
    depth=0,
    statement_latex=render_toda_proof_statement_latex(step.conclusion),
    fallback_type_name=None,
    rule_name=_generator_proof_rule_name(step),
  ) for step in result.proven_steps)
  return WebGeneratorProofView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    conclusion_latex=(steps[-1].statement_latex if steps else "\\\\text{未証明}"),
    steps=steps,
    max_depth=max_depth,
    search_status=result.status.value,
    diagnostics=result.diagnostics,
    open_goal_count=len(result.open_goals),
  )
'''),
'web_generator_proof_scope.py': ("build_standard_web_generator_proof_scope_view", '''def build_standard_web_generator_proof_scope_view(generator_input: str) -> WebGeneratorProofScopeView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  symbol = resolve_generator_input(generator_input)
  result = search_typed_generator_statements(generator_input)
  return WebGeneratorProofScopeView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    occurrence_count=len(result.proven_steps),
    toda_membership_count=0,
    map_relation_count=0,
    toda_memberships=(),
    map_relations=(),
    search_status=result.status.value,
    diagnostics=result.diagnostics,
    open_goal_count=len(result.open_goals),
  )
'''),
'web_generator_applicability.py': ("build_standard_web_generator_applicability_view", '''def build_standard_web_generator_applicability_view(generator_input: str) -> WebGeneratorApplicabilityView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  symbol = resolve_generator_input(generator_input)
  result = search_typed_generator_statements(generator_input)
  return WebGeneratorApplicabilityView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    occurrence_count=len(result.proven_steps),
    candidate_count=0,
    source_count=0,
    rule_group_count=0,
    rule_family_count=0,
    toda_memberships=(), map_relations=(), other_sources=(),
    search_status="not_evaluated",
    diagnostics=result.diagnostics + ("推論規則の適用可能性は未評価。型付き命題検索の成功だけでは適用可能とは判定しない",),
    open_goal_count=len(result.open_goals),
  )
'''),
'web_generator_execution.py': ("build_standard_web_generator_execution_view", '''def build_standard_web_generator_execution_view(generator_input: str, candidate_number: int | None = None) -> WebGeneratorExecutionView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  if candidate_number is not None and (isinstance(candidate_number, bool) or not isinstance(candidate_number, int) or candidate_number < 1):
    raise ValueError("candidate_number must be a positive integer")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  symbol = resolve_generator_input(generator_input)
  result = search_typed_generator_statements(generator_input)
  return WebGeneratorExecutionView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    status=RepositoryGeneratorUserExecutionWorkflowStatus.NONE,
    candidates=(), selected_candidate_number=None,
    conclusion_latex=None, premises=(), rule_name=None, provenance=None,
    search_status="not_executed",
    diagnostics=result.diagnostics + ("推論規則の選択と実行は未実施。検索結果を実行成功に昇格しない",),
    open_goal_count=len(result.open_goals),
  )
'''),
}

FIELDS = '  search_status: str = "not_searched"\n  diagnostics: tuple[str, ...] = ()\n  open_goal_count: int = 0\n'
CLASSES = {
  'web_generator_proof.py': 'WebGeneratorProofView',
  'web_generator_proof_scope.py': 'WebGeneratorProofScopeView',
  'web_generator_applicability.py': 'WebGeneratorApplicabilityView',
  'web_generator_execution.py': 'WebGeneratorExecutionView',
}

def replace_function(source: str, name: str, body: str) -> str:
  nodes = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == name]
  if len(nodes) != 1:
    raise RuntimeError(f"Expected unique function {name}: {len(nodes)}")
  n = nodes[0]
  lines = source.splitlines(keepends=True)
  tail = ''.join(lines[n.end_lineno:])
  return ''.join(lines[:n.lineno-1]) + body.rstrip('\n') + '\n' + tail

def fields_if_needed(source: str, cls: str) -> str:
  cs = [x for x in ast.parse(source).body if isinstance(x, ast.ClassDef) and x.name == cls]
  if len(cs) != 1:
    raise RuntimeError(f"Missing class: {cls}")
  node = cs[0]
  existing = {x.target.id for x in node.body if isinstance(x, ast.AnnAssign) and isinstance(x.target, ast.Name)}
  field_names = {'search_status','diagnostics','open_goal_count'}
  if existing >= field_names:
    return source
  if existing & field_names:
    raise RuntimeError('Incomplete status field installation')
  methods = [x for x in node.body if isinstance(x, ast.FunctionDef)]
  if not methods:
    raise RuntimeError('Class method insertion location missing')
  lines = source.splitlines(keepends=True)
  pos = methods[0].lineno - 1
  return ''.join(lines[:pos]) + FIELDS + '\n' + ''.join(lines[pos:])

def transform(name: str, source: str) -> str:
  func, body = REPLACEMENTS[name]
  source = fields_if_needed(source, CLASSES[name])
  source = replace_function(source, func, body)
  if name == 'web_generator_proof.py':
    source = source.replace('    if not self.steps:\n      raise ValueError(\n        "steps must not be empty"\n      )\n', '    if not self.steps and self.search_status == "complete":\n      raise ValueError("complete proof must contain steps")\n')
  ast.parse(source)
  return source

def apply() -> None:
  plan = {}
  for name in REPLACEMENTS:
    path = ROOT / name
    before = path.read_text(encoding='utf-8')
    plan[name] = (before, transform(name, before))
  backup_root = HERE / 'backup'
  backup_root.mkdir(exist_ok=True)
  for name, (before, after) in plan.items():
    if before == after:
      print(f'R27-R36 already installed: {name}')
      continue
    target_backup = backup_root / name
    if not target_backup.exists():
      target_backup.write_text(before, encoding='utf-8')
    (ROOT / name).write_text(after, encoding='utf-8')
    print(f'R27-R36 installed: {name}')

CLI_FUNCTIONS = {
'_run_show_proof_command': '''def _run_show_proof_command(generator_input: str, max_depth: int | None = None) -> int:
  from phase165_r27_r34_typed_lookup import TypedLookupStatus, search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  if max_depth is not None and (isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0):
    raise ValueError("max_depth must be nonnegative")
  try:
    result = search_typed_generator_statements(generator_input)
  except (TypeError, ValueError) as error:
    build_show_proof_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  for step in result.proven_steps:
    print(f"- ${render_toda_proof_statement_latex(step.conclusion)}$")
  for diagnostic in result.diagnostics:
    print(diagnostic)
  if result.open_goals:
    print(f"Open goals: {len(result.open_goals)}")
  return 0 if result.status is TypedLookupStatus.COMPLETE else 1
''',
'_run_explore_proof_command': '''def _run_explore_proof_command(generator_input: str) -> int:
  from phase165_r27_r34_typed_lookup import TypedLookupStatus, search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  try:
    result = search_typed_generator_statements(generator_input)
  except (TypeError, ValueError) as error:
    build_explore_proof_argument_parser().error(str(error))
  print(f"Search status: {result.status.value}")
  for step in result.proven_steps:
    print(f"- ${render_toda_proof_statement_latex(step.conclusion)}$")
  for diagnostic in result.diagnostics:
    print(diagnostic)
  if result.open_goals:
    print(f"Open goals: {len(result.open_goals)}")
  return 0 if result.status is TypedLookupStatus.COMPLETE else 1
''',
}

_previous_apply = apply

def apply() -> None:
  cli_path = ROOT / 'main.py'
  original = cli_path.read_text(encoding='utf-8')
  planned = original
  for name, code in CLI_FUNCTIONS.items():
    planned = replace_function(planned, name, code)
  ast.parse(planned)
  # Plan and validate every Web change before writing any file.
  web_plan = {}
  for name in REPLACEMENTS:
    before = (ROOT / name).read_text(encoding='utf-8')
    web_plan[name] = (before, transform(name, before))
  backup_root = HERE / 'backup'
  backup_root.mkdir(exist_ok=True)
  for name, (before, after) in [*web_plan.items(), ('main.py', (original, planned))]:
    if before == after:
      print(f'R27-R36 already installed: {name}')
      continue
    backup = backup_root / name
    if not backup.exists():
      backup.write_text(before, encoding='utf-8')
    (ROOT / name).write_text(after, encoding='utf-8')
    print(f'R27-R36 installed: {name}')

if __name__ == '__main__':
  apply()
