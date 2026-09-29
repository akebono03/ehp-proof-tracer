from pathlib import Path

TARGET = Path("toda_proof_narrative_renderer.py")
text = TARGET.read_text(encoding="utf-8")

import_anchor = "from toda_rules import (\n"
import_name = "  TodaLemma54DoubleSuspensionUpToSignStatement,\n"

if import_name not in text:
  index = text.find(import_anchor)
  if index == -1:
    raise SystemExit("Could not locate toda_rules import block.")
  insert_at = index + len(import_anchor)
  text = text[:insert_at] + import_name + text[insert_at:]

branch = """  if isinstance(
    statement,
    TodaLemma54DoubleSuspensionUpToSignStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.left
      )
      + r" = \\pm "
      + render_toda_expression_latex(
        statement.positive_value
      )
    )

"""

literature_anchor = """  if isinstance(
    statement,
    LiteratureStatement,
  ):
"""

if branch not in text:
  index = text.find(literature_anchor)
  if index == -1:
    raise SystemExit("Could not locate LiteratureStatement branch.")
  text = text[:index] + branch + text[index:]

backup = TARGET.with_suffix(TARGET.suffix + ".phase143_75ad_backup")
if not backup.exists():
  backup.write_text(TARGET.read_text(encoding="utf-8"), encoding="utf-8")

TARGET.write_text(text, encoding="utf-8")
print("Phase 143-75AD semantic renderer patch applied.")
