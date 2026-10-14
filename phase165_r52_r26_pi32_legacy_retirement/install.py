"""R26: remove exactly one pi3^2-specialized factory and its two legacy uses."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

NAME = 'toda_pi3_2_free_cyclic_generator_inference_rule'
FILES = ('toda_rules.py', 'toda_upstream_bootstrap.py', 'probes/probe_phase49_capabilities.py')

def retire_source(source: str, path: str) -> tuple[str, int]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    edits = []
    if path == 'toda_rules.py':
        matches = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == NAME]
        if len(matches) != 1:
            raise ValueError(f'{path}: expected exactly one factory definition; found {len(matches)}')
        node = matches[0]
        edits.append((node.lineno - 1, node.end_lineno, ''))
    else:
        imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and any(a.name == NAME for a in n.names)]
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == NAME]
        if len(imports) != 1 or len(calls) != 1:
            raise ValueError(f'{path}: expected one import and one call; got {len(imports)} and {len(calls)}')
        # Existing multiline import lists and rule tuples have the name/call on dedicated lines.
        for n, needle in ((imports[0], NAME + ','), (calls[0], NAME + '(),')):
            candidates = [i for i in range(n.lineno - 1, n.end_lineno) if lines[i].strip() == needle]
            if len(candidates) != 1:
                raise ValueError(f'{path}: not a standalone item: {needle}')
            edits.append((candidates[0], candidates[0]+1, ''))
    for start, end, replacement in sorted(edits, reverse=True):
        lines[start:end] = [replacement] if replacement else []
    new = ''.join(lines)
    ast.parse(new)
    if NAME in new:
        raise ValueError(f'{path}: remaining specialized identifier in active source')
    return new, len(edits)

def install(root: Path) -> dict:
    root = root.resolve()
    planned = {}
    for relative in FILES:
        target = root / relative
        original = target.read_text(encoding='utf-8')
        if NAME not in original:
            # Already installed only when all three files are clean.
            planned[relative] = (original, original, 0)
            continue
        modified, count = retire_source(original, relative)
        planned[relative] = (original, modified, count)
    counts = [planned[p][2] for p in FILES]
    if counts not in ([1,2,2], [0,0,0]):
        raise ValueError(f'Inconsistent repository state: {counts}; no files changed')
    if counts == [1,2,2]:
        for relative, (old, new, _) in planned.items():
            target = root / relative
            backup = target.with_name(target.name + '.phase165_r52_r26_backup')
            if backup.exists():
                raise ValueError(f'Backup already exists: {backup}')
        for relative, (old, new, _) in planned.items():
            target = root / relative
            backup = target.with_name(target.name + '.phase165_r52_r26_backup')
            shutil.copy2(target, backup)
            target.write_text(new, encoding='utf-8', newline='')
    result = {'phase':'165 R52-R26','status':'REMOVED' if counts == [1,2,2] else 'ALREADY_REMOVED','removed_definition_count':counts[0], 'removed_bootstrap_items':counts[1], 'removed_probe_items':counts[2], 'full_pytest_run':False}
    out = Path(__file__).resolve().parent / 'audit_output'
    out.mkdir(exist_ok=True)
    (out/'retirement.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__ == '__main__':
    print(json.dumps(install(Path(__file__).resolve().parent.parent),ensure_ascii=False,indent=2))
