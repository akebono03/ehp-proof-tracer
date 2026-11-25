"""Replace one reviewed rendering branch, preserving all other bytes."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / 'phase168_r3_27_typed_statement_projection.py'
PIN = 'f324c9cfd19a8710daf0bc6c99926b07c6e3b3b5'
COMMON = ROOT / 'toda_conclusion_latex_renderer.py'
COMMON_PIN = 'b73f204b2e187a6873d1650406b7eafeecfda312'
OLD = r'''    if type(statement) is KernelMultipleStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(statement.source_generator)
        if (source is not None and target is not None
                and symbol is not None and generator is not None
                and type(statement.multiple) is int
                and statement.multiple >= 1
                and statement.domain == mapping.source_group):
            return (
                rf"$\ker({symbol}:{source}\to {target})="
                rf"\mathbb{{Z}}\{{{statement.multiple}{generator}\}}$."
            )
        return None
'''
NEW = '''    if type(statement) is KernelMultipleStatement:
        from toda_conclusion_latex_renderer import (
            render_repository_conclusion_latex,
        )
        try:
            latex = render_repository_conclusion_latex(statement)
        except (TypeError, ValueError):
            return None
        return "$" + latex + "$."
'''


def function_node(text):
    nodes = [node for node in ast.parse(text).body
             if isinstance(node, ast.FunctionDef) and node.name == 'typed_sentence']
    if len(nodes) != 1:
        raise ValueError('TYPED_SENTENCE_NOT_UNIQUE')
    return nodes[0]


def updated_source(raw):
    text, eol = normalize(raw)
    if text.count(NEW) == 1 and OLD not in text:
        base = text.replace(NEW, OLD, 1)
    else:
        base = text
    if not pinned(base, PIN) or base.count(OLD) != 1 or NEW in base:
        raise ValueError('UNREVIEWED_PROJECTION_BASELINE')
    node = function_node(base)
    if OLD.rstrip('\n') not in ast.get_source_segment(base, node):
        raise ValueError('KERNEL_BRANCH_OUTSIDE_TYPED_SENTENCE')
    changed = base.replace(OLD, NEW, 1)
    if text not in (base, changed):
        raise ValueError('PARTIAL_OR_MOVED_KERNEL_PATCH')
    actual = ast.get_source_segment(changed, function_node(changed))
    supplied = (PACKAGE / 'typed_sentence_FULL.py.txt').read_text(encoding='utf-8').rstrip('\n')
    if actual != supplied:
        raise ValueError('FULL_FUNCTION_TEMPLATE_MISMATCH')
    return changed.replace('\n', eol).encode('utf-8')


def planned_changes():
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    from phase176_r3r51_verified_db_subgroup_lift.apply import planned_changes as prior_changes
    if any(a != b for a, b in prior_changes().values()):
        raise RuntimeError('R3R51_NOT_APPLIED')
    text, _ = normalize(COMMON.read_bytes())
    if not pinned(text, COMMON_PIN):
        raise RuntimeError('UNREVIEWED_COMMON_RENDERER')
    raw = TARGET.read_bytes()
    return raw, updated_source(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    old, new = planned_changes()
    if not args.dry_run and old != new:
        TARGET.write_bytes(new)
    print('PHASE176_R3R53_HEAD=' + subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())
    print('PHASE176_R3R53_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
