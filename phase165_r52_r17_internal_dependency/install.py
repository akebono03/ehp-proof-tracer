"""Install R17 minimal additive integration in an already-patched Phase 165 tree."""
from pathlib import Path
import ast
import shutil
import sys

root = Path.cwd()
package = Path(__file__).resolve().parent
if not (root / "phase165_r52_r16_web_citation_gate.py").exists():
    raise SystemExit("R16 must be installed in the repository root")

patches = {
    "phase165_r3_recursive_search.py": [
        ('    progress_observer: Callable[[str, object, ProofStep | None], None] | None = None,',
         '    progress_observer: Callable[[str, object, ProofStep | None], None] | None = None,\n    completed_internal_proofs: tuple = (),'),
        ('        active.append(target)\n        try:',
         '        active.append(target)\n        try:\n            if completed_internal_proofs:\n                from phase165_r52_r17_internal_dependency import find_reusable_internal_proof\n                internal = find_reusable_internal_proof(target, goal, completed_internal_proofs)\n                if internal is not None:\n                    solved.append((target, internal))\n                    report("proved", target, internal)\n                    return internal'),
    ],
    "phase165_r52_r2_search_adapter.py": [
        ('    references: tuple[str, ...] = (),',
         '    references: tuple[str, ...] = (),\n    completed_internal_proofs: tuple = (),'),
        ('            progress_observer=observer,',
         '            progress_observer=observer,\n            completed_internal_proofs=completed_internal_proofs,'),
    ],
    "phase165_r52_r9_shared_math.py": [
        ('                              expansion_provider=None):',
         '                              expansion_provider=None, completed_internal_proofs: tuple = ()):'),
        ('        structure_status=GroupStructureStatus.UNKNOWN,',
         '        structure_status=GroupStructureStatus.UNKNOWN,\n        completed_internal_proofs=completed_internal_proofs,'),
    ],
}

for filename, changes in patches.items():
    path = root / filename
    if not path.exists():
        raise SystemExit(f"Missing {filename}")
    original = path.read_text(encoding="utf-8")
    updated = original
    for old, new in changes:
        if new in updated:
            continue
        if updated.count(old) != 1:
            raise SystemExit(f"Unexpected R17 insertion site: {filename}: {old!r}")
        updated = updated.replace(old, new, 1)
    ast.parse(updated)
    if updated != original:
        shutil.copy2(path, path.with_name(path.stem + ".r17_before.py.bak"))
        path.write_text(updated, encoding="utf-8")
        print("Updated:", filename)
    else:
        print("Already installed:", filename)

for name in ("phase165_r52_r17_internal_dependency.py", "test_phase165_r52_r17_internal_dependency.py"):
    shutil.copy2(package / name, root / name)
print("R52-R17 internal proof dependency support installed")
