from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_contribution_renderer.py'
REPLACEMENT = Path(__file__).with_name('modified_function.py').read_text(encoding='utf-8').rstrip() + '\n'
NAME = 'suppress_toda_group_proof_narrative_dangling_connectors'


def main():
    source = TARGET.read_text(encoding='utf-8')
    tree = ast.parse(source)
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == NAME]
    if len(matches) != 1:
        raise RuntimeError('Expected exactly one target function')
    node = matches[0]
    lines = source.splitlines(keepends=True)
    old = ''.join(lines[node.lineno-1:node.end_lineno])
    if 'next_paragraph' not in old or 'standalone_connectors' not in old:
        raise RuntimeError('Unexpected current function implementation; no changes made')
    updated = ''.join(lines[:node.lineno-1]) + REPLACEMENT + ''.join(lines[node.end_lineno:])
    ast.parse(updated)
    backup = TARGET.with_suffix(TARGET.suffix + '.phase162_r7b_before.bak')
    shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding='utf-8')
    print('Updated:', TARGET)
    print('Backup:', backup)


if __name__ == '__main__':
    main()
