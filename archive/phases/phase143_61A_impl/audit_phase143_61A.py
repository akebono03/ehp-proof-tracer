from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _audit(
  n,
  k,
):
  (
    _,
    _,
    _,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  argument = next(
    argument
    for argument in arguments
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    )
  )

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )

  print(
    "=" * 78
  )
  print(
    f"n={n}, k={k}"
  )
  print(
    "conclusion:",
    conclusion_step.conclusion,
  )
  print(
    "direct premise count:",
    len(
      conclusion_step.premises
    ),
  )
  print(
    "derivation premise count:",
    len(
      premises
    ),
  )

  for index, premise in enumerate(
    premises,
    start=1,
  ):
    print(
      f"{index}.",
      premise.conclusion,
    )


def main() -> None:
  _audit(
    3,
    3,
  )

  _audit(
    5,
    3,
  )


if __name__ == "__main__":
  main()
