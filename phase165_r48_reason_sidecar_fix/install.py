from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
REASONS = ROOT / 'toda_group_proof_narrative_reasons.py'
GENERIC = ROOT / 'toda_group_proof_generic_narrative_renderer.py'


def transform(source: str) -> str:
    module = ast.parse(source)
    nodes = [node for node in module.body if isinstance(node, ast.FunctionDef)
             and node.name == '_exactness_to_map_property_reason']
    if len(nodes) != 1:
        raise RuntimeError('Cannot locate one exactness reason classifier')
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    body = ''.join(lines[node.lineno - 1:node.end_lineno])
    old = '''  if isinstance(
    conclusion,
    injective_types,
  ):
    conclusion_kind = "injective"
  elif isinstance(
    conclusion,
    surjective_types,
  ):
    conclusion_kind = "surjective"
  else:
    return None
'''
    new = '''  # Phase 165 R48: the generic statement variants share the same
  # map and exactness prerequisites as the established Toda variants.
  if (
    isinstance(conclusion, injective_types)
    or type(conclusion).__name__ == "MapInjective"
  ):
    conclusion_kind = "injective"
  elif (
    isinstance(conclusion, surjective_types)
    or type(conclusion).__name__ == "MapSurjective"
  ):
    conclusion_kind = "surjective"
  else:
    return None
'''
    if new in body:
        return source
    if body.count(old) != 1:
        raise RuntimeError('Unexpected exactness classifier source; no changes made')
    result = ''.join(lines[:node.lineno - 1]) + body.replace(old, new, 1) + ''.join(lines[node.end_lineno:])
    ast.parse(result)
    return result


def main() -> None:
    before = REASONS.read_text(encoding='utf-8')
    after = transform(before)
    if before != after:
        backup = REASONS.with_name('toda_group_proof_narrative_reasons.phase165_r48_backup.py')
        if not backup.exists():
            shutil.copy2(REASONS, backup)
        REASONS.write_text(after, encoding='utf-8')
        print('Updated existing ReasonSidecar classification; backup:', backup.name)
    else:
        print('ReasonSidecar classification already updated')
    text = GENERIC.read_text(encoding='utf-8')
    extra = '''    # phase165_r48_unified_exactness: derive the lead from proof premises.
    exactness_premise = any(
      isinstance(premise, ProofStep)
      and isinstance(premise.conclusion, TodaProp42ExactnessStatement)
      for premise in proof_step.premises
    )
    if proof_step.inference_rule is not None and exactness_premise:
      lines.append("完全性より,")
      lines.append("")

'''
    if extra in text:
        backup = GENERIC.with_name('toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py')
        if not backup.exists():
            shutil.copy2(GENERIC, backup)
        updated = text.replace(extra, '', 1)
        ast.parse(updated)
        GENERIC.write_text(updated, encoding='utf-8')
        print('Removed unused R48 generic proof-block insertion')
    print('Existing contribution/ReasonSidecar path retained. No full pytest.')


if __name__ == '__main__':
    main()
