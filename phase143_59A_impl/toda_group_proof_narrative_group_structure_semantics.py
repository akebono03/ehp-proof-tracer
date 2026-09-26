from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
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
