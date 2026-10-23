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

    # Each certified window is a path of two typed arrows. Merge only
    # windows sharing the *same* consecutive typed arrow (not merely a group).
    # An ambiguous branch or cycle is left separate, rather than guessed.
    exactness_steps = []
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if (isinstance(statement, TodaProp42ExactnessStatement)
                and prop42_exactness_indices(statement) is not None):
            w = statement.window
            arrows = (
                (w.source_term, w.first_map, w.middle_term),
                (w.middle_term, w.second_map, w.target_term),
            )
            if all(group_tex(g) is not None for g in
                   (w.source_term, w.middle_term, w.target_term)):
                exactness_steps.append((index, arrows))

    # An arrow is represented by its actual source, map and target objects.
    # Only maximal non-branching paths are rendered as combined sequences.
    arrows_to_windows = {}
    for index, pair in exactness_steps:
        for arrow in pair:
            arrows_to_windows.setdefault(arrow, set()).add(index)
    next_arrows = {}
    prev_arrows = {}
    for _, pair in exactness_steps:
        left, right = pair
        next_arrows.setdefault(left, set()).add(right)
        prev_arrows.setdefault(right, set()).add(left)
    seen_arrows = set()
    merged_sequences = []
    suppressed_exactness = set()
    for index, pair in exactness_steps:
        for arrow in pair:
            if arrow in seen_arrows:
                continue
            # Explore the undirected component and verify it is one chain.
            component = set()
            frontier = [arrow]
            while frontier:
                current = frontier.pop()
                if current in component:
                    continue
                component.add(current)
                frontier.extend(next_arrows.get(current, ()))
                frontier.extend(prev_arrows.get(current, ()))
            seen_arrows.update(component)
            if len(component) < 3:
                continue
            if any(len(next_arrows.get(a, ())) > 1 or
                   len(prev_arrows.get(a, ())) > 1 for a in component):
                continue
            starts = [a for a in component if not prev_arrows.get(a)]
            if len(starts) != 1:
                continue
            ordered = []
            current = starts[0]
            while current not in ordered:
                ordered.append(current)
                successors = next_arrows.get(current, ())
                if not successors:
                    break
                current = next(iter(successors))
            if len(ordered) != len(component):
                continue
            included = {i for i, pair in exactness_steps
                        if pair[0] in component and pair[1] in component}
            if len(included) < 2:
                continue
            map_tex = {
                EHP_E_MAP: "E",
                EHP_H_MAP: "H",
                EHP_DELTA_MAP: r"\\Delta",
            }
            if any(a[1] not in map_tex for a in ordered):
                continue
            sequence = group_tex(ordered[0][0])
            for source, map_symbol, target in ordered:
                sequence += (rf" \\xrightarrow{{{map_tex[map_symbol]}}} "
                             + group_tex(target))
            merged_sequences.append((min(included), sequence))
            suppressed_exactness.update(included)
    merged_sequences.sort(key=lambda item: item[0])

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
    for _, sequence in merged_sequences:
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
