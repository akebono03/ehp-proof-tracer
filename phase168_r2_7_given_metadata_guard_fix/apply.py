from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'phase165_r52_r16_web_citation_gate.py'
HERE = Path(__file__).resolve().parent
GUARD = 'if not is_dataclass(assertion.content) or isinstance(assertion.content, type):'
ADDED = 'if type(assertion.content).__name__ == "TodaFixedStatementComponent":'


def modify_source(original: bytes) -> tuple[bytes, bool]:
    text = original.decode('utf-8')
    tree = ast.parse(text)
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == 'screen_shared_proof_context'
    ]
    if len(functions) != 1:
        raise ValueError('GUARD_MISMATCH: exactly one target function required')
    function = functions[0]
    matches = [
        node for node in ast.walk(function)
        if isinstance(node, ast.If) and ast.get_source_segment(text, node.test) == GUARD[3:-1]
    ]
    if len(matches) != 1 or len(matches[0].body) != 1 or not isinstance(matches[0].body[0], ast.Continue):
        raise ValueError('GUARD_MISMATCH: expected dataclass guard is absent or changed')
    guard = matches[0]
    lines = text.splitlines(keepends=True)
    next_index = guard.end_lineno
    if next_index >= len(lines):
        raise ValueError('GUARD_MISMATCH: no statement after dataclass guard')
    indent = ' ' * guard.col_offset
    if ADDED in text:
        if len([node for node in ast.walk(function) if isinstance(node, ast.If) and ast.get_source_segment(text, node.test) == ADDED[3:-1]]) != 1:
            raise ValueError('GUARD_MISMATCH: ambiguous existing metadata guard')
        return original, False
    if 'if type(assertion.content) is type(goal) and assertion.content == goal:' not in lines[next_index]:
        raise ValueError('GUARD_MISMATCH: following goal exclusion changed')
    newline = '\r\n' if b'\r\n' in original else '\n'
    insertion = (
        indent + '# Boundary component metadata is not a mathematical proof premise.' + newline
        + indent + ADDED + newline
        + indent + '    continue' + newline
    )
    lines.insert(next_index, insertion)
    modified = ''.join(lines)
    ast.parse(modified)
    return modified.encode('utf-8'), True


def main() -> None:
    if not TARGET.is_file():
        raise SystemExit(f'MISSING: {TARGET}')
    original = TARGET.read_bytes()
    try:
        patched, changed = modify_source(original)
    except (ValueError, SyntaxError) as error:
        raise SystemExit(str(error)) from error
    if changed:
        backups = HERE / 'backup'
        backups.mkdir(exist_ok=True)
        backup = backups / TARGET.name
        if not backup.exists():
            backup.write_bytes(original)
        TARGET.write_bytes(patched)
        print('PATCHED:', TARGET)
        print('BACKUP:', backup)
    else:
        print('ALREADY_PATCHED:', TARGET)
    source = patched.decode('utf-8')
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'screen_shared_proof_context')
    lines = source.splitlines(keepends=True)
    output = HERE / 'screen_shared_proof_context_full.py'
    output.write_text(''.join(lines[node.lineno - 1:node.end_lineno]), encoding='utf-8')
    print('FULL_FUNCTION:', output)


if __name__ == '__main__':
    main()
