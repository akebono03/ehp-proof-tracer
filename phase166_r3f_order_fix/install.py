from pathlib import Path
import shutil
from datetime import datetime

root = Path(__file__).resolve().parent.parent
path = root / 'phase165_r12_r7_proof_order_guard.py'
source = path.read_text(encoding='utf-8')
old = '''    if not identified:
        return bridge
    if len(identified) != 1:
'''
new = '''    if not identified:
        # A concrete higher-eta goal is an instance of the fifth registered
        # proposition claim. It must retain that claim's proof-use position.
        from phase165_r57_r8_eta_specialization import (
            _is_generic_eta_group_relation, specialize_eta_group_relation,
        )
        from homotopy_groups import TodaPrimaryGroup
        from proof import Relation

        higher = tuple(
            c for c in claims if c.component_name == "higher_eta_group_relation"
        )
        if len(higher) == 1 and isinstance(target, Relation):
            statement = higher[0].statement
            group = getattr(target, "lhs", None)
            if (_is_generic_eta_group_relation(statement)
                    and isinstance(group, TodaPrimaryGroup)
                    and type(group.sphere_dimension) is int
                    and group.sphere_dimension >= 4
                    and specialize_eta_group_relation(statement, group.sphere_dimension) == target):
                identified = higher
    if not identified:
        return bridge
    if len(identified) != 1:
'''
if source.count(old) != 1:
    raise SystemExit('PATCH REFUSED: expected guard block not found uniquely; no files changed')
backup = root / 'phase166_r3f_order_fix' / 'backup'
backup.mkdir(exist_ok=True)
shutil.copy2(path, backup / path.name)
path.write_text(source.replace(old,new),encoding='utf-8')
print('PATCHED', path)
print('BACKUP', backup / path.name)
