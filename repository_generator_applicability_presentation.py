from dataclasses import dataclass

from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class ApplicabilityRuleGroupPresentation:
  catalog_entry: InferenceRuleCatalogEntry
  candidates: tuple[
    RepositoryProofScopeApplicabilityCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.catalog_entry,
      InferenceRuleCatalogEntry,
    ):
      raise TypeError(
        "catalog_entry must be an "
        "InferenceRuleCatalogEntry"
      )

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
          "RepositoryProofScopeApplicabilityCandidate "
          "objects"
        )

      if (
        candidate
        .candidate
        .catalog_entry
        is not self.catalog_entry
      ):
        raise ValueError(
          "candidate catalog_entry identity must "
          "match group catalog_entry"
        )

  @property
  def inference_rule(
    self,
  ):
    return self.catalog_entry.rule

  @property
  def fixed_point_safe(
    self,
  ) -> bool:
    return self.catalog_entry.fixed_point_safe

  @property
  def premise_indexes(
    self,
  ) -> tuple[
    int,
    ...,
  ]:
    return tuple(
      candidate
      .candidate
      .premise_index
      for candidate in self.candidates
    )


@dataclass(frozen=True)
class ApplicabilitySourceGroupPresentation:
  scope_node: RepositoryProofScopeNode
  rule_groups: tuple[
    ApplicabilityRuleGroupPresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.scope_node,
      RepositoryProofScopeNode,
    ):
      raise TypeError(
        "scope_node must be a "
        "RepositoryProofScopeNode"
      )

    if not isinstance(
      self.rule_groups,
      tuple,
    ):
      raise TypeError(
        "rule_groups must be a tuple"
      )

    if not self.rule_groups:
      raise ValueError(
        "rule_groups must not be empty"
      )

    seen_entry_ids = set()

    for rule_group in self.rule_groups:
      if not isinstance(
        rule_group,
        ApplicabilityRuleGroupPresentation,
      ):
        raise TypeError(
          "rule_groups must contain only "
          "ApplicabilityRuleGroupPresentation "
          "objects"
        )

      entry_id = id(
        rule_group.catalog_entry
      )

      if entry_id in seen_entry_ids:
        raise ValueError(
          "rule_groups must not repeat the same "
          "catalog_entry identity"
        )

      seen_entry_ids.add(
        entry_id
      )

      for candidate in (
        rule_group.candidates
      ):
        if (
          candidate.scope_node
          is not self.scope_node
        ):
          raise ValueError(
            "all grouped candidates must use "
            "the source scope_node"
          )

  @property
  def candidates(
    self,
  ) -> tuple[
    RepositoryProofScopeApplicabilityCandidate,
    ...,
  ]:
    return tuple(
      candidate
      for rule_group in self.rule_groups
      for candidate in rule_group.candidates
    )

  @property
  def source_statement(
    self,
  ):
    return self.scope_node.proof_step.conclusion


