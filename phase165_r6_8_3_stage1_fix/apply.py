from pathlib import Path
import ast
import shutil

path = Path.cwd() / 'probes' / 'probe_phase53_capabilities.py'
if not path.is_file():
    raise SystemExit(f'MISSING: {path}')
source = path.read_text(encoding='utf-8')
old_import = '  toda_45_pi4_3_finite_cyclic_transport_inference_rule,\n'
old_call = '    toda_45_pi4_3_finite_cyclic_transport_inference_rule(),'
if old_import not in source or old_call not in source:
    raise SystemExit('STOP: Stage1 baseline does not match; no changes made')
if 'build_phase50_representative_result' in source:
    raise SystemExit('STOP: old Phase 50 dependency is still present')
updated = source.replace(old_import, '')
updated = updated.replace(old_call, '    toda_45_generic_finite_cyclic_transport_inference_rule(),')
insert = 'from toda_stable_group_transport import (\n  toda_45_generic_finite_cyclic_transport_inference_rule,\n)\n'
anchor = 'from phase165_r55_nk_only_goal import search_group_from_registered_goal\n'
if anchor not in updated:
    raise SystemExit('STOP: current Phase 53 search import not found')
updated = updated.replace(anchor, anchor + insert, 1)
ast.parse(updated)
backup = path.with_suffix('.py.phase165_r6_8_3_stage1_fix.bak')
if not backup.exists():
    shutil.copy2(path, backup)
path.write_text(updated, encoding='utf-8')
print('APPLIED: removed obsolete rule reference; reused existing generic Toda (4.5) transport')
print('Phase 55 NOT modified; full pytest NOT run')
