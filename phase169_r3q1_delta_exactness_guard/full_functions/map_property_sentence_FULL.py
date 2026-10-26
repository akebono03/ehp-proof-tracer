def map_property_sentence(statement, step):
    """Render map properties from their typed conclusion and actual proof premises.

    This common path applies to both Map* and Toda* statement families.  It
    never treats a goal, a display label, or an unrelated exactness window as
    evidence for a mathematical implication.
    """
    from homotopy_groups import TodaSuspensionIsomorphismStatement
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from proof import ProofRule
    from toda_rules import (
        TodaDeltaInjectiveStatement,
        TodaDeltaZeroStatement,
        TodaHopfInvariantSurjectiveStatement,
        TodaHopfInvariantZeroStatement,
        TodaSuspensionInjectiveStatement,
        TodaSuspensionSurjectiveStatement,
    )

    injective = (MapInjective, TodaDeltaInjectiveStatement, TodaSuspensionInjectiveStatement)
    surjective = (MapSurjective, TodaHopfInvariantSurjectiveStatement, TodaSuspensionSurjectiveStatement)
    isomorphism = (MapIsomorphism, TodaSuspensionIsomorphismStatement)
    zero = (TodaDeltaZeroStatement, TodaHopfInvariantZeroStatement)
    if not isinstance(statement, injective + surjective + isomorphism + zero):
        return None

    mapping = statement.map
    source = group_tex(getattr(mapping, "source_group", None))
    target = group_tex(getattr(mapping, "target_group", None))
    symbol = map_symbol_tex(mapping)
    if source is None or target is None or symbol is None:
        return None
    label = ("単射" if isinstance(statement, injective)
             else "全射" if isinstance(statement, surjective)
             else "同型" if isinstance(statement, isomorphism)
             else "零写像")
    result = rf"${symbol}: {source}\to {target}$ は{label}."
    if step is None or step.rule is not ProofRule.INFERENCE:
        return result

    premises = tuple(parent.conclusion for parent in step.premises)
    exact = tuple(item.window for item in premises if isinstance(item, TodaProp42ExactnessStatement))

    def window_for(first, second, *, source_term=None, middle_term=None, target_term=None):
        return next((window for window in exact
                     if window.first_map == first and window.second_map == second
                     and (source_term is None or window.source_term == source_term)
                     and (middle_term is None or window.middle_term == middle_term)
                     and (target_term is None or window.target_term == target_term)), None)

    if isinstance(statement, isomorphism):
        has_injective = any(isinstance(parent, injective) and parent.map == mapping for parent in premises)
        has_surjective = any(isinstance(parent, surjective) and parent.map == mapping for parent in premises)
        if has_injective and has_surjective:
            return rf"単射性と全射性より, ${symbol}: {source}\to {target}$ は同型."

    if isinstance(statement, zero) and isinstance(mapping, TodaDeltaMap):
        window = window_for(EHP_H_MAP, EHP_DELTA_MAP,
                            middle_term=mapping.source_group,
                            target_term=mapping.target_group)
        if (window is not None
                and any(isinstance(parent, TodaHopfInvariantSurjectiveStatement)
                        and parent.map == TodaHopfInvariantMap(window.source_term, window.middle_term)
                        for parent in premises)):
            return (rf"$H$ の全射性と完全性より, "
                    rf"$\ker\Delta=\operatorname{{Im}}H={source}$ なので, "
                    rf"${symbol}: {source}\to {target}$ は零写像.")

    if isinstance(statement, zero) and isinstance(mapping, TodaDeltaMap):
        # Another valid source of Delta=0: the following suspension E is
        # already an isomorphism, so its kernel vanishes. This is the same
        # typed exactness principle, not a sphere/stem-specific exception.
        window = window_for(EHP_DELTA_MAP, EHP_E_MAP,
                            source_term=mapping.source_group,
                            middle_term=mapping.target_group)
        if (window is not None
                and any(isinstance(parent, TodaSuspensionIsomorphismStatement)
                        and parent.map == TodaSuspensionMap(window.middle_term, window.target_term)
                        for parent in premises)):
            return (rf"完全性より, $\operatorname{{Im}}\Delta=\ker E=0$ なので, "
                    rf"${symbol}: {source}\to {target}$ は零写像.")

    if isinstance(statement, zero) and isinstance(mapping, TodaHopfInvariantMap):
        window = window_for(EHP_H_MAP, EHP_DELTA_MAP,
                            source_term=mapping.source_group,
                            middle_term=mapping.target_group)
        if (window is not None
                and any(isinstance(parent, TodaDeltaInjectiveStatement)
                        and parent.map == TodaDeltaMap(window.middle_term, window.target_term)
                        for parent in premises)):
            return (rf"完全性より, $\operatorname{{Im}}H=\ker\Delta=0$ なので, "
                    rf"${symbol}: {source}\to {target}$ は零写像.")

    if isinstance(statement, injective) and isinstance(mapping, TodaSuspensionMap):
        window = window_for(EHP_DELTA_MAP, EHP_E_MAP,
                            middle_term=mapping.source_group,
                            target_term=mapping.target_group)
        if (window is not None
                and any(isinstance(parent, TodaDeltaZeroStatement)
                        and parent.map == TodaDeltaMap(window.source_term, window.middle_term)
                        for parent in premises)):
            return (rf"完全性より, $\ker E=\operatorname{{Im}}\Delta=0$ なので, "
                    rf"${symbol}: {source}\to {target}$ は単射.")

    if isinstance(statement, surjective) and isinstance(mapping, TodaSuspensionMap):
        window = window_for(EHP_E_MAP, EHP_H_MAP,
                            source_term=mapping.source_group,
                            middle_term=mapping.target_group)
        if (window is not None
                and any(isinstance(parent, TodaHopfInvariantZeroStatement)
                        and parent.map == TodaHopfInvariantMap(window.middle_term, window.target_term)
                        for parent in premises)):
            return (rf"完全性より, $\operatorname{{Im}}E=\ker H={target}$ なので, "
                    rf"${symbol}: {source}\to {target}$ は全射.")

    # Preserve the existing general map-property wording for other proved
    # EHP inferences.  It is deliberately subordinate to exact window matches.
    if isinstance(statement, (MapInjective, MapSurjective)):
        visited = set()

        def has_exactness(parent):
            if id(parent) in visited:
                return False
            visited.add(id(parent))
            if isinstance(parent.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement)):
                return True
            return any(has_exactness(ancestor) for ancestor in parent.premises)

        if any(has_exactness(parent) for parent in step.premises):
            return "完全性より, " + result
    return result
