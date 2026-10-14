from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    'repository_proof_scope_facade.py': (
        'explore_standard_repository_generator_proof_scope_input',
        'resolve_generator_input',
        'Legacy standard proof-scope exploration is retired in Phase 165 R27-R25; use the common typed proof search.',
    ),
    'repository_generator_known_group_identity_lookup.py': (
        'find_standard_repository_generator_known_group_identity_nodes',
        None,
        'Legacy standard generator known-group identity lookup is retired in Phase 165 R27-R25; use the common typed proof search.',
    ),
}
LEGACY_MODULE = 'standard_production_repository'

def transform(source: str, filename: str) -> str:
    function_name, validation, message = FILES[filename]
    newline = '\r\n' if '\r\n' in source else '\n'
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    relevant = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == function_name]
    if len(relevant) != 1:
        raise RuntimeError(f'{filename}: expected one {function_name}')
    target = relevant[0]
    builder_imports = [n for n in tree.body if isinstance(n, ast.ImportFrom) and n.module == LEGACY_MODULE]
    if len(builder_imports) > 1 or (builder_imports and {a.name for a in builder_imports[0].names} != {'build_standard_production_proof_repository'}):
        raise RuntimeError(f'{filename}: unexpected legacy builder import')
    other_functions = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == 'build_standard_production_proof_repository' and not (target.lineno <= n.lineno <= target.end_lineno)]
    if other_functions:
        raise RuntimeError(f'{filename}: builder referenced outside target function')
    if not builder_imports and 'build_standard_production_proof_repository' not in ast.unparse(target):
        # Can be the already-migrated implementation, but verify it is truly the intended one.
        if not any(isinstance(n, ast.Raise) and isinstance(n.exc, ast.Call) and isinstance(n.exc.func, ast.Name) and n.exc.func.id == 'RuntimeError' for n in ast.walk(target)):
            raise RuntimeError(f'{filename}: function previously modified without known retirement guard')
    if validation is None:
        replacement = f'''def {function_name}(\n  generator: GeneratorSymbol,\n) -> tuple[RepositoryProofScopeNode, ...]:\n  if not isinstance(generator, GeneratorSymbol):\n    raise TypeError("generator must be a GeneratorSymbol")\n  raise RuntimeError({message!r})\n'''
    else:
        replacement = f'''def {function_name}(\n  generator_input: str,\n) -> RepositoryProofScopeExplorationResult:\n  resolve_generator_input(generator_input)\n  raise RuntimeError({message!r})\n'''
    replacements = [(target.lineno-1, target.end_lineno, replacement)]
    for n in builder_imports:
        replacements.append((n.lineno-1,n.end_lineno,''))
    if filename == 'repository_generator_known_group_identity_lookup.py':
        for n in tree.body:
            if isinstance(n, ast.ImportFrom) and n.module == 'phase164_r7_r3_generator_registry':
                if {a.name for a in n.names} != {'validate_generator_repository_registry_links'}:
                    raise RuntimeError('unexpected generator registry import')
                uses = [x for x in ast.walk(tree) if isinstance(x, ast.Name) and x.id == 'validate_generator_repository_registry_links' and not (target.lineno<=x.lineno<=target.end_lineno)]
                if uses:
                    raise RuntimeError('validation remains referenced outside standard entry')
                replacements.append((n.lineno-1,n.end_lineno,''))
    for start, end, new in sorted(replacements, reverse=True):
        lines[start:end] = [new.replace('\n',newline)] if new else []
    result=''.join(lines)
    ast.parse(result)
    assert 'from standard_production_repository import' not in result
    return result

def apply() -> None:
    before_after = {}
    for name in FILES:
        path=ROOT/name
        before=path.read_bytes()
        # Decode with utf-8; preserve original newline via actual decoded bytes
        after=transform(before.decode('utf-8'), name).encode('utf-8')
        before_after[path]=(before,after)
    backup=Path(__file__).resolve().parent/'backups'
    backup.mkdir(exist_ok=True)
    for path,(before,after) in before_after.items():
        if before == after:
            print(f'R27-R25 already installed: {path.name}')
            continue
        target=backup/path.name
        if not target.exists():
            target.write_bytes(before)
        path.write_bytes(after)
        print(f'R27-R25 installed: {path.name}')

if __name__ == '__main__':
    apply()
