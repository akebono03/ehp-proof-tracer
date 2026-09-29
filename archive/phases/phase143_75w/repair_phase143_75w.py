from pathlib import Path


PATH = Path("toda_proof_narrative_renderer.py")
BACKUP = Path(
  "toda_proof_narrative_renderer.py.phase143_75w_backup"
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
    "  Toda54BracketUpToSignStatement,\n"
  )

  if import_name not in text:
    index = text.find(
      import_anchor
    )
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
    "def render_toda_proof_statement_latex(\n"
    "  statement,\n"
    ") -> str | None:\n"
  )

  branch = (
    "  if isinstance(\n"
    "    statement,\n"
    "    Toda54BracketUpToSignStatement,\n"
    "  ):\n"
    "    return (\n"
    "      render_toda_expression_latex(\n"
    "        statement.bracket\n"
    "      )\n"
    "      + r\" = \\{\\pm \"\n"
    "      + render_toda_expression_latex(\n"
    "        statement.positive_value\n"
    "      )\n"
    "      + r\"\\}\"\n"
    "    )\n"
    "\n"
  )

  if branch not in text:
    index = text.find(
      marker
    )
    if index < 0:
      raise RuntimeError(
        "render_toda_proof_statement_latex "
        "function not found"
      )

    insert_at = (
      index
      + len(marker)
    )
    text = (
      text[:insert_at]
      + branch
      + text[insert_at:]
    )

  PATH.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "Phase 143-75W repair applied."
  )
  print(
    "Backup:",
    BACKUP,
  )


if __name__ == "__main__":
  main()
