from dataclasses import dataclass

from expression import GeneratorSymbol
from proof_repository import ProofRepository
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
  find_repository_proof_scope_applicability_candidates,
)
from repository_proof_scope_facade import (
  RepositoryProofScopeExplorationResult,
  explore_repository_generator_proof_scope,
  explore_standard_repository_generator_proof_scope_input,
)
from rule_catalog import (
  InferenceRuleCatalog,
)
from standard_production_applicability_catalog import (
  build_standard_production_applicability_catalog,
)


@dataclass(frozen=True)
class RepositoryGeneratorApplicabilityExplorationResult:
  proof_scope_exploration: RepositoryProofScopeExplorationResult
  candidates: tuple[
    RepositoryProofScopeApplicabilityCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.proof_scope_exploration,
      RepositoryProofScopeExplorationResult,
    ):
      raise TypeError(
        "proof_scope_exploration must be a "
        "RepositoryProofScopeExplorationResult"
      )

    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    occurrence_node_ids = {
      id(
        occurrence.scope_node
      )
      for occurrence
      in self.proof_scope_exploration.occurrences
    }

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

      if id(
        candidate.scope_node
      ) not in occurrence_node_ids:
        raise ValueError(
          "candidate scope_node must contain "
          "the explored generator"
        )

  @property
  def generator(
    self,
  ) -> GeneratorSymbol:
    return (
      self.proof_scope_exploration
      .generator
    )

  @property
  def scope(
    self,
  ):
    return (
      self.proof_scope_exploration
      .scope
    )


def _build_generator_applicability_result(
  proof_scope_exploration,
  catalog,
):
  if not isinstance(
    proof_scope_exploration,
    RepositoryProofScopeExplorationResult,
  ):
    raise TypeError(
      "proof_scope_exploration must be a "
      "RepositoryProofScopeExplorationResult"
    )

  if not isinstance(
    catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "catalog must be an "
      "InferenceRuleCatalog"
    )

  all_candidates = (
    find_repository_proof_scope_applicability_candidates(
      proof_scope_exploration.scope,
      catalog,
    )
  )

  occurrence_node_ids = {
    id(
      occurrence.scope_node
    )
    for occurrence
    in proof_scope_exploration.occurrences
  }

  candidates = tuple(
    candidate
    for candidate in all_candidates
    if id(
      candidate.scope_node
    ) in occurrence_node_ids
  )

  return (
    RepositoryGeneratorApplicabilityExplorationResult(
      proof_scope_exploration=(
        proof_scope_exploration
      ),
      candidates=candidates,
    )
  )


def explore_repository_generator_applicability(
  repository,
  generator,
  catalog,
):
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  if not isinstance(
    catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "catalog must be an "
      "InferenceRuleCatalog"
    )

  proof_scope_exploration = (
    explore_repository_generator_proof_scope(
      repository,
      generator,
    )
  )

  return _build_generator_applicability_result(
    proof_scope_exploration,
    catalog,
  )


def explore_standard_repository_generator_applicability_input(
  generator_input,
  catalog=None,
):
  if not isinstance(
    generator_input,
    str,
  ):
    raise TypeError(
      "generator_input must be a str"
    )

  if catalog is None:
    catalog = (
      build_standard_production_applicability_catalog()
    )
  elif not isinstance(
    catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "catalog must be an "
      "InferenceRuleCatalog or None"
    )

  proof_scope_exploration = (
    explore_standard_repository_generator_proof_scope_input(
      generator_input
    )
  )

  return _build_generator_applicability_result(
    proof_scope_exploration,
    catalog,
  )
