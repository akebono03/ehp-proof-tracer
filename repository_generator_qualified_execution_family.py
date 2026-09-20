from dataclasses import dataclass

from repository_generator_applicability_execution_entry import (
  first_qualified_production_execution_family_name,
)
from repository_generator_qualified_execution_selection import (
  RepositoryGeneratorQualifiedExecutionSelection,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)


def _binding_signature(
  candidate,
):
  return tuple(
    (
      binding.variable,
      binding.value,
    )
    for binding
    in candidate.candidate.bindings
  )


def _family_group_key(
  candidate,
):
  return (
    id(
      candidate.scope_node
    ),
    id(
      candidate.candidate.source_step
    ),
    first_qualified_production_execution_family_name(
      candidate
    ),
    candidate.candidate.premise_index,
    _binding_signature(
      candidate
    ),
  )


@dataclass(frozen=True)
class RepositoryGeneratorQualifiedExecutionFamilyGroup:
  candidates: tuple[
    RepositoryProofScopeApplicabilityCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    if not self.candidates:
      raise ValueError(
        "candidates must not be empty"
      )

    for candidate in self.candidates:
      if not isinstance(
        candidate,
        RepositoryProofScopeApplicabilityCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "RepositoryProofScopeApplicabilityCandidate objects"
        )

    first_key = _family_group_key(
      self.candidates[
        0
      ]
    )

    if any(
      _family_group_key(
        candidate
      )
      != first_key
      for candidate
      in self.candidates[
        1:
      ]
    ):
      raise ValueError(
        "candidates must belong to one qualified "
        "execution family at one source"
      )

    candidate_ids = tuple(
      id(
        candidate
      )
      for candidate
      in self.candidates
    )

    if len(
      set(
        candidate_ids
      )
    ) != len(
      candidate_ids
    ):
      raise ValueError(
        "candidates must not repeat candidate identity"
      )

  @property
  def representative(
    self,
  ) -> RepositoryProofScopeApplicabilityCandidate:
    return self.candidates[
      0
    ]

  @property
  def scope_node(
    self,
  ):
    return self.representative.scope_node

  @property
  def source_step(
    self,
  ):
    return (
      self.representative
      .candidate
      .source_step
    )

  @property
  def root_entry(
    self,
  ):
    return self.representative.root_entry

  @property
  def family_name(
    self,
  ) -> str:
    return (
      first_qualified_production_execution_family_name(
        self.representative
      )
    )


@dataclass(frozen=True)
class RepositoryGeneratorQualifiedExecutionFamilyGrouping:
  selection: RepositoryGeneratorQualifiedExecutionSelection
  groups: tuple[
    RepositoryGeneratorQualifiedExecutionFamilyGroup,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.selection,
      RepositoryGeneratorQualifiedExecutionSelection,
    ):
      raise TypeError(
        "selection must be a "
        "RepositoryGeneratorQualifiedExecutionSelection"
      )

    if not isinstance(
      self.groups,
      tuple,
    ):
      raise TypeError(
        "groups must be a tuple"
      )

    for group in self.groups:
      if not isinstance(
        group,
        RepositoryGeneratorQualifiedExecutionFamilyGroup,
      ):
        raise TypeError(
          "groups must contain only "
          "RepositoryGeneratorQualifiedExecutionFamilyGroup objects"
        )

    flattened = tuple(
      candidate
      for group
      in self.groups
      for candidate
      in group.candidates
    )

    source_candidates = (
      self.selection.candidates
    )

    if len(
      flattened
    ) != len(
      source_candidates
    ):
      raise ValueError(
        "groups must preserve every selected candidate exactly once"
      )

    flattened_ids = {
      id(
        candidate
      )
      for candidate
      in flattened
    }
    source_ids = {
      id(
        candidate
      )
      for candidate
      in source_candidates
    }

    if flattened_ids != source_ids:
      raise ValueError(
        "groups must preserve original selected candidate identities"
      )

  @property
  def representatives(
    self,
  ):
    return tuple(
      group.representative
      for group
      in self.groups
    )


def group_qualified_repository_generator_execution_families(
  selection,
) -> RepositoryGeneratorQualifiedExecutionFamilyGrouping:
  if not isinstance(
    selection,
    RepositoryGeneratorQualifiedExecutionSelection,
  ):
    raise TypeError(
      "selection must be a "
      "RepositoryGeneratorQualifiedExecutionSelection"
    )

  grouped = []
  group_index_by_key = {}

  for candidate in selection.candidates:
    key = _family_group_key(
      candidate
    )

    group_index = (
      group_index_by_key.get(
        key
      )
    )

    if group_index is None:
      group_index_by_key[
        key
      ] = len(
        grouped
      )
      grouped.append(
        [
          candidate,
        ]
      )
      continue

    grouped[
      group_index
    ].append(
      candidate
    )

  groups = tuple(
    RepositoryGeneratorQualifiedExecutionFamilyGroup(
      candidates=tuple(
        candidates
      ),
    )
    for candidates
    in grouped
  )

  return RepositoryGeneratorQualifiedExecutionFamilyGrouping(
    selection=selection,
    groups=groups,
  )
