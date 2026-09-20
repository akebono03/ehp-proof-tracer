from dataclasses import dataclass

from proof import (
  ProofStep,
)
from proof_repository import (
  ProofRepositoryEntry,
)
from repository_generator_qualified_execution_family import (
  RepositoryGeneratorQualifiedExecutionFamilyGroup,
  RepositoryGeneratorQualifiedExecutionFamilyGrouping,
)


@dataclass(frozen=True)
class RepositoryGeneratorQualifiedExecutionFamilySelection:
  grouping: RepositoryGeneratorQualifiedExecutionFamilyGrouping
  groups: tuple[
    RepositoryGeneratorQualifiedExecutionFamilyGroup,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.grouping,
      RepositoryGeneratorQualifiedExecutionFamilyGrouping,
    ):
      raise TypeError(
        "grouping must be a "
        "RepositoryGeneratorQualifiedExecutionFamilyGrouping"
      )

    if not isinstance(
      self.groups,
      tuple,
    ):
      raise TypeError(
        "groups must be a tuple"
      )

    if len(
      self.groups
    ) > 1:
      raise ValueError(
        "root/source selection must identify at most one group"
      )

    source_positions = {
      id(
        group
      ): index
      for index, group
      in enumerate(
        self.grouping.groups
      )
    }

    selected_positions = []
    selected_group_ids = set()

    for group in self.groups:
      if not isinstance(
        group,
        RepositoryGeneratorQualifiedExecutionFamilyGroup,
      ):
        raise TypeError(
          "groups must contain only "
          "RepositoryGeneratorQualifiedExecutionFamilyGroup objects"
        )

      group_id = id(
        group
      )

      if group_id not in source_positions:
        raise ValueError(
          "each group must be an original group "
          "from grouping"
        )

      if group_id in selected_group_ids:
        raise ValueError(
          "groups must not repeat group identity"
        )

      selected_group_ids.add(
        group_id
      )
      selected_positions.append(
        source_positions[
          group_id
        ]
      )

    if selected_positions != sorted(
      selected_positions
    ):
      raise ValueError(
        "groups must preserve grouping order"
      )

  @property
  def selected_group(
    self,
  ) -> RepositoryGeneratorQualifiedExecutionFamilyGroup | None:
    if not self.groups:
      return None

    return self.groups[
      0
    ]

  @property
  def representative(
    self,
  ):
    selected_group = (
      self.selected_group
    )

    if selected_group is None:
      return None

    return selected_group.representative


def select_qualified_repository_generator_execution_family_by_root_and_source(
  grouping,
  root_entry,
  source_step,
) -> RepositoryGeneratorQualifiedExecutionFamilySelection:
  if not isinstance(
    grouping,
    RepositoryGeneratorQualifiedExecutionFamilyGrouping,
  ):
    raise TypeError(
      "grouping must be a "
      "RepositoryGeneratorQualifiedExecutionFamilyGrouping"
    )

  if not isinstance(
    root_entry,
    ProofRepositoryEntry,
  ):
    raise TypeError(
      "root_entry must be a ProofRepositoryEntry"
    )

  if not isinstance(
    source_step,
    ProofStep,
  ):
    raise TypeError(
      "source_step must be a ProofStep"
    )

  original_root_ids = {
    id(
      group.root_entry
    )
    for group
    in grouping.groups
  }

  if id(
    root_entry
  ) not in original_root_ids:
    raise ValueError(
      "root_entry must be an original root entry "
      "from grouping"
    )

  original_source_ids = {
    id(
      group.source_step
    )
    for group
    in grouping.groups
  }

  if id(
    source_step
  ) not in original_source_ids:
    raise ValueError(
      "source_step must be an original source step "
      "from grouping"
    )

  groups = tuple(
    group
    for group
    in grouping.groups
    if (
      group.root_entry
      is root_entry
      and group.source_step
      is source_step
    )
  )

  if len(
    groups
  ) > 1:
    raise ValueError(
      "root/source selection must identify at most one group"
    )

  return RepositoryGeneratorQualifiedExecutionFamilySelection(
    grouping=grouping,
    groups=groups,
  )
