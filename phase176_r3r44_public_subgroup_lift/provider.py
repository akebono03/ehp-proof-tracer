"""Bind the existing subgroup-lift rule to ordinary backward goals.

Concrete presentations (including DB candidates) are only variable bindings.
The rule still requires five independent ProofSteps. Only the codomain
may be a revalidated DB prior under the active proof context.
"""
from __future__ import annotations

from expression import MapApplication, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase165_r12_r2_quotient_rules import CyclicStructureStatement, KernelMultipleStatement
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import expand_finite_cyclic_subgroup_lift
from proof import Relation, RelationType


def build_public_subgroup_lift_provider(available: tuple, prior_conclusions: tuple = (),
                                        *, bridge=None, proof_target=None):
    """Source/prior candidates first, typed DB candidate last; no proof insertion."""
    if not isinstance(available, tuple) or not isinstance(prior_conclusions, tuple):
        raise TypeError("source and prior candidates must be tuples")

    def expand(goal):
        if (type(goal) is not CyclicStructureStatement
                or type(goal.group) is not TodaPrimaryGroup
                or type(goal.order) is not int or goal.order < 2):
            return ()
        a = goal.group
        i, n = a.group_dimension, a.sphere_dimension
        if type(i) is not int or type(n) is not int or n < 3 or i < 2*n-1:
            return ()
        b, c = TodaPrimaryGroup(i, 2*n-1), TodaPrimaryGroup(i-2, n-1)
        exact = EHPImageEqualsKernelStatement(TodaEHPExactnessWindow(a, b, c, EHP_H_MAP, EHP_DELTA_MAP))
        groups = []

        def add(item):
            if (type(item) is Relation and item.relation_type is RelationType.EQUALITY
                    and item.lhs == b and type(item.rhs) is FiniteCyclicGroup
                    and type(item.rhs.order) is int and item.rhs.order > goal.order
                    and item.rhs.order % goal.order == 0 and item not in groups):
                groups.append(item)

        for item in available + prior_conclusions:
            add(item)
            if type(item) is Relation:
                add(specialize_registered_higher_stem(item, b.sphere_dimension))
        # A DB presentation is a candidate for an OPEN codomain goal, never a
        # source leaf or a verified result. It can bind otherwise unknown b,m.
        for item in database_structured_group_goal_candidates(n=b.sphere_dimension,
                                                              k=i-b.sphere_dimension):
            add(item)
        options = []
        for group in groups:
            # Canonical generator of a subgroup of the requested order. The
            # equality H(a)=qb must still be proved; no unit/sign is assumed.
            q = group.rhs.order // goal.order
            generator = group.rhs.generator
            kernel = KernelMultipleStatement(TodaDeltaMap(b,c), b, generator, q)
            image = Relation(MapApplication(EHP_H_MAP, goal.generator), Multiple(q,generator), RelationType.EQUALITY)
            for option in expand_finite_cyclic_subgroup_lift(
                    goal, exact, group, kernel, image, bridge=bridge, proof_target=proof_target):
                if not any(old.subgoals == option.subgoals for old in options):
                    options.append(option)
        return tuple(options)

    return expand
