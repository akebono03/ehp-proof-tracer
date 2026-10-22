"""Fail-closed AST-anchored source patch. Run from repository root."""
from __future__ import annotations
import ast
import datetime
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
GATE = ROOT / 'phase165_r52_r16_web_citation_gate.py'
TRANSPORT = ROOT / 'phase168_r2_toda52_transport.py'


def function_source(text: str, name: str) -> str:
    tree = ast.parse(text)
    found = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == name]
    if len(found) != 1:
        raise RuntimeError(f'Expected exactly one function {name}')
    fn = found[0]
    return ''.join(text.splitlines(keepends=True)[fn.lineno - 1: fn.end_lineno])


def prepared_changes():
    text = GATE.read_text(encoding='utf-8')
    if 'from proof import ProofRule\n' not in text:
        raise RuntimeError('Unknown citation gate import')
    before = function_source(text, 'screen_shared_proof_context')
    if 'def registered_reference_step(' in before:
        raise RuntimeError('Already patched')
    marker = '        for assertion in bridge.registry._assertions.values():\n'
    if before.count(marker) != 1:
        raise RuntimeError('Unexpected citation screening shape')
    helper = '''        def registered_reference_step(assertion, step):
            """Retain provenance of an already screened fixed assertion only."""
            reference = bridge.registry.reference(assertion.reference_id)
            locator = reference.locator
            if not isinstance(locator, str) or not locator:
                return step
            if step.inference_rule is not None and step.inference_rule.literature_reference is not None:
                return step
            return replace(
                step,
                inference_rule=InferenceRule(
                    name="Registered fixed statement: " + locator,
                    literature_reference=LiteratureReference(
                        label="Toda " + locator,
                        locator=locator,
                    ),
                ),
            )

'''
    before2 = before.replace('        from dataclasses import is_dataclass\n', '        from dataclasses import is_dataclass, replace\n')
    before2 = before2.replace('        from proof import ProofStep\n', '        from proof import ProofStep, InferenceRule, LiteratureReference\n')
    before2 = before2.replace(marker, helper + marker, 1)
    old = '''                step=ProofStep(
                    conclusion=assertion.content,
                    premises=(),
                    rule=ProofRule.GIVEN,
                ),'''
    new = '''                step=registered_reference_step(assertion, ProofStep(
                    conclusion=assertion.content,
                    premises=(),
                    rule=ProofRule.GIVEN,
                )),'''
    if before2.count(old) != 1:
        raise RuntimeError('Expected single generated GIVEN site')
    before2 = before2.replace(old, new, 1)
    old = '                candidate = original_links[0]\n'
    new = '                candidate = ProofStepLink(\n                    assertion_id=candidate.assertion_id,\n                    step=registered_reference_step(assertion, original_links[0].step),\n                )\n'
    if before2.count(old) != 1:
        raise RuntimeError('Expected single original link choice')
    before2 = before2.replace(old, new, 1)
    updated_gate = text.replace(before, before2, 1)

    text2 = TRANSPORT.read_text(encoding='utf-8')
    before_rule = function_source(text2, '_toda52_rule')
    # Bound to the specific, source-verified typed Toda52UniversalStatement guarded in this rule.
    old = '        match_guard=guard,\n'
    new = '''        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda (5.2)", locator="(5.2)",
        ),
'''
    if before_rule.count(old) != 1:
        raise RuntimeError('Unexpected transport inference constructor')
    rule_new = before_rule.replace(old, new, 1)
    old_import = 'from proof import InferenceRule, PremisePattern, Relation, RelationType\n'
    new_import = 'from proof import InferenceRule, LiteratureReference, PremisePattern, Relation, RelationType\n'
    if text2.count(old_import) != 1:
        raise RuntimeError('Unexpected transport import')
    updated_transport = text2.replace(old_import, new_import, 1).replace(before_rule, rule_new, 1)
    ast.parse(updated_gate)
    ast.parse(updated_transport)
    return ((GATE, text, updated_gate), (TRANSPORT, text2, updated_transport))


def apply():
    changes = prepared_changes()
    backup = ROOT / 'phase168_r2_8_7_backups' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup.mkdir(parents=True, exist_ok=False)
    for path, old, updated in changes:
        (backup / path.name).write_text(old, encoding='utf-8')
        path.write_text(updated, encoding='utf-8')
        print('PATCHED:', path)
    print('BACKUP:', backup)
    for path, old, updated in changes:
        names = ('screen_shared_proof_context',) if path == GATE else ('_toda52_rule',)
        for name in names:
            out = OUT / (path.stem + '_' + name + '_full.py.txt')
            out.write_text(function_source(updated, name), encoding='utf-8')
            print('FULL_FUNCTION:', out)
    (OUT / 'transport_import_full.py.txt').write_text(
        '\n'.join(line for line in changes[1][2].splitlines() if line.startswith('from ') or line.startswith('import ')) + '\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    apply()
