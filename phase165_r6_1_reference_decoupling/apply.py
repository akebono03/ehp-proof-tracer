from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r14_r38_direct_registry.py'
OLD = '    leaves = backward_leaf_goals(pi32_goal())\n    steps = adopted_leaf_steps(Path(tex_path))'
NEW = '    steps = adopted_leaf_steps(Path(tex_path))\n    leaves = tuple(step.conclusion for step in steps)'

def main() -> None:
    source = TARGET.read_text(encoding='utf-8-sig')
    normalized = source.replace('\r\n','\n')
    tree = ast.parse(normalized)
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build_adopted_typed_reference_registry']
    if len(funcs) != 1:
        raise RuntimeError('expected registry builder absent or duplicate')
    segment = '\n'.join(normalized.splitlines()[funcs[0].lineno-1:funcs[0].end_lineno])
    if NEW in segment:
        status = 'ALREADY_APPLIED'
    elif segment.count(OLD) == 1:
        updated = normalized.replace(OLD, NEW, 1)
        ast.parse(updated)
        backup = TARGET.with_name(TARGET.name + '.phase165_r6_1_reference_backup')
        if not backup.exists():
            shutil.copy2(TARGET, backup)
        TARGET.write_text(updated, encoding='utf-8')
        status = 'CHANGED'
    else:
        raise RuntimeError('source differs from inspected version; no file changed')
    print(json.dumps({'phase':'165 R6-1 source registry decoupling','status':status,'modified_file':TARGET.name,'root_goal_removed_from_reference_leaf_join':True,'downstream_adopted_leaf_steps_still_legacy':True,'full_pytest_run':False},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
