from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def main() -> None:
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    (
      _presentation,
      _blocks,
      _sidecar,
      arguments,
    ) = _method_evidence_data(
      n,
      k,
    )

    print(
      "=" * 78
    )
    print(
      f"n={n}, k={k}"
    )
    print(
      "=" * 78
    )

    for index, argument in enumerate(
      arguments
    ):
      subject = (
        extract_toda_group_proof_narrative_argument_purpose_subject(
          argument
        )
      )
      step = (
        extract_toda_group_proof_narrative_argument_conclusion_step(
          argument
        )
      )

      print(
        f"{index + 1}. "
        f"role={argument.role.value}, "
        f"subject={subject!r}, "
        f"conclusion={None if step is None else step.conclusion!r}"
      )


if __name__ == "__main__":
  main()
