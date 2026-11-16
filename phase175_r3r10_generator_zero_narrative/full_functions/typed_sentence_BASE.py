def typed_sentence(statement, step):
    from phase174_r3_r6_r3_common_narrative.projection import (
        project_verified_index_two_statement,
    )
    index_two = project_verified_index_two_statement(statement, step)
    if index_two is not None:
        return index_two
    map_sentence = map_property_sentence(statement, step)
    if map_sentence is not None:
        return map_sentence
    # Only project the mathematical content already present in a typed claim.
    # These are shared statement formatters, not a proof-tree-specific narrative.
    from expression import Zero
    from proof import Relation, RelationType
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
        Prop27TypedHopfDeltaStatement, typed_specialization,
    )
    if type(statement) is Prop27TypedHopfDeltaStatement:
        if (type(statement.n) is int and statement.n >= 2
                and statement.n % 2 == 0
                and statement == typed_specialization(statement.n)):
            sign = r"\pm" if statement.sign_undetermined else ""
            return (
                rf"$H(\Delta(\iota_{{{statement.source_iota_dimension}}}))="
                rf"{sign}{statement.absolute_coefficient}"
                rf"\iota_{{{statement.target_iota_dimension}}}$."
            )
        return None
    from map_property_rules import ImageZeroStatement
    if type(statement) is ImageZeroStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        if source is not None and target is not None and symbol is not None:
            return rf"${symbol}:{source}\to {target}$ は零写像."
        return None
    if type(statement) is KernelMultipleStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(statement.source_generator)
        if (source is not None and target is not None
                and symbol is not None and generator is not None
                and type(statement.multiple) is int
                and statement.multiple >= 1
                and statement.domain == mapping.source_group):
            return (
                rf"$\ker({symbol}:{source}\to {target})="
                rf"\mathbb{{Z}}\{{{statement.multiple}{generator}\}}$."
            )
        return None
    if (type(statement) is Relation
            and statement.relation_type is RelationType.EQUALITY
            and isinstance(statement.rhs, Zero)):
        from toda_conclusion_latex_renderer import (
            render_repository_conclusion_latex,
        )
        try:
            latex = render_repository_conclusion_latex(statement)
        except (TypeError, ValueError):
            return None
        return "$" + latex + "$."
    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap
    if isinstance(statement, Toda45IsomorphismStatement):
        mapping = statement.map
        if isinstance(mapping, TodaIteratedSuspensionMap):
            source = group_tex(mapping.source_group)
            target = group_tex(mapping.target_group)
            if source is not None and target is not None and type(mapping.exponent) is int:
                symbol = 'E' if mapping.exponent == 1 else rf'E^{{{mapping.exponent}}}'
                evidence = toda45_specialization_evidence(step)
                if evidence is not None:
                    _, bindings = evidence
                    values = dict(bindings)
                    return (
                        rf'$(n,m,k)=({values["n"]},{values["m"]},{values["k"]})$ '
                        rf'に適用すると, ${symbol}: {source}\to {target}$ は同型である.'
                    )
                return rf'${symbol}: {source}\to {target}$ は同型である.'
    if isinstance(statement, GeneratorImage):
        x, y = element_tex(statement.source_generator), element_tex(statement.target_generator)
        symbol = map_symbol_tex(statement.map)
        if x is not None and y is not None and symbol is not None:
            return rf"${symbol}({x})={y}$."
    if isinstance(statement, EHPImageEqualsKernelStatement):
        window = statement.window
        if prop42_exactness_indices(TodaProp42ExactnessStatement(window)) is None:
            return None
        if window.first_map == EHP_DELTA_MAP and window.second_map == EHP_E_MAP:
            return r"完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ."
        if window.first_map == EHP_E_MAP and window.second_map == EHP_H_MAP:
            return r"完全性より, $\operatorname{Im}E=\ker H$ が成り立つ."
    if isinstance(statement, TodaDeltaImageFreeCyclicStatement):
        if not isinstance(statement.map, TodaDeltaMap) or not isinstance(statement.image_group, FreeCyclicGroup):
            return None
        generator = element_tex(statement.image_group.generator)
        if generator is not None:
            return rf"これより, $\operatorname{{Im}}\Delta=\mathbb{{Z}}\{{{generator}\}}$."
    if isinstance(statement, SuspensionKernelFreeCyclicStatement):
        if not isinstance(statement.map, TodaSuspensionMap) or not isinstance(statement.kernel_group, FreeCyclicGroup):
            return None
        generator = element_tex(statement.kernel_group.generator)
        if generator is not None:
            return rf"完全性より, $\ker E=\mathbb{{Z}}\{{{generator}\}}$."
    if isinstance(statement, QuotientIsomorphismStatement):
        if not isinstance(statement.map, TodaSuspensionMap):
            return None
        domain, codomain = group_tex(statement.domain), group_tex(statement.codomain)
        generator = element_tex(statement.source_generator)
        if domain is not None and codomain is not None and generator is not None and type(statement.multiple) is int:
            multiple = statement.multiple
            return rf"全射性と核の決定から, 準同型定理より ${codomain}\cong {domain}/\mathbb{{Z}}\{{{multiple}{generator}\}}$."
    if isinstance(statement, GeneratorSuspension) and isinstance(statement.map, TodaSuspensionMap):
        x, y = element_tex(statement.source_generator), element_tex(statement.target_generator)
        if x is not None and y is not None:
            return rf"$E({x})={y}$."
    return None
