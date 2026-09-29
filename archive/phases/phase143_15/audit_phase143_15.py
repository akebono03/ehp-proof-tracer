import sys
from pathlib import Path

sys.path.insert(
  0,
  str(
    Path.cwd()
    / "tests"
  ),
)

from test_phase143_12_purpose_subject import (
  _arguments,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)


for n, k in (
  (3, 3),
  (5, 3),
  (8, 7),
  (9, 7),
):
  source = _arguments(
    n,
    k,
  )
  ordered = order_toda_group_proof_narrative_arguments(
    source
  )
  source_indices = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      source
    )
  }

  print(
    "=" * 78
  )
  print(
    f"n={n}, k={k}"
  )

  for position, argument in enumerate(
    ordered,
    start=1,
  ):
    source_index = source_indices[
      id(
        argument
      )
    ]
    sentence = (
      render_toda_group_proof_narrative_argument_purpose_sentence(
        argument
      )
    )

    print(
      f"{position:02d}: "
      f"A{source_index + 1:02d} "
      f"{argument.role.value}: "
      f"{sentence}"
    )
