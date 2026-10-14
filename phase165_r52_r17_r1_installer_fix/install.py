"""R17-R1: resume the partially installed R17 patch safely."""
from pathlib import Path
import ast
import re
import shutil

root = Path.cwd()
package = Path(__file__).resolve().parent
if not (root / "phase165_r52_r16_web_citation_gate.py").exists():
    raise SystemExit("Run from repository root with R16 installed")

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
}

def apply_text_patches(filename: str, content: str) -> str:
    for old, new in patches[filename]:
        if new in content:
            continue
        if content.count(old) != 1:
            raise SystemExit(f"Unexpected R17 insertion site in {filename}: {old!r}")
        content = content.replace(old, new, 1)
    return content

def apply_shared_search_patch(content: str) -> str:
    tree = ast.parse(content)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "search_shared_group_goal"]
    if len(matches) != 1:
        raise SystemExit("Expected exactly one search_shared_group_goal function")
    node = matches[0]
    lines = content.splitlines(keepends=True)
    head = "".join(lines[node.lineno - 1:node.body[0].lineno - 1])
    if not any(arg.arg == "completed_internal_proofs" for arg in node.args.args + node.args.kwonlyargs):
        pattern = r"(def\s+search_shared_group_goal\s*\()(.*?)(\)\s*(?:->\s*[^:]+)?\s*:)"
        match = re.search(pattern, head, re.DOTALL)
        if match is None:
            raise SystemExit("Could not locate the R16 search function signature")
        args = match.group(2)
        suffix = "completed_internal_proofs: tuple = ()"
        if not args.strip():
            args = suffix
        elif args.rstrip().endswith(","):
            args += " " + suffix
        else:
            args += ", " + suffix
        new_head = head[:match.start()] + match.group(1) + args + match.group(3) + head[match.end():]
        content = content.replace(head, new_head, 1)
    if "completed_internal_proofs=completed_internal_proofs," not in content:
        anchor = "        structure_status=GroupStructureStatus.UNKNOWN,"
        if content.count(anchor) != 1:
            raise SystemExit("Unexpected R16 shared search call; no changes applied")
        content = content.replace(anchor, anchor + "\n        completed_internal_proofs=completed_internal_proofs,", 1)
    return content

updates = {}
for filename in (*patches, "phase165_r52_r9_shared_math.py"):
    path = root / filename
    if not path.exists():
        raise SystemExit(f"Missing {filename}")
    original = path.read_text(encoding="utf-8")
    updated = (apply_shared_search_patch(original) if filename == "phase165_r52_r9_shared_math.py" else apply_text_patches(filename, original))
    ast.parse(updated)
    updates[filename] = (original, updated)

for filename, (original, updated) in updates.items():
    if original != updated:
        path = root / filename
        shutil.copy2(path, path.with_name(path.stem + ".r17_r1_before.py.bak"))
        path.write_text(updated, encoding="utf-8")
        print("Updated:", filename)
    else:
        print("Already installed:", filename)
for name in ("phase165_r52_r17_internal_dependency.py", "test_phase165_r52_r17_internal_dependency.py"):
    shutil.copy2(package / name, root / name)
print("R52-R17-R1 partial-install recovery complete")
