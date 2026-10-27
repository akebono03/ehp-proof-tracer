"""Guarded single-call-site replacement for the common backward provider."""
from __future__ import annotations

import ast
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
OUTPUT = HERE / 'output'
BACKUP = OUTPUT / 'phase165_r52_r9_shared_math.py.before'
OLD = '''        # R10D2: stem-neutral R7 transport, with publication order checked
        # by the prior-source resolver and each generator image independently proved.
        # Retain the already verified R5B/R6A expansions when they are available.
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and isinstance(goal, Relation)
                and isinstance(goal.lhs, TodaPrimaryGroup)
                and type(goal.lhs.group_dimension) is int
                and type(goal.lhs.sphere_dimension) is int):
            options.extend(expand_prior_general_stable_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))
'''.encode('utf-8')
NEW = '''        # R10E1: one typed entry for zero, cyclic, free and direct-sum groups.
        # Previously verified finite-cyclic derivations retain their R7 adapter.
        # Neither DB results nor candidate generators become GIVEN proof leaves.
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from phase169_r10e1_general_group_transport.transport import (
            expand_prior_general_group_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and ((isinstance(goal, Relation)
                      and isinstance(goal.lhs, TodaPrimaryGroup)
                      and type(goal.lhs.group_dimension) is int
                      and type(goal.lhs.sphere_dimension) is int)
                     or isinstance(goal, TodaPrimaryGroupZeroStatement))):
            options.extend(expand_prior_general_group_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))
'''.encode('utf-8')


def transform(raw: bytes) -> tuple[bytes, str]:
    if not isinstance(raw, bytes):
        raise TypeError('raw source must be bytes')
    crlf = b'\r\n' in raw
    normalized = raw.replace(b'\r\n', b'\n')
    if normalized.count(OLD) != 1 or NEW in normalized:
        raise RuntimeError('R10E1 patch boundary changed; stop without writing')
    changed = normalized.replace(OLD, NEW, 1)
    tree = ast.parse(changed.decode('utf-8'))
    funcs = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == 'shared_expansion_provider']
    if len(funcs) != 1:
        raise RuntimeError('expected one complete shared_expansion_provider')
    node = funcs[0]
    full = ''.join(changed.decode('utf-8').splitlines(True)[node.lineno - 1:node.end_lineno])
    if crlf:
        changed = changed.replace(b'\n', b'\r\n')
    return changed, full


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    raw = TARGET.read_bytes()
    changed, full = transform(raw)
    # All outputs are prepared before mutating production source.
    BACKUP.write_bytes(raw)
    (OUTPUT / 'shared_expansion_provider_FULL.py').write_text(full, encoding='utf-8')
    (OUTPUT / 'phase165_r52_r9_shared_math.py.FULL').write_bytes(changed)
    temporary = TARGET.with_name(TARGET.name + '.r10e1-tmp')
    try:
        temporary.write_bytes(changed)
        os.replace(temporary, TARGET)
    finally:
        if temporary.exists():
            temporary.unlink()
    print('R10E1_PATCHED=' + str(TARGET))
    print('R10E1_BACKUP=' + str(BACKUP))
    print('R10E1_FULL_FUNCTION=' + str(OUTPUT / 'shared_expansion_provider_FULL.py'))
    print('R10E1_FULL_FILE=' + str(OUTPUT / 'phase165_r52_r9_shared_math.py.FULL'))


if __name__ == '__main__':
    main()
