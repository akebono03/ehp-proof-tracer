"""Minimal, repeatable installer: insert the existing-evidence provider in shared search."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
MODULE = ROOT / "phase166_r3v_generator_transport.py"
INSERT = '        from phase166_r3v_generator_transport import expand_generator_transport_normalization\n        options.extend(expand_generator_transport_normalization(goal))\n'
ANCHOR = '        options.extend(expand_cited_eta_generator(goal))'


def main():
    source = TARGET.read_text(encoding="utf-8")
    ast.parse(source)
    if INSERT.strip() in source:
        print("ALREADY INSTALLED: no change")
        return
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'shared_expansion_provider']
    if len(matches) != 1:
        raise RuntimeError('shared_expansion_provider not uniquely identified')
    fn = matches[0]
    lines = source.splitlines(keepends=True)
    positions = [i for i in range(fn.lineno-1, fn.end_lineno) if lines[i].rstrip('\r\n') == ANCHOR]
    if len(positions) != 1:
        raise RuntimeError('Expected one eta generator anchor in shared expansion')
    i = positions[0]
    newline = '\r\n' if '\r\n' in lines[i] else '\n'
    updated = ''.join(lines[:i+1]) + INSERT.replace('\n', newline) + ''.join(lines[i+1:])
    ast.parse(updated)
    # Avoid modifying production until source code and all module syntax passes.
    module_code = (PACKAGE/'phase166_r3v_generator_transport.py').read_text(encoding='utf-8')
    ast.parse(module_code)
    folder = PACKAGE/'backups'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder.mkdir(parents=True)
    shutil.copy2(TARGET, folder/TARGET.name)
    if MODULE.exists():
        shutil.copy2(MODULE, folder/MODULE.name)
    MODULE.write_text(module_code, encoding='utf-8')
    TARGET.write_text(updated, encoding='utf-8')
    ast_new = ast.parse(updated)
    changed_fn = next(node for node in ast_new.body if isinstance(node, ast.FunctionDef) and node.name == 'shared_expansion_provider')
    (PACKAGE/'modified_shared_expansion_provider.txt').write_text(ast.get_source_segment(updated,changed_fn)+'\n',encoding='utf-8')
    print('PATCHED:', TARGET, MODULE)
    print('BACKUP:', folder)
    print('FULL FUNCTION:', PACKAGE/'modified_shared_expansion_provider.txt')

if __name__ == '__main__':
    main()
