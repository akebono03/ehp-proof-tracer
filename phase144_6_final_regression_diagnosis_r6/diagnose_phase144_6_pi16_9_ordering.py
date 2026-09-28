from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from test_phase143_12_purpose_subject import _arguments


def compact_argument(argument, source):
  source_index = next(
    (
      index
      for index, candidate in enumerate(source)
      if candidate is argument
    ),
    None,
  )
  conclusion_source_index = next(
    (
      index
      for index, candidate in enumerate(source)
      if candidate.conclusion_block is argument.conclusion_block
    ),
    None,
  )
  return {
    "source_index_by_argument_identity": source_index,
    "source_index_by_conclusion_identity": conclusion_source_index,
    "role": argument.role.value,
    "conclusion_role": argument.conclusion_block.role.value,
    "children": argument.child_argument_indices,
  }


def main():
  source = _arguments(9, 7)
  ordered = order_toda_group_proof_narrative_arguments(source)

  print("pi_16^9 compact argument-ordering diagnosis")
  print("=" * 72)
  print(f"source_count={len(source)}")
  print(f"ordered_count={len(ordered)}")

  print("\nSOURCE")
  for index, argument in enumerate(source):
    info = compact_argument(argument, source)
    print(
      f"{index}: role={info['role']} "
      f"conclusion={info['conclusion_role']} "
      f"children={info['children']}"
    )

  print("\nORDERED")
  ordered_argument_indices = []
  ordered_conclusion_indices = []
  for position, argument in enumerate(ordered):
    info = compact_argument(argument, source)
    ordered_argument_indices.append(
      info["source_index_by_argument_identity"]
    )
    ordered_conclusion_indices.append(
      info["source_index_by_conclusion_identity"]
    )
    print(
      f"{position}: "
      f"arg_source={info['source_index_by_argument_identity']} "
      f"conclusion_source={info['source_index_by_conclusion_identity']} "
      f"role={info['role']} "
      f"conclusion={info['conclusion_role']} "
      f"children={info['children']}"
    )

  print("\nSUMMARY")
  print(
    "ordered_argument_identity_indices="
    f"{tuple(ordered_argument_indices)}"
  )
  print(
    "ordered_conclusion_identity_indices="
    f"{tuple(ordered_conclusion_indices)}"
  )
  print("expected=(1, 0)")

  if tuple(ordered_conclusion_indices) == (1, 0):
    print("RESULT=ORDERING_CONTRACT_MATCH")
  else:
    print("RESULT=ORDERING_CONTRACT_MISMATCH")


if __name__ == "__main__":
  main()
