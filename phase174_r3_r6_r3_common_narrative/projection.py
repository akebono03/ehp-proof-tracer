"""Phase 174 R3-R6-R3: display projections of existing typed proof steps.

This module never manufactures ProofSteps, looks up a database goal, or adds
source references. All mathematical claims are checked against the supplied
inference step and its exact premises before they are displayed.
"""
from __future__ import annotations

from homotopy_groups import TodaIteratedSuspensionMap
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase168_r3_3_proof_narrative_model import NarrativeCitation, ProofNarrativeModel
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    SOURCE_RECORDS,
)
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48IndexTwoDoubleSuspensionStatement,
    Toda48UniversalConditionalStatement,
    finite_index_two_cyclic_conclusion,
    toda48_delta_goal,
)
from proof import ProofRule, ProofStep


def project_verified_index_two_statement(statement: object, step: object) -> str | None:
    """Verbalize a proved (4.8) instance, never the conditional source alone."""
    if (
        not isinstance(statement, Toda48IndexTwoDoubleSuspensionStatement)
        or not isinstance(step, ProofStep)
        or step.rule is not ProofRule.INFERENCE
        or step.conclusion != statement
        or len(step.premises) != 2
    ):
        return None
    delta_step, source_step = step.premises
    delta = toda48_delta_goal(statement)
    if (
        delta is None
        or delta_step.rule is not ProofRule.INFERENCE
        or delta_step.conclusion != delta
        or source_step.rule is not ProofRule.GIVEN
        or type(source_step.conclusion) is not Toda48UniversalConditionalStatement
        or source_step.conclusion != Toda48UniversalConditionalStatement()
        or not isinstance(statement.map, TodaIteratedSuspensionMap)
    ):
        return None
    from phase168_r3_27_typed_statement_projection import group_tex

    source = group_tex(statement.map.source_group)
    target = group_tex(statement.map.target_group)
    if source is None or target is None:
        return None
    exponent = statement.map.exponent
    order = statement.quotient_order
    return (
        rf"Toda (4.8) と $\Delta=0$ より, "
        rf"$E^{{{exponent}}}:{source}\hookrightarrow {target}$ は単射で, "
        rf"${target}/E^{{{exponent}}}({source})\cong\mathbb{{Z}}/{order}$."
    )


def project_verified_cyclic_extension_reason(statement: object, step: object) -> str | None:
    """Explain |B| and the generator using exactly the three proved premises.

    This deliberately does not repeat B=Z/(2m){b}: the separately certified
    final group relation remains the only displayed conclusion of that form.
    """
    if (
        not isinstance(statement, CyclicStructureStatement)
        or not isinstance(step, ProofStep)
        or step.rule is not ProofRule.INFERENCE
        or step.conclusion != statement
        or len(step.premises) != 3
    ):
        return None
    index_step, prior_step, double_step = step.premises
    if (
        index_step.rule is not ProofRule.INFERENCE
        or double_step.rule is not ProofRule.INFERENCE
        or prior_step.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE)
        or not isinstance(index_step.conclusion, Toda48IndexTwoDoubleSuspensionStatement)
        or toda48_delta_goal(index_step.conclusion) is None
        or finite_index_two_cyclic_conclusion(
            index_step.conclusion, prior_step.conclusion, double_step.conclusion
        ) != statement
    ):
        return None
    from phase168_r3_27_typed_statement_projection import element_tex, group_tex

    source = group_tex(index_step.conclusion.map.source_group)
    target = group_tex(statement.group)
    if source is None or target is None:
        return None
    size = prior_step.conclusion.rhs.order
    order = statement.order
    index = index_step.conclusion.quotient_order
    if type(size) is not int or type(index) is not int or order != index * size:
        return None
    generator = element_tex(statement.generator)
    reason = (
        rf"位数 ${size}$ の巡回群 ${source}$ が単射 $E^2$ により "
        rf"${target}$ に指数 ${index}$ で入り, 証明済みの二倍関係が "
        rf"その生成元を与える. よって "
        rf"$|{target}|={index}\cdot {size}={order}$."
    )
    if generator is not None:
        reason += rf" また, ${generator}$ は位数 ${order}$ を持ち, この群を生成する."
    return reason


def display_cited_nu_family_locator(citation: object, model: object) -> str | None:
    """Shorten only a source-linked ν-family heading; keep locator identity.

    A matching literal label by itself is not enough. The cited source must
    actually own a GIVEN typed general family definition in the proof model.
    """
    if not isinstance(citation, NarrativeCitation) or not isinstance(model, ProofNarrativeModel):
        return None
    locator = citation.reference.locator or citation.reference.label
    records = tuple(row for row in SOURCE_RECORDS if row.family_id == 4)
    if len(records) != 1 or locator != records[0].locator:
        return None
    record = records[0]
    expected = CitedStableFamilyDefinition(
        family_id=record.family_id,
        minimum_n=record.minimum_n,
        stem=record.stem,
    )
    for index in citation.step_indices:
        if type(index) is not int or not 0 <= index < len(model.steps):
            return None
        step = model.steps[index]
        if (
            step.rule is ProofRule.GIVEN
            and step.conclusion == expected
            and index < len(model.step_citation_numbers)
            and citation.number in model.step_citation_numbers[index]
        ):
            return "Chapter V, iii)"
    return None
