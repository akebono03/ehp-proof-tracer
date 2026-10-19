from pathlib import Path
from datetime import datetime, timezone
import shutil

root = Path.cwd()
path = root / 'toda_group_proof_narrative_renderer.py'
if not path.exists():
    raise SystemExit('ERROR: run from repository root')
source = path.read_text(encoding='utf-8')
function_start = source.find('def render_toda_partial_proof_narrative_markdown(result) -> str:')
function_end = source.find('\ndef render_narrative_proof_model(model)', function_start)
if function_start < 0 or function_end < 0:
    raise SystemExit('ERROR: expected renderer function not found; no changes')
old = '''    lines.extend(["**探索状態：" + state + "**", ""])
    if result.open_goals:
'''
new = '''    lines.extend(["**探索状態：" + state + "**", ""])
    if steps:
      lines.extend(["### 確認済み ProofStep（与件を含む）", ""])
      for step in steps:
        rendered = (statement_math(step.conclusion)
                    if isinstance(step.conclusion, str)
                    else _render_generic_narrative_step(step))
        prefix = "- 与件: " if step.rule is ProofRule.GIVEN else "- 推論: "
        lines.append(prefix + rendered)
      lines.append("")
    if result.open_goals:
'''
section = source[function_start:function_end]
if section.count(old) != 1:
    if new in section:
        print('ALREADY PATCHED: no replacement required')
        raise SystemExit(0)
    raise SystemExit('ERROR: unexpected renderer version; no changes')
backup_dir = root / 'phase165_r6_audit_results' / 'runner_backup'
backup_dir.mkdir(parents=True, exist_ok=True)
backup = backup_dir / ('toda_group_proof_narrative_renderer_before_partial_steps_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.py')
shutil.copy2(path, backup)
new_source = source[:function_start] + section.replace(old,new) + source[function_end:]
path.write_text(new_source, encoding='utf-8')
print('PATCHED:', path)
print('BACKUP:', backup)
