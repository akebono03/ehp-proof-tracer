from pathlib import Path

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(
  path.suffix + ".phase143_75ae_backup"
)
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

import_anchor = '''  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)'''
import_replacement = '''  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
  TodaSuspensionZeroStatement,
)'''

if "  TodaSuspensionZeroStatement,\n" not in text:
  if import_anchor not in text:
    raise RuntimeError(
      "Toda rules import anchor not found"
    )
  text = text.replace(
    import_anchor,
    import_replacement,
    1,
  )

branch = '''  if isinstance(
    statement,
    TodaSuspensionZeroStatement,
  ):
    return (
      _render_toda_group_map_latex(
        statement.map
      )
      + r" \\text{ is the zero map}"
    )

'''

if branch not in text:
  anchor = '''  if isinstance(
    statement,
    TodaSuspensionSurjectiveStatement,
  ):
    return (
      _render_toda_group_map_latex(
        statement.map
      )
      + r" \\text{ is surjective}"
    )

'''
  if anchor not in text:
    raise RuntimeError(
      "Suspension-surjective branch anchor not found"
    )
  text = text.replace(
    anchor,
    anchor + branch,
    1,
  )

path.write_text(text, encoding="utf-8")
print(
  "Phase 143-75AE semantic renderer patch applied."
)
