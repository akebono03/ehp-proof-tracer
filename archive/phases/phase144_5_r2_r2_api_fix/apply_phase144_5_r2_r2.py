from pathlib import Path
import shutil

repo = Path.cwd()
package = Path(__file__).resolve().parent

shutil.copyfile(
  package / "toda_group_proof_narrative_equation_numbering.py",
  repo / "toda_group_proof_narrative_equation_numbering.py",
)
shutil.copyfile(
  package / "test_phase144_5_r2_r2_api.py",
  repo / "tests" / "test_phase144_5_r2_r2_api.py",
)

renderer = repo / "toda_group_proof_narrative_argument_multi_renderer.py"
text = renderer.read_text(encoding="utf-8-sig")
old = """number_toda_group_proof_narrative_equations(
      rendered
    )"""
new = """number_toda_group_proof_narrative_equations(
      rendered,
      presentation,
      blocks,
    )"""
if new not in text:
  if old not in text:
    raise RuntimeError("numbering call not found")
  text = text.replace(old, new, 1)
renderer.write_text(text, encoding="utf-8")

print("Phase 144-5-R2-R2 applied.")
print("Directly replaced equation-numbering module with 3-argument API.")
