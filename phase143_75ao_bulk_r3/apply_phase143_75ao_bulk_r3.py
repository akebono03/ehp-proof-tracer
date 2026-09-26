from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
ast.parse(text)

names = [
    "Toda211OrdinaryEHPExactnessStatement",
    "TodaLemma510HopfBracketContainsStatement",
    "TodaLemma510IndexedHopfBracketContainsStatement",
    "TodaLemma510OrdinaryBracketPlusSuspensionImageStatement",
    "TodaLemma510OrdinarySuspensionImageFiniteStatement",
    "TodaLemma510OrdinarySuspensionImageInDoubleStatement",
    "TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement",
    "TodaLemma510Split115Statement",
]

tree = ast.parse(text)
imp = next(
    n for n in tree.body
    if isinstance(n, ast.ImportFrom) and n.module == "toda_rules"
)
existing = {a.name for a in imp.names}
missing = [n for n in names if n not in existing]
if missing:
    lines = text.splitlines(keepends=True)
    idx = imp.end_lineno - 1
    insertion = "".join("  " + n + ",\n" for n in missing)
    lines.insert(idx, insertion)
    text = "".join(lines)

tree = ast.parse(text)
himp = next(
    (
        n for n in tree.body
        if isinstance(n, ast.ImportFrom)
        and n.module == "homotopy_groups"
    ),
    None,
)
if himp is None:
    imports = [
        n for n in tree.body
        if isinstance(n, (ast.Import, ast.ImportFrom))
    ]
    lines = text.splitlines(keepends=True)
    lines.insert(
        imports[-1].end_lineno,
        "from homotopy_groups import (\n"
        "  FiniteHomotopyGroupStatement,\n"
        ")\n",
    )
    text = "".join(lines)
elif not any(a.name == "FiniteHomotopyGroupStatement" for a in himp.names):
    lines = text.splitlines(keepends=True)
    lines.insert(
        himp.end_lineno - 1,
        "  FiniteHomotopyGroupStatement,\n",
    )
    text = "".join(lines)

helper = '''
def _render_phase143_75ao_homotopy_group(group) -> str:
  return (
    r"\\pi_{"
    + str(group.group_dimension)
    + r"}^{"
    + str(group.sphere_dimension)
    + "}"
  )


def _render_phase143_75ao_ehp_window(window) -> str:
  return (
    _render_phase143_75ao_homotopy_group(window.source_term)
    + r" \\xrightarrow{" + window.first_map.name + "} "
    + _render_phase143_75ao_homotopy_group(window.middle_term)
    + r" \\xrightarrow{" + window.second_map.name + "} "
    + _render_phase143_75ao_homotopy_group(window.target_term)
  )


'''

if "def _render_phase143_75ao_homotopy_group" not in text:
    tree = ast.parse(text)
    func = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef)
        and n.name == "render_toda_proof_statement_latex"
    )
    lines = text.splitlines(keepends=True)
    lines.insert(func.lineno - 1, helper)
    text = "".join(lines)

branches = '''  if isinstance(statement, FiniteHomotopyGroupStatement):
    return _render_phase143_75ao_homotopy_group(statement.group) + r" \\text{ is finite}"

  if isinstance(statement, Toda211OrdinaryEHPExactnessStatement):
    return _render_phase143_75ao_ehp_window(statement.window) + r" \\quad\\text{is exact}"

  if isinstance(statement, (TodaLemma510HopfBracketContainsStatement, TodaLemma510IndexedHopfBracketContainsStatement)):
    return render_toda_expression_latex(statement.value) + r" \\in " + render_toda_expression_latex(statement.bracket)

  if isinstance(statement, TodaLemma510Split115Statement):
    return render_toda_expression_latex(statement.indexed_bracket) + r" = " + render_toda_expression_latex(statement.ordinary_bracket)

  if isinstance(statement, TodaLemma510OrdinaryBracketPlusSuspensionImageStatement):
    return (
      render_toda_expression_latex(statement.element)
      + r" \\in "
      + render_toda_expression_latex(statement.bracket)
      + r" + \\operatorname{Im}\\left("
      + statement.suspension_map.name
      + r":"
      + _render_phase143_75ao_homotopy_group(statement.source_group)
      + r"\\to"
      + _render_phase143_75ao_homotopy_group(statement.target_group)
      + r"\\right)"
    )

  if isinstance(statement, TodaLemma510OrdinarySuspensionImageFiniteStatement):
    return (
      r"\\operatorname{Im}\\left("
      + statement.suspension_map.name
      + r":"
      + _render_phase143_75ao_homotopy_group(statement.source_group)
      + r"\\to"
      + _render_phase143_75ao_homotopy_group(statement.target_group)
      + r"\\right) \\text{ is finite}"
    )

  if isinstance(statement, TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement):
    return (
      r"\\operatorname{Im}\\left("
      + statement.suspension_map.name
      + r":"
      + _render_phase143_75ao_homotopy_group(statement.source_group)
      + r"\\to"
      + _render_phase143_75ao_homotopy_group(statement.target_group)
      + r"\\right)_{(2)} = 0"
    )

  if isinstance(statement, TodaLemma510OrdinarySuspensionImageInDoubleStatement):
    return (
      r"\\operatorname{Im}\\left("
      + statement.suspension_map.name
      + r":"
      + _render_phase143_75ao_homotopy_group(statement.source_group)
      + r"\\to"
      + _render_phase143_75ao_homotopy_group(statement.target_group)
      + r"\\right) \\subseteq "
      + str(statement.modulus)
      + _render_phase143_75ao_homotopy_group(statement.target_group)
    )

'''

if "statement, TodaLemma510OrdinaryBracketPlusSuspensionImageStatement" not in text:
    tree = ast.parse(text)
    func = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef)
        and n.name == "render_toda_proof_statement_latex"
    )
    lines = text.splitlines(keepends=True)
    lines.insert(func.body[0].lineno - 1, branches)
    text = "".join(lines)

ast.parse(text)
path.write_text(text, encoding="utf-8")
print("Phase 143-75AO bulk R3 patch applied.")
