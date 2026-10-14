from __future__ import annotations
import ast
from pathlib import Path
import shutil

TARGETS = {
    '_run_explore_proof_command',
    '_run_explore_applicable_command',
    '_run_show_proof_command',
    '_run_execute_command',
}
LEGACY_IMPORTS = {
    'repository_generator_applicability_facade',
    'repository_generator_applicability_renderer',
    'repository_generator_known_group_identity_presentation',
    'repository_generator_known_group_identity_renderer',
    'repository_generator_known_group_proof_replay',
    'repository_generator_known_group_proof_replay_presentation',
    'repository_generator_known_group_proof_replay_renderer',
    'repository_generator_user_execution_candidate_presentation',
    'repository_generator_user_execution_candidate_renderer',
    'repository_generator_user_execution_facade',
    'repository_proof_scope_facade',
    'repository_proof_scope_renderer',
}


def rewrite(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    funcs = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    missing = TARGETS.difference(funcs)
    if missing:
        raise RuntimeError(f'Missing functions: {sorted(missing)}')
    for name in TARGETS:
        func = funcs[name]
        if func.returns is not None and ast.unparse(func.returns) != 'int':
            raise RuntimeError(f'Unexpected return annotation: {name}')
    changes = []
    for name in TARGETS:
        node = funcs[name]
        # Retain the complete original signature, including parameters and annotations.
        def_line = next((i for i in range(node.lineno - 1, node.body[0].lineno) if lines[i].lstrip().startswith(') -> int:')), None)
        if def_line is None:
            raise RuntimeError(f'Cannot locate signature end: {name}')
        body = (
            '  print(\n'
            '    "This legacy generator command is disabled; "\n'
            '    "use the unified proof search when available."\n'
            '  )\n'
            '  return 1\n'
        )
        changes.append((def_line + 1, node.end_lineno, body))
    # Also remove old imports that no longer have active references, but preserve imports
    # if monkeypatches or unrelated code still use a name.
    for a,b,repl in sorted(changes, reverse=True):
        lines[a:b] = [repl]
    interim = ''.join(lines)
    tree2 = ast.parse(interim)
    imported = []
    for node in tree2.body:
        if isinstance(node, ast.ImportFrom) and node.module in LEGACY_IMPORTS:
            imported.append(node)
    # References in post-rewrite AST other than import statements.
    load_names = {node.id for node in ast.walk(tree2) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
    delete_lines = []
    for node in imported:
        names = {alias.asname or alias.name for alias in node.names}
        if not names.intersection(load_names):
            delete_lines.append((node.lineno-1, node.end_lineno))
    # Legacy assignment alias may now be unused as well.
    for node in tree2.body:
        if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == 'render_repository_generator_applicability_markdown' and node.targets[0].id not in load_names:
                delete_lines.append((node.lineno-1, node.end_lineno))
    interim_lines = interim.splitlines(keepends=True)
    for a,b in sorted(delete_lines,reverse=True):
        interim_lines[a:b] = []
    result = ''.join(interim_lines)
    # Recheck imports after dropping the compatibility alias assignment.
    post = ast.parse(result)
    loads = {n.id for n in ast.walk(post) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    removals = []
    for node in post.body:
        if isinstance(node, ast.ImportFrom) and node.module in LEGACY_IMPORTS:
            if not any((alias.asname or alias.name) in loads for alias in node.names):
                removals.append((node.lineno - 1, node.end_lineno))
    post_lines = result.splitlines(keepends=True)
    for a,b in sorted(removals, reverse=True):
        post_lines[a:b] = []
    result = ''.join(post_lines)
    ast.parse(result)
    parsed = ast.parse(result)
    all_calls = {n.id for f in parsed.body if isinstance(f, ast.FunctionDef) and f.name in TARGETS for n in ast.walk(f) if isinstance(n, ast.Name)}
    assert 'build_standard_repository_generator_known_group_proof_replay_input' not in all_calls
    return result


def main() -> int:
    path = Path.cwd() / 'main.py'
    if not path.exists():
        raise SystemExit('Run from repository root (main.py missing)')
    original = path.read_bytes()
    newline = '\r\n' if b'\r\n' in original else '\n'
    text = original.decode('utf-8-sig')
    updated = rewrite(text)
    if updated == text:
        raise SystemExit('No changes made')
    backup = Path(__file__).with_name('main_before_r27_r19.py')
    if not backup.exists():
        shutil.copy2(path,backup)
    tmp = path.with_suffix('.r27_r19_tmp')
    tmp.write_bytes(updated.replace('\n',newline).encode('utf-8'))
    tmp.replace(path)
    print('R27-R19 installed: disabled four legacy generator CLI executors')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
