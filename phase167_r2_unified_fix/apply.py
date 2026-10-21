from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / 'toda_group_proof_narrative_references.py'
TEST = ROOT / 'tests' / 'test_phase167_r2_unified_reference.py'
source = TARGET.read_text(encoding='utf-8')
name = 'render_toda_group_proof_narrative_reference_entries_markdown'
lines = source.splitlines(keepends=True)
found = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
if len(found) != 1:
    raise RuntimeError('Expected a unique Reference renderer')
node = found[0]
start = sum(len(line) for line in lines[:node.lineno - 1])
end = sum(len(line) for line in lines[:node.end_lineno])
func = source[start:end]
if '    if entry.reference.locator == "(5.1)":' in func:
    raise RuntimeError('Old dedicated (5.1) branch still present; do not overlay patch')
anchor = '    for statement_line in statement_lines:\n'
if func.count(anchor) != 1:
    raise RuntimeError('Cannot uniquely identify common reference loop')
# Undo the R2 typed one-off fallback before installing a generalized
# fixed-component normalization. Fail closed if the patch has changed.
old_begin = func.find('    # Typed universal connectivity assertion:')
if old_begin == -1:
    raise RuntimeError('Current R2 implementation differs from expected. No changes made.')
old_end = func.find(anchor, old_begin)
if old_end == -1:
    raise RuntimeError('Current R2 statement processing not recognized')
normalizer = r'''    # Normalize cited fixed-statement components to their registered general
    # form rather than printing selected specialized proof conclusions.
    # This is shared logic: no branch on the literature locator or target group.
    general_formula_by_component = {
      "circle_higher_homotopy_zero": r"\pi_{i}^{1} = 0",
      "sphere_connectivity_zero": r"\pi_{i}^{n} = 0",
      "diagonal_identity_group": r"\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}",
    }
    registered_components = {
      component.component_key: component
      for component in get_toda_fixed_statement_components(
        entry.reference.locator
      )
    }
    identified_components = set()
    for proof_step in entry.proof_steps:
      boundary = classify_toda_literature_statement_step(proof_step)
      if (
        boundary is not None
        and boundary.classification
        == TodaLiteratureStatementClassification.FIXED_STATEMENT
        and boundary.reference_locator == entry.reference.locator
        and boundary.component_key in registered_components
      ):
        identified_components.add(boundary.component_key)
      conclusion = proof_step.conclusion
      if type(conclusion).__name__ == "Toda51BelowDiagonalZeroStatement":
        identified_components.add("sphere_connectivity_zero")
      elif type(conclusion).__name__ == "TodaPrimaryGroupZeroStatement":
        group = getattr(conclusion, "group", None)
        if group is None:
          group = getattr(conclusion, "target_group", None)
        if (
          getattr(group, "sphere_dimension", None) == 1
          and isinstance(getattr(group, "group_dimension", None), int)
          and group.group_dimension > 1
        ):
          identified_components.add("circle_higher_homotopy_zero")
      elif type(conclusion).__name__ == "Relation":
        lhs = getattr(conclusion, "lhs", None)
        rhs = getattr(conclusion, "rhs", None)
        dimension = getattr(lhs, "group_dimension", None)
        if (
          dimension is not None
          and dimension == getattr(lhs, "sphere_dimension", None)
          and type(rhs).__name__ == "FreeCyclicGroup"
        ):
          identified_components.add("diagonal_identity_group")

    general_keys = (
      identified_components
      & registered_components.keys()
      & general_formula_by_component.keys()
    )
    if general_keys:
      normalized_lines = []
      for component_key in registered_components:
        if component_key not in general_keys:
          continue
        component = registered_components[component_key]
        formula = general_formula_by_component[component_key]
        range_text = component.range_text
        if range_text and component.range_is_explicit_in_current_aggregate:
          range_latex = (
            range_text.replace(">=", r"\ge")
            .replace("<=", r"\le")
            .replace(">", ">")
            .replace("<", "<")
          )
          formula += r"\quad(" + range_latex + ")"
        normalized_lines.append("$" + formula + "$.")
      # Fixed components must be shown in general form, not as an arbitrary
      # subset of specialized equations from the current proof.
      statement_lines = tuple(normalized_lines)

'''
func = func[:old_begin] + normalizer + func[old_end:]
patched = source[:start] + func + source[end:]
ast.parse(patched)
# The regression test is deliberately based on actual Web rendered-line fields.
regression_test = r'''from web_group_proof import build_standard_web_group_proof_view


def _reference_text(n: int, k: int) -> str:
    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines
    first = next(i for i, line in enumerate(lines)
                 if line.kind == "heading" and line.prefix == "使用する結果")
    last = next(i for i, line in enumerate(lines)
                if i > first and line.kind == "heading" and line.prefix == "証明")
    return "\n".join(" ".join((line.prefix, line.statement_latex or "", line.suffix))
                     for line in lines[first + 1:last])


def test_phase167_r2_pi32_reference_uses_general_form():
    text = _reference_text(2, 1)
    assert r"\pi_{i}^{1}" in text
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_{3}^{3}" not in text
    assert r"\pi_{2}^{1}" not in text
    assert "Proposition 5.1" in text


def test_phase167_r2_pi43_reference_uses_general_form():
    text = _reference_text(3, 1)
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_{i}^{n}" in text
    assert text.count(r"\pi_{n}^{n}") == 1
    assert "Proposition 5.1" in text
'''
ast.parse(regression_test)
backup = HERE / 'backup' / TARGET.name
backup.parent.mkdir(exist_ok=True, parents=True)
shutil.copy2(TARGET, backup)
TARGET.write_text(patched, encoding='utf-8')
TEST.write_text(regression_test, encoding='utf-8')
(HERE / 'modified_function_full.py').write_text(func, encoding='utf-8')
print(json.dumps({'status': 'PATCHED', 'target': str(TARGET), 'backup': str(backup),
                  'test': str(TEST), 'full_function': str(HERE / 'modified_function_full.py')},
                 ensure_ascii=False, indent=2))
