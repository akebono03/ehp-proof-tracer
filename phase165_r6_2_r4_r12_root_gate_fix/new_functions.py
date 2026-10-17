def _is_symbolic_cited_root_specialization(root_goal: object, expansion: GoalExpansion) -> bool:
    """Accept an exact symbolic instance; proof search must still verify its cited GIVEN leaf.

    This shape check does not itself certify provenance or waive reference screening.
    Concrete self-citation and nonmatching instantiations remain rejected.
    """
    if getattr(expansion.rule, "name", None) not in (
        "Toda Proposition 5.1 generic higher-eta specialization",
        "generic cited typed scalar specialization",
    ):
        return False
    if len(expansion.subgoals) != 1:
        return False
    premise = expansion.subgoals[0]
    if not (isinstance(premise, Relation)
            and premise.relation_type is RelationType.EQUALITY
            and isinstance(premise.lhs, TodaPrimaryGroup)
            and premise != root_goal):
        return False
    from phase165_r57_r20_general_specialization import specialize_typed_statement
    return specialize_typed_statement(premise, root_goal) is not None


def is_unordered_root_structure_specialization(
    root_goal: object, current_goal: object, expansion: GoalExpansion,
) -> bool:
    """Reject concrete self-structure cycles, permitting exact symbolic instances.

    Only a real, separately linked fixed Reference proof leaf can discharge the
    symbolic premise; the gate never manufactures a proof or citation itself.
    """
    structures = (FiniteCyclicGroup, FreeCyclicGroup, DirectSumGroup)
    if not isinstance(expansion, GoalExpansion):
        raise TypeError("expansion must be GoalExpansion")
    if not (
        isinstance(root_goal, Relation)
        and root_goal.relation_type is RelationType.EQUALITY
        and isinstance(root_goal.lhs, TodaPrimaryGroup)
        and isinstance(root_goal.rhs, structures)
        and isinstance(current_goal, Relation)
        and current_goal == root_goal
    ):
        return False
    if _proved_generator_substitution_shape(root_goal, expansion):
        return False
    if _is_symbolic_cited_root_specialization(root_goal, expansion):
        return False
    if (getattr(expansion.rule, "name", None) == "generic cited typed scalar specialization"
            and len(expansion.subgoals) == 1
            and root_goal.lhs.group_dimension == root_goal.lhs.sphere_dimension
            and isinstance(expansion.subgoals[0], Relation)):
        premise = expansion.subgoals[0]
        if (isinstance(premise.lhs, TodaPrimaryGroup)
                and premise.lhs.group_dimension == premise.lhs.sphere_dimension
                and isinstance(premise.rhs, FreeCyclicGroup)):
            return False
    for premise in expansion.subgoals:
        if not (
            isinstance(premise, Relation)
            and premise.relation_type is RelationType.EQUALITY
            and isinstance(premise.lhs, TodaPrimaryGroup)
            and isinstance(premise.rhs, structures)
        ):
            continue
        source_group = premise.lhs
        if source_group == root_goal.lhs:
            return True
        if not isinstance(source_group.sphere_dimension, int):
            return True
    return False
