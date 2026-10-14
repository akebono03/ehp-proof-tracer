from pathlib import Path
import ast
import shutil

root = Path.cwd()
target = root / 'web_group_query.py'
source = target.read_text(encoding='utf-8')
old_import = '''from toda_calculation_facade import (
  build_standard_toda_report,
)
'''
new_import = '''from phase165_r52_partial_proof import (
  GroupStructureStatus,
  ProofSearchStatus,
)
from phase165_r52_r5_auto_search import (
  search_group_structure_automatically,
)
from proof import Relation, RelationType
from toda_presentation import (
  build_toda_group_structure_presentation,
)
'''
old_renderer = '''from toda_human_readable_renderer import (
  render_toda_group_result_latex,
)
'''
new_renderer = '''from toda_human_readable_renderer import (
  render_toda_group_structure_latex,
)
'''
new_function = '''def build_standard_web_group_query_view(
  n: int,
  k: int,
) -> WebGroupQueryView:
  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  domain = classify_toda_group_query_domain(
    query
  )

  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    return WebGroupQueryView(
      n=n,
      k=k,
      status=TodaCalculationStatus.FOUND,
      result_latex=render_toda_group_query_domain_latex(domain),
      proof_available=False,
    )

  result = search_group_structure_automatically(n=n, k=k)
  conclusion = result.conclusion
  if (
    result.status is ProofSearchStatus.COMPLETE
    and result.structure_status is GroupStructureStatus.KNOWN
    and isinstance(conclusion, Relation)
    and conclusion.relation_type is RelationType.EQUALITY
    and conclusion.lhs == query.target
  ):
    structure_latex = render_toda_group_structure_latex(
      build_toda_group_structure_presentation(conclusion.rhs)
    )
    return WebGroupQueryView(
      n=n,
      k=k,
      status=TodaCalculationStatus.FOUND,
      result_latex=structure_latex,
      proof_available=True,
    )

  return WebGroupQueryView(
    n=n,
    k=k,
    status=TodaCalculationStatus.NOT_FOUND,
    result_latex=None,
    proof_available=False,
  )
'''
if old_import not in source and new_import in source:
    print('R27-R22 already installed')
    raise SystemExit(0)
if source.count(old_import) != 1 or source.count(old_renderer) != 1:
    raise SystemExit('Unexpected import layout; no changes made')
module=ast.parse(source)
functions=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='build_standard_web_group_query_view']
if len(functions)!=1:
    raise SystemExit('Unexpected function layout')
node=functions[0]
lines=source.splitlines(keepends=True)
start=sum(len(line) for line in lines[:node.lineno-1])
end=sum(len(line) for line in lines[:node.end_lineno])
if 'build_standard_toda_report(' not in source[start:end]:
    raise SystemExit('Expected old calculation call missing')
patched=source[:start]+new_function+source[end:]
patched=patched.replace(old_import,new_import,1).replace(old_renderer,new_renderer,1)
ast.parse(patched)
backup = root / 'phase165_r27_r22' / 'web_group_query.before_r22.py'
backup.parent.mkdir(exist_ok=True)
shutil.copy2(target,backup)
target.write_text(patched,encoding='utf-8')
print('R27-R22 installed: Group Query uses common typed Backward Search')
