from dataclasses import dataclass

from homotopy_groups import (
  TodaPrimaryGroup,
)
from proof_repository import (
  ProofRepository,
)
from toda_ehp_result import (
  TodaEHPSequenceResult,
)
from toda_group_lookup import (
  find_normalized_toda_group_results,
)
from toda_group_query import (
  TodaGroupQuery,
)
from toda_group_result import (
  TodaGroupResult,
)


@dataclass(frozen=True)
class TodaEHPGroupTermResult:
  term: TodaPrimaryGroup
  group_results: tuple[
    TodaGroupResult,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.term,
      TodaPrimaryGroup,
    ):
      raise TypeError(
        "term must be a TodaPrimaryGroup"
      )

    if not isinstance(
      self.group_results,
      tuple,
    ):
      raise TypeError(
        "group_results must be a tuple"
      )

    for group_result in (
      self.group_results
    ):
      if not isinstance(
        group_result,
        TodaGroupResult,
      ):
        raise TypeError(
          "group_results must contain only "
          "TodaGroupResult objects"
        )

      if (
        group_result.target
        != self.term
      ):
        raise ValueError(
          "each group result target must "
          "match term"
        )


@dataclass(frozen=True)
class TodaEHPGroupEnrichmentResult:
  ehp_result: TodaEHPSequenceResult
  term_results: tuple[
    TodaEHPGroupTermResult,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.ehp_result,
      TodaEHPSequenceResult,
    ):
      raise TypeError(
        "ehp_result must be "
        "a TodaEHPSequenceResult"
      )

    if not isinstance(
      self.term_results,
      tuple,
    ):
      raise TypeError(
        "term_results must be a tuple"
      )

    for term_result in (
      self.term_results
    ):
      if not isinstance(
        term_result,
        TodaEHPGroupTermResult,
      ):
        raise TypeError(
          "term_results must contain only "
          "TodaEHPGroupTermResult objects"
        )

    expected_terms = (
      self.ehp_result.sequence.terms
    )

    actual_terms = tuple(
      term_result.term
      for term_result in (
        self.term_results
      )
    )

    if (
      actual_terms
      != expected_terms
    ):
      raise ValueError(
        "term_results must match "
        "ehp_result.sequence.terms "
        "in order"
      )


def _toda_group_query_for_term(
  term: TodaPrimaryGroup,
) -> TodaGroupQuery:
  if not isinstance(
    term,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "term must be a TodaPrimaryGroup"
    )

  n = term.sphere_dimension
  group_dimension = (
    term.group_dimension
  )

  if (
    isinstance(
      n,
      bool,
    )
    or not isinstance(
      n,
      int,
    )
    or isinstance(
      group_dimension,
      bool,
    )
    or not isinstance(
      group_dimension,
      int,
    )
  ):
    raise TypeError(
      "EHP term dimensions must be ints"
    )

  return TodaGroupQuery(
    n=n,
    k=(
      group_dimension
      - n
    ),
  )


def connect_known_toda_group_results(
  repository: ProofRepository,
  ehp_result: TodaEHPSequenceResult,
) -> TodaEHPGroupEnrichmentResult:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    ehp_result,
    TodaEHPSequenceResult,
  ):
    raise TypeError(
      "ehp_result must be "
      "a TodaEHPSequenceResult"
    )

  term_results = tuple(
    TodaEHPGroupTermResult(
      term=term,
      group_results=(
        find_normalized_toda_group_results(
          repository,
          _toda_group_query_for_term(
            term
          ),
        )
      ),
    )
    for term in (
      ehp_result.sequence.terms
    )
  )

  return TodaEHPGroupEnrichmentResult(
    ehp_result=ehp_result,
    term_results=term_results,
  )
