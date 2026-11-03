"""A generator-independent typed consequence of Toda Proposition 4.4.

A source-screened Proposition 4.4, cited Hopf identity and two independently
admitted earlier DB groups are REQUIRED. Only the abstract group structure is
concluded. This never identifies a named generator or installs a Web route.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    group_coordinates,
    verified_db_step,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase173_r4_r10_general_toda56_core.core import (
    HOPF_ROOT_NAME,
    _abstract_group_signature,
    checked_abstract_inputs,
)
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)


ABSTRACT_RULE_NAME = "Toda Proposition 4.4 source-first abstract direct-sum result"


@dataclass(frozen=True)
class TodaProp44AbstractGroupResult:
    """Abstract cyclic invariants, never a labelled generator presentation.

    A ('free', 0) entry denotes one infinite cyclic summand. Each
    ('finite', m) entry denotes an abstract cyclic summand of order m.
    """

    group: TodaPrimaryGroup
    invariant_summands: tuple[tuple[str, int], ...]


def canonical_abstract_result(proof_target: object) -> TodaProp44AbstractGroupResult | None:
    """Construct only a DB-screened n=4, k-unbounded abstract consequence."""
    pair = checked_abstract_inputs(proof_target)
    coords = group_coordinates(proof_target)
    if pair is None or coords is None:
        return None
    n, k = coords
    if n != 4 or type(k) is not int or k < 3:
        return None
    signatures = tuple(_abstract_group_signature(item) for item in pair)
    if any(signature is None for signature in signatures):
        return None
    invariants = tuple(sorted(signatures[0] + signatures[1]))
    return TodaProp44AbstractGroupResult(
        group=TodaPrimaryGroup(n + k, n),
        invariant_summands=invariants,
    )


def abstract_toda44_rule(
    statement: TodaProp44AbstractGroupResult, *,
    proof_target: object, bridge: object = None,
) -> InferenceRule:
    """Require the exact cited theorem, two verified DB priors and Hopf inference.

    This is an inference-rule candidate only; it NEVER manufactures a GIVEN
    statement or automatically adds a source to a proof context.
    """
    expected_result = canonical_abstract_result(proof_target)
    if expected_result is None or statement != expected_result:
        raise ValueError("Unreviewed or noncanonical abstract Proposition 4.4 target")
    first, second = checked_abstract_inputs(proof_target)
    theorem = TodaProp44UniversalStatement()
    hopf = canonical_hopf_relation()
    expected = (theorem, first, second, hopf)

    def guard(premises, bindings):
        if len(premises) != 4 or bindings:
            return False
        if tuple(step.conclusion for step in premises) != expected:
            return False
        theorem_step, first_step, second_step, hopf_step = premises
        if (theorem_step.rule is not ProofRule.GIVEN
                or not verified_db_step(first_step, proof_target=proof_target, bridge=bridge)
                or not verified_db_step(second_step, proof_target=proof_target, bridge=bridge)):
            return False
        if (hopf_step.rule is not ProofRule.INFERENCE
                or hopf_step.inference_rule is None
                or hopf_step.inference_rule.name != HOPF_ROOT_NAME
                or hopf_step.inference_rule.conclusion_pattern != hopf
                or len(hopf_step.premises) != 1):
            return False
        original = hopf_step.premises[0]
        if (original.rule is not ProofRule.GIVEN
                or original.conclusion != TodaLemma54TypedSource()
                or not hopf_step.inference_rule.match_guard((original,), ())):
            return False
        return (canonical_abstract_result(proof_target) == statement
                and checked_abstract_inputs(proof_target) == (first, second))

    return InferenceRule(
        name=ABSTRACT_RULE_NAME,
        description=(
            "Derive abstract free and 2-primary cyclic invariants by the "
            "source-verified Toda Proposition 4.4 splitting using "
            "H(nu_4)=iota_7 from Lemma 5.4 and two independently adopted "
            "earlier database groups. No individual generator transport is asserted."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=theorem,
            ),
            PremisePattern(statement_type=type(first), statement_pattern=first),
            PremisePattern(statement_type=type(second), statement_pattern=second),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=statement,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_abstract_toda44(
    statement: object, available: tuple[object, ...], *,
    proof_target: object, bridge: object = None,
) -> tuple[GoalExpansion, ...]:
    """Offer an abstract root only in an independently source-screened context."""
    if not isinstance(available, tuple):
        raise TypeError("Source-screened context must be a tuple")
    if not isinstance(statement, TodaProp44AbstractGroupResult):
        return ()
    if canonical_abstract_result(proof_target) != statement:
        return ()
    for source in (TodaProp44UniversalStatement(), TodaLemma54TypedSource()):
        if sum(type(item) is type(source) and item == source for item in available) != 1:
            return ()
    first, second = checked_abstract_inputs(proof_target)
    return (GoalExpansion(
        abstract_toda44_rule(statement, proof_target=proof_target, bridge=bridge),
        (TodaProp44UniversalStatement(), first, second, canonical_hopf_relation()),
    ),)
