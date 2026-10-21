from __future__ import annotations
import ast
import datetime
from pathlib import Path
import shutil

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
SHARED = ROOT / 'phase165_r52_r9_shared_math.py'
GATE = ROOT / 'phase165_r57_r11_proof_order_gate.py'
DEST = ROOT / 'phase166_r3ac_stable_notation.py'
for file in (SHARED, GATE):
    if not file.is_file():
        raise SystemExit(f'Expected project root; missing {file}')

shared = SHARED.read_text(encoding='utf-8')
gate = GATE.read_text(encoding='utf-8')
marker = '        from phase166_r3v_generator_transport import expand_generator_transport_normalization\n'
if marker not in shared.replace('\r\n', '\n'):
    raise SystemExit('Unexpected shared provider: insertion point absent')
addition = ('        from phase166_r3ac_stable_notation import expand_stable_eta_notation\n'
            '        options.extend(expand_stable_eta_notation(goal, tuple(available)))\n')
shared_new = shared.replace('\r\n', '\n').replace(marker,addition + marker,1)
anchor = '    if _proved_generator_suspension_normalization_shape(root_goal, expansion):\n        return False\n'
if anchor not in gate.replace('\r\n','\n'):
    raise SystemExit('Unexpected root gate: insertion point absent')
replacement = anchor + '''    if getattr(expansion.rule, "name", None) == "cited stable eta-family notation for iterated transport":
        from phase166_r3ac_stable_notation import _stable_eta_renaming_shape
        from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
        if (len(expansion.subgoals) == 2
                and expansion.subgoals[1] == TodaEtaFamilyGeneralDefinition()
                and _stable_eta_renaming_shape(expansion.subgoals[0], root_goal)):
            return False
'''
gate_new = gate.replace('\r\n','\n').replace(anchor,replacement,1)
for name,code in ((str(SHARED),shared_new),(str(GATE),gate_new),('new module',(HERE/'phase166_r3ac_stable_notation.py').read_text())):
    ast.parse(code,filename=name)
backup = ROOT/'phase166_r3ac_stable_notation_backups'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup.mkdir(parents=True,exist_ok=True)
for file in (SHARED,GATE):
    shutil.copy2(file,backup/file.name)
if DEST.exists():
    shutil.copy2(DEST,backup/DEST.name)
SHARED.write_text(shared_new,encoding='utf-8')
GATE.write_text(gate_new,encoding='utf-8')
shutil.copy2(HERE/'phase166_r3ac_stable_notation.py',DEST)
for path,fun in ((SHARED,'shared_expansion_provider'),(GATE,'is_unordered_root_structure_specialization')):
    tree=ast.parse(path.read_text(encoding='utf-8'))
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==fun)
    lines=path.read_text(encoding='utf-8').splitlines(keepends=True)
    (HERE/f'{fun}_full.py.txt').write_text(''.join(lines[node.lineno-1:node.end_lineno]),encoding='utf-8')
print('PATCHED:',SHARED)
print('PATCHED:',GATE)
print('INSTALLED:',DEST)
print('BACKUP:',backup)
