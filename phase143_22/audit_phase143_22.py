from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
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

    print(
      f"A{argument_index + 1:02d} "
      f"{argument.role.value}: "
      f"evidence={len(evidence)} "
      f"components={len(components)}"
    )

    for component_index, component in enumerate(
      components,
      start=1,
    ):
      print(
        f"  C{component_index:02d}: "
        f"windows={len(component.windows)} "
        f"blocks={len(component.evidence_blocks)}"
      )

      for window in component.windows:
        print(
          "    "
          + repr(window.source_term)
          + " --"
          + repr(window.first_map)
          + "--> "
          + repr(window.middle_term)
          + " --"
          + repr(window.second_map)
          + "--> "
          + repr(window.target_term)
        )
