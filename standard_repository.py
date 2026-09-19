from proof import ProofStep
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from toda_rules import (
  TodaProp56FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515FiniteDimensionalStatement,
)


def _validate_standard_step(
  step: ProofStep,
  statement_type: type,
  name: str,
) -> None:
  if not isinstance(
    step,
    ProofStep,
  ):
    raise TypeError(
      f"{name} must be a ProofStep"
    )

  if not isinstance(
    step.conclusion,
    statement_type,
  ):
    raise ValueError(
      f"{name} has the wrong conclusion type"
    )


def build_standard_proof_repository(
  prop56_step: ProofStep,
  prop58_step: ProofStep,
  prop511_step: ProofStep,
  prop515_step: ProofStep,
) -> ProofRepository:
  _validate_standard_step(
    prop56_step,
    TodaProp56FiniteDimensionalStatement,
    "prop56_step",
  )
  _validate_standard_step(
    prop58_step,
    TodaProp58FiniteDimensionalStatement,
    "prop58_step",
  )
  _validate_standard_step(
    prop511_step,
    TodaProp511FiniteDimensionalStatement,
    "prop511_step",
  )
  _validate_standard_step(
    prop515_step,
    TodaProp515FiniteDimensionalStatement,
    "prop515_step",
  )

  repository = ProofRepository()

  entries = (
    ProofRepositoryEntry(
      key="standard.toda.prop56",
      step=prop56_step,
      phase="65",
      theorem="Toda Proposition 5.6",
    ),
    ProofRepositoryEntry(
      key="standard.toda.prop58",
      step=prop58_step,
      phase="68",
      theorem="Toda Proposition 5.8",
    ),
    ProofRepositoryEntry(
      key="standard.toda.prop511",
      step=prop511_step,
      phase="73",
      theorem="Toda Proposition 5.11",
    ),
    ProofRepositoryEntry(
      key="standard.toda.prop515",
      step=prop515_step,
      phase="75",
      theorem="Toda Proposition 5.15",
    ),
  )

  for entry in entries:
    repository.register(
      entry
    )

  return repository
