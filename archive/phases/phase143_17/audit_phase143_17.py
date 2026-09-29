from toda_group_proof_narrative_argument_discourse import (
  classify_toda_group_proof_narrative_argument_discourse_roles,
  render_toda_group_proof_narrative_argument_discourse_marker,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)

from test_phase143_12_purpose_subject import (
  _arguments,
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
  ordered = (
    order_toda_group_proof_narrative_arguments(
      source
    )
  )
  roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      source
    )
  )

  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      source
    )
  }

  print("=" * 78)
  print(
    f"n={n}, k={k}"
  )

  for argument, role in zip(
    ordered,
    roles,
  ):
    source_index = source_index_by_identity[
      id(
        argument
      )
    ]
    marker = (
      render_toda_group_proof_narrative_argument_discourse_marker(
        role
      )
    )
    purpose = (
      render_toda_group_proof_narrative_argument_purpose_sentence(
        argument
      )
    )

    print(
      f"A{source_index + 1:02d} "
      f"{argument.role.value}: "
      f"discourse={role.value} "
      f"marker={marker!r}"
    )
    print(
      f"  purpose={purpose!r}"
    )
