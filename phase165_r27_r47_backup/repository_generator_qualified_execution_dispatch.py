from dataclasses import dataclass

from repository_generator_applicability_execution_entry import (
  qualified_production_execution_family_name,
)
from repository_generator_applicability_execution_orchestration import (
  FirstQualifiedProductionApplicabilityExecutionResult,
  execute_first_qualified_production_applicability_candidate,
  execute_second_qualified_production_applicability_candidate,
)
from repository_generator_two_premise_execution_integration import (
  TwoPremiseProductionApplicationExecutionResult,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)


_FIRST_FAMILY = (
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
)

_SECOND_FAMILY = (
  "toda_lemma57_pi6_2_eta2_nu_prime_inference_rule"
)


@dataclass(frozen=True)
class QualifiedProductionApplicabilityExecutionDispatchResult:
  candidate: RepositoryProofScopeApplicabilityCandidate
  goal: object
  family_name: str
  execution: (
    FirstQualifiedProductionApplicabilityExecutionResult
    | TwoPremiseProductionApplicationExecutionResult
  )

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.candidate,
      RepositoryProofScopeApplicabilityCandidate,
    ):
      raise TypeError(
        "candidate must be a "
        "RepositoryProofScopeApplicabilityCandidate"
      )

    expected_family_name = (
      qualified_production_execution_family_name(
        self.candidate
      )
    )

    if (
      self.family_name
      != expected_family_name
    ):
      raise ValueError(
        "family_name must match candidate qualified family"
      )

    if (
      self.execution.candidate
      is not self.candidate
    ):
      raise ValueError(
        "execution candidate must preserve candidate identity"
      )

    if (
      self.execution.goal
      != self.goal
    ):
      raise ValueError(
        "execution goal must match dispatch goal"
      )


def execute_qualified_production_applicability_candidate(
  candidate,
  goal,
  max_depth=2,
  retry_policy=None,
) -> QualifiedProductionApplicabilityExecutionDispatchResult:
  if not isinstance(
    candidate,
    RepositoryProofScopeApplicabilityCandidate,
  ):
    raise TypeError(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    )

  family_name = (
    qualified_production_execution_family_name(
      candidate
    )
  )

  if family_name == _FIRST_FAMILY:
    execution = (
      execute_first_qualified_production_applicability_candidate(
        candidate,
        goal,
        max_depth=max_depth,
        retry_policy=retry_policy,
      )
    )
  elif family_name == _SECOND_FAMILY:
    execution = (
      execute_second_qualified_production_applicability_candidate(
        candidate,
        goal,
        max_depth=max_depth,
        retry_policy=retry_policy,
      )
    )
  else:
    raise ValueError(
      "qualified production execution family "
      "has no dispatch strategy"
    )

  return QualifiedProductionApplicabilityExecutionDispatchResult(
    candidate=candidate,
    goal=goal,
    family_name=family_name,
    execution=execution,
  )
