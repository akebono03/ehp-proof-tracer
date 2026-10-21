"""R57-R11: fail closed when a root group cites its own structure.

R57-R18 permits *derived* cyclic-generator substitution backed by a separately
proved equality, but never accepts an unproved symbolic structure as a root.
"""
from __future__ import annotations

from expression import Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def _proved_generator_substitution_shape(root_goal: object, expansion: GoalExpansion) -> bool:
    """Only exempt substitution from an explicitly equal intermediate generator."""
    if getattr(expansion.rule, "name", None) != "generic finite cyclic generator substitution from proved equality":
        return False
    if len(expansion.subgoals) != 2:
        return False
    structure, equality = expansion.subgoals
    if not (isinstance(root_goal, Relation)
            and isinstance(root_goal.rhs, FiniteCyclicGroup)
            and isinstance(structure, Relation)
            and isinstance(structure.rhs, FiniteCyclicGroup)
            and isinstance(equality, Relation)
            and structure.relation_type is RelationType.EQUALITY
            and equality.relation_type is RelationType.EQUALITY):
        return False
    return (
        structure.lhs == root_goal.lhs
        and structure.rhs.order == root_goal.rhs.order
        and isinstance(structure.rhs.generator, Suspension)
        and equality.lhs == root_goal.rhs.generator
        and equality.rhs == structure.rhs.generator
    )


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


def _proved_generator_suspension_normalization_shape(root_goal: object, expansion: GoalExpansion) -> bool:
    """Permit a proven eta-name normalization, not unproved group self-citation."""
    from expression import IteratedSuspension
    from homotopy_groups import TodaSuspensionMap
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase165_r12_r28_presentation_connection import _matching_eta_name

    if getattr(expansion.rule, "name", None) != "proved generator suspension normalizes transported cyclic group":
        return False
    if len(expansion.subgoals) != 2:
        return False
    transported, witness = expansion.subgoals
    if not (isinstance(root_goal, Relation)
            and root_goal.relation_type is RelationType.EQUALITY
            and isinstance(root_goal.rhs, FiniteCyclicGroup)
            and isinstance(transported, Relation)
            and transported.relation_type is RelationType.EQUALITY
            and isinstance(transported.rhs, FiniteCyclicGroup)
            and isinstance(witness, GeneratorSuspension)
            and isinstance(witness.map, TodaSuspensionMap)):
        return False
    generator = transported.rhs.generator
    return (
        transported != root_goal
        and transported.lhs == root_goal.lhs == witness.map.target_group
        and transported.rhs.order == root_goal.rhs.order
        and isinstance(generator, IteratedSuspension)
        and generator.exponent == 1
        and _matching_eta_name(generator.expression, witness.source_generator)
        and _matching_eta_name(root_goal.rhs.generator, witness.target_generator)
        and witness.map.source_group != witness.map.target_group
    )



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
    if _proved_generator_suspension_normalization_shape(root_goal, expansion):
        return False
    if getattr(expansion.rule, "name", None) == "cited stable eta-family notation for iterated transport":
        from phase166_r3ac_stable_notation import _stable_eta_renaming_shape
        from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
        if (len(expansion.subgoals) == 2
                and expansion.subgoals[1] == TodaEtaFamilyGeneralDefinition()
                and _stable_eta_renaming_shape(expansion.subgoals[0], root_goal)):
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



def retain_ordered_root_expansions(
    root_goal: object, current_goal: object,
    expansions: tuple[GoalExpansion, ...],
) -> tuple[GoalExpansion, ...]:
    """Retain genuinely derived root steps; reject self-structure specialization."""
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    return tuple(
        option for option in expansions
        if not is_unordered_root_structure_specialization(root_goal, current_goal, option)
    )
