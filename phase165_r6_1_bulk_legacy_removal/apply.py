from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# These historical entrypoints are no longer in the public proof generation route.
DELETE_FILES = (
    "phase165_r14_r37_closure.py",
    "phase165_r14_r40_replay.py",
    "phase165_r14_r41_proof_transfer.py",
)
# Historical tests for these deleted entrypoints only.
TEST_FILES = (
    "phase165_r14_r37_closure/test_phase165_r14_r37_closure.py",
    "phase165_r14_r40_common_renderer/test_phase165_r14_r40_common_renderer.py",
    "phase165_r14_r41_proof_transfer/test_phase165_r14_r41_proof_transfer.py",
)
KEEP = ("phase165_r14_r38_direct_registry.py", "phase165_r52_r9_shared_math.py")
OLD_MODULES = {Path(x).stem for x in DELETE_FILES}

def imports_of(path):
    tree=ast.parse(path.read_text(encoding="utf-8-sig"),filename=str(path))
    result=set()
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            result.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n,ast.ImportFrom) and n.module:
            result.add(n.module.split(".")[0])
    return result

def main():
    missing=[s for s in DELETE_FILES if not (ROOT/s).is_file()]
    if missing:
        raise RuntimeError("Missing old files: "+repr(missing))
    candidates=set(DELETE_FILES)|{x for x in TEST_FILES if (ROOT/x).exists()}
    # Root-level production modules: fail closed if an active root module imports
    # anything due for deletion. Historical backups/installers aren't production.
    external={}
    for path in ROOT.glob("*.py"):
        if path.name in DELETE_FILES or "backup" in path.name.lower():
            continue
        hits=imports_of(path)&OLD_MODULES
        if hits:
            external[str(path.relative_to(ROOT))]=sorted(hits)
    if external:
        raise RuntimeError("Other root modules still import targets: "+repr(external))
    for name in KEEP:
        if not (ROOT/name).exists():
            raise RuntimeError("Required active file missing: "+name)
    archive=ROOT/"phase165_r6_1_removed_legacy_backup"
    archive.mkdir(exist_ok=True)
    removed=[]
    for name in sorted(candidates):
        source=ROOT/name
        backup=archive/name
        backup.parent.mkdir(parents=True,exist_ok=True)
        if backup.exists():
            raise RuntimeError("backup already exists; stop without overwriting: "+name)
        shutil.copy2(source,backup)
    for name in sorted(candidates):
        (ROOT/name).unlink()
        removed.append(name)
    print(json.dumps({"status":"REMOVED","removed_files":removed,
                      "preserved_active_registry":True,
                      "full_pytest_run":False},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
