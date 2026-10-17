from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
ADAPTER = ROOT / 'phase165_r52_r23_existing_rule_adapter.py'
IMPORT = 'from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules'
CALL = '            expand_existing_pi43_rules,\n'

def main():
    source = TARGET.read_text(encoding='utf-8')
    module = ast.parse(source)
    live_imports = [node for node in ast.walk(module) if isinstance(node, ast.ImportFrom) and node.module == 'phase165_r52_r23_existing_rule_adapter']
    live_calls = [node for node in ast.walk(module) if isinstance(node, ast.Name) and node.id == 'expand_existing_pi43_rules']
    installed = not live_imports and not live_calls
    if not installed:
        if source.count(IMPORT) != 1 or source.count(CALL) != 1 or len(live_imports) != 1 or len(live_calls) != 1:
            raise RuntimeError('UNEXPECTED shared provider; no changes made')
        new = source.replace(IMPORT + '\n', '', 1).replace(CALL, '', 1)
        ast.parse(new)
        if 'expand_existing_pi43_rules' in new:
            raise RuntimeError('unexpected remaining reference')
        TARGET.with_suffix('.py.before_pi43_adapter_removal.bak').write_text(source, encoding='utf-8')
        TARGET.write_text(new, encoding='utf-8')
    # Do not remove module while any other top-level production file imports it.
    consumers = []
    for file in ROOT.glob('*.py'):
        if file == ADAPTER or file == TARGET:
            continue
        try:
            tree = ast.parse(file.read_text(encoding='utf-8-sig'))
        except (SyntaxError, UnicodeError):
            continue
        if any(isinstance(node, ast.ImportFrom) and node.module == ADAPTER.stem for node in ast.walk(tree)):
            consumers.append(file.name)
    if consumers:
        raise RuntimeError('Other active consumers remain; adapter retained: ' + ', '.join(consumers))
    adapter_deleted = False
    if ADAPTER.exists():
        code = ADAPTER.read_text(encoding='utf-8')
        if 'def expand_existing_pi43_rules(' not in code:
            raise RuntimeError('Adapter contents changed; not deleting')
        # Keep recoverable copy in ZIP-era backup file, not importable Python.
        backup = ADAPTER.with_suffix('.py.removed_adapter_backup.txt')
        if not backup.exists():
            backup.write_text(code, encoding='utf-8')
        ADAPTER.unlink()
        adapter_deleted = True
    print(json.dumps({'status':'REMOVED','shared_provider_modified':not installed,'adapter_deleted':adapter_deleted,'full_pytest_run':False},ensure_ascii=False))

if __name__ == '__main__':
    main()
