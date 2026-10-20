"""Phase 166 R3-O: guarded migration of established order coordinates."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
BACKUP = ROOT / 'phase166_r3o_order_spacing_backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
FILES = (
    'phase163_r4_r94_output/manifest.json',
    'phase166_r3b_publication_order_binding/phase166_r3b_publication_order_binding.py',
    'phase165_r52_r9_shared_math.py',
)


def replace_exact(text: str, old: str, new: str, filename: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f'Unsafe patch: expected exactly one replacement in {filename}: {old!r}, found {text.count(old)}')
    return text.replace(old, new, 1)


def create_changes() -> dict[str, bytes]:
    inputs = {name: (ROOT / name).read_bytes() for name in FILES}
    manuscript = json.loads(inputs[FILES[0]].decode('utf-8-sig'))
    if manuscript.get('phase') != '163 R4-R94' or manuscript.get('reference_count') != 108 or manuscript.get('assertion_count') != 117:
        raise RuntimeError('Manifest contract changed')
    rows = manuscript.get('assertions')
    if not isinstance(rows, list) or len(rows) != 117:
        raise RuntimeError('Unexpected manifest rows')
    reference_pos = {}
    for row in rows:
        name = row['reference_id']
        pos = row['publication_position']
        if not isinstance(pos, int) or isinstance(pos, bool):
            raise RuntimeError('Invalid publication position')
        if name in reference_pos and reference_pos[name] != pos:
            raise RuntimeError('Inconsistent manifest ordering')
        reference_pos[name] = pos
    existing = sorted(reference_pos.values())
    if existing == list(range(100, 10900, 100)):
        raise RuntimeError('Manifest already migrated; no second scaling permitted')
    if existing != list(range(1, 109)):
        raise RuntimeError('Old manifest must be consecutively ordered 1..108')
    for row in rows:
        row['publication_position'] *= 100
        if row.get('component_position') is not None:
            row['component_position'] *= 100
    migrated = (json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

    order_path = FILES[1]
    order_src = inputs[order_path].decode('utf-8')
    old_check = 'sorted(positions.values()) != list(range(1, 109))'
    new_check = 'sorted(positions.values()) != list(range(100, 10900, 100))'
    order_src = replace_exact(order_src, old_check, new_check, order_path)
    ast.parse(order_src)

    shared_path = FILES[2]
    shared_src = inputs[shared_path].decode('utf-8')
    # Preserve R3-L/R3-N additions; modify only the AssertionEntry copy argument.
    tree = ast.parse(shared_src)
    fn = next((item for item in tree.body if isinstance(item, ast.FunctionDef)
               and item.name == 'build_shared_typed_bridge'), None)
    if fn is None:
        raise RuntimeError('build_shared_typed_bridge not found')
    lines = shared_src.splitlines(keepends=True)
    body = ''.join(lines[fn.lineno - 1:fn.end_lineno])
    needle = '                dependencies=tuple(prefix + dep for dep in assertion.dependencies),'
    if body.count(needle) != 1:
        raise RuntimeError('Cannot identify unique assertion copy; no files modified')
    if 'component_position=(' in body:
        raise RuntimeError('Component rank migration already present; no files modified')
    replacement = ( '                component_position=(\n'
        '                    assertion.component_position * 100\n'
        '                    if assertion.component_position is not None\n'
        '                    and assertion.component_position < 100\n'
        '                    else assertion.component_position\n'
        '                ),\n' ).replace('\\n','\n') + needle
    updated = body.replace(needle, replacement, 1)
    shared_src = ''.join(lines[:fn.lineno - 1]) + updated + ''.join(lines[fn.end_lineno:])
    ast.parse(shared_src)
    return {FILES[0]: migrated, order_path: order_src.encode(), shared_path: shared_src.encode()}


def main() -> None:
    patch = create_changes()  # Validate everything before making changes.
    BACKUP.mkdir(parents=True, exist_ok=False)
    for name in FILES:
        p = ROOT / name
        dest = BACKUP / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
    for name, data in patch.items():
        (ROOT / name).write_bytes(data)
        print('PATCHED:', name)
    print('BACKUP:', BACKUP)
    print('FULL MODIFIED FUNCTION: phase165_r52_r9_shared_math.py build_shared_typed_bridge')
    tree = ast.parse((ROOT / FILES[2]).read_text(encoding='utf-8'))
    code = (ROOT / FILES[2]).read_text(encoding='utf-8')
    for item in tree.body:
        if isinstance(item, ast.FunctionDef) and item.name == 'build_shared_typed_bridge':
            print('\n'.join(code.splitlines()[item.lineno-1:item.end_lineno]))
            break
    print('FULL MODIFIED FUNCTION: phase166_r3b_publication_order_binding.py _load_manifest_reference_order')
    code = (ROOT / FILES[1]).read_text(encoding='utf-8')
    for item in ast.parse(code).body:
        if isinstance(item, ast.FunctionDef) and item.name == '_load_manifest_reference_order':
            print('\n'.join(code.splitlines()[item.lineno-1:item.end_lineno]))
            break


if __name__ == '__main__':
    main()
