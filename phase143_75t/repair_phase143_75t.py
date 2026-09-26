from pathlib import Path


PATH = Path("toda_proof_narrative_renderer.py")
BACKUP = Path(
  "toda_proof_narrative_renderer.py.phase143_75t_backup"
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
    "  Toda58EquationStatement,\n"
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
    "    Toda58WhiteheadSquareUpToSignStatement,\n"
    "  ):\n"
  )

  block = (
    "  if isinstance(\n"
    "    statement,\n"
    "    Toda58EquationStatement,\n"
    "  ):\n"
    "    delta_nu_relation = (\n"
    "      statement.delta_nu_relation\n"
    "    )\n"
    "    whitehead_nu_relation = (\n"
    "      statement.whitehead_nu_relation\n"
    "    )\n"
    "    delta_whitehead_relation = (\n"
    "      statement.delta_whitehead_relation\n"
    "    )\n"
    "\n"
    "    if not (\n"
    "      isinstance(\n"
    "        delta_nu_relation,\n"
    "        TodaDeltaImageUpToSignStatement,\n"
    "      )\n"
    "      and isinstance(\n"
    "        whitehead_nu_relation,\n"
    "        Toda58WhiteheadSquareUpToSignStatement,\n"
    "      )\n"
    "      and isinstance(\n"
    "        delta_whitehead_relation,\n"
    "        TodaDeltaImageUpToSignStatement,\n"
    "      )\n"
    "      and delta_nu_relation.map\n"
    "      == delta_whitehead_relation.map\n"
    "      and delta_nu_relation.element\n"
    "      == delta_whitehead_relation.element\n"
    "      and delta_nu_relation.positive_value\n"
    "      == whitehead_nu_relation.positive_value\n"
    "      and delta_whitehead_relation.positive_value\n"
    "      == whitehead_nu_relation.whitehead_square\n"
    "    ):\n"
    "      return None\n"
    "\n"
    "    positive_value_latex = (\n"
    "      render_toda_expression_latex(\n"
    "        delta_nu_relation.positive_value\n"
    "      )\n"
    "    )\n"
    "\n"
    "    if isinstance(\n"
    "      delta_nu_relation.positive_value,\n"
    "      Sum,\n"
    "    ):\n"
    "      positive_value_latex = (\n"
    "        r\"\\left(\"\n"
    "        + positive_value_latex\n"
    "        + r\"\\right)\"\n"
    "      )\n"
    "\n"
    "    return (\n"
    "      r\"\\Delta\\left(\"\n"
    "      + render_toda_expression_latex(\n"
    "        delta_nu_relation.element\n"
    "      )\n"
    "      + r\"\\right)\"\n"
    "      + r\" = \\pm \"\n"
    "      + positive_value_latex\n"
    "      + r\" = \\pm \"\n"
    "      + render_toda_expression_latex(\n"
    "        whitehead_nu_relation.whitehead_square\n"
    "      )\n"
    "    )\n"
    "\n"
  )

  if block not in text:
    index = text.find(marker)
    if index < 0:
      raise RuntimeError(
        "Toda58WhiteheadSquareUpToSignStatement "
        "renderer anchor not found. "
        "Phase 143-75S must be applied first."
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
    "Phase 143-75T repair applied."
  )
  print(
    "Backup:",
    BACKUP,
  )


if __name__ == "__main__":
  main()
