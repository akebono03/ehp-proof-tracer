"""R52-R13-R2 guarded installer; apply only the verified prior state."""
from pathlib import Path
import shutil

root = Path.cwd()
package = Path(__file__).resolve().parent
changes = (
    (
        'phase165_r52_r13_reference_registration.py',
        '        kind=AssertionKind.STATEMENT, content=content,\n        origin=AssertionOrigin.FIXED_STATEMENT,\n',
        '        kind=AssertionKind.STATEMENT, content=content,\n        origin=AssertionOrigin.FIXED_STATEMENT,\n        scope=("typed_composite_fields", tuple(part.name for part in parts)),\n',
    ),
    (
        'phase165_typed_component_lookup.py',
        '        if (is_dataclass(value) and not isinstance(value, type)\n                and type(value).__name__ in ("TodaProp51FiniteDimensionalStatement", "CompositeFact")):\n',
        '        if (is_dataclass(value) and not isinstance(value, type)\n                and (type(value).__name__ == "TodaProp51FiniteDimensionalStatement"\n                     or (isinstance(assertion.scope, tuple)\n                         and len(assertion.scope) == 2\n                         and assertion.scope[0] == "typed_composite_fields"\n                         and assertion.scope[1] == tuple(field.name for field in fields(value))))):\n',
    ),
    (
        'phase165_r52_r7_registered_common_proof.py',
        '        if root is None or root.rule is not ProofRule.INFERENCE:\n            raise GoalSearchIncompleteError("completed proof is not an inference")\n',
        '        if root is None or root.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE):\n            raise GoalSearchIncompleteError("completed proof is not a typed proof step")\n',
    ),
)
prepared = []
for filename, before, after in changes:
    path = root / filename
    if not path.is_file():
        raise SystemExit(f'Missing dependency: {filename}')
    data = path.read_text(encoding='utf-8')
    if after in data:
        print('Already installed:', filename)
        continue
    if data.count(before) != 1:
        raise SystemExit(f'Guard mismatch, no files changed: {filename}')
    prepared.append((path, data.replace(before, after)))
for path, updated in prepared:
    backup = path.with_name(path.name + '.r52_r13_r2_backup')
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(updated, encoding='utf-8')
    print('Updated:', path.name)
shutil.copy2(package / 'test_phase165_r52_r13_r2_generic_reference_fix.py', root / 'test_phase165_r52_r13_r2_generic_reference_fix.py')
print('R52-R13-R2 generic reference and narrative guards installed')
