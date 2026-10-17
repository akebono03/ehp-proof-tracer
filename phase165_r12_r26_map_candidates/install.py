"""Install one general candidate provider in the common search path."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def main() -> None:
    package = Path(__file__).resolve().parent
    project = package.parent
    source = package / 'phase165_r12_r26_map_candidates.py'
    destination = project / source.name
    original = project / 'phase165_r52_r9_shared_math.py'
    content = original.read_text(encoding='utf-8')
    anchor = '    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)'
    insertion = ('    from phase165_r12_r26_map_candidates import build_cited_eta_quotient_provider\n'
                 '    extra_providers = (build_cited_eta_quotient_provider(bridge),) + tuple(extra_providers)\n')
    if insertion.strip() not in content:
        if content.count(anchor) != 1:
            raise ValueError('shared provider anchor changed; refusing patch')
        content = content.replace(anchor, insertion + anchor)
    ast.parse(content)
    if destination.exists() and destination.read_bytes() != source.read_bytes():
        raise ValueError('module already exists with different contents')
    if original.read_text(encoding='utf-8') != content:
        shutil.copy2(original, original.with_name(original.name + '.r12_r26_backup'))
    shutil.copy2(source, destination)
    original.write_text(content, encoding='utf-8')
    print('R12-R26 common candidate provider: INSTALLED')


if __name__ == '__main__':
    main()
