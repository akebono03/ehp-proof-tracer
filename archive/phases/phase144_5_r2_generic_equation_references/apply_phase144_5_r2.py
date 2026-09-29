from pathlib import Path
import shutil


repo = Path.cwd()
package = Path(__file__).resolve().parent

shutil.copyfile(
  package / "toda_group_proof_narrative_equation_numbering.py",
  repo / "toda_group_proof_narrative_equation_numbering.py",
)

shutil.copyfile(
  package / "test_phase144_5_generic_definition_order_equations.py",
  repo
  / "tests"
  / "test_phase144_5_generic_definition_order_equations.py",
)

print("Phase 144-5-R2 applied.")
print("Modified:")
print("  toda_group_proof_narrative_equation_numbering.py")
print("  tests/test_phase144_5_generic_definition_order_equations.py")
print("")
print("No CLI/Web/legacy renderer changes were made.")
