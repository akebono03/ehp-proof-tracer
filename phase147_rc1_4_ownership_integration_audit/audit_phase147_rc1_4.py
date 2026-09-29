from pathlib import Path

from toda_group_proof_narrative_argument_discourse import (
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_header_method_section,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
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


TARGETS = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _legacy_primary(
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
  primary = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )
  return relevant_groups, evidence, components, primary


def _audit_renderer_route():
  path = Path(
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  source = path.read_text(encoding="utf-8")

  new_call = (
    "select_toda_group_proof_narrative_"
    "argument_primary_exactness_component("
  )
  old_call = (
    "select_toda_group_proof_narrative_"
    "primary_exactness_component("
  )

  assert new_call in source, (
    "multi renderer does not call the RC1 ownership API"
  )
  assert old_call not in source, (
    "multi renderer still contains the old inline primary selector"
  )
  assert (
    "extract_toda_group_proof_narrative_argument_method_evidence("
    in source
  ), (
    "RC1 must preserve method-evidence extraction used by body handling"
  )

  print("renderer route: PASS")
  print("  ownership API call: present")
  print("  old inline primary selector: absent")
  print("  method evidence extraction: preserved for RC2 boundary")


def _audit_targets():
  print()
  print("six-group ownership audit")
  print("-" * 78)

  for label, n, k in TARGETS:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _method_evidence_data(
      n,
      k,
    )

    ordered = (
      order_toda_group_proof_narrative_arguments(
        arguments
      )
    )
    discourse_roles = (
      classify_toda_group_proof_narrative_argument_discourse_roles(
        arguments
      )
    )
    source_index_by_identity = {
      id(argument): index
      for index, argument in enumerate(arguments)
    }

    print(label)
    for ordered_position, argument in enumerate(ordered):
      argument_index = source_index_by_identity[id(argument)]
      (
        relevant_groups,
        evidence,
        components,
        legacy_primary,
      ) = _legacy_primary(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
      owned_primary = (
        select_toda_group_proof_narrative_argument_primary_exactness_component(
          presentation,
          blocks,
          sidecar,
          arguments,
          argument_index,
        )
      )

      assert owned_primary == legacy_primary

      header = (
        render_toda_group_proof_narrative_argument_header_method_section(
          argument,
          discourse_roles[ordered_position],
          owned_primary,
        )
      )
      first_line = header.splitlines()[0] if header else ""

      print(
        "  "
        f"{ordered_position}: role={argument.role.value} "
        f"relevant={len(relevant_groups)} "
        f"evidence={len(evidence)} "
        f"components={len(components)} "
        f"owned_primary={owned_primary is not None}"
      )
      print(
        "     header="
        + first_line
      )

    print()


def _audit_pi6_3_goal_method_binding():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  order_index = next(
    index
    for index, argument in enumerate(arguments)
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    )
  )
  group_index = next(
    index
    for index, argument in enumerate(arguments)
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    )
  )

  order_primary = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      order_index,
    )
  )
  group_primary = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      group_index,
    )
  )

  assert order_primary is not None
  assert group_primary is not None
  assert order_primary != group_primary

  ordered = order_toda_group_proof_narrative_arguments(arguments)
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )
  source_index_by_identity = {
    id(argument): index
    for index, argument in enumerate(arguments)
  }

  headers = {}
  for ordered_position, argument in enumerate(ordered):
    argument_index = source_index_by_identity[id(argument)]
    primary = (
      select_toda_group_proof_narrative_argument_primary_exactness_component(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    headers[argument.role] = (
      render_toda_group_proof_narrative_argument_header_method_section(
        argument,
        discourse_roles[ordered_position],
        primary,
      )
    )

  order_header = headers[
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
  ]
  group_header = headers[
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
  ]

  assert (
    "$\\nu'$ の位数を決定するために、"
    "次の完全列を考える."
    in order_header
  )
  assert (
    "$\\pi_{6}^{3}$ の群構造を決定するために、"
    "次の完全列を考える."
    in group_header
  )

  print("pi_6^3 goal-method binding: PASS")
  print("  establish_order owns a primary method")
  print("  establish_group_structure owns a different primary method")
  print("  purpose -> method prose is preserved generically")


def main():
  print("=" * 78)
  print("Phase 147 RC1-4 Ownership Integration Audit")
  print("Production changes: none")
  print("=" * 78)

  _audit_renderer_route()
  _audit_targets()
  _audit_pi6_3_goal_method_binding()

  print()
  print("=" * 78)
  print("RC1-4 AUDIT RESULT: PASS")
  print("RC1 ownership integration is internally consistent.")
  print("RC2-RC6 were not changed.")
  print("=" * 78)


if __name__ == "__main__":
  main()
