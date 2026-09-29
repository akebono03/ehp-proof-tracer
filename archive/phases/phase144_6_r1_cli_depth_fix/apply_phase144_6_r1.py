from pathlib import Path
import shutil

repo = Path.cwd()
package = Path(__file__).resolve().parent

target = repo / "tests" / "test_phase144_6_pi6_generic_production_route.py"
shutil.copyfile(
  package / "test_phase144_6_pi6_generic_production_route.py",
  target,
)

print("Phase 144-6-R1 applied.")
print("Changed only: tests/test_phase144_6_pi6_generic_production_route.py")
print("CLI test depth: 2 -> 3")
