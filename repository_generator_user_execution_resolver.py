from dataclasses import dataclass

from proof import (
  ProofStep,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_qualified_execution_family import (
  RepositoryGeneratorQualifiedExecutionFamilyGroup,
  RepositoryGeneratorQualifiedExecutionFamilyGrouping,
  group_qualified_repository_generator_execution_families,
)
from repository_generator_qualified_execution_selection import (
  RepositoryGeneratorQualifiedExecutionSelection,
  select_all_qualified_repository_generator_applicability_candidates,
)


@dataclass(frozen=True)
class RepositoryGeneratorExecutableTarget:
  group: RepositoryGeneratorQualifiedExecutionFamilyGroup
  target_step: ProofStep

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.group,
      RepositoryGeneratorQualifiedExecutionFamilyGroup,
    ):
      raise TypeError(
        "group must be a "
        "RepositoryGeneratorQualifiedExecutionFamilyGroup"
      )

    if not isinstance(
      self.target_step,
      ProofStep,
    ):
      raise TypeError(
        "target_step must be a ProofStep"
      )

    candidate = (
      self.group.representative
    )

    premise_index = (
      candidate
      .candidate
      .premise_index
    )

    if (
      self.target_step.inference_rule
      is not candidate.candidate.inference_rule
    ):
      raise ValueError(
        "target_step inference_rule identity must match "
        "the group representative"
      )

    if premise_index >= len(
      self.target_step.premises
    ):
      raise ValueError(
        "target_step must contain the representative "
        "premise index"
      )

    if (
      self.target_step.premises[
        premise_index
      ]
      is not self.group.source_step
    ):
      raise ValueError(
        "target_step must preserve source_step identity "
        "at the representative premise index"
      )

  @property
  def representative(
    self,
  ):
    return self.group.representative

  @property
  def root_entry(
    self,
  ):
    return self.group.root_entry

  @property
  def source_step(
    self,
  ):
    return self.group.source_step

  @property
  def family_name(
    self,
  ) -> str:
    return self.group.family_name

  @property
  def goal(
    self,
  ):
    return self.target_step.conclusion


@dataclass(frozen=True)
class StandardRepositoryGeneratorExecutableTargetResolution:
  applicability_result: RepositoryGeneratorApplicabilityExplorationResult
  qualified_selection: RepositoryGeneratorQualifiedExecutionSelection
  family_grouping: RepositoryGeneratorQualifiedExecutionFamilyGrouping
  targets: tuple[
    RepositoryGeneratorExecutableTarget,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.applicability_result,
      RepositoryGeneratorApplicabilityExplorationResult,
    ):
      raise TypeError(
        "applicability_result must be a "
        "RepositoryGeneratorApplicabilityExplorationResult"
      )

    if not isinstance(
      self.qualified_selection,
      RepositoryGeneratorQualifiedExecutionSelection,
    ):
      raise TypeError(
        "qualified_selection must be a "
        "RepositoryGeneratorQualifiedExecutionSelection"
      )

    if not isinstance(
      self.family_grouping,
      RepositoryGeneratorQualifiedExecutionFamilyGrouping,
    ):
      raise TypeError(
        "family_grouping must be a "
        "RepositoryGeneratorQualifiedExecutionFamilyGrouping"
      )

    if not isinstance(
      self.targets,
      tuple,
    ):
      raise TypeError(
        "targets must be a tuple"
      )

    if (
      self.qualified_selection.applicability_result
      is not self.applicability_result
    ):
      raise ValueError(
        "qualified_selection must preserve applicability_result identity"
      )

    if (
      self.family_grouping.selection
      is not self.qualified_selection
    ):
      raise ValueError(
        "family_grouping must preserve qualified_selection identity"
      )

    group_positions = {
      id(
        group
      ): index
      for index, group
      in enumerate(
        self.family_grouping.groups
      )
    }

    scope_step_ids_by_root_id = {}

    for node in self.applicability_result.scope.nodes:
      root_id = id(
        node.root_entry
      )

      scope_step_ids_by_root_id.setdefault(
        root_id,
        set(),
      ).add(
        id(
          node.proof_step
        )
      )

    target_group_ids = set()
    target_positions = []

    for target in self.targets:
      if not isinstance(
        target,
        RepositoryGeneratorExecutableTarget,
      ):
        raise TypeError(
          "targets must contain only "
          "RepositoryGeneratorExecutableTarget objects"
        )

      group_id = id(
        target.group
      )

      if group_id not in group_positions:
        raise ValueError(
          "each target group must be an original group "
          "from family_grouping"
        )

      if group_id in target_group_ids:
        raise ValueError(
          "targets must not repeat group identity"
        )

      target_group_ids.add(
        group_id
      )
      target_positions.append(
        group_positions[
          group_id
        ]
      )

      root_scope_step_ids = (
        scope_step_ids_by_root_id.get(
          id(
            target.root_entry
          ),
          set(),
        )
      )

      if id(
        target.target_step
      ) not in root_scope_step_ids:
        raise ValueError(
          "target_step must be an original proof step "
          "from the target root scope"
        )

    if target_positions != sorted(
      target_positions
    ):
      raise ValueError(
        "targets must preserve family_grouping order"
      )


def _matching_target_steps(
  applicability_result,
  group,
):
  if not isinstance(
    applicability_result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  if not isinstance(
    group,
    RepositoryGeneratorQualifiedExecutionFamilyGroup,
  ):
    raise TypeError(
      "group must be a "
      "RepositoryGeneratorQualifiedExecutionFamilyGroup"
    )

  candidate = (
    group.representative
  )

  premise_index = (
    candidate
    .candidate
    .premise_index
  )

  return tuple(
    node.proof_step
    for node in applicability_result.scope.nodes
    if (
      node.root_entry
      is group.root_entry
      and node.proof_step.inference_rule
      is candidate.candidate.inference_rule
      and premise_index
      < len(
        node.proof_step.premises
      )
      and node.proof_step.premises[
        premise_index
      ]
      is group.source_step
    )
  )


def resolve_standard_repository_generator_executable_targets_input(
  generator_input,
) -> StandardRepositoryGeneratorExecutableTargetResolution:
  if not isinstance(
    generator_input,
    str,
  ):
    raise TypeError(
      "generator_input must be a str"
    )

  applicability_result = (
    explore_standard_repository_generator_applicability_input(
      generator_input
    )
  )

  qualified_selection = (
    select_all_qualified_repository_generator_applicability_candidates(
      applicability_result
    )
  )

  family_grouping = (
    group_qualified_repository_generator_execution_families(
      qualified_selection
    )
  )

  targets = []

  for group in family_grouping.groups:
    matching_target_steps = (
      _matching_target_steps(
        applicability_result,
        group,
      )
    )

    if len(
      matching_target_steps
    ) != 1:
      continue

    targets.append(
      RepositoryGeneratorExecutableTarget(
        group=group,
        target_step=matching_target_steps[
          0
        ],
      )
    )

  return StandardRepositoryGeneratorExecutableTargetResolution(
    applicability_result=applicability_result,
    qualified_selection=qualified_selection,
    family_grouping=family_grouping,
    targets=tuple(
      targets
    ),
  )
