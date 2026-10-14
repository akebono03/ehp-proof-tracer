"""R27-R1: link pre-existing eta2 definition source into Toda (5.2) legacy consumer.

This does not create a GIVEN, change generic search, or restore a specialized rule.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

TARGET = 'toda_upstream_bootstrap.py'
FN = 'build_toda_52_composition_isomorphism_step'
MARKER = '''  premise_steps = (\n    phase49[\n      "premise_steps"\n    ]\n    + (\n'''
REPLACEMENT = '''  phase50 = _build_phase50_result()\n  eta2_definition_steps = tuple(\n    step\n    for step in phase50["premise_steps"]\n    if isinstance(step.conclusion, TodaPi32Eta2DefinitionStatement)\n  )\n  if len(eta2_definition_steps) != 1:\n    raise ValueError(\n      "expected exactly one existing eta2 definition source step"\n    )\n\n  premise_steps = (\n    phase49[\n      "premise_steps"\n    ]\n    + eta2_definition_steps\n    + (\n'''

def _function(source: str):
    t = ast.parse(source)
    matches = [n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == FN]
    if len(matches) != 1:
        raise RuntimeError('Expected one Toda (5.2) function')
    return matches[0]


def install(root: Path):
    root = root.resolve()
    target = root / TARGET
    source = target.read_text(encoding='utf-8')
    node = _function(source)
    lines = source.splitlines(keepends=True)
    old = ''.join(lines[node.lineno-1:node.end_lineno])
    if 'eta2_definition_steps = tuple(' in old:
        status = 'ALREADY_INSTALLED'
        newsource = source
    else:
        if old.count(MARKER) != 1:
            raise RuntimeError('Unexpected Toda (5.2) premise block; no files changed')
        if 'phase50 = _build_phase50_result()' in old:
            raise RuntimeError('Unexpected existing Phase 50 binding; no files changed')
        updated = old.replace(MARKER, REPLACEMENT, 1)
        newsource = ''.join(lines[:node.lineno-1]) + updated + ''.join(lines[node.end_lineno:])
        ast.parse(newsource)
        if 'toda_pi3_2_define_eta2_inference_rule' in newsource or 'toda_pi3_2_eta2_hopf_relation_inference_rule' in newsource:
            raise RuntimeError('Old pi32 dedicated factories still referenced; no files changed')
        backup = target.with_name(target.name + '.phase165_r52_r27_r1_backup')
        if backup.exists():
            raise RuntimeError('Backup already exists; no files changed: ' + str(backup))
        shutil.copy2(target, backup)
        target.write_text(newsource, encoding='utf-8', newline='')
        status = 'INSTALLED'
    n = _function(newsource)
    all_lines = newsource.splitlines(keepends=True)
    rendered = ''.join(all_lines[n.lineno-1:n.end_lineno])
    reportdir = Path(__file__).resolve().parent / 'audit_output'
    reportdir.mkdir(exist_ok=True)
    (reportdir / 'MODIFIED_FUNCTION.md').write_text('# Complete changed function\n\n```python\n' + rendered + '\n```\n', encoding='utf-8')
    result = {'phase':'165 R52-R27-R1','status':status,'changed_file':TARGET,'changed_function':FN,'specialized_rule_restored':False,'new_given_created':False,'full_pytest_run':False}
    (reportdir/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(install(Path(__file__).resolve().parent.parent),ensure_ascii=False,indent=2))
