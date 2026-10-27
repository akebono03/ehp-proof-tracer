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
    """Render only supported generators; normalize typed consecutive eta composites."""
    from expression import Composition

    if isinstance(value, Composition):
        from phase169_r10eb_typed_composition_power.display import (
            typed_stable_composition_power_latex,
        )
        power = typed_stable_composition_power_latex(value)
        if power is not None:
            return power

    if isinstance(value, Multiple) and type(value.coefficient) is int:
        inner = element_tex(value.expression)
        return f"{value.coefficient}{inner}" if inner is not None else None
    if isinstance(value, Composition):
        left, right = value.left, value.right
        if not (isinstance(left, HomotopyElement)
                and isinstance(right, HomotopyElement)):
            return None
        left_symbol = getattr(left, "generator", None)
        right_symbol = getattr(right, "generator", None)
        left_index = (getattr(left_symbol, "index", None) if left_symbol is not None
                      else (left.dimension if left.name == "η" else None))
        right_index = (getattr(right_symbol, "index", None) if right_symbol is not None
                       else (right.dimension if right.name == "η" else None))
        left_eta = (left_symbol.family == "η" if left_symbol is not None
                    else left.name == "η")
        right_eta = (right_symbol.family == "η" if right_symbol is not None
                     else right.name == "η")
        if (type(left_index) is int and type(right_index) is int
                and left_eta and right_eta
                and getattr(left_symbol, "decoration", None) is None
                and getattr(right_symbol, "decoration", None) is None
                and right_index == left_index + 1
                and element_tex(left) == rf"\eta_{{{left_index}}}"
                and element_tex(right) == rf"\eta_{{{right_index}}}"):
            return rf"\eta_{{{left_index}}}^{{2}}"
        return None
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
        return r"\Delta"
    return None



def toda45_specialization_evidence(step):
    """Project an existing cited Toda (4.5) premise and display parameters.

    The Proof Tree already contains the inference applying its typed general
    premise. This function does not re-run the specialization validator or
    decide whether Toda (4.5) applies. Numerical indices are projected from
    the already proven concrete suspension map for presentation only.
    """
    from proof import ProofRule
    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup

    if (step is None or step.rule is not ProofRule.INFERENCE
            or not isinstance(step.conclusion, Toda45IsomorphismStatement)):
        return None
    mapping = step.conclusion.map
    if (not isinstance(mapping, TodaIteratedSuspensionMap)
            or not isinstance(mapping.source_group, TodaPrimaryGroup)
            or not isinstance(mapping.target_group, TodaPrimaryGroup)):
        return None
    n = mapping.source_group.sphere_dimension
    m = mapping.target_group.sphere_dimension
    source_dimension = mapping.source_group.group_dimension
    if any(type(index) is not int for index in (n, m, source_dimension)):
        return None
    # This is a display projection, not a validation of Toda's inequalities.
    bindings = (("n", n), ("m", m), ("k", source_dimension - n))
    visited = set()

    def find_source(node):
        if id(node) in visited:
            return None
        visited.add(id(node))
        for parent in node.premises:
            if (parent.rule is ProofRule.GIVEN
                    and isinstance(parent.conclusion, Toda45IsomorphismStatement)):
                return parent, bindings
            candidate = find_source(parent)
            if candidate is not None:
                return candidate
        return None

    return find_source(step)


def project_toda45_specialization_citation_numbers(model, step_index):
    """Bind Toda (4.5) citations only to their used general Proof Step."""
    step = model.steps[step_index]
    evidence = toda45_specialization_evidence(step)
    if evidence is None:
        return ()
    source_step, _ = evidence
    numbers = []
    for source_index, candidate in enumerate(model.steps):
        if candidate != source_step:
            continue
        for number in model.step_citation_numbers[source_index]:
            if number not in numbers:
                numbers.append(number)
    return tuple(numbers)


def project_stable_eta_notation_transition(model, step_index):
    """Explain an existing cited eta renaming without inferring a new result.

    Both the transported group relation and the cited general eta definition
    must be actual premises of the typed stable-notation inference.
    """
    from expression import IteratedSuspension
    from homotopy_groups import FiniteCyclicGroup
    from proof import ProofRule, Relation, RelationType
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase166_r3ac_stable_notation import _stable_eta_renaming_shape
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel

    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if type(step_index) is not int or not 0 <= step_index < len(model.steps):
        raise ValueError("invalid proof-step index")
    step = model.steps[step_index]
    if step.rule is not ProofRule.INFERENCE or len(step.premises) != 2:
        return None
    transported_step, definition_step = step.premises
    transported = transported_step.conclusion
    if (not isinstance(transported, Relation)
            or transported.relation_type is not RelationType.EQUALITY
            or not isinstance(transported.rhs, FiniteCyclicGroup)
            or not isinstance(transported.rhs.generator, IteratedSuspension)
            or type(transported.rhs.generator.exponent) is not int
            or transported.rhs.generator.exponent < 2
            or definition_step.rule is not ProofRule.GIVEN
            or not isinstance(definition_step.conclusion, TodaEtaFamilyGeneralDefinition)
            or not _stable_eta_renaming_shape(transported, step.conclusion)):
        return None
    source = element_tex(transported.rhs.generator.expression)
    target = element_tex(step.conclusion.rhs.generator)
    if source is None or target is None:
        return None
    numbers = tuple(dict.fromkeys(
        number
        for index, candidate in enumerate(model.steps)
        if candidate == definition_step
        for number in model.step_citation_numbers[index]
    ))
    if not numbers:
        return None
    tags = ", ".join(f"[R{number}]" for number in numbers)
    exponent = transported.rhs.generator.exponent
    return rf"{tags}の $\eta$ 系列の定義より, $E^{{{exponent}}}{source}={target}$."


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

def typed_sentence(statement, step):
    map_sentence = map_property_sentence(statement, step)
    if map_sentence is not None:
        return map_sentence
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

