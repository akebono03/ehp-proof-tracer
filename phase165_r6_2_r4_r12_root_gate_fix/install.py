from pathlib import Path
import ast
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r57_r11_proof_order_gate.py'
FUNCTIONS = Path(__file__).with_name('new_functions.py').read_text(encoding='utf-8')

def function_span(text, name):
    tree = ast.parse(text)
    node = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name), None)
    if node is None:
        raise RuntimeError('missing function: ' + name)
    lines = text.splitlines(keepends=True)
    return sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno]))

def main():
    if not TARGET.is_file():
        raise RuntimeError('target file missing: ' + str(TARGET))
    old = TARGET.read_text(encoding='utf-8')
    ast.parse(FUNCTIONS)
    if '_is_symbolic_cited_root_specialization' in old:
        print('ALREADY_INSTALLED')
        return
    start, end = function_span(old, 'is_unordered_root_structure_specialization')
    block = FUNCTIONS.strip() + '\n\n'
    updated = old[:start] + block + old[end:]
    ast.parse(updated)
    if 'def retain_ordered_root_expansions(' not in updated:
        raise RuntimeError('safety check: retaining function lost')
    backup = TARGET.with_name(TARGET.name + '.r4_r12_before.bak')
    if backup.exists():
        raise RuntimeError('backup already exists: ' + str(backup))
    shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding='utf-8')
    print(json.dumps({'status':'INSTALLED','target':str(TARGET),'backup':str(backup),'production_modified':True,'full_pytest_run':False},ensure_ascii=False))

if __name__ == '__main__':
    main()
