from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_rules import (
  Toda515Sigma8TransportedDecompositionStatement,
)


def _ordered_narrative_summand_keys(
  keys: tuple[
    tuple,
    ...,
  ],
) -> tuple[
  tuple,
  ...,
]:
  return tuple(
    sorted(
      keys,
      key=repr,
    )
  )


def toda_group_structure_narrative_semantic_key(
  group,
) -> tuple:
  if isinstance(
    group,
    FreeCyclicGroup,
  ):
    return (
      "free_cyclic",
      group.generator,
    )

  if isinstance(
    group,
    FiniteCyclicGroup,
  ):
    return (
      "finite_cyclic",
      group.order,
      group.generator,
    )

  if isinstance(
    group,
    DirectSumGroup,
  ):
    summand_keys = tuple(
      toda_group_structure_narrative_semantic_key(
        summand
      )
      for summand in group.summands
    )

    return (
      "direct_sum",
      _ordered_narrative_summand_keys(
        summand_keys
      ),
    )

  raise TypeError(
    "unsupported group structure for "
    "Narrative semantic key"
  )


def _toda_group_structure_narrative_fact(
  statement,
):
  if (
    isinstance(
      statement,
      Relation,
    )
    and statement.relation_type
    is RelationType.EQUALITY
    and isinstance(
      statement.lhs,
      TodaPrimaryGroup,
    )
    and isinstance(
      statement.rhs,
      (
        FreeCyclicGroup,
        FiniteCyclicGroup,
        DirectSumGroup,
      ),
    )
  ):
    return (
      statement.lhs,
      statement.rhs,
    )

  if isinstance(
    statement,
    Toda515Sigma8TransportedDecompositionStatement,
  ):
    return (
      statement
      .prop44_isomorphism
      .map
      .target_group,
      statement.transported_group,
    )

  return None


def extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(
  conclusion_step: ProofStep,
) -> frozenset[
  int
]:
  if not isinstance(
    conclusion_step,
    ProofStep,
  ):
    raise TypeError(
      "conclusion_step must be a ProofStep"
    )

  conclusion_fact = (
    _toda_group_structure_narrative_fact(
      conclusion_step.conclusion
    )
  )

  if conclusion_fact is None:
    return frozenset()

  (
    conclusion_target,
    conclusion_group,
  ) = conclusion_fact

  conclusion_key = (
    toda_group_structure_narrative_semantic_key(
      conclusion_group
    )
  )

  redundant_step_ids = set()

  for premise_step in conclusion_step.premises:
    premise_fact = (
      _toda_group_structure_narrative_fact(
        premise_step.conclusion
      )
    )

    if premise_fact is None:
      continue

    (
      premise_target,
      premise_group,
    ) = premise_fact

    if premise_target != conclusion_target:
      continue

    if (
      toda_group_structure_narrative_semantic_key(
        premise_group
      )
      != conclusion_key
    ):
      continue

    redundant_step_ids.add(
      id(
        premise_step
      )
    )

  return frozenset(
    redundant_step_ids
  )
