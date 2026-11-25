"""Scoped reversible changes against reviewed repository blobs."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
RULE = 'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/rule.py'
PROVIDER = 'phase176_r3r44_public_subgroup_lift/provider.py'
SHARED = 'phase165_r52_r9_shared_math.py'
R48_APPLY = 'phase176_r3r48_cited_finite_delta_kernel/apply.py'
R44_TEST = 'phase176_r3r44_public_subgroup_lift/tests/test_public_subgroup_lift.py'
PINS = {
    RULE: 'adc68818539ddb5975d86b8ce4517107cfb9db78',
    PROVIDER: '551e9105cd35c8df9159cf8027839e7a890d0d81',
    SHARED: '937e8627f2d8d8a60ec7b36186fec5633b5604cd',
    R48_APPLY: '826e51b82f05d2e4d533e0107453ba90f2f8c40a',
    R44_TEST: 'b24b9f8512556178f725e1875fd652e66a6c9086',
}
OLD_HOOK = '''    public_subgroup_lift = build_public_subgroup_lift_provider(
        tuple(available), prior_conclusions,
    )'''
NEW_HOOK = '''    public_subgroup_lift = build_public_subgroup_lift_provider(
        tuple(available), prior_conclusions,
        bridge=bridge, proof_target=proof_target,
    )'''
REPLACEMENTS = {
    RULE: (
        ('from phase171_r2j_r2_cyclic_hopf_surjective.source import _coordinates\n',
         'from phase171_r2j_r2_cyclic_hopf_surjective.source import _coordinates\nfrom phase169_r10e4_ordered_db_prior.db_prior import verified_db_step\n'),
        ('    codomain: Relation, kernel: KernelMultipleStatement, image: Relation,\n) -> InferenceRule:',
         '    codomain: Relation, kernel: KernelMultipleStatement, image: Relation,\n    *, bridge=None, proof_target=None,\n) -> InferenceRule:'),
        ('                and all(step.rule is ProofRule.INFERENCE for step in premises)\n',
         '''                and all(premises[j].rule is ProofRule.INFERENCE for j in (0, 1, 3, 4))
                and (premises[2].rule is ProofRule.INFERENCE
                     or (bridge is not None and proof_target is not None
                         and verified_db_step(premises[2], proof_target=proof_target, bridge=bridge)))
'''),
        ('            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=type(item),\n                           statement_pattern=item)\n            for item in required',
         '''            PremisePattern(proof_rule=(None if j == 2 and bridge is not None
                                       and proof_target is not None else ProofRule.INFERENCE),
                           statement_type=type(item), statement_pattern=item)
            for j, item in enumerate(required)'''),
        ('    goal: object, exactness: object, codomain: object, kernel: object, image: object,\n) -> tuple[GoalExpansion, ...]:',
         '    goal: object, exactness: object, codomain: object, kernel: object, image: object,\n    *, bridge=None, proof_target=None,\n) -> tuple[GoalExpansion, ...]:'),
        ('        finite_cyclic_subgroup_lift_rule(goal, exactness, codomain, kernel, image),',
         '        finite_cyclic_subgroup_lift_rule(goal, exactness, codomain, kernel, image,\n                                         bridge=bridge, proof_target=proof_target),'),
    ),
    PROVIDER: (
        ('The rule still requires five independently inferred ProofSteps.',
         'The rule still requires five independent ProofSteps. Only the codomain\nmay be a revalidated DB prior under the active proof context.'),
        ('def build_public_subgroup_lift_provider(available: tuple, prior_conclusions: tuple = ()):',
         'def build_public_subgroup_lift_provider(available: tuple, prior_conclusions: tuple = (),\n                                        *, bridge=None, proof_target=None):'),
        ('            for option in expand_finite_cyclic_subgroup_lift(goal, exact, group, kernel, image):',
         '            for option in expand_finite_cyclic_subgroup_lift(\n                    goal, exact, group, kernel, image, bridge=bridge, proof_target=proof_target):'),
    ),
    SHARED: ((OLD_HOOK, NEW_HOOK),),
    R48_APPLY: ((
        '    text, eol = normalize(raw)\n    if path == SHARED:\n',
        '''    text, eol = normalize(raw)
    if path == SHARED:
        # R3R51 changes only the existing R44 factory call. Accept that exact
        # successor without removing it; unknown subsequent edits still fail.
        from phase176_r3r51_verified_db_subgroup_lift.apply import OLD_HOOK, NEW_HOOK, PINS as R51_PINS
        from phase176_r3r46r1_prior_group_availability.apply import pinned
        if text.count(NEW_HOOK) == 1 and pinned(text.replace(NEW_HOOK, OLD_HOOK, 1), R51_PINS[SHARED]):
            return raw
'''),),
    R44_TEST: ((
        "    source=TARGET.read_bytes().decode('utf-8')\n",
        '''    # Test the historical R44 installer on the reviewed pre-R51 shared blob.
    import subprocess
    source=subprocess.check_output(
        ['git', 'cat-file', 'blob', '937e8627f2d8d8a60ec7b36186fec5633b5604cd'],
        cwd=TARGET.parent,
    ).decode('utf-8').replace('\\r\\n', '\\n')
'''),),
}


def updated_source(path, raw):
    text, eol = normalize(raw)
    edits = REPLACEMENTS[path]
    # Check exact reviewed base or the exact complete successor, never a partial patch.
    if pinned(text, PINS[path]):
        base = text
    else:
        base = text
        for old, new in reversed(edits):
            if base.count(new) != 1:
                raise ValueError('UNREVIEWED_OR_PARTIAL_PATCH:' + path)
            base = base.replace(new, old, 1)
        if not pinned(base, PINS[path]):
            raise ValueError('UNREVIEWED_BASELINE:' + path)
    changed = base
    for old, new in edits:
        if changed.count(old) != 1:
            raise ValueError('ANCHOR_NOT_UNIQUE:' + path)
        changed = changed.replace(old, new, 1)
    if text not in (base, changed):
        raise ValueError('PARTIAL_PATCH:' + path)
    ast.parse(changed, filename=path)
    return changed.replace('\n', eol).encode('utf-8')


def planned_changes():
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    result = {}
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        result[path] = raw, updated_source(path, raw)
    if any(old == new for old, new in result.values()) and any(old != new for old, new in result.values()):
        raise RuntimeError('PARTIALLY_APPLIED_R3R51')
    return result


def write_full_functions(planned):
    names = {RULE: ('finite_cyclic_subgroup_lift_rule', 'expand_finite_cyclic_subgroup_lift'),
             PROVIDER: ('build_public_subgroup_lift_provider',),
             SHARED: ('shared_expansion_provider',),
             R48_APPLY: ('updated_source',), R44_TEST: ('test_patch_minimal_and_idempotent',)}
    sections = ['# 変更後の import・関数全文\n']
    for path, (_, raw) in planned.items():
        source, _ = normalize(raw)
        tree = ast.parse(source)
        imports = [ast.get_source_segment(source, node) for node in tree.body
                   if isinstance(node, (ast.Import, ast.ImportFrom))]
        sections.append('## `' + path + '`\n\n```python\n' + '\n'.join(imports) + '\n```\n')
        for name in names[path]:
            node, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
            sections.append('### `' + name + '`\n\n```python\n' + ast.get_source_segment(source, node) + '\n```\n')
    (PACKAGE / 'CHANGED_FUNCTIONS_FULL_JA.md').write_text('\n'.join(sections), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    planned = planned_changes()
    if not args.dry_run:
        written = []
        try:
            for path, (old, new) in planned.items():
                if old != new:
                    written.append(path)
                    (ROOT / path).write_bytes(new)
            write_full_functions(planned)
        except BaseException:
            for path in written:
                (ROOT / path).write_bytes(planned[path][0])
            raise
    print('PHASE176_R3R51_HEAD=' + subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())
    print('PHASE176_R3R51_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
