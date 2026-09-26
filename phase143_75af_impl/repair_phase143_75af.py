from pathlib import Path

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(path.suffix + ".phase143_75af_backup")
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

import_name = "  TodaProp44FirstSummandRestrictionStatement,\n"
if import_name not in text:
  block_start = text.find("from toda_rules import (\n")
  if block_start == -1:
    raise RuntimeError("from toda_rules import block not found")
  block_end = text.find("\n)\n", block_start)
  if block_end == -1:
    raise RuntimeError("end of toda_rules import block not found")
  text = text[:block_end] + "\n" + import_name.rstrip("\n") + text[block_end:]

branch = '''  if isinstance(
    statement,
    TodaProp44FirstSummandRestrictionStatement,
  ):
    first_summand = (
      statement.decomposition_map.source_group.summands[
        0
      ]
    )

    return (
      r"\\left."
      + r"\\left("
      + render_toda_expression_latex(
        statement.decomposition_map.formula
      )
      + r"\\right)"
      + r"\\right|_{"
      + render_toda_primary_group_latex(
        first_summand
      )
      + r"}"
      + r" = "
      + _render_toda_group_map_latex(
        statement.suspension_map
      )
    )

'''

if branch not in text:
  marker = '''  if isinstance(
    statement,
    TodaSuspensionInjectiveStatement,
  ):
'''
  insert_at = text.find(marker)
  if insert_at == -1:
    raise RuntimeError("renderer insertion marker not found")
  text = text[:insert_at] + branch + text[insert_at:]

path.write_text(text, encoding="utf-8")
print("Phase 143-75AF semantic renderer patch applied.")
