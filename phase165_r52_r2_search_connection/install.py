"""Minimal guarded replacement of one canonical search function."""
from pathlib import Path
import ast

root = Path.cwd()
package = Path(__file__).resolve().parent
engine = root / "phase165_r3_recursive_search.py"
base = root / "phase165_r52_partial_proof.py"
if not engine.is_file() or not base.is_file():
    raise SystemExit("Required R3 engine and R52 model must already be installed")
source = engine.read_text(encoding="utf-8")
tree = ast.parse(source)
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "reconstruct_registered_goal"]
if len(functions) != 1:
    raise SystemExit("Expected exactly one reconstruct_registered_goal function")
node = functions[0]
old = "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno])
if "progress_observer:" in old:
    if 'report("proved", target, step)' not in old:
        raise SystemExit("Existing observer implementation differs; refusing overwrite")
    print("R52-R2 progress observer already present")
else:
    required = (
        'lookup_mode: str = "legacy"',
        'solved: list[tuple[object, ProofStep]] = []',
        'raise RegisteredGoalUnresolved(',
        'return resolve(goal)',
    )
    if not all(fragment in old for fragment in required):
        raise SystemExit("Canonical search differs from audited version; refusing overwrite")
    replacement = (package / "reconstruct_registered_goal.py.txt").read_text(encoding="utf-8").rstrip("\n")
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [replacement + "\n"]
    candidate = "".join(lines)
    ast.parse(candidate)
    engine.write_text(candidate, encoding="utf-8")
    print("R52-R2 observer added to canonical recursive search")

for name in (
    "phase165_r52_r2_search_adapter.py",
    "test_phase165_r52_r2_search_adapter.py",
    "test_phase165_r52_r2_engine_observer.py",
):
    (root / name).write_bytes((package / name).read_bytes())
    print("Installed", name)
