"""Exact reversible function replacements; preserve unrelated source and EOLs."""
from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r57r1_public_composite_hopf_display import apply as r57

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LAYOUT = r57.LAYOUT
LIFT_FIXTURE = 'phase176_r3r58_finite_cyclic_lift_display_isolated/tests/test_projection.py'
HOPF_FIXTURE = r57.FIXTURE
HOPF_HISTORY = 'phase176_r3r57r1_public_composite_hopf_display/tests/test_connection.py'
SOURCE_HISTORY = r57.HISTORY
PROJECTION = 'phase176_r3r58_finite_cyclic_lift_display_isolated/projection.py'
PINS = {
    LAYOUT: ('8015d70a2fe154c69b7c5911c1e838575fadd8e5', (('format_complete_proof_sentences', 'layout'),)),
    LIFT_FIXTURE: ('d0649c7efe7328631c62f76a6f30b33ef956e1ae', (('verified', 'lift_fixture'),)),
    HOPF_FIXTURE: ('062d9c5734520b624e56b63265aa5e739904853e', (('verified', 'hopf_fixture'),)),
    HOPF_HISTORY: ('eaedac911289b68c2760a5510da37f8528960428', (
        ('test_exact_replacements_are_idempotent_and_reject_unknown_bytes', 'hopf_exact'),
        ('test_previous_public_source_connection_is_preserved', 'hopf_history'),)),
    SOURCE_HISTORY: ('061e1c2eb6adbdc1cc337dc8a8e5f41a1e6c6370', (('test_two_exact_replacements_are_idempotent', 'source_history'),)),
}


def template(key, version):
    return (PACKAGE / f'{key}_{version}.py.txt').read_text(encoding='utf-8').rstrip('\n')


def previous_source(path, raw):
    pin, replacements = PINS[path]
    source, eol = normalize(raw)
    stages = set()
    for name, key in replacements:
        old, new = template(key, 'BEFORE'), template(key, 'FULL')
        current = r57.function_text(source, name)
        if current not in (old, new) or source.count(current) != 1:
            raise ValueError('UNREVIEWED_FUNCTION:' + path + ':' + name)
        stages.add(current == new)
        source = source.replace(current, old, 1)
    if len(stages) != 1 or not pinned(source, pin):
        raise ValueError('UNREVIEWED_OR_PARTIAL_PREVIOUS_STAGE:' + path)
    return source.replace('\n', eol).encode('utf-8')


def updated_source(path, raw):
    source, eol = normalize(previous_source(path, raw))
    for name, key in PINS[path][1]:
        old, new = template(key, 'BEFORE'), template(key, 'FULL')
        source = source.replace(old, new, 1)
        if r57.function_text(source, name) != new:
            raise ValueError('REPLACEMENT_MISMATCH:' + path + ':' + name)
    return source.replace('\n', eol).encode('utf-8')


def r57_stage_bytes(path):
    raw = (ROOT / path).read_bytes()
    return previous_source(path, raw) if path in PINS else raw


def r57_stage_changes():
    # Execute the original strict R57R1 preflight with exact inverse-verified
    # bytes for its three changed inputs; all other reads remain real.
    restored = {ROOT / path: r57_stage_bytes(path) for path in r57.PINS}
    read_bytes = Path.read_bytes

    def read_at_previous_stage(path):
        if path in restored:
            return restored[path]
        return read_bytes(path)

    with patch.object(Path, 'read_bytes', read_at_previous_stage):
        return r57.planned_changes()


def planned_changes():
    changes = {}
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        changes[path] = (raw, updated_source(path, raw))
    applied = {raw == new for raw, new in changes.values()}
    if len(applied) != 1:
        raise RuntimeError('PARTIALLY_APPLIED_R58R1')
    if any(raw != new for raw, new in r57_stage_changes().values()):
        raise RuntimeError('R57R1_NOT_APPLIED')
    if not pinned(normalize((ROOT / PROJECTION).read_bytes())[0],
                  '408e517adb9af0053b7bee84dd4297254eb35d2b'):
        raise RuntimeError('R58_PROJECTION_CHANGED')
    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    changes = planned_changes()
    if not args.dry_run:
        if any((ROOT / path).read_bytes() != raw for path, (raw, _) in changes.items()):
            raise RuntimeError('SOURCE_CHANGED_DURING_PREFLIGHT')
        written = []
        try:
            for path, (raw, new) in changes.items():
                if raw != new:
                    written.append(path)
                    (ROOT / path).write_bytes(new)
        except BaseException:
            for path in reversed(written):
                (ROOT / path).write_bytes(changes[path][0])
            raise
    print('PHASE176_R3R58R1_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    if args.dry_run:
        print('PHASE176_R3R58R1_GATE=PASS_R3R58R1_DRYRUN')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