@dataclass(frozen=True)
class RepositoryGeneratorApplicabilityPresentation:
  source_result: RepositoryGeneratorApplicabilityExplorationResult
  source_groups: tuple[
    ApplicabilitySourceGroupPresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      RepositoryGeneratorApplicabilityExplorationResult,
    ):
      raise TypeError(
        "source_result must be a "
        "RepositoryGeneratorApplicabilityExplorationResult"
      )

    if not isinstance(
      self.source_groups,
      tuple,
    ):
      raise TypeError(
        "source_groups must be a tuple"
      )

    for source_group in self.source_groups:
      if not isinstance(
        source_group,
        ApplicabilitySourceGroupPresentation,
      ):
        raise TypeError(
          "source_groups must contain only "
          "ApplicabilitySourceGroupPresentation "
          "objects"
        )

    grouped_candidates = tuple(
      candidate
      for source_group in self.source_groups
      for candidate in source_group.candidates
    )

    source_candidates = (
      self.source_result.candidates
    )

    if (
      len(
        grouped_candidates
      )
      != len(
        source_candidates
      )
    ):
      raise ValueError(
        "grouped candidates must preserve every "
        "source_result candidate"
      )

    grouped_candidate_ids = sorted(
      id(
        candidate
      )
      for candidate in grouped_candidates
    )

    source_candidate_ids = sorted(
      id(
        candidate
      )
      for candidate in source_candidates
    )

    if (
      grouped_candidate_ids
      != source_candidate_ids
    ):
      raise ValueError(
        "grouped candidates must preserve source "
        "candidate identity exactly once"
      )

  def _source_groups_for_node_ids(
    self,
    node_ids,
  ):
    return tuple(
      source_group
      for source_group in self.source_groups
      if id(
        source_group.scope_node
      ) in node_ids
    )

  @property
  def toda_membership_source_groups(
    self,
  ) -> tuple[
    ApplicabilitySourceGroupPresentation,
    ...,
  ]:
    node_ids = {
      id(
        membership
        .source_occurrence
        .scope_node
      )
      for membership in (
        self.source_result
        .proof_scope_exploration
        .toda_memberships
      )
    }

    return self._source_groups_for_node_ids(
      node_ids
    )

  @property
  def map_relation_source_groups(
    self,
  ) -> tuple[
    ApplicabilitySourceGroupPresentation,
    ...,
  ]:
    toda_node_ids = {
      id(
        source_group.scope_node
      )
      for source_group in (
        self.toda_membership_source_groups
      )
    }

    map_node_ids = {
      id(
        map_relation
        .source_occurrence
        .scope_node
      )
      for map_relation in (
        self.source_result
        .proof_scope_exploration
        .map_relations
      )
    }

    return tuple(
      source_group
      for source_group in self.source_groups
      if (
        id(
          source_group.scope_node
        ) in map_node_ids
        and id(
          source_group.scope_node
        ) not in toda_node_ids
      )
    )

  @property
  def other_source_groups(
    self,
  ) -> tuple[
    ApplicabilitySourceGroupPresentation,
    ...,
  ]:
    grouped_ids = {
      id(
        source_group
        .scope_node
      )
      for source_group in (
        self.toda_membership_source_groups
        + self.map_relation_source_groups
      )
    }

    return tuple(
      source_group
      for source_group in self.source_groups
      if id(
        source_group.scope_node
      ) not in grouped_ids
    )

  @property
  def rule_group_count(
    self,
  ) -> int:
    return sum(
      len(
        source_group.rule_groups
      )
      for source_group in self.source_groups
    )


def build_repository_generator_applicability_presentation(
  result,
):
  if not isinstance(
    result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  source_records = []
  source_record_by_node_id = {}

  for candidate in result.candidates:
    node_id = id(
      candidate.scope_node
    )

    record = (
      source_record_by_node_id.get(
        node_id
      )
    )

    if record is None:
      record = {
        "scope_node": candidate.scope_node,
        "candidates": [],
      }

      source_record_by_node_id[
        node_id
      ] = record

      source_records.append(
        record
      )

    record[
      "candidates"
    ].append(
      candidate
    )

  source_groups = []

  for source_record in source_records:
    rule_records = []
    rule_record_by_entry_id = {}

    for candidate in source_record[
      "candidates"
    ]:
      catalog_entry = (
        candidate
        .candidate
        .catalog_entry
      )

      entry_id = id(
        catalog_entry
      )

      rule_record = (
        rule_record_by_entry_id.get(
          entry_id
        )
      )

      if rule_record is None:
        rule_record = {
          "catalog_entry": catalog_entry,
          "candidates": [],
        }

        rule_record_by_entry_id[
          entry_id
        ] = rule_record

        rule_records.append(
          rule_record
        )

      rule_record[
        "candidates"
      ].append(
        candidate
      )

    rule_groups = tuple(
      ApplicabilityRuleGroupPresentation(
        catalog_entry=(
          rule_record[
            "catalog_entry"
          ]
        ),
        candidates=tuple(
          rule_record[
            "candidates"
          ]
        ),
      )
      for rule_record in rule_records
    )

    source_groups.append(
      ApplicabilitySourceGroupPresentation(
        scope_node=(
          source_record[
            "scope_node"
          ]
        ),
        rule_groups=rule_groups,
      )
    )

  return (
    RepositoryGeneratorApplicabilityPresentation(
      source_result=result,
      source_groups=tuple(
        source_groups
      ),
    )
  )
