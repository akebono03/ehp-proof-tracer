"""Exact reversible replacements; historical checks see only validated prior bytes."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r57r1_public_composite_hopf_display.apply import function_text
from phase176_r3r58r1_public_finite_cyclic_lift_display import apply as r58

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LAYOUT = r58.LAYOUT
ISOLATED = 'phase176_r3r59r3_definitional_suspension_elision_isolated'
PINS = {
    LAYOUT: ('71351ba0072f9bb60f74eb8dffb5f21f4724e549', (('format_complete_proof_sentences', 'layout'),)),
    r58.LIFT_FIXTURE: ('5d12ce30fa007992b1eaf9f9fb99459b15b306ca', (('verified', 'lift_fixture'),)),
    r58.HOPF_HISTORY: ('c2771a0fc6ef12ce64d13486f455f03a2de89baf', (
        ('test_exact_replacements_are_idempotent_and_reject_unknown_bytes', 'hopf_exact'),
        ('test_previous_public_source_connection_is_preserved', 'hopf_history'),)),
    r58.SOURCE_HISTORY: ('602fd5f5ccc37a9a6e073a737734f5b9f0b13863', (('test_two_exact_replacements_are_idempotent', 'source_history'),)),
    'phase176_r3r58r1_public_finite_cyclic_lift_display/tests/test_connection.py': (
        '1117bbd5e05d514def106be9f648f126d4fedf54', (
            ('test_exact_replacements_and_unknown_bytes', 'lift_exact'),
            ('test_prior_stage_is_preserved', 'lift_history'),
            ('test_public_finite_cyclic_lift_on_verified_model', 'lift_public'),)),
    ISOLATED + '/tests/test_projection.py': ('cf225695a06ed878212a9b3fec01bbe78a65af30', (('verified', 'elision_fixture'),)),
}


def template(key, version):
    return (PACKAGE / f'{key}_{version}.py.txt').read_text(encoding='utf-8').rstrip('\n')


def previous_source(path, raw):
    pin, replacements = PINS[path]
    source, eol = normalize(raw)
    stages = set()
    for name, key in replacements:
        old, new = template(key, 'BEFORE'), template(key, 'FULL')
        current = function_text(source, name)
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
        if function_text(source, name) != new:
            raise ValueError('REPLACEMENT_MISMATCH:' + path + ':' + name)
    return source.replace('\n', eol).encode('utf-8')


@contextmanager
def previous_stage():
    """Scope the inverse-verified file reads and display hook to historical checks.

    No disk writes, no changed trust/search behavior, no global pytest fixture.
    Production rendering never enters this context.
    """
    from phase176_r3r59r3_definitional_suspension_elision_isolated import projection
    restored = {ROOT / path: previous_source(path, (ROOT / path).read_bytes()) for path in PINS}
    read_bytes = Path.read_bytes

    def read_at_previous_stage(path):
        if path in restored:
            return restored[path]
        return read_bytes(path)

    with patch.object(Path, 'read_bytes', read_at_previous_stage), patch.object(
            projection, 'project_definitional_suspension_elision',
            lambda markdown, model: (markdown, {})):
        yield


def planned_changes():
    changes = {}
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        changes[path] = (raw, updated_source(path, raw))
    if len({raw == new for raw, new in changes.values()}) != 1:
        raise RuntimeError('PARTIALLY_APPLIED_R59R4')
    for path, pin in {
        ISOLATED + '/projection.py': '1fe8211bc55ee4db825c3a20c3737153d2e7280f',
        ISOLATED + '/audit.py': 'cfa44cb04a5c9c0aaeea9bea263316ff102f7bb4',
    }.items():
        if not pinned(normalize((ROOT / path).read_bytes())[0], pin):
            raise RuntimeError('UNREVIEWED_ISOLATED_SOURCE:' + path)
    from phase176_r3r59r3_definitional_suspension_elision_isolated.audit import preflight
    with previous_stage():
        preflight()
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
    print('PHASE176_R3R59R4_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    if args.dry_run:
        print('PHASE176_R3R59R4_GATE=PASS_R3R59R4_DRYRUN')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
