from pathlib import Path


PATH = Path("toda_proof_narrative_renderer.py")
BACKUP = Path(
  "toda_proof_narrative_renderer.py.phase143_75s_backup"
)


def main():
  text = PATH.read_text(
    encoding="utf-8"
  )

  if not BACKUP.exists():
    BACKUP.write_text(
      text,
      encoding="utf-8",
    )

  import_anchor = (
    "from toda_rules import (\n"
  )
  import_name = (
    "  Toda58WhiteheadSquareUpToSignStatement,\n"
  )

  if import_name not in text:
    index = text.find(import_anchor)
    if index < 0:
      raise RuntimeError(
        "toda_rules import block not found"
      )

    insert_at = (
      index
      + len(import_anchor)
    )
    text = (
      text[:insert_at]
      + import_name
      + text[insert_at:]
    )

  marker = (
    "  if isinstance(\n"
    "    statement,\n"
    "    TodaDeltaImageUpToSignStatement,\n"
    "  ):\n"
  )

  block = (
    "  if isinstance(\n"
    "    statement,\n"
    "    Toda58WhiteheadSquareUpToSignStatement,\n"
    "  ):\n"
    "    positive_value_latex = (\n"
    "      render_toda_expression_latex(\n"
    "        statement.positive_value\n"
    "      )\n"
    "    )\n"
    "\n"
    "    if isinstance(\n"
    "      statement.positive_value,\n"
    "      Sum,\n"
    "    ):\n"
    "      positive_value_latex = (\n"
    "        r\"\\left(\"\n"
    "        + positive_value_latex\n"
    "        + r\"\\right)\"\n"
    "      )\n"
    "\n"
    "    return (\n"
    "      render_toda_expression_latex(\n"
    "        statement.whitehead_square\n"
    "      )\n"
    "      + r\" = \\pm \"\n"
    "      + positive_value_latex\n"
    "    )\n"
    "\n"
  )

  if block not in text:
    index = text.find(marker)
    if index < 0:
      raise RuntimeError(
        "TodaDeltaImageUpToSignStatement "
        "renderer anchor not found"
      )

    text = (
      text[:index]
      + block
      + text[index:]
    )

  PATH.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "Phase 143-75S repair applied."
  )
  print(
    "Backup:",
    BACKUP,
  )


if __name__ == "__main__":
  main()
