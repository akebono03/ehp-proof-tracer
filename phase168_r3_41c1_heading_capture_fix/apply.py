"""Strict two-function patch with atomic backup and rollback; no other files."""
from __future__ import annotations

import ast
import datetime
import json
import os
from pathlib import Path
import shutil
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
STATE = PACKAGE / "installed_state.json"
CHANGES = (
    ("web_group_proof.py", "build_web_partial_group_proof_view", "build_web_partial_group_proof_view_FULL.py",
     ('def build_web_partial_group_proof_view(', 'build_partial_web_group_proof_view(', 'mode=mode,')),
    ("phase165_r52_r4_flask_bridge.py", "build_group_proof_progress_view", "build_group_proof_progress_view_FULL.py",
     ('def build_group_proof_progress_view(', 'search_registered_partial_proof(', 'narrative_model=')),
)


def replace_one(source: str, func_name: str, replacement: str, required: tuple[str, ...]) -> str:
    tree = ast.parse(source)
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == func_name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one function {func_name}")
    node = matches[0]
    lines = source.splitlines(keepends=True)
    old = "".join(lines[node.lineno-1:node.end_lineno])
    if not all(part in old for part in required[:2]):
        raise RuntimeError(f"Current {func_name} differs from inspected prerequisite")
    if 'R3-41C' in old or 'narrative_model=narrative_model' in old:
        raise RuntimeError(f"Already patched or unexpected {func_name}; no modifications")
    new_line_ending = "\r\n" if "\r\n" in source else "\n"
    replacement = replacement.replace("\r\n", "\n").rstrip("\n").replace("\n",new_line_ending)
    updated = "".join(lines[:node.lineno-1]) + replacement + new_line_ending + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated


def apply() -> None:
    if STATE.exists():
        raise RuntimeError("A previous R3-41C1 patch state exists; do not overwrite its backup")
    changed = []
    for rel, func, snippet, required in CHANGES:
        target = ROOT / rel
        if not target.is_file():
            raise FileNotFoundError(target)
        data = target.read_bytes()
        source = data.decode("utf-8-sig")
        replacement = (PACKAGE/"full_functions"/snippet).read_text(encoding="utf-8")
        updated = replace_one(source, func, replacement,required)
        encoding = b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
        changed.append((rel, target, data, encoding+updated.encode('utf-8')))
    stamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    backup = PACKAGE/'backup'/stamp
    backup.mkdir(parents=True,exist_ok=False)
    for rel,_,old,_ in changed:
        out=backup/rel
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_bytes(old)
    temp_paths=[]
    try:
        for rel,path,_,new in changed:
            temp = path.with_name(path.name+'.r3_41c_tmp')
            temp.write_bytes(new)
            temp_paths.append(temp)
            os.replace(temp,path)
            print('PATCHED',rel)
        STATE.write_text(json.dumps({'backup':str(backup),'files':[rel for rel,_,_,_ in changed]},indent=2),encoding='utf-8')
    except Exception:
        for rel,path,old,_ in changed:
            path.write_bytes(old)
        for temp in temp_paths:
            temp.unlink(missing_ok=True)
        raise
    print('FULL_FUNCTIONS',PACKAGE/'full_functions')
    print('FULL_IMPORTS',PACKAGE/'full_imports')


def rollback() -> None:
    if not STATE.exists():
        print('NO_PATCH_STATE_TO_ROLLBACK')
        return
    state=json.loads(STATE.read_text(encoding='utf-8'))
    backup=Path(state['backup'])
    for rel in state['files']:
        src=backup/rel
        if not src.is_file():
            raise RuntimeError('Missing backup: '+str(src))
        shutil.copyfile(src,ROOT/rel)
        print('ROLLBACK',rel)
    STATE.unlink()

if __name__=='__main__':
    if sys.argv[1:]==['--rollback']:
        rollback()
    elif not sys.argv[1:]:
        apply()
    else:
        raise SystemExit('usage: python -m phase168_r3_41c_partial_web_cutover.apply [--rollback]')
