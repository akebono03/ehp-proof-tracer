from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
ast.parse(text)

names = ['Toda211OrdinaryEHPApplicabilityStatement', 'Toda515Sigma8Prop44SpecializationStatement', 'Toda515Sigma8TransportedDecompositionStatement', 'TodaLemma510Nu6OrdinaryCompositionReductionStatement', 'TodaLemma510Nu6OrdinaryCompositionZeroStatement', 'TodaLemma510OrdinaryIndeterminacyDoubleStatement']

tree = ast.parse(text)
imp = next(
    n for n in tree.body
    if isinstance(n, ast.ImportFrom)
    and n.module == "toda_rules"
)
existing = {alias.name for alias in imp.names}
missing = [name for name in names if name not in existing]

if missing:
    lines = text.splitlines(keepends=True)
    index = imp.end_lineno - 1
    if lines[index].strip() != ")":
        raise RuntimeError("Unexpected toda_rules import ending.")
    insertion = "".join(
        "  " + name + ",\\n"
        for name in missing
    )
    lines.insert(index, insertion)
    text = "".join(lines)

branches = '  if isinstance(statement, TodaLemma510OrdinaryIndeterminacyDoubleStatement):\n    return (\n      r"\\\\operatorname{Ind}\\\\left("\n      + render_toda_expression_latex(statement.bracket)\n      + r"\\\\right) \\\\subseteq "\n      + str(statement.modulus)\n      + _render_phase143_75ao_homotopy_group(statement.ambient_group)\n    )\n\n  if isinstance(statement, TodaLemma510Nu6OrdinaryCompositionZeroStatement):\n    return (\n      render_toda_expression_latex(statement.left_element)\n      + r" \\\\circ "\n      + _render_phase143_75ao_homotopy_group(statement.ordinary_right_group)\n      + r" = 0"\n    )\n\n  if isinstance(statement, TodaLemma510Nu6OrdinaryCompositionReductionStatement):\n    return (\n      render_toda_expression_latex(statement.left_element)\n      + r" \\\\circ "\n      + _render_phase143_75ao_homotopy_group(statement.ordinary_right_group)\n      + r" = "\n      + render_toda_expression_latex(statement.left_element)\n      + r" \\\\circ "\n      + render_toda_expression_latex(statement.two_primary_right_group)\n    )\n\n  if isinstance(statement, Toda211OrdinaryEHPApplicabilityStatement):\n    conditions = []\n    if statement.m_is_odd:\n      conditions.append(r"m\\\\text{ is odd}")\n    if statement.i_less_than_3m_minus_1:\n      conditions.append(r"i < 3m - 1")\n    return (\n      _render_phase143_75ao_ehp_window(statement.window)\n      + r",\\\\qquad "\n      + r",\\\\ ".join(conditions)\n    )\n\n  if isinstance(statement, Toda515Sigma8TransportedDecompositionStatement):\n    return (\n      render_toda_expression_latex(statement.prop44_isomorphism.map.target_group)\n      + r" = "\n      + render_toda_expression_latex(statement.transported_group)\n    )\n\n  if isinstance(statement, Toda515Sigma8Prop44SpecializationStatement):\n    return (\n      render_toda_expression_latex(statement.alpha)\n      + r" \\\\in "\n      + render_toda_expression_latex(statement.membership.group)\n      + r",\\\\qquad "\n      + render_toda_expression_latex(statement.hopf_relation)\n    )\n\n'
tree = ast.parse(text)
func = next(
    n for n in tree.body
    if isinstance(n, ast.FunctionDef)
    and n.name == "render_toda_proof_statement_latex"
)
function_text = "\\n".join(
    text.splitlines()[func.lineno - 1:func.end_lineno]
)
marker = "TodaLemma510OrdinaryIndeterminacyDoubleStatement"

if marker not in function_text:
    lines = text.splitlines(keepends=True)
    lines.insert(func.body[0].lineno - 1, branches)
    text = "".join(lines)

ast.parse(text)
path.write_text(text, encoding="utf-8")
print("Phase 143-75AP R2 patch applied.")
