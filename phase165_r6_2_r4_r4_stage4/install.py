"""Install R4-4 stage4 without disturbing local stage1-3 or registry patches."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

MODULE = 'phase165_r6_2_r4_r4_stage4_binding.py'
MARKER = '    # R4-4 stage4: exactness-map binding from cited fixed statements only.\n'
INSERT = (MARKER +
          '    from phase165_r6_2_r4_r4_stage4_binding import build_exactness_binding_provider\n'
          '    extra_providers = (build_exactness_binding_provider(bridge),) + tuple(extra_providers)\n')


def install(root: Path) -> str:
    source = Path(__file__).with_name(MODULE)
    shared = root / 'phase165_r52_r9_shared_math.py'
    destination = root / MODULE
    if not shared.is_file():
        raise FileNotFoundError(shared)
    if destination.exists() and destination.read_bytes() != source.read_bytes():
        raise RuntimeError('Existing stage4 module differs; refusing overwrite')
    text = shared.read_text(encoding='utf-8-sig')
    if MARKER in text:
        if INSERT not in text or not destination.is_file():
            raise RuntimeError('Partial stage4 installation')
        return 'ALREADY_INSTALLED'
    marker = '    available = []\n'
    if text.count(marker) != 1:
        raise RuntimeError('shared_expansion_provider insertion point not unique')
    tree = ast.parse(text)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    if len(functions) != 1:
        raise RuntimeError('shared_expansion_provider not found')
    f = functions[0]
    if not (f.lineno < text[:text.index(marker)].count('\n') + 1 <= f.end_lineno):
        raise RuntimeError('insertion anchor is outside shared_expansion_provider')
    # Refuse to run without the prerequisite typed rule names.
    mp = root / 'map_property_rules.py'
    if not mp.exists():
        raise FileNotFoundError(mp)
    known = {node.name for node in ast.parse(mp.read_text(encoding='utf-8-sig')).body
             if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    required = {'KernelZeroStatement', 'ImageWholeStatement', 'ImageZeroStatement',
                'KernelWholeStatement',
                'exactness_and_zero_image_implies_zero_kernel_inference_rule',
                'exactness_and_whole_kernel_implies_whole_image_inference_rule'}
    if not required.issubset(known):
        raise RuntimeError('stage2 or stage3 prerequisite missing')
    updated = text.replace(marker, INSERT + marker, 1)
    ast.parse(updated)
    if not destination.exists():
        shutil.copy2(source, destination)
    backup = root / 'phase165_r52_r9_shared_math.py.r4_r4_stage4_before.bak'
    if not backup.exists():
        shutil.copy2(shared, backup)
    shared.write_text(updated, encoding='utf-8')
    return 'INSTALLED'


if __name__ == '__main__':
    print(install(Path.cwd()))
