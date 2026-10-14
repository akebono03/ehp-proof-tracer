from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
CATALOG = ROOT / 'standard_production_applicability_catalog.py'
REMOVABLE = ('standard_production_repository.py', 'toda_prop515_upper_bootstrap.py')
OLD_MODULE = 'standard_production_repository'
OLD_FUNCTION = 'build_standard_production_proof_repository'
CATALOG_FUNCTION = 'build_standard_production_applicability_catalog'
RETIRE_MESSAGE = 'Legacy production applicability catalog is retired in Phase 165 R27-R26; use the unified statement registry and common typed Backward Search.'

def _imports(tree: ast.AST, module: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            return True
        if isinstance(node, ast.Import) and any(item.name == module for item in node.names):
            return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == '__import__' and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == module:
            return True
    return False

def transform_catalog(source: str) -> str:
    tree = ast.parse(source)
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == CATALOG_FUNCTION]
    imports = [node for node in tree.body if isinstance(node, ast.ImportFrom) and node.module == OLD_MODULE]
    if len(imports) > 1 or (imports and {a.name for a in imports[0].names} != {OLD_FUNCTION}):
        raise RuntimeError('Unexpected legacy builder import in catalog')
    old_call_owners = []
    for function in funcs:
        if any(isinstance(node, ast.Name) and node.id == OLD_FUNCTION for node in ast.walk(function)):
            old_call_owners.append(function)
    if len(old_call_owners) > 1:
        raise RuntimeError('Multiple definitions directly reference legacy builder')
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == OLD_FUNCTION:
            if not any(owner.lineno <= node.lineno <= owner.end_lineno for owner in old_call_owners):
                raise RuntimeError('Legacy builder referenced outside standard catalog entry')
    if not funcs:
        if imports:
            raise RuntimeError('Catalog function absent but legacy builder import remains; manual inspection required')
        return source
    newline = '\r\n' if '\r\n' in source else '\n'
    replacement = (
        'def build_standard_production_applicability_catalog(\n'
        ') -> InferenceRuleCatalog:\n'
        '  raise RuntimeError(\n'
        '    "Legacy production applicability catalog is retired in Phase 165 R27-R26; "\n'
        '    "use the unified statement registry and common typed Backward Search."\n'
        '  )\n'
    )
    changes = []
    # Previous definitions may be captured by old classifier decorators/aliases.
    # Disable the original builder as well as the final effective public entry.
    for fn in {id(f): f for f in (old_call_owners + [funcs[-1]])}.values():
        current = ast.get_source_segment(source, fn) or ''
        if ast.dump(fn, include_attributes=False) != ast.dump(ast.parse(replacement).body[0], include_attributes=False):
            changes.append((fn.lineno-1, fn.end_lineno, replacement))
    changes.extend((node.lineno-1, node.end_lineno, '') for node in imports)
    lines = source.splitlines(keepends=True)
    for start, end, text in sorted(changes, reverse=True):
        lines[start:end] = [text.replace('\n', newline)] if text else []
    result = ''.join(lines)
    parsed = ast.parse(result)
    if _imports(parsed, OLD_MODULE) or any(isinstance(n, ast.Name) and n.id == OLD_FUNCTION for n in ast.walk(parsed)):
        raise RuntimeError('Catalog still references legacy builder')
    return result

def blocking_imports(after_catalog: str) -> list[str]:
    blocks=[]
    for path in ROOT.glob('*.py'):
        if path.name in REMOVABLE or path.name == 'standard_production_applicability_catalog.py':
            continue
        if '.phase' in path.name or '.backup' in path.name or path.name.startswith('test_') or path.name.startswith('audit_'):
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        except (UnicodeError, SyntaxError):
            blocks.append(f'{path.name}: unreadable/invalid source')
            continue
        for module in ('standard_production_repository','toda_prop515_upper_bootstrap'):
            if _imports(tree,module):
                blocks.append(f'{path.name}: imports {module}')
    if _imports(ast.parse(after_catalog),OLD_MODULE):
        blocks.append('standard_production_applicability_catalog.py: still imports builder')
    return blocks

def apply() -> dict:
    source = CATALOG.read_text(encoding='utf-8-sig')
    updated = transform_catalog(source)
    blocking = blocking_imports(updated)
    report = dict(phase='165 R27-R26',blocked=blocking,removed_files=[],catalog_modified=False,full_pytest_run=False)
    if blocking:
        (HERE/'audit_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False,indent=2))
        raise RuntimeError('Production imports remain; NO FILES MODIFIED')
    backup = HERE / 'removed_files_backup'
    backup.mkdir(exist_ok=True)
    originals = {}
    for filename in REMOVABLE:
        path=ROOT/filename
        if path.exists():
            originals[path]=path.read_bytes()
    if source != updated:
        originals[CATALOG]=CATALOG.read_bytes()
    for path,data in originals.items():
        target=backup/path.name
        if not target.exists():
            target.write_bytes(data)
    if source != updated:
        CATALOG.write_text(updated,encoding='utf-8',newline='')
        report['catalog_modified']=True
    for filename in REMOVABLE:
        path=ROOT/filename
        if path.exists():
            path.unlink()
            report['removed_files'].append(filename)
    (HERE/'audit_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__ == '__main__':
    apply()
