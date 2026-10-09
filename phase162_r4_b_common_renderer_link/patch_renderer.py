"""Safely install the R4-B common-renderer hook into the current source.

The original public stable branch is retained. Only the existing baseline
function is replaced with its full implementation plus the narrow hook.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'toda_group_proof_narrative_renderer.py'
IMPORT_LINE = 'from toda_group_proof_narrative_transport_link import (\n  add_transport_link_to_common_markdown,\n)\n'
HOOK = '''    public_rendered = (
      add_transport_link_to_common_markdown(
        presentation.root_step,
        public_rendered,
        _render_group_proof_narrative_latex,
      )
    )

'''
TARGET = '''    return (
      _finalize_toda_group_proof_narrative_markdown(
        public_rendered
      )
    )'''


def main():
    src = SOURCE.read_text(encoding='utf-8-sig')
    tree = ast.parse(src)
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == '_phase158_baseline_render_toda_group_proof_narrative_markdown']
    if len(funcs) != 1:
        raise RuntimeError('Expected exactly one baseline function; no files changed')
    lines = src.splitlines(keepends=True)
    original = ''.join(lines[funcs[0].lineno - 1:funcs[0].end_lineno])
    if 'add_transport_link_to_common_markdown(' in original:
        print('Already installed; unchanged')
        return
    if original.count(TARGET) != 1:
        raise RuntimeError('Baseline return signature changed; no files changed')
    replacement = original.replace(TARGET, HOOK + TARGET)
    src_new = src.replace(original, replacement, 1)
    if IMPORT_LINE not in src_new:
        anchor = 'import re\n'
        if anchor not in src_new:
            raise RuntimeError('Import anchor missing; no files changed')
        src_new = src_new.replace(anchor, anchor + IMPORT_LINE, 1)
    ast.parse(src_new)
    backup = SOURCE.with_name(SOURCE.stem + '.phase162_r4_b_prelink.bak')
    if not backup.exists():
        backup.write_text(src, encoding='utf-8')
    SOURCE.write_text(src_new, encoding='utf-8')
    print('Updated:', SOURCE.name)
    print('Backup:', backup.name)


if __name__ == '__main__':
    main()
