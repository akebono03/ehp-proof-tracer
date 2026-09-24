from expression import (
  Expression,
)
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
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def is_completed_group_result_step(
  proof_step: ProofStep,
) -> bool:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  conclusion = proof_step.conclusion

  return (
    isinstance(
      conclusion,
      Relation,
    )
    and conclusion.relation_type
    is RelationType.EQUALITY
    and isinstance(
      conclusion.lhs,
      TodaPrimaryGroup,
    )
    and isinstance(
      conclusion.rhs,
      (
        FreeCyclicGroup,
        FiniteCyclicGroup,
        DirectSumGroup,
      ),
    )
  )


def root_generator(
  presentation: TodaGroupProofPresentation,
) -> Expression | None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  generators = (
    presentation
    .source_replay
    .group_result
    .generators
  )

  if len(
    generators
  ) != 1:
    return None

  return generators[
    0
  ]


def root_target_group(
  presentation: TodaGroupProofPresentation,
) -> TodaPrimaryGroup:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  return (
    presentation
    .source_replay
    .group_result
    .target
  )
