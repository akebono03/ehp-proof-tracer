from pathlib import Path

path = Path(
  "toda_group_proof_narrative_renderer.py"
)
text = path.read_text(
  encoding="utf-8"
)

old_import = """from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
)
"""

new_import = """from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
  render_toda_raw_group_structure_latex,
)
"""

if old_import not in text:
  raise SystemExit(
    "Expected toda_proof_narrative_renderer "
    "import block was not found."
  )

text = text.replace(
  old_import,
  new_import,
  1,
)

old_rules = """  Toda56Nu4DecompositionStatement,
  TodaDeltaZeroStatement,
  TodaEtaFamilyDefinitionStatement,
"""

new_rules = """  Toda56Nu4DecompositionStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaDeltaZeroStatement,
  TodaEtaFamilyDefinitionStatement,
"""

if old_rules not in text:
  raise SystemExit(
    "Expected Toda rule import location "
    "was not found."
  )

text = text.replace(
  old_rules,
  new_rules,
  1,
)

old_rules_2 = """  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
)
"""

new_rules_2 = """  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)
"""

if old_rules_2 not in text:
  raise SystemExit(
    "Expected Toda suspension import location "
    "was not found."
  )

text = text.replace(
  old_rules_2,
  new_rules_2,
  1,
)

needle = """  if isinstance(
    statement,
    TodaSuspensionMap,
  ):
    return (
      "E: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \\to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
    )

"""

addition = """  if isinstance(
    statement,
    TodaDeltaSurjectiveStatement,
  ):
    return (
      r"\\Delta: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \\twoheadrightarrow "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    TodaSuspensionKernelFreeCyclicStatement,
  ):
    return (
      r"\\ker\\left(E: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \\to "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
      + r"\\right) = "
      + render_toda_raw_group_structure_latex(
        statement.kernel_group
      )
    )

  if isinstance(
    statement,
    TodaDeltaImageFreeCyclicStatement,
  ):
    return (
      r"\\operatorname{Im}\\left(\\Delta: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \\to "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
      + r"\\right) = "
      + render_toda_raw_group_structure_latex(
        statement.image_group
      )
    )

  if isinstance(
    statement,
    TodaDeltaKernelFreeCyclicStatement,
  ):
    return (
      r"\\ker\\left(\\Delta: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \\to "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
      + r"\\right) = "
      + render_toda_raw_group_structure_latex(
        statement.kernel_group
      )
    )

"""

if needle not in text:
  raise SystemExit(
    "Expected TodaSuspensionMap rendering "
    "block was not found."
  )

text = text.replace(
  needle,
  needle + addition,
  1,
)

path.write_text(
  text,
  encoding="utf-8",
)

print(
  "Phase 143-75F implementation applied."
)
print(
  "Changed: "
  "toda_group_proof_narrative_renderer.py"
)
