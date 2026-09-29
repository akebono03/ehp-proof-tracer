from toda_group_proof_narrative_transitions import (
  extract_toda_group_proof_narrative_transitions,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def main():
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    (
      presentation,
      blocks,
      _sidecar,
      arguments,
    ) = _method_evidence_data(
      n,
      k,
    )
    transitions = (
      extract_toda_group_proof_narrative_transitions(
        presentation,
        blocks,
        arguments,
      )
    )

    print("=" * 78)
    print(
      f"n={n}, k={k}, transitions={len(transitions)}"
    )
    print("=" * 78)

    for index, transition in enumerate(
      transitions,
      start=1,
    ):
      print(
        f"{index}. "
        f"role={transition.role.value}, "
        f"sources="
        f"{tuple(block.role.value for block in transition.source_blocks)}, "
        f"target={transition.target_block.role.value}"
      )

    print()


if __name__ == "__main__":
  main()
