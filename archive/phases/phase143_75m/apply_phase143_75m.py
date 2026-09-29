from pathlib import Path
import shutil

PATH = Path("toda_group_proof_narrative_renderer.py")
BACKUP = Path(
  "toda_group_proof_narrative_renderer.py.phase143_75m_backup"
)

if not PATH.exists():
  raise SystemExit(
    "toda_group_proof_narrative_renderer.py was not found."
  )

text = PATH.read_text(encoding="utf-8")
shutil.copy2(PATH, BACKUP)

raw_import = "  render_toda_raw_group_structure_latex,\n"
if raw_import not in text:
  marker = (
    "from toda_proof_narrative_renderer import (\n"
  )
  start = text.find(marker)
  if start < 0:
    raise SystemExit(
      "toda_proof_narrative_renderer import block was not found."
    )
  end = text.find(
    ")\n",
    start + len(marker),
  )
  if end < 0:
    raise SystemExit(
      "toda_proof_narrative_renderer import block end was not found."
    )
  text = (
    text[:end]
    + raw_import
    + text[end:]
  )

helper = r'''def _render_finite_dimensional_aggregate_statement_latex(
  statement,
) -> str | None:
  target_names = {
    "TodaProp53FiniteDimensionalStatement",
    "TodaProp58FiniteDimensionalStatement",
    "TodaProp59FiniteDimensionalStatement",
    "TodaProp511NuSquaredFiniteDimensionalStatement",
  }

  if type(statement).__name__ not in target_names:
    return None

  parts = []
  range_latex = None

  for field_name in statement.__dataclass_fields__:
    value = getattr(
      statement,
      field_name,
    )

    if isinstance(
      value,
      Relation,
    ):
      if (
        value.relation_type
        != RelationType.EQUALITY
      ):
        return None

      parts.append(
        render_toda_primary_group_latex(
          value.lhs
        )
        + " = "
        + render_toda_raw_group_structure_latex(
          value.rhs
        )
      )
      continue

    if (
      type(value).__name__
      == "TodaPrimaryGroupZeroStatement"
    ):
      parts.append(
        render_toda_primary_group_latex(
          value.group
        )
        + " = 0"
      )
      continue

    if (
      type(value).__name__
      == "ScalarGreaterEqualStatement"
    ):
      range_latex = (
        _render_scalar_latex(
          value.left
        )
        + r" \ge "
        + _render_scalar_latex(
          value.right
        )
      )

  if not parts:
    return None

  latex = r",\quad ".join(parts)

  if range_latex is not None:
    latex += (
      r"\qquad ("
      + range_latex
      + ")"
    )

  return latex
'''

helper_marker = (
  "def _render_finite_dimensional_aggregate_statement_latex(\n"
)
if helper_marker not in text:
  insertion = text.find(
    "def _render_group_proof_narrative_latex(\n"
  )
  if insertion < 0:
    raise SystemExit(
      "_render_group_proof_narrative_latex was not found."
    )
  text = (
    text[:insertion]
    + helper
    + "\n\n"
    + text[insertion:]
  )

needle = (
  "  statement = proof_step.conclusion\n"
  "\n"
  "  try:\n"
)
replacement = (
  "  statement = proof_step.conclusion\n"
  "\n"
  "  finite_dimensional_latex = (\n"
  "    _render_finite_dimensional_aggregate_statement_latex(\n"
  "      statement\n"
  "    )\n"
  "  )\n"
  "\n"
  "  if finite_dimensional_latex is not None:\n"
  "    return finite_dimensional_latex\n"
  "\n"
  "  try:\n"
)
if replacement not in text:
  if needle not in text:
    raise SystemExit(
      "Insertion point inside "
      "_render_group_proof_narrative_latex was not found."
    )
  text = text.replace(
    needle,
    replacement,
    1,
  )

PATH.write_text(
  text,
  encoding="utf-8",
)

TEST_SOURCE = Path(
  "phase143_75m/test_phase143_75m_finite_dimensional_semantic_rendering.py"
)
TEST_DESTINATION = Path(
  "tests/test_phase143_75m_finite_dimensional_semantic_rendering.py"
)
if not TEST_SOURCE.exists():
  raise SystemExit(
    "Phase 143-75M focused test source was not found."
  )
shutil.copy2(
  TEST_SOURCE,
  TEST_DESTINATION,
)

print(
  "Phase 143-75M production patch applied."
)
print(
  "Backup:",
  BACKUP,
)
