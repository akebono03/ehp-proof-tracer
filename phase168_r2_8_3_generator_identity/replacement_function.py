def _same_group_structure(goal: Relation, assertion_relation: Relation) -> bool:
    """Compare concrete group presentations without inferring new equalities.

    Prefer exact equality; otherwise use the registered HyoujiGen identities
    only for the supported, fully resolved generator factors.
    """
    if goal == assertion_relation:
        return True
    a = goal.rhs
    b = assertion_relation.rhs
    if type(a) is not type(b):
        return False
    if isinstance(a, FiniteCyclicGroup) and a.order != b.order:
        return False
    if isinstance(a, FiniteCyclicGroup) and a.generator == b.generator:
        return True
    if isinstance(a, FreeCyclicGroup) and a.generator == b.generator:
        return True
    if isinstance(a, DirectSumGroup) and a == b:
        return True
    from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
    return same_registered_group_presentation(a, b)
