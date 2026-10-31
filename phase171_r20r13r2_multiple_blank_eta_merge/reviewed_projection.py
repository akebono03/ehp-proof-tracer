"""Source-bound presentation of adjacent eta equations and sentence boundaries.

This module never infers new mathematics. It combines only existing rendered
sentences whose exact content is backed by INFERENCE ProofSteps in the final
root ancestry and a cited general eta definition. Partial proofs are unchanged.
"""
from __future__ import annotations

from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase168_r3_27_typed_statement_projection import element_tex, typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from homotopy_groups import TodaSuspensionMap
from proof import ProofRule


def verified_eta_display_sentences(model) -> dict[str, tuple[str, str]]:
    """Map existing source-tagged sentences to (same tag, existing math body).

    A line is eligible only if it is an exact rendering of a certified typed
    suspension step with an actually cited eta-definition GIVEN ancestor.
    """
    if model.root_index is None:
        return {}
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    allowed: dict[str, tuple[str, str]] = {}
    for index in scope:
        step = model.steps[index]
        statement = step.conclusion
        if step.rule is not ProofRule.INFERENCE:
            continue
        if not isinstance(statement, (GeneratorSuspension, GeneratorImage)):
            continue
        if not isinstance(statement.map, TodaSuspensionMap):
            continue
        source = element_tex(statement.source_generator)
        target = element_tex(statement.target_generator)
        if source is None or target is None:
            continue
        if not (source.startswith(r"\eta_{") and target.startswith(r"\eta_{")):
            continue
        sentence = typed_sentence(statement, step)
        if sentence is None or not sentence.startswith("$E(") or not sentence.endswith("$."):
            continue
        cited: list[int] = []
        visited: set[int] = set()
        pending = [step]
        while pending:
            ancestor = pending.pop()
            if id(ancestor) in visited:
                continue
            visited.add(id(ancestor))
            if (ancestor.rule is ProofRule.GIVEN
                    and isinstance(ancestor.conclusion, TodaEtaFamilyGeneralDefinition)):
                for source_index, source_step in enumerate(model.steps):
                    if source_step is ancestor or source_step == ancestor:
                        for number in model.step_citation_numbers[source_index]:
                            if number not in cited:
                                cited.append(number)
                        break
            pending.extend(ancestor.premises)
        if not cited:
            continue
        tag = ", ".join(f"[R{number}]" for number in cited) + "より, "
        full_line = tag + sentence
        math_body = sentence[1:-2]  # take only existing TeX, excluding $ and period
        allowed[full_line] = (tag, math_body)
    return allowed


def combine_adjacent_verified_eta_sentences(lines: list[str], model) -> list[str]:
    """Combine neighboring printed certified equations sharing one citation.

    Empty Markdown separators between these equations may be crossed. Other
    mathematics, differently sourced results and nonadjacent lines are kept.
    """
    allowed = verified_eta_display_sentences(model)
    result: list[str] = []
    index = 0
    while index < len(lines):
        first = allowed.get(lines[index])
        if first is None:
            result.append(lines[index])
            index += 1
            continue
        tag, first_math = first
        terms = [first_math]
        cursor = index + 1
        while cursor < len(lines):
            # Standard narrative inserts precisely one empty line per sentence.
            has_separator = lines[cursor] == ""
            next_index = cursor + 1 if has_separator else cursor
            if next_index >= len(lines):
                break
            candidate = allowed.get(lines[next_index])
            if candidate is None or candidate[0] != tag:
                break
            terms.append(candidate[1])
            cursor = next_index + 1
        if len(terms) < 2:
            result.append(lines[index])
            index += 1
            continue
        result.append(tag + "$" + r",\quad ".join(terms) + "$.")
        index = cursor
    return result


def _split_outside_math_at_period(line: str) -> list[str]:
    """Split ASCII '. ' prose boundaries, not decimals or math expressions."""
    pieces: list[str] = []
    begin = 0
    math_mode = False
    index = 0
    while index < len(line):
        char = line[index]
        if char == "$" and (index == 0 or line[index - 1] != "\\"):
            math_mode = not math_mode
        if (not math_mode and char == "."
                and index + 1 < len(line) and line[index + 1] == " "
                and index > 0):
            # Dot is part of the sentence. Subsequent prose starts a new line.
            pieces.append(line[begin:index + 1].strip())
            begin = index + 2
        index += 1
    pieces.append(line[begin:].strip())
    return [piece for piece in pieces if piece]


def split_completed_proof_sentences(lines: list[str]) -> list[str]:
    """Use real Markdown paragraph breaks at periods only in the proof body.

    Do not touch citation locators (e.g. Proposition 5.6.), reference bodies,
    math notation, or an incomplete proof's diagnostic section.
    """
    result: list[str] = []
    in_body = False
    for line in lines:
        if line == "証明":
            in_body = True
            result.append(line)
            continue
        if not in_body or not line or line == "□":
            result.append(line)
            continue
        sentences = _split_outside_math_at_period(line)
        if len(sentences) < 2:
            result.append(line)
            continue
        for i, sentence in enumerate(sentences):
            if i:
                result.append("")
            result.append(sentence)
    return result


def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    return split_completed_proof_sentences(
        combine_adjacent_verified_eta_sentences(lines, model)
    )
