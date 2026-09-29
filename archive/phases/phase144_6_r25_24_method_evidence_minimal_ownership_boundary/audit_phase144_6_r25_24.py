from phase144_6_r25_24_method_evidence_minimal_ownership_boundary.test_phase144_6_r25_24 import (
  TARGETS,
  _complete_data,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)


def main():
  print(
    "Phase 144-6 R25-24 method evidence minimal ownership audit"
  )
  print(
    "legacy -> minimal exactness evidence counts"
  )
  print()

  for n, k in TARGETS:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _complete_data(
      n,
      k,
    )

    print(
      "=" * 72
    )
    print(
      f"pi_{n + k}^{n}: arguments={len(arguments)}"
    )

    for argument_index, argument in enumerate(
      arguments
    ):
      legacy = (
        extract_toda_group_proof_narrative_argument_method_evidence(
          presentation,
          blocks,
          sidecar,
          arguments,
          argument_index,
        )
      )
      minimal = (
        extract_toda_group_proof_narrative_argument_method_evidence(
          presentation,
          blocks,
          sidecar,
          arguments,
          argument_index,
          minimal_ownership=True,
        )
      )

      if (
        legacy
        or minimal
        or argument.role
        in (
          TodaGroupProofNarrativeArgumentRole
          .ESTABLISH_ORDER,
          TodaGroupProofNarrativeArgumentRole
          .ESTABLISH_GROUP_STRUCTURE,
        )
      ):
        print(
          f"  {argument_index:03d} "
          f"{argument.role.value}: "
          f"{len(legacy)} -> {len(minimal)}"
        )

    print()


if __name__ == "__main__":
  main()
