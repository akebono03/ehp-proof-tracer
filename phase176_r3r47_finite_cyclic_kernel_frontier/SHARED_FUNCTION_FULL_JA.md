# 変更後の共通表示関数全文

```python
def render_repository_conclusion_latex(conclusion) -> str:
    """Render established Relation, membership and Expression forms unchanged."""
    # Render subgroup generation, not an assertion of infinite cyclic order.
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase168_r3_27_typed_statement_projection import (
        element_tex, group_tex, map_symbol_tex,
    )
    if type(conclusion) is KernelMultipleStatement:
        mapping = conclusion.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(conclusion.source_generator)
        if (source is not None and target is not None and symbol is not None
                and generator is not None and type(conclusion.multiple) is int
                and conclusion.multiple >= 1
                and conclusion.domain == mapping.source_group):
            return (rf"\ker({symbol}:{source}\to {target})="
                    rf"\langle {conclusion.multiple}{generator}\rangle")
        raise TypeError("unsupported typed kernel multiple for LaTeX rendering")
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
```
