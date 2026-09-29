from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
source = (
  package_root
  / "payload"
  / "tests"
  / "test_phase135_1_web_narrative_display_math.py"
)
target = (
  Path.cwd()
  / "tests"
  / "test_phase135_1_web_narrative_display_math.py"
)

if not target.exists():
  raise RuntimeError(
    "tests/test_phase135_1_web_narrative_display_math.py "
    "not found"
  )

shutil.copy2(
  source,
  target,
)

print("Phase 144-6 Public Route Cutover R3 applied.")
print("Production code changes: none.")
print(
  "Replaced: tests/"
  "test_phase135_1_web_narrative_display_math.py"
)
