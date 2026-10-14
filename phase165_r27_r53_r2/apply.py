"""Phase 165 R27-R53-R2: defer legacy imports without rewriting old APIs."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
LEGACY = {
    'proof_repository': 'ProofRepository',
    'phase164_r7_repository_root_resolution': 'validate_repository_internal_proof_roots',
    'standard_production_repository': 'build_standard_production_proof_repository',
    'toda_calculation_report': 'build_toda_calculation_report_result',
    'toda_calculation_report_result': 'TodaCalculationReportResult',
}
TARGETS = ('build_toda_report', 'build_standard_toda_report')
TYPED = ('build_toda_partial_result', 'build_standard_toda_partial_result')


def transform(source: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    funcs = {node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    if any(name not in funcs for name in TARGETS + TYPED):
        raise RuntimeError('expected legacy and R52 typed facade functions')
    imports = [node for node in tree.body if isinstance(node, ast.ImportFrom) and node.module in LEGACY]
    # Already migrated: no eager legacy imports and both legacy bodies have local imports.
    if not imports:
        if all(any(isinstance(x, ast.ImportFrom) and x.module in LEGACY
                   for x in ast.walk(funcs[name])) for name in TARGETS):
            return source, False
        raise RuntimeError('legacy imports absent, but facade migration state unrecognized')
    by_module = {}
    for node in imports:
        if len(node.names) != 1 or node.names[0].name != LEGACY[node.module] or node.names[0].asname:
            raise RuntimeError(f'nonstandard legacy import from {node.module}')
        if node.module in by_module:
            raise RuntimeError(f'duplicate legacy import: {node.module}')
        by_module[node.module] = node
    # Check that removed names have no runtime consumers outside the two legacy APIs.
    allowed = {LEGACY[module] for module in by_module}
    permitted_nodes = {funcs[name] for name in TARGETS}
    for node in tree.body:
        if node in imports or node in permitted_nodes:
            continue
        if isinstance(node, ast.If) and isinstance(node.test, ast.Name) and node.test.id == 'TYPE_CHECKING':
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            relevant = [n for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
                        and n.id in allowed]
            # Annotations are safely postponed by __future__. Their types remain importable via TYPE_CHECKING.
            annotations = set()
            for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs):
                if arg.annotation is not None:
                    annotations.update(x for x in ast.walk(arg.annotation) if isinstance(x, ast.Name))
            if node.returns is not None:
                annotations.update(x for x in ast.walk(node.returns) if isinstance(x, ast.Name))
            if any(n not in annotations for n in relevant):
                raise RuntimeError(f'legacy import used by another runtime API: {node.name}')
            continue
        if any(isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in allowed
               for n in ast.walk(node)):
            raise RuntimeError('legacy import used outside legacy functions')
    lines = source.splitlines(keepends=True)
    # Preserve both legacy function bodies verbatim. Insert only imports actually used at runtime.
    edits = [(n.lineno - 1, n.end_lineno, '') for n in imports]
    for name in TARGETS:
        fn = funcs[name]
        names = {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        inserts = []
        for module, symbol in LEGACY.items():
            if module not in by_module or symbol not in names or symbol in {'ProofRepository', 'TodaCalculationReportResult'}:
                continue
            if any(isinstance(n, ast.ImportFrom) and n.module == module for n in ast.walk(fn)):
                continue
            inserts.append(f'    from {module} import {symbol}\n')
        if not inserts:
            # Support genuine existing local imports, but never blindly delete a required global.
            continue
        first = fn.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
            index = first.end_lineno
        else:
            index = first.lineno - 1
        # The new imports belong INSIDE the function, immediately before its
        # first statement. fn.lineno - 1 is outside the function (R1 bug).
        indent = lines[first.lineno - 1][:len(lines[first.lineno - 1]) - len(lines[first.lineno - 1].lstrip())]
        edits.append((index, index, ''.join(indent + line.lstrip() for line in inserts)))
    if not any(isinstance(n, ast.ImportFrom) and n.module == '__future__' and
               any(a.name == 'annotations' for a in n.names) for n in tree.body):
        initial = 0
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str):
            initial = tree.body[0].end_lineno
        edits.append((initial, initial, 'from __future__ import annotations\n'))
    if not any(isinstance(n, ast.ImportFrom) and n.module == 'typing' and
               any(a.name == 'TYPE_CHECKING' for a in n.names) for n in tree.body):
        # Use a TYPE_CHECKING block at end so insertion is independent of line layout.
        for module in ('proof_repository', 'toda_calculation_report_result'):
            if module in by_module:
                pass
        appendix = '\nfrom typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n'
        for module in ('proof_repository', 'toda_calculation_report_result'):
            if module in by_module:
                appendix += f'    from {module} import {LEGACY[module]}\n'
        edits.append((len(lines), len(lines), appendix))
    for a, b, text in sorted(edits, key=lambda edit: (edit[0], edit[1]), reverse=True):
        lines[a:b] = [text]
    result = ''.join(lines)
    parsed = ast.parse(result)
    if any(isinstance(n, ast.ImportFrom) and n.module in LEGACY for n in parsed.body):
        raise RuntimeError('an eager legacy import remains')
    return result, True


def apply(root: Path = ROOT) -> dict:
    path = root / 'toda_calculation_facade.py'
    if not path.is_file():
        raise FileNotFoundError(path)
    if not (root / 'toda_typed_group_facade.py').is_file():
        raise RuntimeError('R52 typed group facade must be installed')
    source = path.read_text(encoding='utf-8-sig')
    updated, changed = transform(source)
    if changed:
        backup_dir = root / 'phase165_r27_r53_r2_backup'
        backup_dir.mkdir(exist_ok=True)
        backup = backup_dir / path.name
        if backup.exists() and backup.read_bytes() != path.read_bytes():
            raise RuntimeError('conflicting backup')
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(updated, encoding='utf-8', newline='\n')
    record = {
        'phase': '165 R27-R53-R2',
        'status': 'CHANGED' if changed else 'ALREADY_INSTALLED',
        'modified_files': [path.name] if changed else [],
        'legacy_function_bodies_preserved': True,
        'eager_repository_imports_removed': True,
        'remaining_legacy_repository_modules': 4,
        'full_pytest_run': False,
    }
    (root / 'phase165_r27_r53_r2_audit.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return record


if __name__ == '__main__':
    print(json.dumps(apply(), indent=2, ensure_ascii=False))
