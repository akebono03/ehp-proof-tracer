"""Install the minimal R3-C repair on the current project, preserving a backup."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
PACKAGE = ROOT / 'phase166_r3b_publication_order_binding'
INIT = PACKAGE / '__init__.py'


def install() -> None:
    if not (PACKAGE / 'phase166_r3b_publication_order_binding.py').is_file():
        raise FileNotFoundError('Phase 166 R3-B module missing')
    if not INIT.is_file():
        raise FileNotFoundError('Phase 166 R3-C import fix missing (__init__.py)')
    original = TARGET.read_text(encoding='utf-8-sig')
    tree = ast.parse(original)
    method = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'build_shared_typed_bridge')
    source = ast.get_source_segment(original, method)
    marker = '        prefix = f"shared:{index}:"'
    injected = '''        # R3-C: reuse Phase 163 positions on original reference IDs before\n        # shared: index namespacing. No locator or synthetic rank matching.\n        from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (\n            connect_phase163_publication_order,\n        )\n        source, _publication_binding = connect_phase163_publication_order(source)\n'''
    if injected.strip() in original:
        print('ALREADY INSTALLED')
        return
    if source.count(marker) != 1:
        raise RuntimeError('Current build_shared_typed_bridge layout changed')
    updated = original.replace(marker, injected + marker, 1)
    # Crucial: an inferred context ID is NOT a genuine citation target. The
    # existing public proof path is retained; callers supplying an explicit
    # target may separately select the ordered mode in a later integration.
    ast.parse(updated)
    backup_dir = ROOT / 'phase166_r3c_reimplementation' / 'backups'
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = backup_dir / f'phase165_r52_r9_shared_math.{stamp}.bak'
    shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding='utf-8')
    (ROOT / 'phase166_r3c_reimplementation' / 'INSTALLED_SOURCE.py.txt').write_text(updated, encoding='utf-8')
    print('PATCHED:', TARGET)
    print('BACKUP:', backup)
    print('Ordered metadata connected before shared prefixing; public proof search unchanged')


if __name__ == '__main__':
    install()
