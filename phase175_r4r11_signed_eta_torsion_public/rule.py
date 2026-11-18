"""Source-conditional normalization of a signed Delta image along a 2-torsion suspension.

Let beta = eta_n (n>=3), so beta is a suspension by the cited eta-family
notation.  If 2 beta = 0 and Delta(gamma)=+/-( (2k a - b) o beta ), then
Delta(gamma)=b o beta. The two signs agree because 2(b o beta)=0.

No source fact, order relation, or group result is manufactured here.
"""
from __future__ import annotations

from expression import (
    Composition,
    GeneratorSymbol,
    HomotopyElement,
    MapApplication,
    Multiple,
    Sum,
    Zero,
)
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


RULE_NAME = "signed Delta image normalized by proved eta-family two-torsion"


def eta_two_torsion_normalization_inputs(
    goal: object,
    signed: object,
    two_beta_zero: object,
    definition: object,
) -> tuple[TodaDeltaImageUpToSignStatement, Relation, TodaEtaFamilyGeneralDefinition] | None:
    """Check all typed dimensions and the two independently proved obligations."""
    if (type(goal) is not Relation
            or goal.relation_type is not RelationType.EQUALITY
            or type(goal.lhs) is not MapApplication
            or goal.lhs.map != EHP_DELTA_MAP
            or type(goal.rhs) is not Composition
            or type(signed) is not TodaDeltaImageUpToSignStatement
            or type(signed.positive_value) is not Composition
            or type(signed.positive_value.left) is not Sum
            or type(two_beta_zero) is not Relation
            or two_beta_zero.relation_type is not RelationType.EQUALITY
            or type(two_beta_zero.lhs) is not Multiple
            or type(two_beta_zero.rhs) is not Zero
            or type(definition) is not TodaEtaFamilyGeneralDefinition
            or definition != TodaEtaFamilyGeneralDefinition()):
        return None

    linear = signed.positive_value.left
    beta = signed.positive_value.right
    if (type(linear.left) is not Multiple
            or type(linear.right) is not Multiple
            or type(linear.left.coefficient) is not int
            or linear.left.coefficient % 2 != 0
            or type(linear.right.coefficient) is not int
            or linear.right.coefficient != -1
            or type(beta) is not HomotopyElement
            or type(beta.dimension) is not int
            or type(beta.source) is not int
            or type(beta.target) is not int):
        return None
    n = beta.target
    if (n < 3 or beta.dimension != n or beta.source != n + 1
            or beta.generator != GeneratorSymbol("η", index=n)):
        return None
    # eta_n=E^(n-2) eta_2: n>=3 is a suspension; arbitrary
    # unsuspended two-torsion beta is NOT enough for left distributivity.
    a = linear.left.expression
    b = linear.right.expression
    a_span = typed_endpoints(a)
    b_span = typed_endpoints(b)
    beta_span = typed_endpoints(beta)
    gamma_span = typed_endpoints(signed.element)
    if (a_span is None or a_span != b_span
            or beta_span is None or beta_span[1] != a_span[0]
            or gamma_span is None
            or typed_endpoints(signed.positive_value) != (beta_span[0], a_span[1])
            or signed.map != TodaDeltaMap(
                TodaPrimaryGroup(*gamma_span),
                TodaPrimaryGroup(beta_span[0], a_span[1]),
            )):
        return None
    expected_zero = Relation(Multiple(2, beta), Zero(), RelationType.EQUALITY)
    expected_exact = Relation(
        MapApplication(EHP_DELTA_MAP, signed.element),
        Composition(b, beta),
        RelationType.EQUALITY,
    )
    if two_beta_zero != expected_zero or goal != expected_exact:
        return None
    return signed, two_beta_zero, definition


def signed_eta_two_torsion_rule(
    goal: Relation,
    signed: TodaDeltaImageUpToSignStatement,
    two_beta_zero: Relation,
    definition: TodaEtaFamilyGeneralDefinition,
) -> InferenceRule:
    """Require INFERENCE signed image, INFERENCE order-zero, GIVEN eta definition."""
    required = eta_two_torsion_normalization_inputs(
        goal, signed, two_beta_zero, definition,
    )
    if required is None:
        raise ValueError("not an admissible signed two-torsion Delta normalization")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.INFERENCE
            and premises[2].rule is ProofRule.GIVEN
            and not premises[2].premises
            and tuple(step.conclusion for step in premises) == required
            and eta_two_torsion_normalization_inputs(
                goal, signed, two_beta_zero, definition,
            ) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "For a cited eta_n suspension (n>=3), a proved 2 eta_n=0, "
            "and independently proved signed Delta(gamma)=+/-( (2k a-b)o eta_n ), "
            "left distributivity gives -(b o eta_n) up to sign. "
            "Since 2(b o eta_n)=0, both signs equal +(b o eta_n). "
            "No group structure is inferred and no missing source is assumed."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaDeltaImageUpToSignStatement,
                statement_pattern=required[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[1],
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaEtaFamilyGeneralDefinition,
                statement_pattern=required[2],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_signed_eta_two_torsion(
    goal: object,
    candidates: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose only against independently source-discovered signed candidates."""
    if not isinstance(candidates, tuple):
        raise TypeError("candidates must be a tuple")
    if not isinstance(goal, Relation):
        return ()
    definition = TodaEtaFamilyGeneralDefinition()
    if (not isinstance(goal.rhs, Composition)
            or not isinstance(goal.rhs.right, HomotopyElement)):
        return ()
    beta = goal.rhs.right
    order_zero = Relation(Multiple(2, beta), Zero(), RelationType.EQUALITY)
    options = []
    for signed in candidates:
        if not isinstance(signed, TodaDeltaImageUpToSignStatement):
            continue
        required = eta_two_torsion_normalization_inputs(
            goal, signed, order_zero, definition,
        )
        if required is None or required in (x.subgoals for x in options):
            continue
        options.append(GoalExpansion(
            signed_eta_two_torsion_rule(goal, signed, order_zero, definition),
            required,
        ))
    return tuple(options)
