from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_generic_narrative_renderer import (
  _GENERIC_INJECTIVE_STATEMENT_TYPES,
  _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  _generic_group_map_name,
  _generic_short_exact_sequence_latex,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


def matching_map_property_steps(presentation, exactness_step):
  statement = exactness_step.conclusion
  assert isinstance(statement, TodaProp42ExactnessStatement)
  window = statement.window
  first_map_name = getattr(window.first_map, "name", None)
  second_map_name = getattr(window.second_map, "name", None)

  injective_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        _GENERIC_INJECTIVE_STATEMENT_TYPES,
      )
      and node.proof_step.conclusion.map.source_group
      == window.source_term
      and node.proof_step.conclusion.map.target_group
      == window.middle_term
      and _generic_group_map_name(
        node.proof_step.conclusion.map
      )
      == first_map_name
    )
  )
  surjective_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        _GENERIC_SURJECTIVE_STATEMENT_TYPES,
      )
      and node.proof_step.conclusion.map.source_group
      == window.middle_term
      and node.proof_step.conclusion.map.target_group
      == window.target_term
      and _generic_group_map_name(
        node.proof_step.conclusion.map
      )
      == second_map_name
    )
  )
  return injective_steps, surjective_steps


def main():
  presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)

  derived = []
  for block_index, block in enumerate(blocks):
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    ):
      continue
    contributions = (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )
    for contribution in contributions:
      if (
        contribution.kind
        is TodaGroupProofNarrativeExactnessDisplayContributionKind
        .DERIVED_SHORT_EXACT_SEQUENCE
      ):
        derived.append((block_index, contribution))

  print("=" * 78)
  print("Phase 150 / RC4-5E-1 SHORT_EXACT_DERIVATION reason-chain audit")
  print("=" * 78)
  print("derived short exact contribution count:", len(derived))

  safe_records = []
  for record_index, (block_index, contribution) in enumerate(derived):
    exactness_step = contribution.proof_step
    statement = exactness_step.conclusion
    injective_steps, surjective_steps = matching_map_property_steps(
      presentation,
      exactness_step,
    )
    generated = _generic_short_exact_sequence_latex(
      presentation,
      exactness_step,
    )

    print("-" * 78)
    print("record:", record_index)
    print("block index:", block_index)
    print("exactness statement type:", type(statement).__name__)
    print("exactness line:", _render_generic_narrative_step(exactness_step))
    print("short exact:", contribution.latex)
    print("helper agrees:", generated == contribution.latex)
    print("injective matches:", len(injective_steps))
    for step in injective_steps:
      print("  injective:", _render_generic_narrative_step(step))
      print("  injective type:", type(step.conclusion).__name__)
      print(
        "  injective in presentation:",
        any(node.proof_step is step for node in presentation.nodes),
      )
    print("surjective matches:", len(surjective_steps))
    for step in surjective_steps:
      print("  surjective:", _render_generic_narrative_step(step))
      print("  surjective type:", type(step.conclusion).__name__)
      print(
        "  surjective in presentation:",
        any(node.proof_step is step for node in presentation.nodes),
      )

    window = statement.window
    map_identity_ok = (
      len(injective_steps) == 1
      and len(surjective_steps) == 1
      and injective_steps[0].conclusion.map.source_group
      == window.source_term
      and injective_steps[0].conclusion.map.target_group
      == window.middle_term
      and surjective_steps[0].conclusion.map.source_group
      == window.middle_term
      and surjective_steps[0].conclusion.map.target_group
      == window.target_term
      and _generic_group_map_name(
        injective_steps[0].conclusion.map
      )
      == getattr(window.first_map, "name", None)
      and _generic_group_map_name(
        surjective_steps[0].conclusion.map
      )
      == getattr(window.second_map, "name", None)
    )
    print("typed map/window identity:", map_identity_ok)

    safe_records.append(
      generated is not None
      and generated == contribution.latex
      and map_identity_ok
    )

  print("-" * 78)
  print("Classification diagnosis")
  safe = bool(safe_records) and all(safe_records)
  print(
    "EXISTING_DERIVATION_CONTRACT="
    + (
      "exactness window + matching injective first map + "
      "matching surjective second map"
      if safe
      else "insufficient"
    )
  )
  print(
    "SHORT_EXACT_DERIVATION_TYPED="
    + ("YES" if safe else "NO")
  )
  print(
    "PROPOSED_REASON_KIND="
    + ("SHORT_EXACT_DERIVATION" if safe else "NONE")
  )
  print(
    "TARGET_SPECIFIC_HARDCODING_REQUIRED="
    + ("NO" if safe else "UNKNOWN")
  )
  print(
    "SAFE_GENERIC_REASON="
    + ("YES" if safe else "NO")
  )
  print(
    "RECOMMENDED_PROSE="
    + (
      "この完全性と、左の写像が単射、右の写像が全射であることより、"
      "次の短完全列を得る."
      if safe
      else "NONE"
    )
  )
  print("AUDIT_RESULT=" + ("PASS" if safe else "FAIL"))

  if not safe:
    raise SystemExit(1)


if __name__ == "__main__":
  main()
