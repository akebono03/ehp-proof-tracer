"""Guarded insertions into the reviewed shared functions and historical test."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

from phase176_r3r46r1_prior_group_availability.apply import normalize, checked_insertions

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SHARED = 'phase165_r52_r9_shared_math.py'
HISTORICAL_TEST = 'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py'
PINS = {
    SHARED: '73e8a6b1d3127502a5459fc36cc439f00a745107',
    HISTORICAL_TEST: '4de6cc39adf53de802d69e67cc55da10faba93fe',
}
SOURCE_ANCHOR = '    registry = UnifiedStatementRegistry()\n'
SOURCE_SETUP = '''    # R3R48: append the independently cited signed Lemma 5.7 clause.
    if default_sources:
        from phase176_r3r48_cited_finite_delta_kernel.source import build_cited_lemma57_delta_source
        sources = sources + (build_cited_lemma57_delta_source(),)
'''
PROVIDER_ANCHOR = '    shared_provider_registry = build_shared_expansion_provider_registry(\n'
PROVIDER_SETUP = '''    # R3R48: finite cyclic Delta kernel from three open proof obligations.
    from phase176_r3r48_cited_finite_delta_kernel.provider import build_finite_delta_kernel_provider
    extra_providers = tuple(extra_providers) + (
        build_finite_delta_kernel_provider(bridge=bridge, proof_target=proof_target),
    )

'''
TEST_ANCHOR = '        assert updated_source(path, raw) == raw\n'
TEST_SETUP = '''        # This is a historical R46 installer contract, not a pin on all future Phases.
        if path == 'phase165_r52_r9_shared_math.py':
            import subprocess
            raw = subprocess.check_output(
                ['git', 'cat-file', 'blob', '73e8a6b1d3127502a5459fc36cc439f00a745107'],
                cwd=ROOT,
            )
'''


def updated_source(path, raw):
    text, eol = normalize(raw)
    if path == SHARED:
        # R3R51 changes only the existing R44 factory call. Accept that exact
        # successor without removing it; unknown subsequent edits still fail.
        from phase176_r3r51_verified_db_subgroup_lift.apply import OLD_HOOK, NEW_HOOK, PINS as R51_PINS
        from phase176_r3r46r1_prior_group_availability.apply import pinned
        if text.count(NEW_HOOK) == 1 and pinned(text.replace(NEW_HOOK, OLD_HOOK, 1), R51_PINS[SHARED]):
            return raw
        # Scope the source anchor to build_shared_typed_bridge. Other functions
        # may also create registries; the combined anchor is unique.
        anchor = '        sources = sources + (build_cited_toda55_quadruple_source(),)\n' + SOURCE_ANCHOR
        # Use a guarded insertion after the first line of that combined anchor.
        from phase176_r3r46r1_prior_group_availability.apply import pinned
        prefix = '        sources = sources + (build_cited_toda55_quadruple_source(),)\n'
        full = prefix + SOURCE_SETUP + SOURCE_ANCHOR
        provider_full = PROVIDER_SETUP + PROVIDER_ANCHOR
        base = text.replace(full, anchor, 1).replace(provider_full, PROVIDER_ANCHOR, 1)
        if not pinned(base, PINS[path]):
            raise ValueError('UNREVIEWED_SHARED_BLOB')
        if base.count(anchor) != 1 or base.count(PROVIDER_ANCHOR) != 1:
            raise ValueError('SHARED_ANCHOR_NOT_UNIQUE')
        changed = base.replace(anchor, full, 1).replace(PROVIDER_ANCHOR, provider_full, 1)
        if text not in (base, changed):
            raise ValueError('PARTIAL_OR_MOVED_PATCH')
        tree = ast.parse(changed)
        for name, token in (('build_shared_typed_bridge', 'build_cited_lemma57_delta_source'),
                            ('shared_expansion_provider', 'build_finite_delta_kernel_provider')):
            node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
            if token not in ast.get_source_segment(changed, node):
                raise ValueError('WRONG_FUNCTION_SCOPE:' + name)
    elif path == HISTORICAL_TEST:
        changed = checked_insertions(text, ((TEST_SETUP, TEST_ANCHOR),), PINS[path])
    else:
        raise ValueError('UNKNOWN_PATCH_TARGET')
    ast.parse(changed)
    return changed.replace('\n', eol).encode('utf-8')


def planned_changes():
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    from phase176_r3r48_cited_finite_delta_kernel.source import build_cited_lemma57_delta_source
    build_cited_lemma57_delta_source(ROOT)
    planned = {}
    for path in PINS:
        old = (ROOT / path).read_bytes()
        planned[path] = old, updated_source(path, old)
    return planned


def write_full_functions(planned):
    names = {SHARED: ('build_shared_typed_bridge', 'shared_expansion_provider'),
             HISTORICAL_TEST: ('test_patch_idempotent_and_rejects_unknown_bytes',)}
    sections = ['# 変更後の関数全文\n']
    for path, (_, raw) in planned.items():
        source, _ = normalize(raw)
        tree = ast.parse(source)
        imports = [ast.get_source_segment(source, node) for node in tree.body
                   if isinstance(node, (ast.Import, ast.ImportFrom))]
        sections.append('## `' + path + '` — import 全文\n\n```python\n' + '\n'.join(imports) + '\n```\n')
        for name in names[path]:
            node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
            sections.append('### `' + name + '`\n\n```python\n' + ast.get_source_segment(source, node) + '\n```\n')
    (PACKAGE / 'SHARED_FUNCTIONS_FULL_JA.md').write_text('\n'.join(sections), encoding='utf-8')


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
    print('PHASE176_R3R48_HEAD=' + subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    print('PHASE176_R3R48_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
