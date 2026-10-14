"""R27-R45: install shared typed execution and its Web entry."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NEW_MODULE = 'toda_typed_execution.py'
WEB_FILE = 'web_generator_execution.py'
WEB_FUNCTION = '''def build_standard_web_generator_execution_view(generator_input: str, candidate_number: int | None = None) -> WebGeneratorExecutionView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  if candidate_number is not None and (isinstance(candidate_number, bool) or not isinstance(candidate_number, int) or candidate_number < 1):
    raise ValueError("candidate_number must be a positive integer")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_typed_execution import execute_typed_applicable_rules, TypedExecutionOutcome
  from toda_typed_execution_status import TypedGeneratorExecutionStatus
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  symbol = resolve_generator_input(generator_input)
  search = search_typed_generator_statements(generator_input)
  execution = execute_typed_applicable_rules(search.proven_steps, candidate_number=candidate_number)
  base = dict(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    diagnostics=search.diagnostics,
    open_goal_count=len(search.open_goals),
  )
  if execution.status is TypedExecutionOutcome.NONE:
    return WebGeneratorExecutionView(
      **base, status=TypedGeneratorExecutionStatus.NONE,
      candidates=(), selected_candidate_number=None,
      conclusion_latex=None, premises=(), rule_name=None, provenance=None,
      search_status="not_executed",
    )
  if execution.status is TypedExecutionOutcome.AMBIGUOUS:
    candidates = []
    for index, match in enumerate(execution.matches, start=1):
      try:
        statement = render_toda_proof_statement_latex(match.inference_rule.conclusion_pattern)
      except (TypeError, ValueError, AttributeError):
        statement = None
      candidates.append(WebGeneratorExecutionCandidateView(
        candidate_number=index,
        statement_latex=statement,
        fallback_type_name=None if statement else type(match.inference_rule.conclusion_pattern).__name__,
      ))
    return WebGeneratorExecutionView(
      **base, status=TypedGeneratorExecutionStatus.AMBIGUOUS,
      candidates=tuple(candidates), selected_candidate_number=None,
      conclusion_latex=None, premises=(), rule_name=None, provenance=None,
      search_status="ambiguous",
    )
  step = execution.proof_step
  assert step is not None
  try:
    conclusion_latex = render_toda_proof_statement_latex(step.conclusion)
  except (TypeError, ValueError, AttributeError):
    conclusion_latex = r"\\text{導出された命題（表示未対応）}"
  premises = []
  for index, premise in enumerate(step.premises, start=1):
    try:
      statement_latex = render_toda_proof_statement_latex(premise.conclusion)
    except (TypeError, ValueError, AttributeError):
      statement_latex = None
    premises.append(WebGeneratorExecutionPremiseView(
      premise_number=index,
      statement_latex=statement_latex,
      fallback_type_name=None if statement_latex else type(premise.conclusion).__name__,
    ))
  return WebGeneratorExecutionView(
    **base, status=TypedGeneratorExecutionStatus.EXECUTED,
    candidates=(), selected_candidate_number=execution.selected_candidate_number,
    conclusion_latex=conclusion_latex, premises=tuple(premises),
    rule_name=step.inference_rule.name,
    provenance=WebGeneratorExecutionProvenanceView(
      key="typed-inference:" + step.inference_rule.name, theorem=None, phase=None,
    ),
    search_status="executed",
  )
'''


def replace_function(source: str, name: str, body: str) -> str:
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f'exactly one {name} required')
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    changed = ''.join(lines[:node.lineno - 1]) + body.rstrip() + '\n' + ''.join(lines[node.end_lineno:])
    ast.parse(changed)
    return changed


def apply(root: Path = ROOT) -> dict:
    web = root / WEB_FILE
    applicability = root / 'toda_typed_applicability.py'
    if not web.is_file() or not applicability.is_file():
        raise RuntimeError('R44 Web Execution or R43 applicability is missing')
    new_text = (HERE / NEW_MODULE).read_text(encoding='utf-8')
    dest = root / NEW_MODULE
    if dest.exists() and dest.read_text(encoding='utf-8-sig') != new_text:
        raise RuntimeError('typed execution module conflict')
    old = web.read_text(encoding='utf-8-sig')
    node = next((n for n in ast.parse(old).body if isinstance(n, ast.FunctionDef) and n.name == 'build_standard_web_generator_execution_view'), None)
    if node is None:
        raise RuntimeError('Web Execution function missing')
    original_function = ast.get_source_segment(old, node)
    if 'execute_typed_applicable_rules' in original_function:
        modified = old
    else:
        if 'search_typed_generator_statements' not in original_function:
            raise RuntimeError('R36 typed search Web entry not installed')
        modified = replace_function(old, 'build_standard_web_generator_execution_view', WEB_FUNCTION)
    changes = {}
    if modified != old:
        changes[web] = modified
    if not dest.exists():
        changes[dest] = new_text
    backup = root / 'phase165_r27_r45_backup'
    for path in changes:
        if path.exists() and (backup / path.name).exists() and (backup / path.name).read_bytes() != path.read_bytes():
            raise RuntimeError(f'backup conflict: {path.name}')
    backup.mkdir(exist_ok=True)
    for path, value in changes.items():
        if path.exists() and not (backup / path.name).exists():
            shutil.copy2(path, backup / path.name)
        path.write_text(value, encoding='utf-8')
    report = {'phase':'165 R27-R45','status':'CHANGED' if changes else 'ALREADY_INSTALLED','modified_files':[p.name for p in changes], 'typed_execution_enabled':True,'full_pytest_run':False}
    (root / 'phase165_r27_r45_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report


if __name__ == '__main__':
    apply()
