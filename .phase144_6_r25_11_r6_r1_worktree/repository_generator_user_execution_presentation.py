from dataclasses import dataclass

from proof import (
  ProofStep,
)
from repository_generator_user_execution_proof_step import (
  RepositoryGeneratorExecutedProofStepResult,
)


@dataclass(frozen=True)
class RepositoryGeneratorUserExecutionPresentation:
  source_result: RepositoryGeneratorExecutedProofStepResult
  conclusion: object
  premises: tuple[
    ProofStep,
    ...,
  ]
  rule_name: str

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      RepositoryGeneratorExecutedProofStepResult,
    ):
      raise TypeError(
        "source_result must be a "
        "RepositoryGeneratorExecutedProofStepResult"
      )

    proof_step = (
      self.source_result.proof_step
    )

    if (
      self.conclusion
      is not proof_step.conclusion
    ):
      raise ValueError(
        "conclusion must preserve proof_step conclusion identity"
      )

    if (
      self.premises
      != proof_step.premises
    ):
      raise ValueError(
        "premises must match proof_step premises"
      )

    if not isinstance(
      self.premises,
      tuple,
    ):
      raise TypeError(
        "premises must be a tuple"
      )

    if any(
      not isinstance(
        premise,
        ProofStep,
      )
      for premise in self.premises
    ):
      raise TypeError(
        "premises must contain only ProofStep objects"
      )

    if not isinstance(
      self.rule_name,
      str,
    ):
      raise TypeError(
        "rule_name must be a str"
      )

    if not self.rule_name:
      raise ValueError(
        "rule_name must not be empty"
      )

    expected_rule_name = (
      proof_step.inference_rule.name
      if proof_step.inference_rule is not None
      else proof_step.rule.value
    )

    if self.rule_name != expected_rule_name:
      raise ValueError(
        "rule_name must match proof_step rule"
      )

  @property
  def proof_step(
    self,
  ) -> ProofStep:
    return self.source_result.proof_step


def build_repository_generator_user_execution_presentation(
  result,
) -> RepositoryGeneratorUserExecutionPresentation:
  if not isinstance(
    result,
    RepositoryGeneratorExecutedProofStepResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryGeneratorExecutedProofStepResult"
    )

  proof_step = (
    result.proof_step
  )

  rule_name = (
    proof_step.inference_rule.name
    if proof_step.inference_rule is not None
    else proof_step.rule.value
  )

  return RepositoryGeneratorUserExecutionPresentation(
    source_result=result,
    conclusion=proof_step.conclusion,
    premises=proof_step.premises,
    rule_name=rule_name,
  )
