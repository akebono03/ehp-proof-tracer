from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
)
from toda_group_proof_narrative_argument_single_renderer import (
  render_toda_group_proof_narrative_single_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


cases = (
  (
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
    0,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .FIRST,
  ),
  (
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    0,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .MIDDLE,
  ),
  (
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
    0,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .FINAL,
  ),
  (
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    1,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .DETACHED,
  ),
)

for (
  n,
  k,
  role,
  occurrence,
  discourse_role,
) in cases:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  matches = tuple(
    argument_index
    for argument_index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )
  argument_index = matches[
    occurrence
  ]
  argument = arguments[
    argument_index
  ]

  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )
  primary_component = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_single_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
      discourse_role,
      primary_component,
    )
  )

  print("=" * 78)
  print(
    f"n={n}, k={k}, "
    f"role={role.value}, "
    f"primary={primary_component is not None}, "
    f"discourse={discourse_role.value}"
  )
  print(rendered)
