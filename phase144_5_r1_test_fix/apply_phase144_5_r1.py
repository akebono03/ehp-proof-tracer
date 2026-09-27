from pathlib import Path
import shutil


repo = Path.cwd()
package = Path(__file__).resolve().parent

target = (
  repo
  / "tests"
  / "test_phase144_5_generic_definition_order_equations.py"
)

shutil.copyfile(
  package / "test_phase144_5_generic_definition_order_equations.py",
  target,
)

print("Phase 144-5-R1 test correction applied.")
print("Modified:")
print("  tests/test_phase144_5_generic_definition_order_equations.py")
print("")
print("Production source files were not changed by R1.")
