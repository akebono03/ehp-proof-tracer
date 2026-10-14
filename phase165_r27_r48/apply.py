from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

PHASE = '165 R27-R48'
START = '# Phase 165 R27-R48 typed rule catalog'


def _span(source: str, node: ast.AST) -> tuple[int, int]:
    lines = source.splitlines(keepends=True)
    return sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno]))


def transform(source: str) -> str:
    tree = ast.parse(source)
    base = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build_standard_production_applicability_catalog'), None)
    if base is None:
        raise RuntimeError('base applicability catalog builder not found')
    if START in source:
        return source
    old = ast.get_source_segment(source, base)
    if 'build_repository_proof_scope' not in old or 'build_standard_production_proof_repository' not in old:
        raise RuntimeError('base builder differs from inspected GitHub source; refusing change')
    new = '''def build_standard_production_applicability_catalog() -> InferenceRuleCatalog:
  """Enumerate typed rules, not legacy repository proof-tree nodes.

  This catalog is for metadata. A rule here is NOT a proved theorem or an
  executable match; those require checked premises via typed applicability.
  """
  from phase165_r8_rule_provider import discover_inference_rules

  rules, _report = discover_inference_rules()
  catalog = InferenceRuleCatalog()
  for index, rule in enumerate(rules):
    pattern = rule.conclusion_pattern
    if pattern is None:
      continue
    conclusion_type = pattern if isinstance(pattern, type) else type(pattern)
    catalog.register(InferenceRuleCatalogEntry(
      key=f"standard.production.applicability.{index:04d}",
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=False,
      relevance_category=_representative_relevance_category(rule, conclusion_type),
    ))
  return catalog
'''
    a, b = _span(source, base)
    source = source[:a] + new + source[b:]
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    removals = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module in {'repository_proof_scope', 'standard_production_repository'}:
            names = {n.name for n in node.names}
            if node.module == 'repository_proof_scope' and names != {'build_repository_proof_scope'}:
                raise RuntimeError('unknown scope imports')
            if node.module == 'standard_production_repository' and names != {'build_standard_production_proof_repository'}:
                raise RuntimeError('unknown repository imports')
            removals.append(_span(source, node))
    for a, b in reversed(removals):
        source = source[:a] + source[b:]
    source = START + '\n' + source
    ast.parse(source)
    if 'from repository_proof_scope import' in source or 'from standard_production_repository import' in source:
        raise RuntimeError('legacy import remains')
    return source


def apply(root: Path) -> dict:
    path = root / 'standard_production_applicability_catalog.py'
    if not path.is_file() or not (root / 'phase165_r8_rule_provider.py').is_file():
        raise RuntimeError('required production files not found')
    original = path.read_text(encoding='utf-8')
    updated = transform(original)
    changed = updated != original
    if changed:
        backup = root / 'phase165_r27_r48_backup' / path.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(updated, encoding='utf-8')
    leftover = [p.stem for p in root.glob('repository_*.py')]
    audit = {'phase': PHASE, 'status': 'CHANGED' if changed else 'ALREADY_INSTALLED', 'modified_files': [path.name] if changed else [], 'base_catalog_source': 'typed_inference_rule_provider', 'classification_wrappers_preserved': True, 'group_calculation_unchanged': True, 'remaining_legacy_modules': sorted(leftover), 'full_pytest_run': False}
    (root / 'phase165_r27_r48_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    return audit


if __name__ == '__main__':
    print(json.dumps(apply(Path(__file__).resolve().parent.parent), ensure_ascii=False, indent=2))
