"""Two exact function replacements; all other reviewed bytes are preserved."""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r56r2_namespace_source_fix import apply as namespace_fix

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SOURCE = 'phase176_r3r56_cited_source_display_isolated/projection.py'
LAYOUT = 'phase171_r20r13_eta_sentence_layout/projection.py'
PINS = {SOURCE: ('8298813c634ba77d533387f12bd594c1372acf08', 'source_citation'),
        LAYOUT: ('5deaa8886f36ec967d52b9fcd603d135ae290b39', 'format_complete_proof_sentences')}


def template(name, version):
    return (PACKAGE / f'{name}_{version}.py.txt').read_text(encoding='utf-8').rstrip('\n')


def function_node(source, name):
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise ValueError('FUNCTION_NOT_UNIQUE:' + name)
    return nodes[0]


def baseline_source(path, raw):
    pin, name = PINS[path]
    text, eol = normalize(raw)
    old, new = template(name, 'BEFORE'), template(name, 'FULL')
    current = ast.get_source_segment(text, function_node(text, name))
    if current not in (old, new) or text.count(current) != 1:
        raise ValueError('UNREVIEWED_FUNCTION:' + path)
    base = text.replace(current, old, 1)
    if not pinned(base, pin):
        raise ValueError('UNREVIEWED_BASELINE:' + path)
    return base, eol


def updated_source(path, raw):
    base, eol = baseline_source(path, raw)
    _, name = PINS[path]
    new = template(name, 'FULL')
    changed = base.replace(template(name, 'BEFORE'), new, 1)
    if ast.get_source_segment(changed, function_node(changed, name)) != new:
        raise ValueError('FULL_FUNCTION_MISMATCH:' + path)
    return changed.replace('\n', eol).encode('utf-8')


def planned_changes():
    changes = {}
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        changes[path] = (raw, updated_source(path, raw))
    # Check the already applied historical namespace fix exactly. The older
    # preflight also pins the final layout; allow only our inverse-verified blob.
    current = normalize(changes[LAYOUT][0])[0].encode('utf-8')
    sha = hashlib.sha1(b'blob ' + str(len(current)).encode('ascii') + b'\0' + current).hexdigest()
    with patch.dict(namespace_fix.r56.baseline.PINS, {LAYOUT: sha}):
        raw = namespace_fix.preflight()
    if namespace_fix.updated_source(raw) != raw:
        raise RuntimeError('R56R2_NOT_APPLIED')
    return changes


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE.name
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    changes = planned_changes()
    if not args.dry_run:
        if any((ROOT / p).read_bytes() != raw for p, (raw, _) in changes.items()):
            raise RuntimeError('SOURCE_CHANGED_DURING_PREFLIGHT')
        for path, (raw, changed) in changes.items():
            if raw != changed:
                (ROOT / path).write_bytes(changed)
    folder = artifact_folder()
    for _, name in PINS.values():
        (folder / f'{name}_FULL.py.txt').write_text(template(name, 'FULL') + '\n', encoding='utf-8')
    print('PHASE176_R3R56R3_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    if args.dry_run:
        print('PHASE176_R3R56R3_GATE=PASS_R3R56R3_DRYRUN')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
