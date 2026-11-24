"""Apply exactly two local hooks to the reviewed shared provider, preserving bytes."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
BASE = '165f2d0ad78e0dcb05d01ec0784b974a92c5ee02'
ISOLATED = ROOT / 'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/rule.py'
RULE_HASH = 'f0df5964beb9c32eec0ae2ec674e0330b046327e6e4aeb18ad0d60e0926ad401'
SETUP_ANCHOR = '    if not isinstance(prior_conclusions, tuple):\n        raise TypeError("prior_conclusions must be a tuple")\n'
SETUP = '''    # Phase 176 R3R44: bind five open obligations to the existing isolated rule.
    from phase176_r3r44_public_subgroup_lift.provider import (
        build_public_subgroup_lift_provider,
    )
    public_subgroup_lift = build_public_subgroup_lift_provider(
        tuple(available), prior_conclusions,
    )
'''
DISPATCH_ANCHOR = '        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n'
DISPATCH = '        options.extend(public_subgroup_lift(goal))\n'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def unique_function(nodes, name):
    matches = [node for node in nodes if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError('FUNCTION_NOT_UNIQUE:' + name)
    return matches[0]


def updated_source(source):
    if '\r' in source or source.startswith('\ufeff'):
        raise ValueError('EXPECTED_LF_SOURCE')
    tree = ast.parse(source)
    fn = unique_function(tree.body, 'shared_expansion_provider')
    expand = unique_function(fn.body, 'expand')
    lines = source.splitlines(keepends=True)
    setup_body = ''.join(lines[fn.lineno-1:expand.lineno-1])
    dispatch_body = ''.join(lines[expand.lineno-1:expand.end_lineno])
    if setup_body.count(SETUP_ANCHOR) != 1 or dispatch_body.count(DISPATCH_ANCHOR) != 1:
        raise ValueError('HOOK_ANCHOR_NOT_UNIQUE')
    if 'public_subgroup_lift' in source:
        if (source.count(SETUP) != 1 or source.count(DISPATCH) != 1
                or SETUP_ANCHOR+SETUP not in setup_body
                or DISPATCH_ANCHOR+DISPATCH not in dispatch_body
                or source.count('public_subgroup_lift') != (SETUP+DISPATCH).count('public_subgroup_lift')):
            raise ValueError('PARTIAL_OR_MOVED_PATCH')
        return source
    changed = source.replace(SETUP_ANCHOR, SETUP_ANCHOR+SETUP, 1).replace(DISPATCH_ANCHOR, DISPATCH_ANCHOR+DISPATCH, 1)
    if source.count(SETUP_ANCHOR) != 1 or source.count(DISPATCH_ANCHOR) != 1:
        raise ValueError('GLOBAL_HOOK_ANCHOR_NOT_UNIQUE')
    ast.parse(changed)
    return changed


def reviewed_source():
    if git('branch','--show-current') != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    if not ISOLATED.is_file() or hashlib.sha256(ISOLATED.read_bytes().replace(b'\r\n',b'\n')).hexdigest() != RULE_HASH:
        raise RuntimeError('R3R43R1_REVIEWED_RULE_MISSING_OR_CHANGED')
    original = TARGET.read_bytes().decode('utf-8')
    changed = updated_source(original)
    baseline = changed.replace(SETUP,'',1).replace(DISPATCH,'',1)
    if blob(baseline.encode('utf-8')) != BASE:
        raise RuntimeError('SHARED_BASELINE_CHANGED')
    # Permit only the exact pre/post patch shared file; never overwrite other edits.
    head_blob = git('rev-parse','HEAD:phase165_r52_r9_shared_math.py')
    if head_blob not in (BASE, blob(changed.encode('utf-8'))):
        raise RuntimeError('SHARED_HEAD_CHANGED')
    tracked = set(git('diff','--name-only','HEAD').splitlines())
    if tracked - {TARGET.name}:
        raise RuntimeError('UNRELATED_TRACKED_CHANGES:' + repr(sorted(tracked - {TARGET.name})))
    if git('diff','--cached','--name-only'):
        raise RuntimeError('STAGED_CHANGES_PRESENT')
    return original, changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    original, changed = reviewed_source()
    fn = unique_function(ast.parse(changed).body,'shared_expansion_provider')
    full = '\n'.join(changed.splitlines()[fn.lineno-1:fn.end_lineno])
    if not args.dry_run:
        if original != changed:
            TARGET.write_bytes(changed.encode('utf-8'))
        (Path(__file__).parent/'SHARED_FUNCTION_FULL_JA.md').write_bytes(('# 変更後の共有関数全文\n\n```python\n'+full+'\n```\n').encode('utf-8'))
    print('PHASE176_R3R44_HEAD='+git('rev-parse','HEAD'))
    print('PHASE176_R3R44_PATCH='+('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
