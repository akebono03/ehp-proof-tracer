from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
source = (
  package_root
  / "payload"
  / "tests"
  / "test_phase144_6_public_route_cutover.py"
)
target = (
  Path.cwd()
  / "tests"
  / "test_phase144_6_public_route_cutover.py"
)

if not target.parent.exists():
  raise RuntimeError(
    "repository tests directory not found"
  )

shutil.copy2(
  source,
  target,
)

print("Phase 144-6 Public Route Cutover R2 applied.")
print("Production code changes: none.")
print(
  "Replaced: tests/"
  "test_phase144_6_public_route_cutover.py"
)
