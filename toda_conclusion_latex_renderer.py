"""Repository-independent rendering of typed Toda conclusions.

Phase 165 R27-R39: preserve the former mathematical formatting contract.
"""
from expression import Expression
from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaPrimaryGroup,
)
from proof import Relation, RelationType
from toda_human_readable_renderer import (
    render_toda_expression_latex,
    render_toda_group_structure_latex,
    render_toda_target_latex,
)
from toda_presentation import (
    build_toda_group_structure_presentation,
    build_toda_target_presentation,
)
from toda_rules import (
    TodaBracketMembershipStatement,
    TodaBracketMembershipTheoremStatement,
)


def _render_repository_conclusion_value_latex(value) -> str:
    if isinstance(value, Expression):
        return render_toda_expression_latex(value)
    if isinstance(value, TodaPrimaryGroup):
        return render_toda_target_latex(build_toda_target_presentation(value))
    if isinstance(value, (FreeCyclicGroup, FiniteCyclicGroup, DirectSumGroup)):
        return render_toda_group_structure_latex(
            build_toda_group_structure_presentation(value)
        )
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    raise TypeError("unsupported conclusion value for LaTeX rendering")


def render_repository_conclusion_latex(conclusion) -> str:
    """Render established Relation, membership and Expression forms unchanged."""
    if isinstance(conclusion, Relation):
        if conclusion.relation_type is not RelationType.EQUALITY:
            raise ValueError(
                "only equality Relation conclusions are supported in Phase 99-18"
            )
        return (
            _render_repository_conclusion_value_latex(conclusion.lhs)
            + " = "
            + _render_repository_conclusion_value_latex(conclusion.rhs)
        )
    if isinstance(
        conclusion,
        (TodaBracketMembershipStatement, TodaBracketMembershipTheoremStatement),
    ):
        return (
            render_toda_expression_latex(conclusion.element)
            + r" \in "
            + render_toda_expression_latex(conclusion.bracket)
        )
    if isinstance(conclusion, Expression):
        return render_toda_expression_latex(conclusion)
    raise TypeError("unsupported repository conclusion for LaTeX rendering")
