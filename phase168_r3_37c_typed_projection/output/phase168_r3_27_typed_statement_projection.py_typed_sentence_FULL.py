def typed_sentence(statement, step):
    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap
    if isinstance(statement, Toda45IsomorphismStatement):
        mapping = statement.map
        if isinstance(mapping, TodaIteratedSuspensionMap):
            source = group_tex(mapping.source_group)
            target = group_tex(mapping.target_group)
            if source is not None and target is not None and type(mapping.exponent) is int:
                symbol = 'E' if mapping.exponent == 1 else rf'E^{{{mapping.exponent}}}'
                return rf'${symbol}: {source}	o {target}$ は同型である.'
    if isinstance(statement, TodaDeltaZeroStatement):
        delta = statement.map
        if isinstance(delta, TodaDeltaMap):
            source = group_tex(delta.source_group)
            target = group_tex(delta.target_group)
            if source is not None and target is not None:
                return (rf"完全性と懸垂写像の同型性より, "
                        rf"$\Delta: {source}\to {target}$ は零写像である.")
    if isinstance(statement, GeneratorImage):
        x, y = element_tex(statement.source_generator), element_tex(statement.target_generator)
        symbol = map_symbol_tex(statement.map)
        if x is not None and y is not None and symbol is not None:
            return rf"${symbol}({x})={y}$."
    if isinstance(statement, (MapInjective, MapSurjective, MapIsomorphism,
                              TodaSuspensionIsomorphismStatement)):
        source = group_tex(getattr(statement.map, "source_group", None))
        target = group_tex(getattr(statement.map, "target_group", None))
        symbol = map_symbol_tex(statement.map)
        if source is not None and target is not None and symbol is not None:
            label = ("単射" if isinstance(statement, MapInjective)
                     else "全射" if isinstance(statement, MapSurjective)
                     else "同型")
            return rf"${symbol}: {source}\to {target}$ は{label}."
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
