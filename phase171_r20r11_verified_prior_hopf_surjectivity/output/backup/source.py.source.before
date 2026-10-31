"""Source-bound cyclic-generator surjectivity, without recycled complete proofs.

The printed group theorem is specialized as an INFERENCE from a screened
fixed general statement.  H(x)=g is separately reconstructed from its own
cited premises; neither is admitted as a new GIVEN.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension, MapApplication, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase171_r2i_eta_hopf_bridge.source import eligible_eta_hopf_chains
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def _coordinates(value: object) -> tuple[int, int] | None:
    """Return (source, target) of a well-typed concrete homotopy element."""
    if isinstance(value, HomotopyElement):
        s, t = value.source, value.target
        if (type(s) is int and type(t) is int
                and type(value.dimension) is int
                and value.dimension == t and s >= t >= 2):
            return s, t
        return None
    if isinstance(value, Composition):
        left = _coordinates(value.left)
        right = _coordinates(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    if isinstance(value, Suspension):
        inner = _coordinates(value.expression)
        return None if inner is None else (inner[0] + 1, inner[1] + 1)
    if isinstance(value, IteratedSuspension):
        inner = _coordinates(value.expression)
        k = value.exponent
        return (inner[0] + k, inner[1] + k) if inner is not None and type(k) is int and k >= 0 else None
    return None


def _same_generator(left: object, right: object, order: int) -> bool:
    """Use exact typed equality or the pre-existing, ID-checked name alias."""
    if left == right:
        return True
    if type(order) is not int or order <= 1:
        return False
    return same_registered_group_presentation(
        FiniteCyclicGroup(order, left), FiniteCyclicGroup(order, right),
    )


def _eligible_group_instance(source: object, group: Relation) -> bool:
    """Recognize one existing positioned higher-stem group theorem.

    The general source provides the mathematics. HyoujiGen supplies only
    the spelling/degree identity of its concrete named generator.
    """
    if (not isinstance(source, Relation)
            or not isinstance(group, Relation)
            or group.relation_type is not RelationType.EQUALITY
            or not isinstance(group.lhs, TodaPrimaryGroup)
            or not isinstance(group.rhs, FiniteCyclicGroup)):
        return False
    n = group.lhs.sphere_dimension
    if type(n) is not int:
        return False
    specialized = specialize_registered_higher_stem(source, n)
    return (specialized is not None
            and specialized == group
            and type(group.rhs.order) is int
            and group.rhs.order > 1)


def cyclic_group_from_cited_general_rule(goal: Relation, source: Relation) -> InferenceRule:
    """Specialize the screened general fixed theorem, never the DB result."""
    if not _eligible_group_instance(source, goal):
        raise ValueError("source does not specialize to this typed cyclic group")

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and premises[0].conclusion == source
                and _eligible_group_instance(source, goal))

    return InferenceRule(
        name="specialize earlier cited cyclic group schema",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=Relation,
            relation_type=RelationType.EQUALITY,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def _valid_surjective_pair(
    goal: MapSurjective, group: Relation, image: Relation,
) -> bool:
    """Check the exact H-domain, codomain and generating image."""
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaHopfInvariantMap):
        return False
    mapping = goal.map
    if (not isinstance(mapping.source_group, TodaPrimaryGroup)
            or not isinstance(mapping.target_group, TodaPrimaryGroup)
            or not isinstance(group, Relation)
            or group.relation_type is not RelationType.EQUALITY
            or group.lhs != mapping.target_group
            or not isinstance(group.rhs, FiniteCyclicGroup)
            or type(group.rhs.order) is not int or group.rhs.order <= 1
            or not isinstance(image, Relation)
            or image.relation_type is not RelationType.EQUALITY
            or not isinstance(image.lhs, MapApplication)
            or image.lhs.map != EHP_H_MAP):
        return False
    src = _coordinates(image.lhs.expression)
    dst = _coordinates(image.rhs)
    generator = _coordinates(group.rhs.generator)
    if src is None or dst is None or generator is None:
        return False
    q, n = src
    if (q < n or mapping.source_group != TodaPrimaryGroup(q, n)
            or mapping.target_group != TodaPrimaryGroup(q, 2 * n - 1)
            or dst != (q, 2 * n - 1)
            or generator != dst):
        return False
    return _same_generator(group.rhs.generator, image.rhs, group.rhs.order)


def cyclic_generator_image_surjectivity_rule(
    goal: MapSurjective, group: Relation, image: Relation,
) -> InferenceRule:
    """A homomorphism hitting a certified cyclic generator is surjective."""
    if not _valid_surjective_pair(goal, group, image):
        raise ValueError("cyclic group and Hopf generator image do not match")

    def guard(premises, bindings):
        return (len(premises) == 2
                and all(step.rule is ProofRule.INFERENCE for step in premises)
                and premises[0].conclusion == group
                and premises[1].conclusion == image
                and _valid_surjective_pair(goal, group, image))

    return InferenceRule(
        name="cyclic codomain generator in image implies Hopf surjectivity",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_cyclic_hopf_surjectivity(
    goal: object, available: tuple[object, ...], *, proof_target: object = None,
) -> tuple[GoalExpansion, ...]:
    """Propose only backed-up group specializations and R2I Hopf chains.

    Do not duplicate the group root's independent existing proof search.
    In subgoals of another proof, the specialized group schema remains a
    separate inference obligation; it is never inserted as a GIVEN.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    sources = tuple(value for value in available if isinstance(value, Relation))
    if isinstance(goal, Relation):
        if proof_target is None or goal == proof_target:
            return ()
        proposals = []
        for source in sources:
            if _eligible_group_instance(source, goal):
                proposals.append(GoalExpansion(
                    cyclic_group_from_cited_general_rule(goal, source),
                    (source,),
                ))
        return tuple(proposals)
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaHopfInvariantMap):
        return ()
    proposals = []
    for chain in eligible_eta_hopf_chains(available):
        for source in sources:
            target = goal.map.target_group
            if not isinstance(target, TodaPrimaryGroup):
                continue
            n = target.sphere_dimension
            if type(n) is not int:
                continue
            group = specialize_registered_higher_stem(source, n)
            if group is None or not _valid_surjective_pair(goal, group, chain.conclusion):
                continue
            candidate = GoalExpansion(
                cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion),
                (group, chain.conclusion),
            )
            if not any(x.subgoals == candidate.subgoals for x in proposals):
                proposals.append(candidate)
    return tuple(proposals)
