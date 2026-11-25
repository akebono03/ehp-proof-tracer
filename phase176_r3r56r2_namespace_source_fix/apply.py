"""Apply the one reviewed source lookup change, retaining historical tests."""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r56_cited_source_display_isolated import audit as r56
from phase176_r3r56r1_historical_source_audit.audit import TEST, TEST_PIN

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RELATIVE = 'phase175_r3r11_cited_hopf_narrative/projection.py'
TARGET = ROOT / RELATIVE
PIN = 'a9ecbffc4b89c2da84bc523fd9388b44d476fb26'
OLD = (PACKAGE / '_source_citation_BEFORE.py.txt').read_text(encoding='utf-8').rstrip('\n')
NEW = (PACKAGE / '_source_citation_FULL.py.txt').read_text(encoding='utf-8').rstrip('\n')


def function_node(source):
    nodes = [n for n in ast.parse(source).body
             if isinstance(n, ast.FunctionDef) and n.name == '_source_citation']
    if len(nodes) != 1:
        raise ValueError('SOURCE_LOOKUP_NOT_UNIQUE')
    return nodes[0]


def baseline_source(raw):
    source, eol = normalize(raw)
    current = ast.get_source_segment(source, function_node(source))
    if current not in (OLD, NEW):
        raise ValueError('UNREVIEWED_SOURCE_LOOKUP')
    if source.count(current) != 1:
        raise ValueError('AMBIGUOUS_SOURCE_LOOKUP')
    base = source.replace(current, OLD, 1)
    if not pinned(base, PIN):
        raise ValueError('UNREVIEWED_PROJECTION_BASELINE')
    return base, eol


def updated_source(raw):
    base, eol = baseline_source(raw)
    changed = base.replace(OLD, NEW, 1)
    if ast.get_source_segment(changed, function_node(changed)) != NEW:
        raise ValueError('FULL_FUNCTION_MISMATCH')
    return changed.replace('\n', eol).encode('utf-8')


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE.name
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def preflight():
    raw = TARGET.read_bytes()
    updated_source(raw)  # Check the inverse against the exact old Git blob first.
    if not pinned(normalize(TEST.read_bytes())[0], TEST_PIN):
        raise RuntimeError('UNREVIEWED_HISTORICAL_TEST')
    # Old preflight pins the historical source file. Rebind only its already
    # independently checked blob in memory; all other dependencies remain pinned.
    text, _ = normalize(raw)
    data = text.encode('utf-8')
    current_pin = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
    with patch.dict(r56.baseline.PINS, {RELATIVE: current_pin}), patch.dict(r56.PINS, {RELATIVE: current_pin}):
        r56.preflight()
    return raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    raw = preflight()
    changed = updated_source(raw)
    if not args.dry_run and raw != changed:
        if TARGET.read_bytes() != raw:
            raise RuntimeError('SOURCE_CHANGED_DURING_PREFLIGHT')
        TARGET.write_bytes(changed)
    folder = artifact_folder()
    (folder / '_source_citation_FULL.py.txt').write_text(NEW + '\n', encoding='utf-8')
    print('PHASE176_R3R56R2_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    print('ARTIFACTS=' + str(folder))
    if args.dry_run:
        print('PHASE176_R3R56R2_GATE=PASS_R3R56R2_DRYRUN')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
