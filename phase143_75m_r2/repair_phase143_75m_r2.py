from pathlib import Path
import shutil

PATH = Path("toda_group_proof_narrative_renderer.py")
BACKUP = Path(
  "toda_group_proof_narrative_renderer.py.phase143_75m_r2_backup"
)

if not PATH.exists():
  raise SystemExit(
    "toda_group_proof_narrative_renderer.py was not found."
  )

text = PATH.read_text(encoding="utf-8")
shutil.copy2(PATH, BACKUP)

IMPORT_BLOCK = (
  "from toda_proof_narrative_renderer import (\n"
)
RAW_IMPORT = (
  "  render_toda_raw_group_structure_latex,\n"
)

if RAW_IMPORT not in text:
  import_start = text.find(IMPORT_BLOCK)
  if import_start < 0:
    raise SystemExit(
      "toda_proof_narrative_renderer import block was not found."
    )
  import_end = text.find(
    "\n)\n",
    import_start,
  )
  if import_end < 0:
    raise SystemExit(
      "toda_proof_narrative_renderer import block end was not found."
    )
  text = (
    text[:import_end]
    + "\n"
    + RAW_IMPORT.rstrip("\n")
    + text[import_end:]
  )

HELPER_NAME = (
  "def _render_finite_dimensional_aggregate_statement_latex(\n"
)

HELPER = '''def _render_finite_dimensional_aggregate_statement_latex(
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
        + r" \\ge "
        + _render_scalar_latex(
          value.right
        )
      )

  if not parts:
    return None

  latex = r",\\quad ".join(parts)

  if range_latex is not None:
    latex += (
      r"\\qquad ("
      + range_latex
      + ")"
    )

  return latex
'''

FUNCTION_ANCHOR = (
  "def _render_group_proof_narrative_latex(\n"
)

if HELPER_NAME not in text:
  function_start = text.find(FUNCTION_ANCHOR)
  if function_start < 0:
    raise SystemExit(
      "_render_group_proof_narrative_latex was not found."
    )
  text = (
    text[:function_start]
    + HELPER
    + "\n\n"
    + text[function_start:]
  )

CALL_MARKER = (
  "  finite_dimensional_latex = (\n"
  "    _render_finite_dimensional_aggregate_statement_latex(\n"
)

if CALL_MARKER not in text:
  function_start = text.find(FUNCTION_ANCHOR)
  fact_start = text.find(
    "def _render_group_proof_narrative_fact(\n",
    function_start,
  )
  if function_start < 0 or fact_start < 0:
    raise SystemExit(
      "Narrative function boundaries were not found."
    )

  statement_line = (
    "  statement = proof_step.conclusion\n"
  )
  statement_pos = text.find(
    statement_line,
    function_start,
    fact_start,
  )
  if statement_pos < 0:
    raise SystemExit(
      "statement assignment inside "
      "_render_group_proof_narrative_latex was not found."
    )

  insert_pos = statement_pos + len(statement_line)

  call = '''

  finite_dimensional_latex = (
    _render_finite_dimensional_aggregate_statement_latex(
      statement
    )
  )

  if finite_dimensional_latex is not None:
    return finite_dimensional_latex
'''

  text = (
    text[:insert_pos]
    + call
    + text[insert_pos:]
  )

PATH.write_text(text, encoding="utf-8")

TEST_SOURCE = Path(
  "phase143_75m_r2/"
  "test_phase143_75m_finite_dimensional_semantic_rendering.py"
)
TEST_DESTINATION = Path(
  "tests/"
  "test_phase143_75m_finite_dimensional_semantic_rendering.py"
)

if not TEST_SOURCE.exists():
  raise SystemExit(
    "Focused test source was not found."
  )

shutil.copy2(TEST_SOURCE, TEST_DESTINATION)

print("Phase 143-75M R2 repair applied.")
print("Backup:", BACKUP)
