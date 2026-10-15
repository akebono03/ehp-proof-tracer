"""Render a verified concrete transport chain using only its ProofStep premises.

This is an early, focused branch of the existing common narrative entry point.
No target-specific reference lookup or appended prose is performed.
"""

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import ProofStep, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement, TodaEtaFamilyDefinitionStatement
from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference
from toda_human_readable_renderer import render_toda_expression_latex
from toda_proof_narrative_renderer import render_toda_primary_group_latex, render_toda_raw_group_structure_latex


def render_concrete_transport_proof_from_steps(root: ProofStep) -> str | None:
    """Use a connected transport-and-normalization ancestry, or decline it."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    if root.inference_rule is None or root.inference_rule.name != "Toda eta-family concrete transported-generator normalization":
        return None
    if len(root.premises) != 3:
        return None
    transported, base_definition, target_definition = root.premises
    if not all(isinstance(step, ProofStep) for step in root.premises):
        return None
    if not isinstance(base_definition.conclusion, TodaEtaFamilyDefinitionStatement):
        return None
    if not isinstance(target_definition.conclusion, TodaEtaFamilyDefinitionStatement):
        return None
    if transported.inference_rule is None or transported.inference_rule.name != "Toda 4.5 generic finite-cyclic transport":
        return None
    if len(transported.premises) != 2:
        return None
    source, isomorphism = transported.premises
    if not isinstance(isomorphism.conclusion, Toda45IsomorphismStatement):
        return None
    target_statement = root.conclusion
    source_statement = source.conclusion
    transport_statement = transported.conclusion
    if not all(isinstance(s, Relation) and s.relation_type == RelationType.EQUALITY for s in (target_statement, source_statement, transport_statement)):
        return None
    if not all(isinstance(s.rhs, FiniteCyclicGroup) and isinstance(s.lhs, TodaPrimaryGroup) for s in (target_statement, source_statement, transport_statement)):
        return None
    n = target_statement.lhs.sphere_dimension
    base_n = source_statement.lhs.sphere_dimension
    if not isinstance(n, int) or not isinstance(base_n, int) or n <= base_n:
        return None
    if isomorphism.conclusion.map.source_group.sphere_dimension != base_n:
        return None
    if isomorphism.conclusion.map.target_group.sphere_dimension != n:
        return None
    if not isinstance(transport_statement.rhs.generator, IteratedSuspension):
        return None
    if transport_statement.rhs.generator.expression != source_statement.rhs.generator:
        return None
    if target_statement.rhs.generator != target_definition.conclusion.element:
        return None
    if source_statement.rhs.generator != base_definition.conclusion.element:
        return None
    if base_definition.conclusion.index != base_n or target_definition.conclusion.index != n:
        return None
    if transport_statement.rhs.order != source_statement.rhs.order or target_statement.rhs.order != source_statement.rhs.order:
        return None
    reference = extract_toda_group_proof_step_literature_reference(isomorphism)
    if reference is None or reference.locator != "(4.5)":
        return None

    def group_eq(statement: Relation) -> str:
        return render_toda_primary_group_latex(statement.lhs) + " = " + render_toda_raw_group_structure_latex(statement.rhs)

    exponent = n - base_n
    e = "E" if exponent == 1 else f"E^{{{exponent}}}"
    source_group = render_toda_primary_group_latex(source_statement.lhs)
    target_group = render_toda_primary_group_latex(target_statement.lhs)
    old_generator = render_toda_expression_latex(source_statement.rhs.generator)
    new_generator = render_toda_expression_latex(target_statement.rhs.generator)
    return "\n".join((
        "# Group proof narrative", "", "## 証明対象", "", f"${group_eq(target_statement)}$.", "",
        "## 使用する結果", "", f"**[R1] {reference.locator}.**", "Toda (4.5) の安定範囲における懸垂同型.", "", "---", "",
        "## 証明", "", f"基準群の証明より, ${group_eq(source_statement)}$.", "",
        f"[R1]を適用すると, ${e}: {source_group} \\xrightarrow{{\\cong}} {target_group}$.", "",
        f"したがって, ${group_eq(transport_statement)}$.", "",
        f"生成元の定義から, ${e}{old_generator} = {new_generator}$.", "",
        f"以上より, ${group_eq(target_statement)}$.", "", r"$\square$", "",
    ))
