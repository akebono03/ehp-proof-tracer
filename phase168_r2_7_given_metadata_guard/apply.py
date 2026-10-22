from __future__ import annotations
import ast
from pathlib import Path
import shutil
import sys

ROOT = Path.cwd()
TARGET = ROOT / 'phase165_r52_r16_web_citation_gate.py'
HERE = Path(__file__).resolve().parent
OLD = '''            if not is_dataclass(assertion.content) or isinstance(assertion.content, type):
                continue
            if type(assertion.content) is type(goal) and assertion.content == goal:
'''
NEW = '''            if not is_dataclass(assertion.content) or isinstance(assertion.content, type):
                continue
            # A boundary component describes a printed statement; it is not
            # itself a mathematical claim usable as a GIVEN proof leaf.
            if type(assertion.content).__name__ == "TodaFixedStatementComponent":
                continue
            if type(assertion.content) is type(goal) and assertion.content == goal:
'''

def main() -> None:
    if not TARGET.is_file():
        raise SystemExit(f'MISSING: {TARGET}')
    original = TARGET.read_bytes()
    content = original.decode('utf-8')
    if content.count(OLD) == 1:
        changed = content.replace(OLD, NEW, 1)
        backup_dir = HERE / 'backup'
        backup_dir.mkdir(exist_ok=True)
        backup = backup_dir / TARGET.name
        if not backup.exists():
            backup.write_bytes(original)
        TARGET.write_bytes(changed.encode('utf-8'))
        print('PATCHED:', TARGET)
        print('BACKUP:', backup)
    elif content.count(NEW) == 1:
        changed = content
        print('ALREADY_PATCHED:', TARGET)
    else:
        raise SystemExit('GUARD_MISMATCH: original function differs; no change performed')
    tree = ast.parse(changed)
    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'screen_shared_proof_context']
    if len(funcs) != 1:
        raise SystemExit('FUNCTION_NOT_FOUND')
    lines = changed.splitlines(keepends=True)
    func = ''.join(lines[funcs[0].lineno - 1:funcs[0].end_lineno])
    (HERE / 'screen_shared_proof_context_full.py').write_text(func, encoding='utf-8')
    print('FULL_FUNCTION:', HERE / 'screen_shared_proof_context_full.py')

if __name__ == '__main__':
    main()
