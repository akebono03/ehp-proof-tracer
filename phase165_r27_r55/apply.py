"""Phase 165 R27-R55: isolate legacy calculation-only imports without changing algorithms."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    'toda_calculation.py': frozenset({
        'repository_foundational_group_specialization',
        'repository_proof_scope',
        'repository_symbolic_sigma_specialization',
        'repository_symbolic_stable_group_specialization',
    }),
    'toda_calculation_report.py': frozenset({'toda_calculation'}),
}


def _future_position(tree: ast.Module) -> int:
    if not tree.body:
        return 0
    first = tree.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return first.end_lineno
    return 0


def transform(source: str, modules: frozenset[str]) -> tuple[str, bool, tuple[str, ...]]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    imports = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module in modules:
            if any(x.asname for x in node.names):
                raise RuntimeError('aliased legacy import: '+node.module)
            imports.append(node)
    if not imports:
        # Idempotence: at least one deferred import must exist, and no eager imports.
        local = any(isinstance(n, ast.ImportFrom) and n.module in modules
                    for top in tree.body if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef))
                    for n in ast.walk(top))
        if not local:
            raise RuntimeError('legacy imports absent but no deferred imports found')
        return source, False, ()
    # Prevent unsafe removal if top-level executable code accesses legacy names.
    symbols = {alias.name for node in imports for alias in node.names}
    functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for node in tree.body:
        if node in imports or node in functions:
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if any(isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load) and x.id in symbols for x in ast.walk(node)):
            raise RuntimeError('legacy symbol used at module scope')
    changes: list[tuple[int,int,str]] = [(node.lineno-1,node.end_lineno,'') for node in imports]
    defer_count = 0
    for fn in functions:
        runtime_ids = {n.id for stmt in fn.body for n in ast.walk(stmt)
                       if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        needed = []
        for node in imports:
            chosen = [n.name for n in node.names if n.name in runtime_ids]
            if chosen:
                # Don't insert duplicate imports into functions already migrated.
                existing = {(n.module, a.name) for n in ast.walk(fn)
                            if isinstance(n, ast.ImportFrom) for a in n.names}
                chosen = [n for n in chosen if (node.module,n) not in existing]
                if chosen:
                    needed.append('from '+node.module+' import '+', '.join(chosen))
        if not needed:
            continue
        first = fn.body[0]
        pos = first.end_lineno if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value,str) else first.lineno-1
        prefix = lines[first.lineno-1][:len(lines[first.lineno-1])-len(lines[first.lineno-1].lstrip())]
        if not prefix:
            raise RuntimeError('unexpected function indentation')
        changes.append((pos,pos,''.join(prefix+n+'\n' for n in needed)))
        defer_count += len(needed)
    if defer_count == 0:
        raise RuntimeError('no executable consumer of old imports was found')
    # Annotation-only uses need deferred evaluation.
    if not any(isinstance(n, ast.ImportFrom) and n.module == '__future__' and any(a.name == 'annotations' for a in n.names) for n in tree.body):
        changes.append((_future_position(tree),_future_position(tree),'from __future__ import annotations\n'))
    # Make edits based on ORIGINAL coordinates, descending. Append empty chunks rather than move other lines.
    for a,b,replacement in sorted(changes,key=lambda x:(x[0], x[1]), reverse=True):
        lines[a:b]=[replacement]
    output=''.join(lines)
    new_tree=ast.parse(output)
    if any(isinstance(n,ast.ImportFrom) and n.module in modules for n in new_tree.body):
        raise RuntimeError('eager import remains')
    return output,True,tuple(sorted({n.module for n in imports}))


def apply(root: Path=ROOT)->dict:
    staged=[]
    for name,modules in TARGETS.items():
        path=root/name
        if not path.is_file():
            raise FileNotFoundError(path)
        original=path.read_text(encoding='utf-8-sig')
        updated,changed,moved=transform(original,modules)
        staged.append((path,original,updated,changed,moved))
    # Check everything before writing anything, including conflicts.
    backup=root/'phase165_r27_r55_backup'
    for path,original,updated,changed,moved in staged:
        if changed and (backup/path.name).exists() and (backup/path.name).read_text(encoding='utf-8') != original:
            raise RuntimeError('backup conflict for '+path.name)
    updated_paths=[]
    for path,original,updated,changed,moved in staged:
        if not changed:
            continue
        backup.mkdir(exist_ok=True)
        if not (backup/path.name).exists():
            shutil.copy2(path,backup/path.name)
        path.write_text(updated,encoding='utf-8',newline='\n')
        updated_paths.append(path.name)
    audit={'phase':'165 R27-R55','status':'CHANGED' if updated_paths else 'ALREADY_INSTALLED',
           'modified_files':updated_paths,'deferred_modules':{p.name:list(m) for p,o,u,c,m in staged},
           'legacy_execution_paths_preserved':True,'old_repository_modules_deleted':[],
           'full_pytest_run':False}
    (root/'phase165_r27_r55_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return audit

if __name__=='__main__':
    print(json.dumps(apply(),ensure_ascii=False,indent=2))
