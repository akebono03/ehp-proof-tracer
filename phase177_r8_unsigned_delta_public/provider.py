"""Source-screened backward candidates for the existing unsigned Prop 2.5 rule."""
from __future__ import annotations

from expression import Composition, IteratedSuspension, MapApplication
from map_facts import EHP_DELTA_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
from phase175_r4r12r10r1_cited_511_public.provider import expand_cited_511
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511
from phase177_r3_unsigned_delta_composition_isolated.rule import expand_unsigned_prop25
from proof import Relation, RelationType


def is_delta_equality(value: object) -> bool:
    return (type(value) is Relation and value.relation_type is RelationType.EQUALITY
            and type(value.lhs) is MapApplication and value.lhs.map == EHP_DELTA_MAP
            and value.source is None and value.note is None)


def expand_public_unsigned_delta(goal: object, available: tuple,
                                 prior_conclusions: tuple = ()) -> tuple[GoalExpansion, ...]:
    """Generate open obligations from screened sources, not generator names."""
    if not isinstance(available, tuple) or not isinstance(prior_conclusions, tuple):
        raise TypeError('source and prior candidates must be tuples')
    if (not is_delta_equality(goal) or type(goal.rhs) is not Composition
            or available.count(CitedTodaProp25()) != 1):
        return ()
    gamma, x, beta = goal.lhs.expression, goal.rhs.left, goal.rhs.right
    bases = []
    for item in available + prior_conclusions:
        if is_delta_equality(item) and item not in bases:
            bases.append(item)
    for item in available:
        if type(item) is CitedToda511 and expand_cited_511(item.statement, available):
            if item.statement not in bases:
                bases.append(item.statement)
    if type(gamma) is Composition:
        shaped = Relation(MapApplication(EHP_DELTA_MAP, gamma.left), x)
        if shaped not in bases and expand_cited_511(shaped, available):
            bases.append(shaped)
    results = []
    for base in bases:
        if base.rhs != x:
            continue
        explicit = Composition(base.lhs.expression, IteratedSuspension(beta, 2))
        identity = None if explicit == gamma else Relation(explicit, gamma)
        for option in expand_unsigned_prop25(goal, base, identity):
            if not any(old.subgoals == option.subgoals for old in results):
                results.append(option)
    return tuple(results)


def build_public_unsigned_delta_provider(bridge, prior_conclusions: tuple = ()):
    """Capture exact fixed-statement source links in this DFS context."""
    available = screened_cited_facts(bridge)
    if not isinstance(prior_conclusions, tuple):
        raise TypeError('prior_conclusions must be a tuple')

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return expand_public_unsigned_delta(goal, available, prior_conclusions)

    return expand
