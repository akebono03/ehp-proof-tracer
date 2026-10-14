"""Phase 165 R27-R46: switch CLI execute to shared typed inference."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FUNCTION = '''def _run_execute_command(
  generator_input: str,
  candidate_number: int | None = None,
) -> int:
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_typed_execution import TypedExecutionOutcome, execute_typed_applicable_rules
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex

  try:
    if not isinstance(generator_input, str) or not generator_input.strip():
      raise ValueError("generator is required")
    search = search_typed_generator_statements(generator_input.strip())
    result = execute_typed_applicable_rules(
      search.proven_steps, candidate_number=candidate_number,
    )
  except (TypeError, ValueError) as error:
    parser = build_execute_argument_parser()
    parser.error(str(error))

  if result.status is TypedExecutionOutcome.NONE:
    print(f"No typed inference candidate found for {generator_input}.")
    for diagnostic in search.diagnostics:
      print(diagnostic)
    return 1

  if result.status is TypedExecutionOutcome.AMBIGUOUS:
    print(f"Multiple typed inference candidates for {generator_input}:")
    for index, match in enumerate(result.matches, start=1):
      print(f"  {index}. {match.inference_rule.name}")
    print("Specify --candidate N to execute one candidate.")
    return 0

  if result.status is not TypedExecutionOutcome.EXECUTED:
    raise RuntimeError("unsupported typed execution status")
  step = result.proof_step
  if step is None or step.inference_rule is None:
    raise RuntimeError("executed inference must supply a proof step")
  print(f"Inference rule: {step.inference_rule.name}")
  for index, premise in enumerate(step.premises, start=1):
    rendered = render_toda_proof_statement_latex(premise.conclusion)
    print(f"Premise {index}: {rendered if rendered is not None else repr(premise.conclusion)}")
  conclusion = render_toda_proof_statement_latex(step.conclusion)
  print(f"Conclusion: {conclusion if conclusion is not None else repr(step.conclusion)}")
  return 0
'''


def replace_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f'exactly one {name} required')
    n = nodes[0]
    lines = source.splitlines(keepends=True)
    new = ''.join(lines[:n.lineno - 1]) + replacement.rstrip() + '\n' + ''.join(lines[n.end_lineno:])
    ast.parse(new)
    return new


def apply(root: Path = ROOT) -> dict:
    path = root / 'main.py'
    required = ['toda_typed_execution.py', 'toda_typed_applicability.py', 'phase165_r27_r34_typed_lookup.py']
    if not path.is_file() or any(not (root / p).is_file() for p in required):
        raise RuntimeError('R45 typed execution or CLI main.py not installed')
    old = path.read_text(encoding='utf-8-sig')
    node = next((n for n in ast.parse(old).body if isinstance(n, ast.FunctionDef) and n.name == '_run_execute_command'), None)
    if node is None:
        raise RuntimeError('CLI execute command not found')
    existing = ast.get_source_segment(old, node)
    if 'execute_typed_applicable_rules' in existing:
        new = old
    elif 'run_standard_repository_generator_user_execution_workflow' in existing:
        new = replace_function(old, '_run_execute_command', FUNCTION)
    else:
        raise RuntimeError('unrecognized CLI execute command; refusing to overwrite')
    changed = old != new
    backup = root / 'phase165_r27_r46_backup'
    if changed:
        original = backup / path.name
        if original.exists() and original.read_bytes() != path.read_bytes():
            raise RuntimeError('backup conflict')
        backup.mkdir(exist_ok=True)
        if not original.exists():
            shutil.copy2(path, original)
        path.write_text(new, encoding='utf-8')
    result = {
        'phase': '165 R27-R46',
        'status': 'CHANGED' if changed else 'ALREADY_INSTALLED',
        'modified_files': ['main.py'] if changed else [],
        'cli_typed_execution_enabled': True,
        'full_pytest_run': False,
    }
    (root / 'phase165_r27_r46_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    apply()
