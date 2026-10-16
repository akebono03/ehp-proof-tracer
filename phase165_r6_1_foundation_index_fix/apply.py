from pathlib import Path
import ast, json, shutil
root = Path(__file__).resolve().parent.parent
target = root / "phase165_r14_r36_adopted_backward.py"
source = target.read_text(encoding="utf-8-sig")
old = "foundation_goal = instantiate_foundational_identity_suspension(2).statement"
new = "foundation_goal = instantiate_foundational_identity_suspension(1).statement"
if old in source:
    if source.count(old) != 1:
        raise RuntimeError("ambiguous foundational statement")
    updated = source.replace(old, new)
    ast.parse(updated)
    backup = target.with_name(target.name + ".r6_1_foundation_index_before.bak")
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(updated, encoding="utf-8")
    status = "CHANGED"
elif new in source:
    status = "ALREADY_INSTALLED"
else:
    raise RuntimeError("expected adopted_leaf_steps implementation not found")
print(json.dumps({"status":status, "modified_file":str(target.relative_to(root)), "full_pytest_run":False}, indent=2))
