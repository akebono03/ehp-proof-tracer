from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'web_group_proof.py'
BACKUP = Path(__file__).resolve().parent / 'backup' / 'web_group_proof.py'
SOURCE = TARGET.read_text(encoding='utf-8')
TREE = ast.parse(SOURCE)
FUNCTIONS = [x for x in TREE.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == 'build_standard_web_group_proof_view']
if len(FUNCTIONS) != 1:
    raise RuntimeError('Expected exactly one build_standard_web_group_proof_view')
FN = FUNCTIONS[0]
kw = FN.args.kwonlyargs
if [a.arg for a in kw] != ['goal', 'citation_source']:
    raise RuntimeError('Unexpected keyword-only function signature')
value = FN.args.kw_defaults[1]
if not isinstance(value, ast.Constant) or value.value not in ('legacy', 'model'):
    raise RuntimeError('Unexpected existing citation_source default')
if value.value == 'model':
    print('ALREADY_PATCHED:', TARGET)
else:
    segment = ast.get_source_segment(SOURCE, FN)
    if segment is None or 'citation_source: str = "legacy"' not in segment:
        raise RuntimeError('Unexpected function source')
    if 'Legacy is the default until the full-length narrative consumes the model.' not in segment:
        raise RuntimeError('Unexpected function docstring')
    changed = segment.replace('citation_source: str = "legacy"', 'citation_source: str = "model"', 1)
    changed = changed.replace('Legacy is the default until the full-length narrative consumes the model.', 'The model is the default; legacy remains an explicit compatibility option.', 1)
    lines = SOURCE.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:FN.lineno - 1]) + FN.col_offset
    end = sum(len(line) for line in lines[:FN.end_lineno - 1]) + FN.end_col_offset
    assert SOURCE[start:end] == segment
    BACKUP.parent.mkdir(exist_ok=True)
    shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(SOURCE[:start] + changed + SOURCE[end:], encoding='utf-8')
    print('PATCHED:', TARGET)
new_source = TARGET.read_text(encoding='utf-8')
new_fn = next(x for x in ast.parse(new_source).body if isinstance(x, ast.FunctionDef) and x.name == FN.name)
full = ast.get_source_segment(new_source, new_fn)
(Path(__file__).resolve().parent / 'build_standard_web_group_proof_view_FULL.py').write_text(full + '\n', encoding='utf-8')
print('FULL_FUNCTION:', Path(__file__).resolve().parent / 'build_standard_web_group_proof_view_FULL.py')
# The earlier regression explicitly asserted the old default. Keep its long-form
# compatibility assertion while making the intent explicit.
TEST = ROOT / 'phase168_r3_6_standard_web_entry' / 'tests' / 'test_phase168_r3_6_standard_web_entry.py'
if TEST.exists():
    old = TEST.read_text(encoding='utf-8')
    anchor = 'def test_r36_default_pi32_preserves_long_form():\n    view = build_standard_web_group_proof_view(2, 1)'
    revised = 'def test_r36_default_pi32_preserves_long_form():\n    view = build_standard_web_group_proof_view(2, 1, citation_source="legacy")'
    if anchor in old:
        test_backup = Path(__file__).resolve().parent / 'backup' / 'test_phase168_r3_6_standard_web_entry.py'
        shutil.copy2(TEST, test_backup)
        TEST.write_text(old.replace(anchor, revised, 1), encoding='utf-8')
        print('UPDATED_EXISTING_TEST:', TEST)
    elif revised in old:
        print('EXISTING_TEST_ALREADY_UPDATED:', TEST)
    else:
        raise RuntimeError('Unexpected historical regression test contents')
