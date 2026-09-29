from pathlib import Path

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(path.suffix + ".phase143_75ag_backup")
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

import_name = "  TodaLemma510BracketModuloStatement,\n"
if import_name not in text:
  block_start = text.find("from toda_rules import (\n")
  if block_start == -1:
    raise RuntimeError("from toda_rules import block not found")
  block_end = text.find("\n)\n", block_start)
  if block_end == -1:
    raise RuntimeError("end of toda_rules import block not found")
  text = text[:block_end] + "\n" + import_name.rstrip("\n") + text[block_end:]

branch = """  if isinstance(
    statement,
    TodaLemma510BracketModuloStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.element
      )
      + r" \\in "
      + render_toda_expression_latex(
        statement.bracket
      )
      + r" \\pmod{"
      + render_toda_scalar_latex(
        statement.modulus
      )
      + render_toda_primary_group_latex(
        statement.ambient_group
      )
      + r"}"
    )

"""

if branch not in text:
  markers = [
    "  if isinstance(\n    statement,\n    TodaLemma510HopfBracketContainsStatement,\n  ):\n",
    "  if isinstance(\n    statement,\n    TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,\n  ):\n",
  ]
  insert_at = -1
  for marker in markers:
    insert_at = text.find(marker)
    if insert_at != -1:
      break
  if insert_at == -1:
    raise RuntimeError("Phase 143-75AG renderer insertion marker not found")
  text = text[:insert_at] + branch + text[insert_at:]

path.write_text(text, encoding="utf-8")
print("Phase 143-75AG semantic renderer patch applied.")
