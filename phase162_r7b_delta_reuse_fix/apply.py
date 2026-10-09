from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_contribution_renderer.py'
BACKUP = ROOT / 'toda_group_proof_narrative_contribution_renderer.py.phase162_r7b_delta_reuse_before.bak'

OLD = '''    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]'''
NEW = '''    if not matches:
      return None

    return matches[
      0
    ]'''


def find_function(source: str) -> tuple[int, int, str]:
    tree = ast.parse(source)
    candidates = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'insert_toda_group_proof_narrative_map_property_dependencies']
    if len(candidates) != 1:
        raise RuntimeError('Target function must exist exactly once')
    node = candidates[0]
    lines = source.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:node.lineno - 1])
    end = sum(len(line) for line in lines[:node.end_lineno])
    return start, end, source[start:end]


def main() -> None:
    source = TARGET.read_text(encoding='utf-8')
    start, end, function = find_function(source)
    if OLD in function:
        modified = function.replace(OLD, NEW)
        if modified == function or modified.count(NEW) != 1:
            raise RuntimeError('Unsafe replacement')
        changed = source[:start] + modified + source[end:]
        ast.parse(changed)
        if not BACKUP.exists():
            BACKUP.write_text(source, encoding='utf-8')
        TARGET.write_text(changed, encoding='utf-8')
        print('Updated:', TARGET)
        print('Backup:', BACKUP)
        function = modified
    elif NEW in function:
        print('Already applied:', TARGET)
    else:
        raise RuntimeError('Current source does not match reviewed function; no changes performed')
    # A complete, immediately replaceable copy of the modified function.
    (Path(__file__).parent / 'modified_function.py').write_text(function.rstrip() + '\n', encoding='utf-8')
    print('Full replacement function:', Path(__file__).parent / 'modified_function.py')


if __name__ == '__main__':
    main()
