from tests.test_phase75_515_pi15_8_final_group import (
  build_phase75_8e4_data,
)
from toda_group_proof_narrative_group_structure_semantics import (
  toda_group_structure_narrative_semantic_key,
)


def main() -> None:
  data = build_phase75_8e4_data()

  transported_group = (
    data[
      "transported_statement"
    ].transported_group
  )
  final_group = (
    data[
      "final_step"
    ].conclusion
    .rhs
  )

  transported_key = (
    toda_group_structure_narrative_semantic_key(
      transported_group
    )
  )
  final_key = (
    toda_group_structure_narrative_semantic_key(
      final_group
    )
  )

  print(
    "transported_group == final_group:",
    transported_group == final_group,
  )
  print(
    "transported_key == final_key:",
    transported_key == final_key,
  )
  print(
    "transported summand types:",
    tuple(
      type(
        summand
      ).__name__
      for summand in transported_group.summands
    ),
  )
  print(
    "final summand types:",
    tuple(
      type(
        summand
      ).__name__
      for summand in final_group.summands
    ),
  )


if __name__ == "__main__":
  main()
