from __future__ import annotations
import ast
import shutil
from pathlib import Path

ROOT = Path.cwd()
SOURCE = ROOT / 'web_group_proof.py'
ADAPTER = ROOT / 'phase165_r52_r3_web_adapter.py'
COMMON = ROOT / 'web_group_proof_common.py'
NAMES = ('WebGroupProofStepView', 'WebGroupProofInlineSegmentView', 'WebGroupProofRenderedLineView', 'WebGroupProofView', '_group_proof_rule_name', '_group_proof_statement_latex', '_split_group_proof_rendered_line', '_build_group_proof_inline_segments', '_build_group_proof_rendered_lines')
COMMON_IMPORTS = '''from dataclasses import dataclass
from repository_element_presentation import render_repository_conclusion_latex
from toda_human_readable_renderer import render_toda_public_group_relation_latex
from toda_proof_narrative_renderer import render_toda_proof_statement_latex

'''
ALIAS = '''from web_group_proof_common import (
    WebGroupProofStepView,
    WebGroupProofInlineSegmentView,
    WebGroupProofRenderedLineView,
    WebGroupProofView,
    _group_proof_rule_name,
    _group_proof_statement_latex,
    _split_group_proof_rendered_line,
    _build_group_proof_inline_segments,
    _build_group_proof_rendered_lines,
)

'''

def inspect(text: str):
    tree = ast.parse(text)
    found = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in NAMES}
    if set(found) != set(NAMES):
        raise RuntimeError('Expected shared definitions not found: ' + str(set(NAMES) - set(found)))
    lines = text.splitlines(keepends=True)
    spans = []
    for name in NAMES:
        node = found[name]
        start = min([node.lineno] + [d.lineno for d in node.decorator_list]) if isinstance(node, ast.ClassDef) else node.lineno
        spans.append((start, node.end_lineno, name, ''.join(lines[start-1:node.end_lineno])))
    return sorted(spans)

def main():
    if not SOURCE.is_file() or not ADAPTER.is_file():
        raise RuntimeError('Run from the repository root')
    original = SOURCE.read_text(encoding='utf-8-sig')
    adapter = ADAPTER.read_text(encoding='utf-8-sig')
    if COMMON.exists() and 'from web_group_proof_common import (' in original and 'from web_group_proof_common import (' in adapter:
        print('R27-R10 already installed')
        return
    if COMMON.exists():
        raise RuntimeError('Common module exists but installation state is inconsistent')
    spans = inspect(original)
    if 'from web_group_proof import (' not in adapter:
        raise RuntimeError('Adapter import differs from audited version')
    if 'def build_standard_web_group_proof_view(' not in original:
        raise RuntimeError('Legacy API missing; refuse to change file')
    new_common = COMMON_IMPORTS + '\n\n'.join(part.rstrip() for _, _, _, part in spans) + '\n'
    ast.parse(new_common)
    lines = original.splitlines(keepends=True)
    for start, end, _, _ in reversed(spans):
        del lines[start-1:end]
    # Keep historic module as a compatibility API; it no longer owns common classes.
    new_original = ALIAS + ''.join(lines)
    replacement = adapter.replace('from web_group_proof import (', 'from web_group_proof_common import (', 1)
    for name, value in [('web_group_proof.py', new_original), ('phase165_r52_r3_web_adapter.py', replacement), ('web_group_proof_common.py', new_common)]:
        ast.parse(value, filename=name)
    for path in (SOURCE, ADAPTER):
        backup = path.with_name(path.name + '.phase165_r27_r10_backup')
        if backup.exists():
            raise RuntimeError('Backup exists, refusing to overwrite: ' + str(backup))
    for path in (SOURCE, ADAPTER):
        shutil.copy2(path, path.with_name(path.name + '.phase165_r27_r10_backup'))
    COMMON.write_text(new_common, encoding='utf-8')
    SOURCE.write_text(new_original, encoding='utf-8')
    ADAPTER.write_text(replacement, encoding='utf-8')
    print('R27-R10 installed: shared Web representation isolated; legacy proof builder retained')

if __name__ == '__main__':
    main()
