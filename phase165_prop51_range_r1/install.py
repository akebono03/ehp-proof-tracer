from pathlib import Path
import ast
import shutil
import json

root = Path(__file__).resolve().parent.parent
patches = {}

p = root / 'phase165_r52_r13_reference_registration.py'
s = p.read_text(encoding='utf-8')
old = 'content: object, reference_kind: ReferenceKind = ReferenceKind.PROPOSITION,\n'
new = 'content: object, reference_kind: ReferenceKind = ReferenceKind.PROPOSITION,\n    clause_ranges: tuple[tuple[str, str, int], ...] = (),\n'
assert old in s
s=s.replace(old,new,1)
old='scope=("typed_composite_fields", tuple(part.name for part in parts)), '
# preserve formatting
old='scope=("typed_composite_fields", tuple(part.name for part in parts)),'
new='scope=("typed_composite_fields", tuple(part.name for part in parts)),\n        # Typed clause applicability metadata (component, scalar variable, lower bound).\n        applicability=clause_ranges,'
# No applicability field on AssertionEntry! instead pack into scope
new='scope=("typed_composite_fields", tuple(part.name for part in parts)),\n        '
# change to scope with third element only for prop51 via keyword argument; preserve existing when no ranges
new='scope=("typed_composite_fields", tuple(part.name for part in parts))\n        + (("clause_ranges", clause_ranges),) if clause_ranges else\n        ("typed_composite_fields", tuple(part.name for part in parts)),'
assert old in s
s=s.replace(old,new,1)
old='content=content,\n    )\n'
# only inside build_adopted_prop51_reference use unique tail
needle='        content=content,\n    )\n'
pos=s.rfind(needle)
assert pos!=-1
s=s[:pos]+s[pos:].replace(needle,'        content=content,\n        clause_ranges=(("higher_eta_group_relation", "n", 4),),\n    )\n',1)
ast.parse(s)
patches[p]=s

p=root/'phase165_r57_r8_eta_specialization.py';s=p.read_text('utf-8')
s=s.replace('sphere_dimension < 3:', 'sphere_dimension < 4:').replace('n < 3:', 'n < 4:').replace('requires n >= 3', 'requires n >= 4').replace('Instantiate n >= 3', 'Instantiate n >= 4')
assert 'n < 3:' not in s
ast.parse(s);patches[p]=s

p=root/'phase165_r57_r20_general_specialization.py';s=p.read_text('utf-8')
old='    if _instantiate(source, bindings) != goal:\n        return None\n    return tuple(sorted(bindings.items()))'
new='    if _instantiate(source, bindings) != goal:\n        return None\n    from phase165_prop51_range_guard import allows_typed_specialization\n    if not allows_typed_specialization(source, bindings):\n        return None\n    return tuple(sorted(bindings.items()))'
assert old in s
s=s.replace(old,new)
ast.parse(s);patches[p]=s

# installation fail closed to avoid unknowingly installing over unrecognized local patches
for target, content in patches.items():
    backup=target.with_name(target.name+'.prop51_range_r1_before.bak')
    if not backup.exists():
        shutil.copy2(target,backup)
    target.write_text(content,encoding='utf-8')
print(json.dumps({'status':'INSTALLED','modified_files':[str(x.name) for x in patches], 'full_pytest_run':False},ensure_ascii=False))
