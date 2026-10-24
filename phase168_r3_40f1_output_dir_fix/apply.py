"""Install the R3-40F1 audit-only output-directory fix with strict file guards."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / 'phase168_r3_40f_residual_route_audit'
FILES = ('audit.py', 'tests/test_phase168_r3_40f_residual_route_audit.py')


def main() -> None:
    if not TARGET.is_dir():
        raise SystemExit('R3-40F audit package not found; R3-40F must be extracted first')
    hashes = json.loads((PACKAGE / 'expected_hashes.json').read_text(encoding='utf-8'))
    plans = []
    for name in FILES:
        destination = TARGET / name
        source = PACKAGE / 'full_files' / name
        if not destination.is_file():
            raise SystemExit('Missing target file: ' + str(destination))
        data = destination.read_bytes()
        # Windows line endings can differ after extraction; compare text as well.
        before = hashlib.sha256(destination.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
        if before not in (hashes[name]['before'], hashes[name]['after']):
            raise SystemExit('Unexpected R3-40F source contents; no files changed: ' + name)
        replacement = source.read_text(encoding='utf-8')
        if hashlib.sha256(replacement.encode('utf-8')).hexdigest() != hashes[name]['after']:
            raise SystemExit('Installer payload checksum mismatch: ' + name)
        plans.append((destination, replacement, before == hashes[name]['after']))
    for destination, replacement, already in plans:
        if already:
            print('UNCHANGED', destination.relative_to(ROOT))
        else:
            destination.write_text(replacement, encoding='utf-8')
            print('PATCHED', destination.relative_to(ROOT))
    print('AUDIT_PACKAGE_ONLY: no project implementation file modified')


if __name__ == '__main__':
    main()
