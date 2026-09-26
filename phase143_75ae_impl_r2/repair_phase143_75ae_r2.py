from pathlib import Path

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

backup = path.with_suffix(path.suffix + ".phase143_75ae_r2_backup")
if not backup.exists():
  backup.write_text(text, encoding="utf-8")

import_name = "  TodaSuspensionZeroStatement,\n"
if import_name not in text:
  block_start = text.find("from toda_rules import (\n")
  if block_start == -1:
    raise RuntimeError("from toda_rules import block not found")
  block_end = text.find("\n)\n", block_start)
  if block_end == -1:
    raise RuntimeError("end of toda_rules import block not found")
  text = text[:block_end] + "\n  TodaSuspensionZeroStatement," + text[block_end:]

branch = (
  "  if isinstance(\n"
  "    statement,\n"
  "    TodaSuspensionZeroStatement,\n"
  "  ):\n"
  "    return (\n"
  "      _render_toda_group_map_latex(\n"
  "        statement.map\n"
  "      )\n"
  "      + r\" \\\\text{ is the zero map}\"\n"
  "    )\n\n"
)

if branch not in text:
  marker = (
    "  if isinstance(\n"
    "    statement,\n"
    "    TodaSuspensionSurjectiveStatement,\n"
    "  ):\n"
  )
  start = text.find(marker)
  if start == -1:
    raise RuntimeError("TodaSuspensionSurjectiveStatement renderer branch not found")
  next_branch = text.find("\n  if isinstance(\n", start + len(marker))
  if next_branch == -1:
    raise RuntimeError("next renderer branch not found")
  text = text[:next_branch + 1] + branch + text[next_branch + 1:]

path.write_text(text, encoding="utf-8")
print("Phase 143-75AE R2 semantic renderer patch applied.")
