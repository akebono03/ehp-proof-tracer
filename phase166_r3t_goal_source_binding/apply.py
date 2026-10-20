"""Conservative AST-guarded replacement of one function and one import."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r55_nk_only_goal.py"
PKG = Path(__file__).resolve().parent


def main() -> None:
    original = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(original)
    names = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == "search_group_from_registered_goal"]
    if len(names) != 1:
        raise RuntimeError("Expected exactly one search_group_from_registered_goal function")
    node = names[0]
    old = '\n'.join(original.splitlines()[node.lineno - 1:node.end_lineno])
    call = '''    result = search_shared_group_goal(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
    )'''
    if old.count(call) != 1:
        raise RuntimeError("Current target call differs; refusing to modify")
    new_call = '''    citing_id = resolve_specialized_goal_citing_id(bridge, candidate)
    search_kwargs = dict(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
    )
    if citing_id is not None:
        search_kwargs["citing_assertion_id"] = citing_id
    result = search_shared_group_goal(**search_kwargs)'''
    amended = old.replace(call, new_call)
    helper_import = 'from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id\n'
    anchor = 'from unified_statement_registry import AssertionOrigin\n'
    if original.count(anchor) != 1:
        raise RuntimeError("Unexpected import layout")
    lines = original.splitlines(keepends=True)
    ending = '\r\n' if '\r\n' in original else '\n'
    patch_lines = amended.splitlines(keepends=True)
    out = ''.join(lines[:node.lineno-1]) + ending.join(amended.splitlines()) + ending + ''.join(lines[node.end_lineno:])
    out = out.replace(anchor, anchor + helper_import, 1)
    ast.parse(out)
    backup = PKG / "backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(TARGET, backup / TARGET.name)
    TARGET.write_text(out, encoding="utf-8")
    (PKG / 'modified_function.txt').write_text(amended + '\n', encoding='utf-8')
    print('PATCHED:', TARGET)
    print('BACKUP:', backup)
    print('FULL FUNCTION:', PKG / 'modified_function.txt')


if __name__ == '__main__':
    main()
