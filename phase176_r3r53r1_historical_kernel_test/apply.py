"""Update only the exact reviewed historical test; never rewrite a renderer."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r53_common_kernel_renderer.apply import planned_changes as prior_changes

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / 'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py'
PIN = '0252703a8fd4f180af44993aa6a5b68619c59a45'
OLD = r'''def test_pi43_existing_typed_output_maintained():
    text = _render(3, 1)
    assert "準同型定理" in text
    assert r"\ker E=\mathbb{Z}\{2\eta_{2}\}" in text
    assert text.count("次の完全列を考える") == 1
'''
NEW = (PACKAGE / 'test_function_FULL.py.txt').read_text(encoding='utf-8')


def updated_source(raw):
    source, eol = normalize(raw)
    base = source.replace(NEW, OLD, 1) if source.count(NEW) == 1 else source
    if not pinned(base, PIN) or base.count(OLD) != 1:
        raise ValueError('UNREVIEWED_HISTORICAL_TEST')
    changed = base.replace(OLD, NEW, 1)
    if source not in (base, changed):
        raise ValueError('PARTIAL_HISTORICAL_TEST_PATCH')
    nodes = [node for node in ast.parse(changed).body if isinstance(node, ast.FunctionDef)
             and node.name == 'test_pi43_existing_typed_output_maintained']
    if len(nodes) != 1 or ast.get_source_segment(changed, nodes[0]) != NEW.rstrip('\n'):
        raise ValueError('TEST_FUNCTION_TEMPLATE_MISMATCH')
    return changed.replace('\n', eol).encode('utf-8')


def planned_changes():
    old, new = prior_changes()
    if old != new:
        raise RuntimeError('R3R53_RENDERER_NOT_APPLIED')
    raw = TARGET.read_bytes()
    return raw, updated_source(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    old, new = planned_changes()
    if not args.dry_run:
        # Refuse to update a historical assertion unless the real proof and
        # both projections were inspected successfully in this process.
        from phase176_r3r53r1_historical_kernel_test.audit import observe
        observe()
        if TARGET.read_bytes() != old:
            raise RuntimeError('HISTORICAL_TEST_CHANGED_DURING_AUDIT')
        if old != new:
            TARGET.write_bytes(new)
    print('PHASE176_R3R53R1_HEAD=' + subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip())
    print('PHASE176_R3R53R1_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
