"""Cited Toda Proposition 2.5 for unsigned, explicitly typed Delta images."""
from __future__ import annotations

from expression import Composition, IteratedSuspension, MapApplication
from map_facts import EHP_DELTA_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "cited Toda Proposition 2.5 conditional unsigned Delta composition equality"


def unsigned_prop25_inputs(
    goal: object, base: object, composition_identity: object = None,
) -> tuple[object, ...] | None:
    """Validate exact syntax, map dimensions and the arithmetic equality branch.

    Without a separate identity the argument must literally be alpha o E^2 beta.
    Otherwise that identity is a mandatory, independently inferred premise.
    No alias conversion, sign normalization or 2-primary flag is assumed.
    """
    for relation in (goal, base):
        if (type(relation) is not Relation
                or relation.relation_type is not RelationType.EQUALITY
                or type(relation.lhs) is not MapApplication
                or relation.lhs.map != EHP_DELTA_MAP):
            return None
    if type(goal.rhs) is not Composition or goal == base:
        return None
    alpha, x = base.lhs.expression, base.rhs
    beta = goal.rhs.right
    if goal.rhs.left != x:
        return None
    explicit = Composition(alpha, IteratedSuspension(beta, 2))
    gamma = goal.lhs.expression
    a = typed_endpoints(alpha)
    b = typed_endpoints(beta)
    if a is None or b is None or (a[1] - 1) % 2:
        return None
    m, i, j = (a[1] - 1) // 2, a[0] - 1, b[0] + 1
    if (m < 2 or i < 2*m or j < i or b != (j-1, i-1)
            or not (m % 2 == 1 or j < 3*m-1)
            or typed_endpoints(x) != (i-1, m)
            or typed_endpoints(explicit) != (j+1, 2*m+1)
            or typed_endpoints(gamma) != (j+1, 2*m+1)
            or typed_endpoints(goal.rhs) != (j-1, m)):
        return None
    if composition_identity is None:
        if gamma != explicit:
            return None
        return (CitedTodaProp25(), base)
    if (type(composition_identity) is not Relation
            or composition_identity.relation_type is not RelationType.EQUALITY
            or composition_identity.lhs != explicit
            or composition_identity.rhs != gamma
            or composition_identity in (goal, base)):
        return None
    return (CitedTodaProp25(), base, composition_identity)


def unsigned_prop25_rule(
    goal: Relation, base: Relation, composition_identity: Relation | None = None,
) -> InferenceRule:
    """Require an actual cited GIVEN and the exact independently inferred inputs."""
    required = unsigned_prop25_inputs(goal, base, composition_identity)
    if required is None:
        raise ValueError("not a typed conditional unsigned Proposition 2.5 goal")

    def guard(premises, bindings):
        return (len(premises) == len(required)
                and tuple(step.conclusion for step in premises) == required
                and type(premises[0].conclusion) is CitedTodaProp25
                and premises[0].rule is ProofRule.GIVEN
                and not premises[0].premises
                and all(step.rule is ProofRule.INFERENCE for step in premises[1:])
                and unsigned_prop25_inputs(goal, base, composition_identity) == required)

    return InferenceRule(
        name=RULE_NAME,
        description=("Toda Proposition 2.5: when m is odd or j < 3m-1, "
                     "Delta(alpha o E^2 beta) = Delta(alpha) o beta. "
                     "Require a proved unsigned base equality and, if the argument "
                     "is not literal, a separately proved composition equality."),
        literature_reference=LiteratureReference(
            label="Toda Proposition 2.5", locator="Proposition 2.5"),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN, statement_type=CitedTodaProp25,
            statement_pattern=required[0]),) + tuple(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=statement)
            for statement in required[1:]),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_unsigned_prop25(
    goal: object, base: object, composition_identity: object = None,
) -> tuple[GoalExpansion, ...]:
    """Return only an ordinary backward proposal; create no proof or GIVEN."""
    required = unsigned_prop25_inputs(goal, base, composition_identity)
    if required is None:
        return ()
    return (GoalExpansion(unsigned_prop25_rule(goal, base, composition_identity), required),)
