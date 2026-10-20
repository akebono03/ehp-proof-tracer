"""Guarded single-function installation from the repository root."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

root=Path.cwd()
module=root/'phase165_r52_r9_shared_math.py'
assert module.exists(), 'Run from repository root'
assert (root/'phase166_r3l_all_reference_order'/'phase166_r3l_reference_order.py').exists()
src=module.read_text(encoding='utf-8')
original='''    from phase165_r52_r12_component_bridge import expand_cited_given_components
    return expand_cited_given_components(
        RegistryBridgeResult(registry, tuple(records), tuple(links))
    )'''
replacement='''    from phase165_r52_r12_component_bridge import expand_cited_given_components
    from phase166_r3l_reference_order import connect_all_reference_orders
    joined = expand_cited_given_components(
        RegistryBridgeResult(registry, tuple(records), tuple(links))
    )
    ordered, _order_report = connect_all_reference_orders(joined)
    return ordered'''
if original not in src:
    if replacement in src:
        print('ALREADY APPLIED: '+str(module))
    else:
        raise RuntimeError('Current function does not match reviewed anchor; no patch applied')
else:
    backup=root/'phase166_r3l_all_reference_order'/'backup'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup.mkdir(parents=True,exist_ok=True)
    shutil.copy2(module,backup/module.name)
    module.write_text(src.replace(original,replacement,1),encoding='utf-8')
    print('PATCHED:',module,'BACKUP:',backup)
shutil.copy2(root/'phase166_r3l_all_reference_order'/'phase166_r3l_reference_order.py',root/'phase166_r3l_reference_order.py')
text=module.read_text(encoding='utf-8')
node=next(n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name=='build_shared_typed_bridge')
print('FULL MODIFIED FUNCTION:')
print('\n'.join(text.splitlines()[node.lineno-1:node.end_lineno]))
