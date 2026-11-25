"""Exact three-function replacement; proof/search source is not modified."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r56r3_public_cited_source_display import apply as r56
from phase176_r3r56r2_namespace_source_fix import apply as namespace_fix
from phase176_r3r55r1_public_equality_projection import apply as r55

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LAYOUT = 'phase171_r20r13_eta_sentence_layout/projection.py'
FIXTURE = 'phase176_r3r57_composite_hopf_display_isolated/tests/test_projection.py'
HISTORY = 'phase176_r3r56r3_public_cited_source_display/tests/test_connection.py'
PROJECTION = 'phase176_r3r57_composite_hopf_display_isolated/projection.py'
PINS = {
    LAYOUT: ('4f8aa3bdbf0ce4caa12b27d86d87fe0af807d554', 'format_complete_proof_sentences'),
    FIXTURE: ('2a5ae5dbd471cc076e8ee9554cd131ad7afa258d', 'verified'),
    HISTORY: ('1fc0d95655405c76b056a354119a2e5f0b3e423d', 'test_two_exact_replacements_are_idempotent'),
}


def template(name, version):
    return (PACKAGE / f'{name}_{version}.py.txt').read_text(encoding='utf-8').rstrip('\n')


def function_text(source, name):
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise ValueError('FUNCTION_NOT_UNIQUE:' + name)
    return ast.get_source_segment(source, nodes[0])


def previous_source(path, raw):
    pin, name = PINS[path]
    text, eol = normalize(raw)
    old, new = template(name, 'BEFORE'), template(name, 'FULL')
    current = function_text(text, name)
    if current not in (old, new) or text.count(current) != 1:
        raise ValueError('UNREVIEWED_FUNCTION:' + path)
    base = text.replace(current, old, 1)
    if not pinned(base, pin):
        raise ValueError('UNREVIEWED_PREVIOUS_STAGE:' + path)
    return base.replace('\n', eol).encode('utf-8')


def updated_source(path, raw):
    base, eol = normalize(previous_source(path, raw))
    _, name = PINS[path]
    changed = base.replace(template(name, 'BEFORE'), template(name, 'FULL'), 1)
    if function_text(changed, name) != template(name, 'FULL'):
        raise ValueError('REPLACEMENT_MISMATCH:' + path)
    return changed.replace('\n', eol).encode('utf-8')


def planned_changes():
    changes = {}
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        changes[path] = (raw, updated_source(path, raw))
    previous_layout = previous_source(LAYOUT, changes[LAYOUT][0])
    if r56.updated_source(LAYOUT, previous_layout) != previous_layout:
        raise RuntimeError('R56_LAYOUT_NOT_APPLIED')
    raw = (ROOT / r56.SOURCE).read_bytes()
    if r56.updated_source(r56.SOURCE, raw) != raw:
        raise RuntimeError('R56_SOURCE_NOT_APPLIED')
    raw = namespace_fix.TARGET.read_bytes()
    if namespace_fix.updated_source(raw) != raw:
        raise RuntimeError('R56R2_NOT_APPLIED')
    raw = r55.TARGET.read_bytes()
    if r55.updated_source(raw) != raw:
        raise RuntimeError('R55R1_NOT_APPLIED')
    if not pinned(normalize((ROOT / PROJECTION).read_bytes())[0], '2f54ed18b2729070b64f3b0613cc62a6f5f9dcf9'):
        raise RuntimeError('R57_PROJECTION_CHANGED')
    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    changes = planned_changes()
    if not args.dry_run:
        if any((ROOT / path).read_bytes() != raw for path, (raw, _) in changes.items()):
            raise RuntimeError('SOURCE_CHANGED_DURING_PREFLIGHT')
        for path, (raw, changed) in changes.items():
            if raw != changed:
                (ROOT / path).write_bytes(changed)
    print('PHASE176_R3R57R1_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    if args.dry_run:
        print('PHASE176_R3R57R1_GATE=PASS_R3R57R1_DRYRUN')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
