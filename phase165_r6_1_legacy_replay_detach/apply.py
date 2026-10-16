from pathlib import Path
import ast, shutil, json
root = Path(__file__).resolve().parent.parent
files = ("phase165_r14_r40_replay.py", "phase165_r14_r41_proof_transfer.py")
for name in files:
    target = root / name
    old = target.read_text(encoding="utf-8-sig")
    if "reconstruct_registered_pi32" not in old and "build_registered_common_replay" not in old:
        raise RuntimeError(f"unexpected old file {name}")
    replacement = (Path(__file__).resolve().parent / name).read_text(encoding="utf-8")
    ast.parse(replacement)
    if old != replacement:
        backup = target.with_name(target.name + ".r6_1_detach_before.bak")
        if not backup.exists():
            shutil.copy2(target,backup)
        target.write_text(replacement, encoding="utf-8")
print(json.dumps({"status":"DELEGATED","files":files,"full_pytest_run":False},indent=2))
