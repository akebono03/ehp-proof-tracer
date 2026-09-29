from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_relevance import (
  is_toda_group_proof_narrative_exactness_component_directly_relevant,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
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


TARGETS = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _component_index(
  components,
  component,
):
  if component is None:
    return None

  for index, candidate in enumerate(components):
    if candidate == component:
      return index

  return None


def _block_index_by_identity(
  blocks,
):
  return {
    id(block): index
    for index, block in enumerate(blocks)
  }


def _classify_component(
  relevant_groups,
  component,
  primary_component,
):
  if (
    primary_component is not None
    and component == primary_component
  ):
    return "PRIMARY_METHOD"

  if (
    is_toda_group_proof_narrative_exactness_component_directly_relevant(
      relevant_groups,
      component,
    )
  ):
    return "DIRECT_SUPPORT_CANDIDATE"

  return "RECURSIVE_PROVENANCE_CANDIDATE"


def _audit_argument(
  presentation,
  blocks,
  sidecar,
  arguments,
  argument_index,
):
  argument = arguments[argument_index]
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
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  block_indices = _block_index_by_identity(blocks)

  print(
    "  "
    f"argument[{argument_index}] "
    f"role={argument.role.value} "
    f"relevant_groups={len(relevant_groups)} "
    f"evidence_blocks={len(evidence)} "
    f"components={len(components)} "
    f"primary={_component_index(components, primary_component)}"
  )

  if not evidence:
    print("    exactness evidence: none")
    return

  for component_index, component in enumerate(components):
    classification = _classify_component(
      relevant_groups,
      component,
      primary_component,
    )
    print(
      "    "
      f"component[{component_index}] "
      f"class={classification} "
      f"windows={len(component.windows)} "
      f"blocks={len(component.evidence_blocks)}"
    )

    for block in component.evidence_blocks:
      contributions = (
        extract_toda_group_proof_narrative_exactness_display_contributions(
          presentation,
          block,
        )
      )
      visible = (
        filter_toda_group_proof_narrative_exactness_body_contributions(
          block,
          contributions,
          primary_component,
        )
      )

      print(
        "      "
        f"block[{block_indices[id(block)]}] "
        f"contributions={len(contributions)} "
        f"currently_visible={len(visible)}"
      )

      for contribution in contributions:
        current_state = (
          "VISIBLE"
          if contribution in visible
          else "SUPPRESSED"
        )
        print(
          "        "
          f"{current_state} "
          f"{contribution.kind.value}: "
          f"${contribution.latex}$"
        )


def _audit_target(
  label,
  n,
  k,
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

  for argument_index in range(len(arguments)):
    _audit_argument(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )


def _assert_rc2_1_boundary():
  source_path = (
    "toda_group_proof_narrative_exactness_contribution_ownership.py"
  )
  source = open(
    source_path,
    encoding="utf-8",
  ).read()

  assert (
    "if primary_component is None:"
    in source
  )
  assert (
    "if not is_primary_evidence_block:"
    in source
  )
  assert (
    "return contributions"
    in source
  )

  print("RC2-1 boundary preflight: PASS")
  print(
    "  current non-primary evidence preservation "
    "is observed, not modified"
  )


def main():
  print("=" * 78)
  print("Phase 148 RC2-1 Recursive Exactness Evidence Exposure Audit")
  print("Production changes: none")
  print("Existing test changes: none")
  print("=" * 78)

  _assert_rc2_1_boundary()

  for target in TARGETS:
    _audit_target(*target)

  print()
  print("=" * 78)
  print("RC2-1 AUDIT COMPLETE")
  print(
    "Classification labels are diagnostic only; "
    "they are not production exposure policy."
  )
  print(
    "RC2-2 will design the general exposure rule. "
    "RC3 ordering is intentionally untouched."
  )
  print("=" * 78)


if __name__ == "__main__":
  main()
