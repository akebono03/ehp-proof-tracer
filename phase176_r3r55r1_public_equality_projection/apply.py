"""Connect the reviewed R55 shadow insertion without changing its conditions."""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r55_equality_display_isolated import audit as isolated
from phase176_r3r54_narrative_audit import audit as baseline

ROOT = Path(__file__).resolve().parents[1]
TARGET = isolated.RENDERER
PACKAGE = Path(__file__).resolve().parent.name
PIN = isolated.PINS[TARGET.name]
ANCHOR = isolated.ANCHOR
INSERT = '''    if not incomplete:
        protected_equalities = set()
        if order_summary is not None:
            protected_equalities.update(order)
        if direct_sum_display is not None:
            protected_equalities.add(direct_sum_display.root_index)
        if stable_chain_display is not None:
            protected_equalities.add(stable_chain_display.root_index)
        if hopf_display is not None:
            protected_equalities.update((hopf_display.formula_index, hopf_display.image_index))
        from phase176_r3r55_equality_display_isolated.projection import (
            project_redundant_equalities,
        )
        suppressed_body_indices.update(project_redundant_equalities(
            model, order, suppressed_body_indices, protected_equalities,
        ))
'''
LOCAL_PINS = {
    'phase176_r3r55_equality_display_isolated/projection.py': 'ccb485948201d188caaa970cb3e575df1c6f96c588b89577a4d6a187ee0cd948',
    'phase176_r3r55_equality_display_isolated/audit.py': '6bf2fcf275b40bc9dc478215d4046996fc0ac915d9afe3904889d4f3f43ab04c',
}


def function_node(source):
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef)
             and node.name == 'render_model_backed_narrative_markdown']
    if len(nodes) != 1:
        raise ValueError('RENDER_FUNCTION_NOT_UNIQUE')
    return nodes[0]


def baseline_source(raw):
    source, eol = normalize(raw)
    if source.count(INSERT + ANCHOR) == 1:
        base = source.replace(INSERT + ANCHOR, ANCHOR, 1)
    else:
        base = source
    if not pinned(base, PIN) or base.count(ANCHOR) != 1 or INSERT in base:
        raise ValueError('UNREVIEWED_RENDERER_BASELINE')
    changed = base.replace(ANCHOR, INSERT + ANCHOR, 1)
    if source not in (base, changed):
        raise ValueError('PARTIAL_OR_MOVED_PUBLIC_CONNECTION')
    if INSERT.rstrip() not in ast.get_source_segment(changed, function_node(changed)):
        raise ValueError('CONNECTION_OUTSIDE_RENDER_FUNCTION')
    # The tested shadow block and public block differ only by the local import
    # and the observer's name. The production projection is the same callable.
    local_import = '''        from phase176_r3r55_equality_display_isolated.projection import (
            project_redundant_equalities,
        )
'''
    if INSERT.replace(local_import, '').replace('project_redundant_equalities(', '_r55_observe_projection(') != isolated.INSERT:
        raise ValueError('SHADOW_AND_PUBLIC_INSERTIONS_DIFFER')
    return base, eol


def updated_source(raw):
    base, eol = baseline_source(raw)
    return base.replace(ANCHOR, INSERT + ANCHOR, 1).replace('\n', eol).encode('utf-8')


def check_dependencies():
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    for path, sha in {**baseline.prior.PINS, **baseline.PINS, **isolated.PINS}.items():
        if path == TARGET.name:
            continue
        text, _ = normalize((ROOT / path).read_bytes())
        if not pinned(text, sha):
            raise RuntimeError('UNREVIEWED_DEPENDENCY:' + path)
    for path, sha in LOCAL_PINS.items():
        source, _ = normalize((ROOT / path).read_bytes())
        if hashlib.sha256(source.encode('utf-8')).hexdigest() != sha:
            raise RuntimeError('UNREVIEWED_R55_PACKAGE:' + path)
    from phase176_r3r53r1_historical_kernel_test.apply import planned_changes
    old, new = planned_changes()
    if old != new:
        raise RuntimeError('R3R53R1_NOT_APPLIED')


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    check_dependencies()
    old = TARGET.read_bytes()
    new = updated_source(old)
    base, _ = baseline_source(old)
    changed, _ = normalize(new)
    folder = artifact_folder()
    (folder / 'render_model_backed_narrative_markdown_FULL.py.txt').write_text(
        ast.get_source_segment(changed, function_node(changed)) + '\n', encoding='utf-8')
    (folder / 'renderer_before.py.txt').write_text(base, encoding='utf-8')
    if not args.dry_run and old != new:
        if TARGET.read_bytes() != old:
            raise RuntimeError('RENDERER_CHANGED_DURING_PREFLIGHT')
        TARGET.write_bytes(new)
    print('PHASE176_R3R55R1_HEAD=' + subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())
    print('PHASE176_R3R55R1_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    print('ARTIFACTS=' + str(folder))
    if args.dry_run:
        print('PHASE176_R3R55R1_GATE=PASS_R3R55R1_DRYRUN')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
