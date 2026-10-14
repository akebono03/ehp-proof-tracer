"""Phase 165 R27-R44: connect existing typed applicability matcher to Web/CLI."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WEB_FUNCTION = '''def build_standard_web_generator_applicability_view(generator_input: str) -> WebGeneratorApplicabilityView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_typed_applicability import find_typed_applicable_rules
  symbol = resolve_generator_input(generator_input)
  search = search_typed_generator_statements(generator_input)
  applicable = find_typed_applicable_rules(search.proven_steps)
  return WebGeneratorApplicabilityView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    occurrence_count=len(search.proven_steps),
    candidate_count=sum(len(item.matches) for item in applicable),
    source_count=0,
    rule_group_count=0,
    rule_family_count=len(applicable),
    toda_memberships=(),
    map_relations=(),
    other_sources=(),
    search_status=(search.status.value if not search.open_goals else "partial"),
    diagnostics=search.diagnostics + (
      "適用候補は証明済みの前提に対する規則照合結果であり、結論は未実行",),
    open_goal_count=len(search.open_goals),
  )
'''
CLI_FUNCTION = '''def _run_explore_applicable_command(generator_input: str, detailed: bool = False) -> int:
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_typed_applicability import find_typed_applicable_rules
  try:
    search = search_typed_generator_statements(generator_input)
    applicable = find_typed_applicable_rules(search.proven_steps)
  except (TypeError, ValueError) as error:
    build_explore_applicable_argument_parser().error(str(error))
  print(f"Search status: {search.status.value}")
  print(f"Proven premises: {len(search.proven_steps)}")
  print(f"Applicable rule families: {len(applicable)}")
  print(f"Applicable matches: {sum(len(item.matches) for item in applicable)}")
  for item in applicable:
    print(f"- {item.rule.name}: {len(item.matches)} match(es)")
    if detailed:
      for match in item.matches:
        print(f"  Premises: {len(match.premises)}")
  for diagnostic in search.diagnostics:
    print(diagnostic)
  if search.open_goals:
    print(f"Open goals: {len(search.open_goals)}")
  print("Applicability only: no inference rule executed")
  return 0 if not search.open_goals else 1
'''
CHANGES = {'web_generator_applicability.py': ('build_standard_web_generator_applicability_view', WEB_FUNCTION), 'main.py': ('_run_explore_applicable_command', CLI_FUNCTION)}

def replace_function(source: str, name: str, new_body: str) -> str:
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f"Expected exactly one {name}; found {len(nodes)}")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    changed = ''.join(lines[:node.lineno - 1]) + new_body.rstrip() + '\n' + ''.join(lines[node.end_lineno:])
    ast.parse(changed)
    return changed

def apply(root: Path = ROOT) -> dict:
    if not (root / 'toda_typed_applicability.py').is_file():
        raise RuntimeError('R27-R43 typed applicability module is missing')
    staged = {}
    for filename, (name, body) in CHANGES.items():
        path = root / filename
        if not path.is_file():
            raise RuntimeError(f'Missing file: {filename}')
        old = path.read_text(encoding='utf-8-sig')
        if 'find_typed_applicable_rules' in ast.get_source_segment(old, next(n for n in ast.parse(old).body if isinstance(n, ast.FunctionDef) and n.name == name)):
            continue
        new = replace_function(old, name, body)
        staged[filename] = (old, new)
    backup = root / 'phase165_r27_r44_backup'
    for filename, (old, _) in staged.items():
        if (backup / filename).exists() and (backup / filename).read_text(encoding='utf-8') != old:
            raise RuntimeError(f'Backup mismatch: {filename}')
    backup.mkdir(exist_ok=True)
    for filename, (old, new) in staged.items():
        destination = backup / filename
        if not destination.exists():
            destination.write_text(old, encoding='utf-8')
        (root / filename).write_text(new, encoding='utf-8')
    report = {'phase':'165 R27-R44','status':'CHANGED' if staged else 'ALREADY_INSTALLED','modified_files':list(staged),'shared_typed_applicability':True,'old_catalog_unchanged':True,'inference_execution_performed':False,'full_pytest_run':False}
    (root / 'phase165_r27_r44_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return report

if __name__ == '__main__':
    print(json.dumps(apply(), ensure_ascii=False, indent=2))
