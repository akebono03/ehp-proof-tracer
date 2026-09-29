from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_exposure import (
  classify_toda_group_proof_narrative_exactness_component_exposure,
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


CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _render_case(
  n,
  k,
):
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      n,
      k,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    rendered,
  )


def _component_contribution_latex(
  presentation,
  component,
):
  values = []

  for block in component.evidence_blocks:
    for contribution in (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    ):
      if contribution.latex not in values:
        values.append(
          contribution.latex
        )

  return tuple(
    values
  )


def main():
  print("=" * 78)
  print("Phase 148 RC2-4 Cross-group Exactness Exposure Audit")
  print("Production changes: none")
  print("Existing repository test changes: none")
  print("=" * 78)

  totals = {
    "arguments": 0,
    "components": 0,
    "owned_primary": 0,
    "unowned_recursive": 0,
    "ambiguous_relevant": 0,
  }

  for label, n, k in CASES:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
      rendered,
    ) = _render_case(
      n,
      k,
    )

    exactness_blocks = tuple(
      block
      for block in blocks
      if (
        block.role
        is TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      )
    )

    print()
    print("=" * 78)
    print(label)
    print(
      f"blocks={len(blocks)} "
      f"exactness_blocks={len(exactness_blocks)} "
      f"arguments={len(arguments)}"
    )
    print("=" * 78)

    totals["arguments"] += len(
      arguments
    )

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
      relevant_groups = (
        extract_toda_group_proof_narrative_argument_relevant_groups(
          presentation,
          blocks,
          argument,
        )
      )

      print(
        f"  argument[{argument_index}] "
        f"role={argument.role.value} "
        f"relevant_groups={len(relevant_groups)} "
        f"evidence_blocks={len(evidence)} "
        f"components={len(components)}"
      )

      for component_index, component in enumerate(
        components
      ):
        exposure = (
          classify_toda_group_proof_narrative_exactness_component_exposure(
            relevant_groups,
            components,
            component,
          )
        )
        totals["components"] += 1
        totals[
          exposure.value
        ] += 1

        latex_values = (
          _component_contribution_latex(
            presentation,
            component,
          )
        )
        visible_values = tuple(
          latex
          for latex in latex_values
          if latex in rendered
        )

        print(
          f"    component[{component_index}] "
          f"exposure={exposure.value} "
          f"blocks={len(component.evidence_blocks)} "
          f"contributions={len(latex_values)} "
          f"visible_in_final={len(visible_values)}"
        )

        for latex in latex_values:
          status = (
            "VISIBLE"
            if latex in rendered
            else "HIDDEN"
          )
          print(
            f"      {status}: {latex}"
          )

      if not components:
        print(
          "    exactness component: none"
        )

    print()
    print("  FINAL NARRATIVE")
    print("  " + "-" * 74)
    for line in rendered.splitlines():
      print(
        "  " + line
      )

  print()
  print("=" * 78)
  print("RC2-4 SUMMARY")
  print(
    "arguments="
    + str(
      totals["arguments"]
    )
  )
  print(
    "components="
    + str(
      totals["components"]
    )
  )
  print(
    "owned_primary="
    + str(
      totals["owned_primary"]
    )
  )
  print(
    "unowned_recursive="
    + str(
      totals["unowned_recursive"]
    )
  )
  print(
    "ambiguous_relevant="
    + str(
      totals["ambiguous_relevant"]
    )
  )
  print("Proof graph / evidence traversal is not modified by this audit.")
  print("RC3 Narrative ordering is intentionally not audited here.")
  print("=" * 78)


if __name__ == "__main__":
  main()
