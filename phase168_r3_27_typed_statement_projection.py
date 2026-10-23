"""Typed proof-step prose projection shared by the new renderer.

Only registered typed conclusions in the Proof Tree are rendered.
This module does not search for new premises or sources.
"""
from __future__ import annotations

from expression import HomotopyElement, Multiple
from homotopy_groups import (
    FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup,
    TodaSuspensionMap, TodaHopfInvariantMap, TodaSuspensionIsomorphismStatement,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import (
    GeneratorImage, MapInjective, MapIsomorphism, MapSurjective,
)
from toda_rules import (
    TodaDeltaImageFreeCyclicStatement,
    TodaDeltaZeroStatement,
    TodaProp42ExactnessStatement,
)

def group_tex(group):
    if not isinstance(group, TodaPrimaryGroup):
        return None
    i, n = group.group_dimension, group.sphere_dimension
    if type(i) is not int or type(n) is not int:
        return None
    return rf"\pi_{{{i}}}^{{{n}}}"

def element_tex(value):
    if isinstance(value, Multiple) and type(value.coefficient) is int:
        inner = element_tex(value.expression)
        return f"{value.coefficient}{inner}" if inner is not None else None
    if isinstance(value, HomotopyElement):
        symbol = value.generator
        if symbol is not None and type(symbol.index) is int:
            family = {"η": r"\eta", "ι": r"\iota", "ν": r"\nu", "σ": r"\sigma"}.get(symbol.family)
            if family is not None:
                return f"{family}_{{{symbol.index}}}"
        if value.name in ("η", "ι", "ν", "σ") and type(value.dimension) is int:
            family = {"η": r"\eta", "ι": r"\iota", "ν": r"\nu", "σ": r"\sigma"}[value.name]
            return f"{family}_{{{value.dimension}}}"
    return None

def map_symbol_tex(map_object):
    if isinstance(map_object, TodaSuspensionMap):
        return "E"
    if isinstance(map_object, TodaHopfInvariantMap):
        return "H"
    if isinstance(map_object, TodaDeltaMap):
        return r"\\Delta"
    return None


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
                return rf'${symbol}: {source}\to {target}$ は同型である.'
    if isinstance(statement, TodaDeltaZeroStatement):
        delta = statement.map
        if isinstance(delta, TodaDeltaMap):
            source = group_tex(delta.source_group)
            target = group_tex(delta.target_group)
            if source is not None and target is not None:
                return (rf"完全性より, $\operatorname{{Im}}\Delta=\ker E=0$ なので, "
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
            # Wording is justified only by the typed inference represented in
            # the Proof Tree, not by the goal's dimension or a source lookup.
            from proof import ProofRule
            if step is not None and step.rule is ProofRule.INFERENCE:
                if isinstance(statement, (MapInjective, MapSurjective)):
                    if step.premises and any(
                        "exact" in str(getattr(p.inference_rule, "name", "")).lower()
                        or isinstance(p.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement))
                        for p in step.premises
                    ):
                        return rf"完全性より, ${symbol}: {source}\to {target}$ は{label}である."
                    # An EHP surjectivity or injectivity inference can have
                    # exactness deeper than its immediate typed premises.
                    def has_exactness(p, seen):
                        if id(p) in seen:
                            return False
                        seen.add(id(p))
                        if isinstance(p.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement)):
                            return True
                        return any(has_exactness(q, seen) for q in p.premises)
                    if any(has_exactness(p, set()) for p in step.premises):
                        return rf"完全性より, ${symbol}: {source}\to {target}$ は{label}である."
                if isinstance(statement, (MapIsomorphism, TodaSuspensionIsomorphismStatement)):
                    has_inj = any(isinstance(p.conclusion, MapInjective) for p in step.premises)
                    has_surj = any(isinstance(p.conclusion, MapSurjective) for p in step.premises)
                    if has_inj and has_surj:
                        return rf"単射性と全射性より, ${symbol}: {source}\to {target}$ は同型である."
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

