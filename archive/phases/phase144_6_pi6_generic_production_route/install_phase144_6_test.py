from pathlib import Path
import shutil

repo=Path.cwd()
package=Path(__file__).resolve().parent
shutil.copyfile(
  package/"test_phase144_6_pi6_generic_production_route.py",
  repo/"tests"/"test_phase144_6_pi6_generic_production_route.py",
)
print("Phase 144-6 test installed.")
