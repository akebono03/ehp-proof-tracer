"""Apply only exact reviewed file replacements; preserve line ending style."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PINS = {
    'phase176_r3r41_public_quadruple_connection/source.py': (
        'b2d7d81b6981c6483db279028da43729805e6d76',
        '79bb68a6bdddd29155d92ec027caeaf7a0ad821f', 'r41_source.txt'),
    'phase176_r3r49_hopf_image_frontier/audit.py': (
        '3c72ab0d5fb4dc0c67e169929c28620ed0e67fc2',
        '27d3205d1af2644565b5b31dd2965cac61528fef', 'r49_audit.txt'),
    'phase176_r3r49_hopf_image_frontier/tests/test_frontier.py': (
        '4f074965c6e530d56028967d40a605240bbfa72d',
        'cb799c26c06cc8217427c7316b0706e3d138f145', 'r49_test.txt'),
}


def blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def updated_source(path: str, raw: bytes) -> bytes:
    old_pin, new_pin, template = PINS[path]
    lf = raw.replace(b'\r\n', b'\n')
    if b'\r' in lf or (raw != lf and raw != lf.replace(b'\n', b'\r\n')):
        raise ValueError('MIXED_OR_UNSUPPORTED_EOL:' + path)
    if blob(lf) not in (old_pin, new_pin):
        raise ValueError('UNREVIEWED_FILE_BYTES:' + path)
    replacement = (PACKAGE / 'replacements' / template).read_bytes()
    if blob(replacement) != new_pin:
        raise ValueError('REPLACEMENT_HASH_MISMATCH:' + path)
    ast.parse(replacement.decode('utf-8'), filename=path)
    return replacement if raw == lf else replacement.replace(b'\n', b'\r\n')


def planned_changes() -> dict[str, tuple[bytes, bytes]]:
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED:' + branch)
    from phase176_r3r48_cited_finite_delta_kernel.apply import planned_changes as prior
    if any(old != new for old, new in prior().values()):
        raise RuntimeError('R3R48_NOT_APPLIED')
    # R3R49 audit sources may still be untracked; their exact ZIP bytes are pinned.
    result = {}
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        result[path] = (raw, updated_source(path, raw))
    # The original strict guard is also reviewed, never patched by this Phase.
    guard = ROOT / 'phase175_r4r12r13r7_typed_nu_prime_notation/notation.py'
    if blob(guard.read_bytes().replace(b'\r\n', b'\n')) != '70ee0c0a00002f9946ac8d243097fd87b3e4c299':
        raise ValueError('UNREVIEWED_NU_PRIME_GUARD')
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    changes = planned_changes()
    print('PHASE176_R3R50_HEAD=' + subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())
    if not args.dry_run:
        written = []
        try:
            for path, (old, new) in changes.items():
                if old != new:
                    (ROOT / path).write_bytes(new)
                    written.append(path)
        except BaseException:
            for path in reversed(written):
                (ROOT / path).write_bytes(changes[path][0])
            raise
    print('PHASE176_R3R50_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
