"""Phase 165 R52-R13-R3: guarded compatibility fix for legacy component schema."""
from pathlib import Path
import shutil

root = Path.cwd()
source = root / 'phase165_typed_component_lookup.py'
if not source.is_file():
    raise SystemExit('Missing phase165_typed_component_lookup.py; no changes made')
old = '''        if (is_dataclass(value) and not isinstance(value, type)
                and (type(value).__name__ == "TodaProp51FiniteDimensionalStatement"
                     or (isinstance(assertion.scope, tuple)
                         and len(assertion.scope) == 2
                         and assertion.scope[0] == "typed_composite_fields"
                         and assertion.scope[1] == tuple(field.name for field in fields(value))))):
'''
new = '''        component_fields = (
            tuple(field.name for field in fields(value))
            if is_dataclass(value) and not isinstance(value, type) else ()
        )
        legacy_prop51_fields = (
            "pi3_2_group_relation",
            "eta2_hopf_relation",
            "delta_iota5_relation",
            "higher_eta_group_relation",
        )
        explicitly_declared = (
            isinstance(assertion.scope, tuple)
            and len(assertion.scope) == 2
            and assertion.scope[0] == "typed_composite_fields"
            and assertion.scope[1] == component_fields
        )
        if component_fields and (
            explicitly_declared or component_fields == legacy_prop51_fields
        ):
'''
current = source.read_text(encoding='utf-8')
if new in current:
    print('Already installed: phase165_typed_component_lookup.py')
elif current.count(old) != 1:
    raise SystemExit('Guard mismatch: expected R52-R13-R2 code not found; no changes made')
else:
    backup = source.with_name(source.name + '.r52_r13_r3_backup')
    if not backup.exists():
        shutil.copy2(source, backup)
    source.write_text(current.replace(old, new), encoding='utf-8')
    print('Updated: phase165_typed_component_lookup.py')
package = Path(__file__).resolve().parent
shutil.copy2(package / 'test_phase165_r52_r13_r3_compat_fix.py', root / 'test_phase165_r52_r13_r3_compat_fix.py')
print('R52-R13-R3 legacy schema compatibility installed')
