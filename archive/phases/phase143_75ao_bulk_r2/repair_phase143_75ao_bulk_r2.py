from pathlib import Path
import ast
import runpy

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

broken = (
  "  Toda211OrdinaryEHPExactnessStatement,\\n"
  "  TodaLemma510HopfBracketContainsStatement,\\n"
  "  TodaLemma510IndexedHopfBracketContainsStatement,\\n"
  "  TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,\\n"
  "  TodaLemma510OrdinarySuspensionImageFiniteStatement,\\n"
  "  TodaLemma510OrdinarySuspensionImageInDoubleStatement,\\n"
  "  TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,\\n"
  "  TodaLemma510Split115Statement,\\n"
)

fixed = (
  "  Toda211OrdinaryEHPExactnessStatement,\n"
  "  TodaLemma510HopfBracketContainsStatement,\n"
  "  TodaLemma510IndexedHopfBracketContainsStatement,\n"
  "  TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,\n"
  "  TodaLemma510OrdinarySuspensionImageFiniteStatement,\n"
  "  TodaLemma510OrdinarySuspensionImageInDoubleStatement,\n"
  "  TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,\n"
  "  TodaLemma510Split115Statement,\n"
)

if broken in text:
  text = text.replace(broken, fixed, 1)
  path.write_text(text, encoding="utf-8")
  print("Repaired literal import newline sequence.")
else:
  print("Literal import newline sequence was not present.")

ast.parse(path.read_text(encoding="utf-8"))
print("Syntax repair passed.")

runpy.run_path(
  "phase143_75ao_bulk_impl/"
  "repair_phase143_75ao_bulk.py",
  run_name="__main__",
)

ast.parse(path.read_text(encoding="utf-8"))
print("Phase 143-75AO bulk R2 patch application passed.")
