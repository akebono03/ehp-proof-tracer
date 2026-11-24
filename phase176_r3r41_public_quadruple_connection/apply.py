"""Minimal byte-preserving connection to the reviewed shared provider."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
SETUP_ANCHOR = '    if not isinstance(prior_conclusions, tuple):\n'
SETUP = '''    # Phase 176 R3R41: audited source-screened quadruple connection.
    from phase176_r3r41_public_quadruple_connection.source import (
        build_public_quadruple_connection_provider,
    )
    public_quadruple_connection = build_public_quadruple_connection_provider(
        tuple(available),
    )
'''
DISPATCH_ANCHOR = ('        options = []\n'
                   '        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (\n'
                   '            expand_public_cited_prop27_goal,\n')
DISPATCH = '        options.extend(public_quadruple_connection(goal))\n'
PATCHED_DISPATCH_ANCHOR = '        options = []\n' + DISPATCH + DISPATCH_ANCHOR.split('\n', 1)[1]


def _unique_function(nodes, name: str) -> ast.FunctionDef:
    matches = [node for node in nodes
               if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError('SHARED_FUNCTION_NOT_UNIQUE:' + name)
    return matches[0]


def updated_source(source: str) -> str:
    """Edit only the reviewed function and its immediate nested expand."""
    if '\r' in source or source.startswith('\ufeff'):
        raise ValueError('EXPECTED_REPAIRED_LF_SOURCE')
    tree = ast.parse(source)
    function = _unique_function(tree.body, 'shared_expansion_provider')
    expand = _unique_function(function.body, 'expand')
    lines = source.splitlines(keepends=True)
    start, stop = function.lineno - 1, function.end_lineno
    body = ''.join(lines[start:stop])
    dispatch_body = ''.join(lines[expand.lineno - 1:expand.end_lineno])
    setup_body = ''.join(lines[start:expand.lineno - 1])
    if body.count(SETUP_ANCHOR) != 1 or setup_body.count(SETUP_ANCHOR) != 1:
        raise ValueError('SHARED_SETUP_ANCHOR_NOT_UNIQUE')
    if dispatch_body.count('options.extend(public_right_hopf_transport(goal))') != 1:
        raise ValueError('R3R39_HOOK_MISSING')
    if SETUP in setup_body and DISPATCH in dispatch_body:
        if (source.count(SETUP) != 1 or source.count(DISPATCH) != 1
                or source.count('public_quadruple_connection') != SETUP.count('public_quadruple_connection') + DISPATCH.count('public_quadruple_connection')
                or setup_body.count(SETUP + SETUP_ANCHOR) != 1
                or dispatch_body.count(PATCHED_DISPATCH_ANCHOR) != 1
                or DISPATCH_ANCHOR in dispatch_body):
            raise ValueError('DUPLICATE_OR_MOVED_R3R41_PATCH')
        return source
    if 'public_quadruple_connection' in source:
        raise ValueError('PARTIAL_OR_CHANGED_R3R41_PATCH')
    if dispatch_body.count(DISPATCH_ANCHOR) != 1 or body.count(DISPATCH_ANCHOR) != 1:
        raise ValueError('SHARED_DISPATCH_ANCHOR_NOT_UNIQUE')
    changed_body = body.replace(SETUP_ANCHOR, SETUP + SETUP_ANCHOR, 1)
    changed_body = changed_body.replace(DISPATCH_ANCHOR, PATCHED_DISPATCH_ANCHOR, 1)
    changed = ''.join(lines[:start]) + changed_body + ''.join(lines[stop:])
    ast.parse(changed)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    original = TARGET.read_bytes().decode('utf-8')
    changed = updated_source(original)
    if not args.dry_run:
        if changed != original:
            TARGET.write_bytes(changed.encode('utf-8'))
        tree = ast.parse(changed)
        function = _unique_function(tree.body, 'shared_expansion_provider')
        full = '\n'.join(changed.splitlines()[function.lineno-1:function.end_lineno])
        (Path(__file__).parent / 'SHARED_FUNCTION_FULL_JA.md').write_bytes(
            ('# 変更後の共有関数全文\n\n```python\n' + full + '\n```\n').encode('utf-8'))
    print('PHASE176_R3R41_PATCH=' + ('DRY_RUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
