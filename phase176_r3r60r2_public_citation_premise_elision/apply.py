"""Exact reversible function replacements, scoped historical compatibility."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r57r1_public_composite_hopf_display.apply import function_text

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LAYOUT = 'phase171_r20r13_eta_sentence_layout/projection.py'
HISTORY = 'phase176_r3r59r4_public_definitional_suspension_elision'
ISOLATED = 'phase176_r3r60r1_citation_premise_elision_isolated'
PINS = {
    LAYOUT: ('2b82ba6dfe4c34d71d84743dbe46de311d89ec8a', (('format_complete_proof_sentences', 'layout'),)),
    HISTORY + '/apply.py': ('96f66b711b1e6cafbe6f3a07f336204308de4967', (('previous_stage', 'history_context'),)),
    HISTORY + '/tests/test_connection.py': ('32c7abd426e53ed64995121a4e1a8355153261bc', (
        ('test_exact_replacements_and_unknown_bytes', 'history_exact'),
        ('test_prior_stage_is_exact_and_restored', 'history_restore'),
        ('test_actual_public_elision', 'history_public'),)),
    ISOLATED + '/tests/test_projection.py': ('4fb9f604ebc4befb7890ba3002250baf09c0cae5', (('verified', 'isolated_fixture'),)),
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
    """Restore only inverse-verified R59R4-era bytes and disable only R60R2.

    This context is for historical checks; it is never used by production.
    Nested calls before entering the older R59R4 context are safe because
    the R60R2 inverse accepts the exact previous stage as well.
    """
    from phase176_r3r60r1_citation_premise_elision_isolated import projection
    restored = {ROOT / path: previous_source(path, (ROOT / path).read_bytes()) for path in PINS}
    read_bytes = Path.read_bytes

    def read_at_previous_stage(path):
        if path in restored:
            return restored[path]
        return read_bytes(path)

    with patch.object(Path, 'read_bytes', read_at_previous_stage), patch.object(
            projection, 'project_citation_premise_elision',
            lambda markdown, model: (markdown, {})):
        yield


def planned_changes():
    changes = {}
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        changes[path] = (raw, updated_source(path, raw))
    if len({raw == new for raw, new in changes.values()}) != 1:
        raise RuntimeError('PARTIALLY_APPLIED_R60R2')
    for path, pin in {
        ISOLATED + '/projection.py': 'd57075464d3b39a06f31e5be17b86d66a3306bbe',
        ISOLATED + '/audit.py': '5aa520f922c1233f8380d6f0c4bfd458d31be055',
        'phase176_r3r53_common_kernel_renderer/audit.py': '1f6bf584e4b24066937be87f65f3649d54bf1d16',
        'phase176_r3r54_narrative_audit/audit.py': 'df62b1231e905ac66721be3b499644e8f11ba9f2',
    }.items():
        if not pinned(normalize((ROOT / path).read_bytes())[0], pin):
            raise RuntimeError('UNREVIEWED_SOURCE:' + path)
    from phase176_r3r60r1_citation_premise_elision_isolated.audit import preflight
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
    print('PHASE176_R3R60R2_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    if args.dry_run:
        print('PHASE176_R3R60R2_GATE=PASS_R3R60R2_DRYRUN')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
