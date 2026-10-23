"""Render an explicitly supplied Proof Narrative Model without source inference."""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_12_body_binding import build_narrative_body_lines


def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render typed conclusions from Proof Tree; references come only from model."""
    from expression import HomotopyElement, Multiple
    from proof import ProofRule, Relation, RelationType
    from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaSuspensionMap, TodaPrimaryGroup
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
    from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase165_r14_r6_generic_iso import MapSurjective
    from toda_rules import TodaDeltaImageFreeCyclicStatement, TodaProp42ExactnessStatement
    from phase168_r3_26_exactness_projection import project_exactness_chains

    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    body_lines = build_narrative_body_lines(result, model)
    body_by_step = {line.step_index: line for line in body_lines}

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

    def typed_sentence(statement, step):
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
        if isinstance(statement, MapSurjective) and isinstance(statement.map, TodaSuspensionMap):
            source = group_tex(statement.map.source_group)
            target = group_tex(statement.map.target_group)
            if source is not None and target is not None:
                return rf"完全性より, $E: {source}\to {target}$ は全射."
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

    chains = project_exactness_chains(model)
    suppressed_exactness = {index for chain in chains for index in chain.step_indices}

    # Place an inferred quotient after an actually present domain presentation.
    # Only already proved Relation steps qualify: no presentation is fabricated.
    postponed_quotients = {}
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if not isinstance(statement, QuotientIsomorphismStatement):
            continue
        for later in range(index + 1, len(model.steps)):
            candidate = model.steps[later].conclusion
            if (isinstance(candidate, Relation)
                and candidate.relation_type is RelationType.EQUALITY
                and candidate.lhs == statement.domain):
                postponed_quotients.setdefault(later, []).append(index)
                break

    postponed_indices = {item for values in postponed_quotients.values() for item in values}
    lines = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        lines.append(f"**[R{citation.number}] {locator}.**")
        lines.append("")
    lines.extend(("証明", ""))
    for chain in chains:
        map_tex = {EHP_E_MAP: "E", EHP_H_MAP: "H", EHP_DELTA_MAP: r"\Delta"}
        sequence = group_tex(chain.arrows[0][0])
        for source, symbol, target in chain.arrows:
            if group_tex(target) is None or symbol not in map_tex:
                raise ValueError("unsupported certified exactness arrow")
            sequence += rf" \xrightarrow{{{map_tex[symbol]}}} {group_tex(target)}"
        lines.append("群構造を決定するために, 次の完全列を考える.")
        lines.append("")
        lines.append(f"${sequence}$.")
        lines.append("")
    for index, step in enumerate(model.steps):
        if index in suppressed_exactness or index in postponed_indices:
            continue
        body_line = body_by_step.get(index)
        if body_line is None:
            sentence = typed_sentence(step.conclusion, step)
            if sentence is not None:
                numbers = model.step_citation_numbers[index]
                tags = ", ".join(f"[R{number}]" for number in numbers)
                if tags and step.rule is ProofRule.GIVEN:
                    sentence = f"{tags}より, " + sentence
                lines.extend((sentence, ""))
            continue
        tags = ", ".join(f"[R{number}]" for number in body_line.citation_numbers)
        if body_line.role == "given":
            prefix = f"{tags}より, " if tags else "前提として, "
        elif body_line.role == "root":
            prefix = f"{tags}を用いて, " if tags else "以上より, "
        else:
            prefix = f"{tags}を用いて, " if tags else "導出により, "
        statement_latex = body_line.statement_latex
        if isinstance(step.conclusion, TodaProp42ExactnessStatement):
            statement_latex = statement_latex.replace(r" \text{ is exact}", "")
            lines.append(f"{prefix}${statement_latex}$ は完全列である.")
        else:
            lines.append(f"{prefix}${statement_latex}$ を得る.")
        lines.append("")
        for postponed in postponed_quotients.get(index, ()):
            postponed_step = model.steps[postponed]
            sentence = typed_sentence(postponed_step.conclusion, postponed_step)
            if sentence is not None:
                lines.extend((sentence, ""))
    if result.status is ProofSearchStatus.COMPLETE:
        lines.append("□")
    return "\n".join(lines).rstrip() + "\n"
