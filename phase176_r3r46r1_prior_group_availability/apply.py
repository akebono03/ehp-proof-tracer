"""Guarded three-file patch. Preserve EOLs and all unrelated source bytes."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
DB = 'phase169_r10e4_ordered_db_prior/db_prior.py'
DFS = 'phase165_r3_recursive_search.py'
SHARED = 'phase165_r52_r9_shared_math.py'
PINS = {
    DB: 'ed8c6a1f0f6f130005d42a2edba4ab40991e879b',
    DFS: '06009bfcf57f99cac58c229d99c53f16324692d0',
    SHARED: '2dca975cd4a9e1353c3022c791d98817575f2ced',
}
# Rule bodies relied on by the new connection, not modified here.
DEPENDENCIES = {
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py': '66407339808ed4ba8a65c04fd3bfbbf05bde6745',
    'phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py': 'dfa1519c629eef92ca1c5dae265acc050883649b',
    'phase175_r4r14r9_literature_zero_image/rule.py': '82d69284c16a3e77eacf1b23a4eb84a13249dd56',
    'phase176_r3r16_public_connection/provider.py': 'c34306ab748fb3a6ca559efc596e2f4e98b100ca',
}
DFS_SETUP_ANCHOR = '    def resolve(target: object) -> ProofStep:\n'
DFS_SETUP = '''    from phase176_r3r46r1_prior_group_availability.pruning import contradiction_witness

    def contradicted(target: object) -> bool:
        return contradiction_witness(
            target, bridge=bridge, citing_id=citing_assertion_id,
            lookup_mode=lookup_mode, verified_assertion_ids=verified_assertion_ids,
            proof_target=goal, solved=tuple(solved),
            completed_internal_proofs=completed_internal_proofs,
        ) is not None

'''
DFS_GOAL_ANCHOR = '            expansions = expansion_provider(actual)\n'
DFS_GOAL = '''            # Reject an impossible unproved zero obligation before its Provider.
            if contradicted(target):
                raise RegisteredGoalUnresolved("zero goal contradicted by eligible nonzero evidence")
'''
DFS_BRANCH_ANCHOR = '                try:\n                    premises = tuple(resolve(child) for child in expansion.subgoals)\n'
DFS_BRANCH = '''                # Preflight all immediate zero obligations before visiting any.
                if any(contradicted(child) for child in expansion.subgoals):
                    continue
'''
SHARED_ANCHOR = '    shared_provider_registry = build_shared_expansion_provider_registry(\n'
SHARED_SETUP = '''    # R3R46R1: reuse admitted prior domains without the stable-family gate.
    # Append after the existing source-specific providers; no new rule.
    from phase176_r3r46r1_prior_group_availability.provider import build_prior_zero_image_provider
    extra_providers = tuple(extra_providers) + (
        build_prior_zero_image_provider(bridge=bridge, proof_target=proof_target),
    )

'''


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def normalize(raw):
    if b'\r' in raw.replace(b'\r\n', b'') or (b'\r\n' in raw and b'\n' in raw.replace(b'\r\n', b'')):
        raise ValueError('MIXED_LINE_ENDINGS')
    return raw.decode('utf-8').replace('\r\n', '\n'), '\r\n' if b'\r\n' in raw else '\n'


def pinned(text, pin):
    return pin in (blob(text.encode('utf-8')), blob(text.replace('\n','\r\n').encode('utf-8')))


def checked_insertions(text, pairs, pin):
    """Accept only the reviewed baseline or the exact idempotent new patch."""
    if any(chunk in text for chunk, _ in pairs):
        if not all(text.count(chunk + anchor) == 1 for chunk, anchor in pairs):
            raise ValueError('PARTIAL_OR_MOVED_PATCH')
        for chunk, anchor in pairs:
            text = text.replace(chunk + anchor, anchor, 1)
    if not pinned(text, pin):
        raise ValueError('UNREVIEWED_SOURCE_BLOB')
    for chunk, anchor in pairs:
        if text.count(anchor) != 1:
            raise ValueError('ANCHOR_NOT_UNIQUE')
        text = text.replace(anchor, chunk + anchor, 1)
    return text


def updated_source(path, raw):
    text, newline = normalize(raw)
    if path == DB:
        addition = '\n\n' + (PACKAGE / 'db_addition.py.txt').read_text(encoding='utf-8')
        if text.endswith(addition):
            text = text[:-len(addition)]
        if not pinned(text, PINS[path]):
            raise ValueError('UNREVIEWED_DB_PRIOR_BLOB')
        changed = text + addition
    elif path == DFS:
        changed = checked_insertions(text, ((DFS_SETUP, DFS_SETUP_ANCHOR),
                    (DFS_GOAL, DFS_GOAL_ANCHOR), (DFS_BRANCH, DFS_BRANCH_ANCHOR)), PINS[path])
    elif path == SHARED:
        changed = checked_insertions(text, ((SHARED_SETUP, SHARED_ANCHOR),), PINS[path])
    else:
        raise ValueError('UNKNOWN_PATCH_TARGET')
    ast.parse(changed)
    return changed.replace('\n', newline).encode('utf-8')


def planned_changes():
    if subprocess.check_output(['git','branch','--show-current'], cwd=ROOT, text=True).strip() != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    for path, pin in DEPENDENCIES.items():
        text, _ = normalize((ROOT / path).read_bytes())
        if not pinned(text, pin):
            raise ValueError('UNREVIEWED_DEPENDENCY:' + path)
    planned = {}
    for path in PINS:
        original = (ROOT / path).read_bytes()
        try:
            changed = updated_source(path, original)
        except ValueError as exc:
            raise ValueError(path + ': ' + str(exc)) from exc
        planned[path] = original, changed
    return planned


def write_full_functions(planned):
    names = {DB:'admitted_prior_group_step', DFS:'reconstruct_registered_goal',
             SHARED:'shared_expansion_provider'}
    docs = ['# 変更後の関数全文\n']
    for path, (_, raw) in planned.items():
        source, _ = normalize(raw)
        node = next(n for n in ast.parse(source).body
                    if isinstance(n, ast.FunctionDef) and n.name == names[path])
        full = '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
        docs.append('## `' + path + '`\n\n```python\n' + full + '\n```\n')
    (PACKAGE / 'SHARED_FUNCTIONS_FULL_JA.md').write_text('\n'.join(docs), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    planned = planned_changes()
    if not args.dry_run:
        # Check all files before writing any, and roll back a failed write.
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
    print('PHASE176_R3R46R1_HEAD=' + subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    print('PHASE176_R3R46R1_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
