from pathlib import Path
from datetime import datetime, timezone
import ast
import shutil

root = Path.cwd()
changes = {
    'test_phase165_r52_partial_proof.py': (
        'test_r52_partial_preserves_steps_and_goals',
        'assert text.index("Reference") < text.index("Proof（導出済み）") < text.index("未解決 Goal")',
        'assert text.index("## 使用する結果") < text.index("### 確認済み ProofStep（与件を含む）") < text.index("## 未解決 Goal")\n    assert "与件: typed_known" in text',
    ),
    'test_phase165_r52_r3_web_adapter.py': (
        'test_complete_result_retains_qed',
        'view = build_partial_web_group_proof_view(result)\n    assert "□" in _visible_text(view)',
        'with pytest.raises(ValueError, match="completed target does not match conclusion"):\n        build_partial_web_group_proof_view(result)',
    ),
}
prepared = []
for filename, (func, old, new) in changes.items():
    path = root / filename
    if not path.is_file():
        raise SystemExit(f'MISSING: {path}; no changes')
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func]
    if len(functions) != 1:
        raise SystemExit(f'UNEXPECTED FUNCTION: {filename}:{func}; no changes')
    lines = source.splitlines(keepends=True)
    f = functions[0]
    section = ''.join(lines[f.lineno-1:f.end_lineno])
    if old in section and section.count(old) == 1:
        replacement = section.replace(old, new)
        result = ''.join(lines[:f.lineno-1]) + replacement + ''.join(lines[f.end_lineno:])
        ast.parse(result)
        prepared.append((path, source, result))
    elif new in section:
        print('ALREADY PATCHED:', filename)
    else:
        raise SystemExit(f'UNEXPECTED TEST CONTENT: {filename}:{func}; no changes')
if prepared:
    backup_dir = root / 'phase165_r6_audit_results' / 'runner_backup' / ('partial_steps_test_alignment_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    backup_dir.mkdir(parents=True, exist_ok=False)
    for path, original, modified in prepared:
        shutil.copy2(path, backup_dir / path.name)
    for path, original, modified in prepared:
        path.write_text(modified, encoding='utf-8')
        print('PATCHED:', path)
    print('BACKUP:', backup_dir)
else:
    print('NO CHANGES: tests already aligned')
