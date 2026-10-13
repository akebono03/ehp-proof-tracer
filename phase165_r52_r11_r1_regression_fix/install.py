"""Install the R52-R11 regression expectation update only."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parent.parent
target = root / "test_phase165_r52_r8_show_proof_route.py"
source = Path(__file__).resolve().parent / target.name

old = '    assert b"search_failed" in response.data'
new = '    assert "証明未完成".encode("utf-8") in response.data'
if not target.is_file():
    raise SystemExit(f"Required existing test file not found: {target}")
current = target.read_text(encoding="utf-8")
if current.count(new) == 1 and old not in current:
    print("Already updated: " + target.name)
    sys.exit(0)
if current.count(old) != 1 or new in current:
    raise SystemExit(
        "Test contents differ from audited R52-R8 test; "
        "no changes made. Please share the current test file."
    )

# Preserve all local test contents other than the one stale assertion.
updated = current.replace(old, new)
import ast
ast.parse(updated)
target.write_text(updated, encoding="utf-8")
print("Updated one R52-R8 test assertion: " + target.name)
