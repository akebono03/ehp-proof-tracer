"""Guarded installation of a generic expansion into the canonical search."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


ANCHOR = '    from phase165_r12_r15_toda51 import expand_cited_toda51_zero\n'
HOOK = ('    from phase165_r12_r24_web_search_connection import expand_finite_cyclic_relation\n')
EXPANSION_ANCHOR = '        options = []\n        options.extend(expand_cited_toda51_zero(goal, tuple(available)))\n'
EXPANSION_REPLACEMENT = ('        options = []\n'
                         '        options.extend(expand_finite_cyclic_relation(goal))\n'
                         '        options.extend(expand_cited_toda51_zero(goal, tuple(available)))\n')


def install(project: Path, package: Path) -> str:
    target = project / 'phase165_r52_r9_shared_math.py'
    original = target.read_text(encoding='utf-8')
    altered = original
    if HOOK not in altered:
        if altered.count(ANCHOR) != 1:
            raise ValueError('canonical provider import anchor changed')
        altered = altered.replace(ANCHOR, ANCHOR + HOOK, 1)
    if EXPANSION_REPLACEMENT not in altered:
        if altered.count(EXPANSION_ANCHOR) != 1:
            raise ValueError('canonical provider expansion anchor changed')
        altered = altered.replace(EXPANSION_ANCHOR, EXPANSION_REPLACEMENT, 1)
    ast.parse(altered)
    new_module = package / 'phase165_r12_r24_web_search_connection.py'
    ast.parse(new_module.read_text(encoding='utf-8'))
    if altered == original and (project / new_module.name).exists():
        return 'ALREADY_INSTALLED'
    if altered != original:
        backup = target.with_name(target.name + '.phase165_r12_r24_backup')
        if not backup.exists():
            shutil.copy2(target, backup)
    shutil.copy2(new_module, project / new_module.name)
    if altered != original:
        target.write_text(altered, encoding='utf-8')
    return 'INSTALLED'


def main() -> None:
    package = Path(__file__).resolve().parent
    project = package.parent
    print('R12-R24 common backward expansion:', install(project, package))


if __name__ == '__main__':
    main()
