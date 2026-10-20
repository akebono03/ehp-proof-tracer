"""Install a narrow ordered-lookup change into existing shared search."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r3_recursive_search.py"
START = '            if lookup_mode == "typed_reference_ordered":'
END = '            # A uniquely registered fixed Reference'
REPLACEMENT = '''            # R3-C: one ordered fixed-reference lookup for every existing mode.
            # Deprecated review IDs remain accepted for API compatibility.
            from phase166_r3c_ordered_search.phase166_r3c_ordered_search import (
                ordered_fixed_reference_steps,
            )
            options = list(ordered_fixed_reference_steps(bridge, target, citing_assertion_id))
'''
IMPORT = '''from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import connect_phase163_publication_order\n'''
ANCHOR = '    bridge.registry.assertion(citing_assertion_id)\n'
INJECT = '''    # Reuse the Phase 163 ranks already attached by R3-B; never renumber.
    # A detached copy leaves the caller's registry untouched.
    bridge, _publication_binding = connect_phase163_publication_order(bridge)
'''


def install() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(f"missing current production search: {TARGET}")
    if not (ROOT / 'phase166_r3b_publication_order_binding' / 'phase166_r3b_publication_order_binding.py').is_file():
        raise FileNotFoundError('R3-B binding module not installed')
    original = TARGET.read_text(encoding='utf-8-sig')
    if 'R3-C: one ordered fixed-reference lookup' in original:
        print('ALREADY_INSTALLED: Phase 166 R3-C')
        return
    if original.count(START) != 1 or original.count(END) != 1:
        raise RuntimeError('unexpected shared-search structure; no changes made')
    a = original.index(START)
    b = original.index(END, a)
    section = original[a:b]
    for required in ('ordered_typed_reference_steps', 'find_eligible_goal_candidates', '_typed_reference_steps'):
        if required not in section:
            raise RuntimeError(f'expected current lookup path missing: {required}')
    if original.count(ANCHOR) != 1:
        raise RuntimeError('unexpected citing assertion entry; no changes made')
    if IMPORT in original:
        raise RuntimeError('unexpected preexisting R3-B import')
    adjusted = original[:a] + REPLACEMENT + original[b:]
    adjusted = adjusted.replace(ANCHOR, ANCHOR + INJECT, 1)
    header = 'from unified_statement_registry import AssertionOrigin\n'
    if header not in adjusted:
        raise RuntimeError('expected existing import not found')
    adjusted = adjusted.replace(header, header + IMPORT, 1)
    ast.parse(adjusted)
    backup_dir = ROOT / 'phase166_r3c_ordered_search' / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / (TARGET.name + '.' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.bak')
    shutil.copy2(TARGET, backup)
    TARGET.write_text(adjusted, encoding='utf-8')
    print('PATCHED:', TARGET)
    print('BACKUP:', backup)
    # Record complete actual source, including whole functions and import section.
    (ROOT / 'phase166_r3c_ordered_search' / 'INSTALLED_SOURCE.py.txt').write_text(adjusted, encoding='utf-8')


if __name__ == '__main__':
    install()
