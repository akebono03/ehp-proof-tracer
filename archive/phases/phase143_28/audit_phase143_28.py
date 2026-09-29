from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_relevance import (
  is_toda_group_proof_narrative_exactness_component_directly_relevant,
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


for n, k in (
  (3, 3),
  (5, 3),
  (8, 7),
  (9, 7),
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  print("=" * 78)
  print(f"n={n}, k={k}")

  for argument_index, argument in enumerate(
    arguments
  ):
    subject = (
      extract_toda_group_proof_narrative_argument_purpose_subject(
        argument
      )
    )
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
    direct_flags = tuple(
      is_toda_group_proof_narrative_exactness_component_directly_relevant(
        relevant_groups,
        component,
      )
      for component in components
    )
    selected = (
      select_toda_group_proof_narrative_primary_exactness_component(
        relevant_groups,
        components,
      )
    )

    selected_index = (
      None
      if selected is None
      else components.index(
        selected
      ) + 1
    )

    print(
      f"A{argument_index + 1:02d} "
      f"{argument.role.value}: "
      f"subject={subject!r}"
    )
    print(
      f"  relevant_groups={relevant_groups!r}"
    )
    print(
      f"  direct_relevance={direct_flags!r}"
    )
    print(
      f"  primary_component={selected_index!r}"
    )
