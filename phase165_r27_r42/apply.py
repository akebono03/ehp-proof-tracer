"""R27-R42: detach Web Execution status from removed repository execution workflow."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = 'web_generator_execution.py'
NEW = 'toda_typed_execution_status.py'
OLD = 'RepositoryGeneratorUserExecutionWorkflowStatus'
NEW_NAME = 'TypedGeneratorExecutionStatus'
MODULE = '''"""Status of a typed generator execution request (not proof certification)."""
from enum import Enum


class TypedGeneratorExecutionStatus(str, Enum):
    NONE = "none"
    AMBIGUOUS = "ambiguous"
    EXECUTED = "executed"
'''


def transform(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    imports = [node for node in tree.body if isinstance(node, ast.ImportFrom) and node.module == 'repository_generator_user_execution_facade']
    if len(imports) > 1:
        raise ValueError('unexpected multiple legacy Execution imports')
    if imports:
        node = imports[0]
        aliases = {a.name for a in node.names}
        if OLD not in aliases:
            raise ValueError('legacy Execution status not found in import')
        # Replacing an active legacy workflow invocation is not a status-only migration.
        if any(a.name != OLD for a in node.names):
            used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
            remaining = [a for a in node.names if a.name != OLD and (a.asname or a.name) in used]
            if remaining:
                raise ValueError('legacy Execution functions still used; refuse incomplete migration')
        lines[node.lineno-1:node.end_lineno] = []
    source = ''.join(lines)
    tree = ast.parse(source)
    # Confirm all references to the old enum are bare names, never strings or attributes.
    names = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == OLD]
    if not names and NEW_NAME not in source:
        raise ValueError('neither legacy nor typed Execution status exists')
    if names:
        offsets = source.splitlines(keepends=True)
        for n in sorted(names, key=lambda n:(n.lineno,n.col_offset), reverse=True):
            line = offsets[n.lineno-1]
            if line[n.col_offset:n.end_col_offset] != OLD:
                raise ValueError('status token position mismatch')
            offsets[n.lineno-1] = line[:n.col_offset] + NEW_NAME + line[n.end_col_offset:]
        source = ''.join(offsets)
    if 'from toda_typed_execution_status import TypedGeneratorExecutionStatus' not in source:
        source = 'from toda_typed_execution_status import TypedGeneratorExecutionStatus\n' + source
    ast.parse(source)
    return source


def install(root: Path = ROOT) -> dict:
    path = root / TARGET
    module_path = root / NEW
    if not path.is_file():
        raise FileNotFoundError(path)
    if module_path.exists() and module_path.read_text(encoding='utf-8-sig') != MODULE:
        raise ValueError('typed status module conflict')
    old = path.read_text(encoding='utf-8-sig')
    new = transform(old)
    changes = {path: new, module_path: MODULE}
    changed = [p for p, text in changes.items() if not p.exists() or p.read_text(encoding='utf-8-sig') != text]
    backup = root / 'phase165_r27_r42_backup'
    for p in changed:
        if p.exists() and (backup/p.name).exists() and (backup/p.name).read_bytes()!=p.read_bytes():
            raise ValueError(f'backup conflict: {p.name}')
    backup.mkdir(exist_ok=True)
    for p in changed:
        if p.exists() and not (backup/p.name).exists():
            shutil.copy2(p,backup/p.name)
        p.write_text(changes[p],encoding='utf-8')
    audit = {'phase':'165 R27-R42','status':'CHANGED' if changed else 'ALREADY_INSTALLED', 'modified_files':[p.name for p in changed], 'old_execution_facade_import_removed': 'from repository_generator_user_execution_facade import' not in new, 'group_calculation_unchanged': True, 'applicability_catalog_unchanged': True, 'full_pytest_run':False}
    (root/'phase165_r27_r42_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(audit,ensure_ascii=False,indent=2))
    return audit

if __name__ == '__main__':
    install()
