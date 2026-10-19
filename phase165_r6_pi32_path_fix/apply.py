from pathlib import Path
import ast
import shutil
from datetime import datetime, timezone

path = Path('tests/test_phase49_probe.py')
if not path.is_file() or not Path('phase165_r14_r39_toda51.tex').is_file():
    raise SystemExit('Run from repository root; source .tex must exist at root')
text = path.read_text(encoding='utf-8')
tree = ast.parse(text)
names = {
    'test_phase49_probe_derives_final_pi_3_2_group',
    'test_phase49_probe_all_derived_steps_preserve_inference_rule',
}
old = 'Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")'
new = 'Path(__file__).resolve().parent.parent / "phase165_r14_r39_toda51.tex"'
lines = text.splitlines(keepends=True)
changes = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in names:
        body = ''.join(lines[node.lineno - 1:node.end_lineno])
        if body.count(old) != 1:
            raise SystemExit(f'GUARD FAILED: {node.name} missing exact old path')
        changes.append((node.lineno - 1, node.end_lineno, body.replace(old, new)))
if len(changes) != 2:
    raise SystemExit('GUARD FAILED: expected exactly two functions')
backup = Path('phase165_r6_audit_results/runner_backup') / ('pi32_path_fix_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(path, backup / path.name)
for start, end, body in reversed(changes):
    lines[start:end] = [body]
updated = ''.join(lines)
ast.parse(updated)
path.write_text(updated, encoding='utf-8')
print('PATCHED:', path, 'FUNCTIONS:', ', '.join(sorted(names)))
print('BACKUP:', backup)
