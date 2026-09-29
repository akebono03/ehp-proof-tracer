from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

old = """  child_argument_indices: tuple[
    int,
    ...,
  ]
  conclusion_block: TodaGroupProofNarrativeBlock
"""

new = """  conclusion_block: TodaGroupProofNarrativeBlock
  child_argument_indices: tuple[
    int,
    ...,
  ] = ()
"""

if old not in text:
    raise RuntimeError(
      "Phase143-10 NarrativeArgument field block not found."
    )

path.write_text(
  text.replace(
    old,
    new,
    1,
  ),
  encoding="utf-8",
)
print("Updated:", path)

from pathlib import Path

path = Path("tests/test_phase143_7_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

old = """  assert any(
    block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.ORDER
    for block in target_argument.supporting_blocks
  )
"""

new = """  order_argument_index = next(
    argument_index
    for argument_index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    )
  )

  assert (
    order_argument_index
    in target_argument.child_argument_indices
  )
"""

if old not in text:
    raise RuntimeError(
      "Phase143-7 target argument expectation not found."
    )

path.write_text(
  text.replace(
    old,
    new,
    1,
  ),
  encoding="utf-8",
)
print("Updated:", path)
