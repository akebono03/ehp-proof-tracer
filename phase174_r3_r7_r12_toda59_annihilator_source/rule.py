"""Generic instance inference from a separately certified family annihilator.

This candidate has no production wiring and creates no mathematical GIVEN.
The source schema must be independently admitted by an audited registry before
any real proof search can close the instance as an INFERENCE.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families, registered_family_of,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "source-qualified general family annihilator specialization"


def canonical_annihilator_instance(
    source: object,
    left_index: object,
) -> Relation | None:
    """Construct a typed goal for any valid certified family-pair schema."""
    if not isinstance(source, CitedFamilyAnnihilator):
        return None
    if (type(left_index) is not int or type(source.minimum_left_index) is not int
            or left_index < max(2, source.minimum_left_index)
            or type(source.right_index_offset) is not int
            or source.right_index_offset < 1
            or type(source.left_family_id) is not int
            or type(source.right_family_id) is not int
            or not source.citation_locator):
        return None
    families = read_registered_stable_families()
    left = tuple(f for f in families if f.family_id == source.left_family_id)
    right = tuple(f for f in families if f.family_id == source.right_family_id)
    if len(left) != 1 or len(right) != 1:
        return None
    first, second = left[0], right[0]
    j = left_index + source.right_index_offset
    if (first.stem != source.right_index_offset
            or left_index < first.minimum_n or j < second.minimum_n
            or first.stem <= 0 or second.stem <= 0):
        return None

    def member(family: object, n: int) -> HomotopyElement:
        return HomotopyElement(
            name=family.name_at(n), dimension=n,
            source=n + family.stem, target=n,
            generator=GeneratorSymbol(family.symbol_family, n),
        )

    a, b = member(first, left_index), member(second, j)
    if (registered_family_of(a) != first or registered_family_of(b) != second
            or a.source != b.target):
        return None
    return Relation(
        lhs=Composition(a, b), rhs=Zero(), relation_type=RelationType.EQUALITY,
    )


def annihilator_specialization_inputs(
    goal: object,
    available: tuple[object, ...],
) -> tuple[CitedFamilyAnnihilator, ...]:
    """Find only explicitly available cited schemas; never create a source leaf."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.rhs, Zero)
            or not isinstance(goal.lhs, Composition)
            or not isinstance(goal.lhs.left, HomotopyElement)):
        return ()
    n = goal.lhs.left.dimension
    found: list[CitedFamilyAnnihilator] = []
    for source in available:
        if not isinstance(source, CitedFamilyAnnihilator) or source in found:
            continue
        if canonical_annihilator_instance(source, n) == goal:
            found.append(source)
    return tuple(found)


def cited_annihilator_specialization_rule(
    goal: Relation,
    source: CitedFamilyAnnihilator,
) -> InferenceRule:
    """Require the exact certified general-source statement as a GIVEN step."""
    if annihilator_specialization_inputs(goal, (source,)) != (source,):
        raise ValueError("nonmatching source-qualified family relation")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == source
            and annihilator_specialization_inputs(goal, (source,)) == (source,)
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "A citation-screened general family annihilator may be instantiated "
            "at a type-compatible index. The cited law itself must be proved "
            "as a source leaf independently; this rule never creates one."
        ),
        premise_patterns=(PremisePattern(
            statement_type=CitedFamilyAnnihilator,
            statement_pattern=source,
            proof_rule=ProofRule.GIVEN,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_cited_annihilator_specialization(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Return source-bound *unproved* goals without production registration."""
    source_options = annihilator_specialization_inputs(goal, available)
    return tuple(
        GoalExpansion(
            rule=cited_annihilator_specialization_rule(goal, source),
            subgoals=(source,),
        )
        for source in source_options
    )
