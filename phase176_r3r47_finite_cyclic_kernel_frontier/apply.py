"""Pin and extend the common conclusion renderer, not mathematical inference."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / 'toda_conclusion_latex_renderer.py'
PINS = {
    'toda_conclusion_latex_renderer.py': '8f8b30043fab1cdc207d5d9afbbe332290620ccf',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py': 'fac88c852cd4c18e8d013e3dc12ab95ad57d7b03',
    'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/rule.py': 'adc68818539ddb5975d86b8ce4517107cfb9db78',
    'phase176_r3r44_public_subgroup_lift/provider.py': '551e9105cd35c8df9159cf8027839e7a890d0d81',
}
ANCHOR = '''    """Render established Relation, membership and Expression forms unchanged."""
'''
INSERT = '''    # Render subgroup generation, not an assertion of infinite cyclic order.
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase168_r3_27_typed_statement_projection import (
        element_tex, group_tex, map_symbol_tex,
    )
    if type(conclusion) is KernelMultipleStatement:
        mapping = conclusion.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(conclusion.source_generator)
        if (source is not None and target is not None and symbol is not None
                and generator is not None and type(conclusion.multiple) is int
                and conclusion.multiple >= 1
                and conclusion.domain == mapping.source_group):
            return (rf"\\ker({symbol}:{source}\\to {target})="
                    rf"\\langle {conclusion.multiple}{generator}\\rangle")
        raise TypeError("unsupported typed kernel multiple for LaTeX rendering")
'''


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def normalize(raw):
    lf = raw.replace(b'\r\n', b'\n')
    if b'\r' in lf or (b'\r\n' in raw and raw != lf.replace(b'\n', b'\r\n')):
        raise ValueError('MIXED_LINE_ENDINGS')
    return lf.decode('utf-8'), '\r\n' if b'\r\n' in raw else '\n'


def pinned(text, expected):
    return expected in (blob(text.encode('utf-8')), blob(text.replace('\n', '\r\n').encode('utf-8')))


def updated_source(raw):
    source, eol = normalize(raw)
    baseline = source.replace(ANCHOR + INSERT, ANCHOR, 1)
    if not pinned(baseline, PINS['toda_conclusion_latex_renderer.py']):
        raise ValueError('UNREVIEWED_RENDERER_BASELINE')
    if baseline.count(ANCHOR) != 1:
        raise ValueError('RENDERER_ANCHOR_NOT_UNIQUE')
    changed = baseline.replace(ANCHOR, ANCHOR + INSERT, 1)
    if source not in (baseline, changed):
        raise ValueError('PARTIAL_OR_MOVED_PATCH')
    ast.parse(changed)
    return changed.replace('\n', eol).encode('utf-8')


def preflight():
    if subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip() != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    for path, sha in PINS.items():
        if ROOT / path == TARGET:
            continue
        source, _ = normalize((ROOT / path).read_bytes())
        if not pinned(source, sha):
            raise RuntimeError('UNREVIEWED_DEPENDENCY:' + path)
    # R46R1 must already be installed; no clean-tree requirement for its local edits.
    from phase176_r3r46r1_prior_group_availability.apply import planned_changes
    if any(old != new for old, new in planned_changes().values()):
        raise RuntimeError('R3R46R1_NOT_APPLIED')
    old = TARGET.read_bytes()
    return old, updated_source(old)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    old, new = preflight()
    if not args.dry_run:
        if old != new:
            TARGET.write_bytes(new)
        source, _ = normalize(new)
        tree = ast.parse(source)
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'render_repository_conclusion_latex')
        function = '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
        (PACKAGE / 'SHARED_FUNCTION_FULL_JA.md').write_text(
            '# 変更後の共通表示関数全文\n\n```python\n' + function + '\n```\n', encoding='utf-8')
    print('PHASE176_R3R47_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
