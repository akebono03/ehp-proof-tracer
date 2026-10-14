"""Install minimal R52-R12 shared bridge wiring with an exact match guard."""
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
root = Path.cwd()
shared = root / 'phase165_r52_r9_shared_math.py'
if not shared.is_file():
    raise SystemExit('Repository root not found: phase165_r52_r9_shared_math.py missing')
source = shared.read_text(encoding='utf-8')
needle = '    return RegistryBridgeResult(registry, tuple(records), tuple(links))'
replacement = ('    from phase165_r52_r12_component_bridge import expand_cited_given_components\n'
               '    return expand_cited_given_components(\n'
               '        RegistryBridgeResult(registry, tuple(records), tuple(links))\n'
               '    )')
if replacement in source:
    print('R52-R12 shared wiring already installed')
elif source.count(needle) == 1:
    backup = shared.with_name(shared.name + '.r52_r12_backup')
    if not backup.exists():
        shutil.copy2(shared, backup)
    shared.write_text(source.replace(needle, replacement), encoding='utf-8')
    print('R52-R12 shared wiring installed')
else:
    raise SystemExit('Shared wiring signature changed; no production files modified')
for name in ('phase165_r52_r12_component_bridge.py', 'test_phase165_r52_r12_component_bridge.py'):
    shutil.copy2(package / name, root / name)
