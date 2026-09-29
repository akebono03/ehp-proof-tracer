from pathlib import Path
import shutil

source = (
  Path(__file__).resolve().parent
  / "payload"
  / "tests"
  / "test_phase144_6_public_route_cutover.py"
)
target = (
  Path.cwd()
  / "tests"
  / "test_phase144_6_public_route_cutover.py"
)

target.parent.mkdir(
  parents=True,
  exist_ok=True,
)
shutil.copy2(
  source,
  target,
)

print(
  "Installed: tests/"
  "test_phase144_6_public_route_cutover.py"
)
