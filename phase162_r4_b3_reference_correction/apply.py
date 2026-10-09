from pathlib import Path
import shutil

root = Path.cwd()
path = root / 'toda_group_proof_narrative_renderer.py'
content = path.read_text(encoding='utf-8')
import_block = ('from toda_group_proof_narrative_concrete_transport import (\n'
                '  render_concrete_transport_proof_from_steps,\n' ' )\n')
# Match the exact Phase 162 R4-B3 injected import (no whitespace guesswork).
actual_import = 'from toda_group_proof_narrative_concrete_transport import (\n  render_concrete_transport_proof_from_steps,\n)\n'
entry = 'def _phase158_baseline_render_toda_group_proof_narrative_markdown('
branch = '  concrete = render_concrete_transport_proof_from_steps(presentation.root_step)\n  if concrete is not None:\n    return concrete\n\n'
start = content.find(entry)
if start == -1 or content.find(entry, start + 1) != -1:
    raise RuntimeError('共通Rendererの対象関数が一意に見つかりません。変更していません。')
end = content.find('\ndef ', start + len(entry))
if end < 0:
    raise RuntimeError('関数境界が見つかりません。変更していません。')
body = content[start:end]
if body.count(branch) != 1 or content.count(actual_import) != 1:
    raise RuntimeError('前回の専用分岐の形が一致しません。変更していません。')
content = content[:start] + body.replace(branch, '', 1) + content[end:]
content = content.replace(actual_import, '', 1)
backup = path.with_name('toda_group_proof_narrative_renderer.phase162_r4_b3_pre_reference_correction.bak')
if not backup.exists():
    shutil.copy2(path, backup)
path.write_text(content, encoding='utf-8')
print('Updated:', path.name)
print('Backup:', backup.name)
print('Removed dedicated template routing; default common renderer restored.')
