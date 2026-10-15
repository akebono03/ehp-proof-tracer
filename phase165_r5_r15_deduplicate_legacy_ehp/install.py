from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / 'phase162_web_narrative_integration.py'
BACKUP = HERE / 'phase162_web_narrative_integration.before_r5_r15.py'
REPLACEMENT = (HERE / 'replacement_function.py.txt').read_text(encoding='utf-8')

def function_node(tree: ast.Module, name: str) -> ast.FunctionDef:
    found = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(found) != 1:
        raise ValueError(f'Expected exactly one {name} definition, found {len(found)}')
    return found[0]

def install() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    raw = TARGET.read_bytes()
    bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    content = raw[len(bom):].decode('utf-8')
    tree = ast.parse(content)
    old = function_node(tree, '_build_phase162_legacy_validated_isomorphism_markdown')
    function_node(tree, '_build_phase162_existing_group_connection')
    reexport = [n for n in tree.body if isinstance(n, ast.ImportFrom) and n.module == 'phase162_ehp_leaf_inputs' and any(a.name == '_phase162_ehp_leaves' for a in n.names)]
    if len(reexport) != 1 or not (ROOT / 'phase162_ehp_leaf_inputs.py').is_file():
        raise ValueError('R5-R11 shared EHP leaves not installed')
    if not (ROOT / 'phase162_pi5_3_web_replay.py').read_text(encoding='utf-8-sig').find('from phase162_ehp_leaf_inputs import _phase162_ehp_leaves') >= 0:
        raise ValueError('Replay must consume shared EHP leaves')
    source = ast.get_source_segment(content, old)
    if '_phase162_ehp_leaves()' in source:
        raise ValueError('Function already migrated, do not overwrite')
    required = ['build_phase55_representative_result()', 'build_phase58_representative_result()', 'TodaEHPExactnessWindow(', 'reconstruct_phase161_r7_validated_goal(', 'render_validated_backward_proof_markdown(']
    if not all(x in source for x in required):
        raise ValueError('Unexpected local legacy function; no changes made')
    new_tree = ast.parse(REPLACEMENT)
    replacement = function_node(new_tree, '_build_phase162_legacy_validated_isomorphism_markdown')
    if len(new_tree.body) != 1 or replacement.name != old.name:
        raise ValueError('Invalid replacement function')
    if BACKUP.exists():
        raise ValueError('Existing backup present; refuse to overwrite')
    lines = content.splitlines(keepends=True)
    style = '\r\n' if '\r\n' in content else '\n'
    new_text = ''.join(lines[:old.lineno - 1]) + REPLACEMENT.rstrip('\n').replace('\n', style) + style + style + ''.join(lines[old.end_lineno:])
    ast.parse(new_text)
    shutil.copy2(TARGET, BACKUP)
    try:
        TARGET.write_bytes(bom + new_text.encode('utf-8'))
    except BaseException:
        TARGET.write_bytes(raw)
        BACKUP.unlink(missing_ok=True)
        raise
    print(json.dumps({'status':'INSTALLED','modified_files':[TARGET.name],'removed_duplicate_ehp_window_construction':True,'legacy_renderer_retired':False,'full_pytest_run':False},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    install()
