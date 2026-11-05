"""Focused common-renderer checks: no new proof facts, citations or hardcoded goal."""
from __future__ import annotations

from dataclasses import replace

from expression import HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import NarrativeCitation, ProofNarrativeModel
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    SOURCE_RECORDS,
)
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48IndexTwoDoubleSuspensionStatement,
    Toda48UniversalConditionalStatement,
    toda48_delta_goal,
)
from phase174_r3_r6_r3_common_narrative.projection import (
    display_cited_nu_family_locator,
    project_verified_cyclic_extension_reason,
    project_verified_index_two_statement,
)
from proof import LiteratureReference, ProofRule, ProofStep, Relation, RelationType


def _configuration(n: int, m: int):
    a = TodaPrimaryGroup(2 * n - 2, n - 1)
    b = TodaPrimaryGroup(2 * n, n + 1)
    generator_a = HomotopyElement("a", n - 1, 2 * n - 2, n - 1)
    generator_b = HomotopyElement("b", n + 1, 2 * n, n + 1)
    statement = Toda48IndexTwoDoubleSuspensionStatement(TodaIteratedSuspensionMap(2, a, b))
    delta = toda48_delta_goal(statement)
    assert delta is not None
    delta_step = ProofStep(delta, (), ProofRule.INFERENCE)
    source_step = ProofStep(Toda48UniversalConditionalStatement(), (), ProofRule.GIVEN)
    index_step = ProofStep(statement, (delta_step, source_step), ProofRule.INFERENCE)
    prior = Relation(a, FiniteCyclicGroup(m, generator_a), RelationType.EQUALITY)
    double = Relation(Multiple(2, generator_b), IteratedSuspension(generator_a, 2), RelationType.EQUALITY)
    cyclic = CyclicStructureStatement(b, generator_b, 2 * m)
    cyclic_step = ProofStep(cyclic, (
        index_step,
        ProofStep(prior, (), ProofRule.INFERENCE),
        ProofStep(double, (), ProofRule.INFERENCE),
    ), ProofRule.INFERENCE)
    return index_step, cyclic_step


def test_index_two_presents_only_verified_conditional_instance() -> None:
    index_step, cyclic_step = _configuration(4, 4)
    rendered = project_verified_index_two_statement(index_step.conclusion, index_step)
    assert rendered is not None
    assert r"E^{2}:\pi_{6}^{3}\hookrightarrow \pi_{8}^{5}" in rendered
    assert r"\pi_{8}^{5}/E^{2}(\pi_{6}^{3})\cong\mathbb{Z}/2" in rendered
    assert project_verified_index_two_statement(
        index_step.conclusion,
        ProofStep(index_step.conclusion, (index_step.premises[0],), ProofRule.INFERENCE),
    ) is None
    assert project_verified_index_two_statement(
        index_step.conclusion,
        ProofStep(index_step.conclusion, index_step.premises, ProofRule.GIVEN),
    ) is None
    assert project_verified_index_two_statement(cyclic_step.conclusion, cyclic_step) is None


def test_cyclic_reason_uses_typed_premises_not_fixed_generator_or_sphere() -> None:
    _, step_four = _configuration(4, 4)
    _, step_six = _configuration(6, 6)
    four = project_verified_cyclic_extension_reason(step_four.conclusion, step_four)
    six = project_verified_cyclic_extension_reason(step_six.conclusion, step_six)
    assert four is not None and six is not None
    assert r"|\pi_{8}^{5}|=2\cdot 4=8" in four
    assert r"|\pi_{12}^{7}|=2\cdot 6=12" in six
    assert "ν₅" not in four + six
    assert r"\pi_{8}^{5}=\mathbb{Z}/8" not in four


def test_cyclic_reason_rejects_mismatched_and_unproved_premises() -> None:
    _, cyclic_step = _configuration(4, 4)
    wrong_double = ProofStep(
        cyclic_step.premises[2].conclusion, (), ProofRule.GIVEN,
    )
    wrong = ProofStep(cyclic_step.conclusion, (
        cyclic_step.premises[0], cyclic_step.premises[1], wrong_double,
    ), ProofRule.INFERENCE)
    assert project_verified_cyclic_extension_reason(wrong.conclusion, wrong) is None
    wrong_statement = replace(cyclic_step.conclusion, order=16)
    assert project_verified_cyclic_extension_reason(wrong_statement, cyclic_step) is None


def test_short_nu_heading_requires_an_owned_typed_given_source() -> None:
    record = next(row for row in SOURCE_RECORDS if row.family_id == 4)
    source = CitedStableFamilyDefinition(record.family_id, record.minimum_n, record.stem)
    citation = NarrativeCitation(
        number=1,
        reference=LiteratureReference(label=record.locator, locator=record.locator),
        step_indices=(0,),
    )
    cited = ProofStep(source, (), ProofRule.GIVEN)
    model = ProofNarrativeModel(
        steps=(cited,), citations=(citation,), step_citation_numbers=((1,),),
        root_index=0, status=ProofSearchStatus.COMPLETE,
    )
    assert display_cited_nu_family_locator(citation, model) == "Chapter V, iii)"
    bad_step = ProofStep(source, (), ProofRule.INFERENCE)
    bad_model = replace(model, steps=(bad_step,))
    assert display_cited_nu_family_locator(citation, bad_model) is None
    bad_citation = replace(citation, reference=LiteratureReference(
        label="unverified", locator="unverified",
    ))
    assert display_cited_nu_family_locator(bad_citation, model) is None


def test_real_completed_proof_displays_index_order_and_reference_once() -> None:
    from phase174_r3_r6_r2_prop44_lemma54.audit import inspect

    result = inspect()
    assert result["root_status"] == "complete"
    assert result["root_proven_steps"] == 16
    assert result["new_group_given"] == 0
    narrative = result["narrative"]
    assert r"E^{2}:\pi_{6}^{3}\hookrightarrow \pi_{8}^{5}" in narrative
    assert r"\pi_{8}^{5}/E^{2}(\pi_{6}^{3})\cong\mathbb{Z}/2" in narrative
    assert r"|\pi_{8}^{5}|=2\cdot 4=8" in narrative
    assert "Chapter V, iii)" in narrative
    assert "Chapter V, ν-family definition (after Lemma 5.5)" not in narrative
    conclusion_lines = tuple(
        line for line in narrative.splitlines()
        if r"\pi_{8}^{5}" in line and r"\mathbb{Z}/8" in line and "=" in line
    )
    assert len(conclusion_lines) == 1, conclusion_lines
