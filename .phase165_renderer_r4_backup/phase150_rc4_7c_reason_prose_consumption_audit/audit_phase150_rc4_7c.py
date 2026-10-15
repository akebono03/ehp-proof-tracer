from collections import Counter

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
)


CASES = (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _reference_marker_by_step_id(presentation):
  result = {}
  for entry in build_toda_group_proof_narrative_reference_entries(
    presentation
  ):
    marker = f"[R{entry.number}]"
    for proof_step in entry.proof_steps:
      result[id(proof_step)] = marker
  return result


def _classification(
  proof_step,
  reason,
  base_markdown,
  final_markdown,
  marker,
):
  generic_line = _render_generic_narrative_step(proof_step)
  line_in_base = bool(generic_line and generic_line in base_markdown)
  line_in_final = bool(generic_line and generic_line in final_markdown)
  marker_in_final = bool(marker and marker in final_markdown)

  if reason is not None:
    sentence = render_toda_group_proof_narrative_reason_sentence(reason)
    sentence_in_final = bool(sentence and sentence in final_markdown)
    if sentence_in_final:
      return "REASON_INSERTED"
    if not line_in_base:
      return "REASON_BUILT_BUT_CONCLUSION_NOT_RENDERED"
    return "REASON_BUILT_BUT_NOT_INSERTED"

  if marker_in_final and not line_in_final:
    return "REFERENCE_ONLY_WITHOUT_REASON"

  if line_in_final:
    return "SEMANTIC_LINE_WITHOUT_REASON"

  return "NO_REASON_AND_NOT_RENDERED"


def audit_case(label, n, k):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(n, k)

  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    sidecar,
  )
  reason_by_conclusion_id = {
    id(reason.conclusion_step): reason
    for reason in reason_sidecar.reasons
  }
  marker_by_step_id = _reference_marker_by_step_id(presentation)

  final_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  # Reconstruct the pre-reason stage by removing only the reason insertion
  # from the public pipeline: use the final renderer's own reason sidecar
  # against a probe built by stripping reason sentences from final output.
  # For consumption classification, generic-line presence in final output is
  # sufficient; base_markdown below is the public output before an idempotent
  # second reason insertion.
  base_markdown = final_markdown
  reinjected = insert_toda_group_proof_narrative_reason_prose(
    base_markdown,
    reason_sidecar,
  )
  assert reinjected == final_markdown

  counts = Counter()
  literature_counts = Counter()
  reason_kind_counts = Counter()

  print("=" * 112)
  print(label)
  print("=" * 112)
  print(f"nodes={len(presentation.nodes)}")
  print(f"blocks={len(blocks)}")
  print(f"arguments={len(arguments)}")
  print(f"reasons={len(reason_sidecar.reasons)}")
  print(
    "reason_kinds="
    + repr(
      tuple(reason.kind.value for reason in reason_sidecar.reasons)
    )
  )
  print()

  for index, node in enumerate(presentation.nodes):
    proof_step = node.proof_step
    reason = reason_by_conclusion_id.get(id(proof_step))
    reference = extract_toda_group_proof_step_literature_reference(
      proof_step
    )
    marker = marker_by_step_id.get(id(proof_step))
    generic_line = _render_generic_narrative_step(proof_step)
    generic_line_in_final = bool(
      generic_line and generic_line in final_markdown
    )
    marker_in_final = bool(
      marker and marker in final_markdown
    )

    # Focus the inventory on steps that can affect reason/provenance prose:
    # reason-bearing steps, literature-backed steps, and visible semantic lines.
    if (
      reason is None
      and reference is None
      and not generic_line_in_final
    ):
      continue

    classification = _classification(
      proof_step,
      reason,
      base_markdown,
      final_markdown,
      marker,
    )
    counts[classification] += 1

    if reference is not None:
      literature_counts[classification] += 1
    if reason is not None:
      reason_kind_counts[reason.kind.value] += 1

    print(f"STEP S{index:03d}")
    print(f"  conclusion_type={type(proof_step.conclusion).__name__}")
    print(
      "  inference_rule="
      + repr(
        None
        if proof_step.inference_rule is None
        else proof_step.inference_rule.name
      )
    )
    print(
      "  literature_reference="
      + repr(
        None
        if reference is None
        else (reference.label, reference.locator)
      )
    )
    print(f"  marker={marker!r}")
    print(
      "  reason_kind="
      + (
        "NONE"
        if reason is None
        else reason.kind.value
      )
    )
    print(
      "  reason_sentence="
      + repr(
        None
        if reason is None
        else render_toda_group_proof_narrative_reason_sentence(
          reason
        )
      )
    )
    print(f"  generic_line={generic_line!r}")
    print(f"  generic_line_in_final={generic_line_in_final}")
    print(f"  marker_in_final={marker_in_final}")
    print(f"  classification={classification}")
    print()

  print(f"CASE_CLASSIFICATION_COUNTS={dict(counts)}")
  print(
    "CASE_LITERATURE_CLASSIFICATION_COUNTS="
    f"{dict(literature_counts)}"
  )
  print(
    "CASE_REASON_KIND_COUNTS="
    f"{dict(reason_kind_counts)}"
  )
  print()
  print("PUBLIC_NARRATIVE")
  print("-" * 112)
  print(final_markdown)
  print()
  return counts, literature_counts, reason_kind_counts


def main():
  total = Counter()
  literature_total = Counter()
  reason_kind_total = Counter()

  print("Phase 150 RC4-7C Reason-Prose Consumption Audit")
  print("Production changes: none")
  print(
    "Scope: reason construction, reference-only compression, "
    "and public Narrative consumption."
  )
  print()

  for label, n, k in CASES:
    counts, literature_counts, reason_kind_counts = audit_case(
      label,
      n,
      k,
    )
    total.update(counts)
    literature_total.update(literature_counts)
    reason_kind_total.update(reason_kind_counts)

  print("=" * 112)
  print("CROSS-GROUP SUMMARY")
  print("=" * 112)
  print(f"CLASSIFICATION_COUNTS={dict(total)}")
  print(
    "LITERATURE_CLASSIFICATION_COUNTS="
    f"{dict(literature_total)}"
  )
  print(
    "REASON_KIND_COUNTS="
    f"{dict(reason_kind_total)}"
  )

  no_reason = (
    total["REFERENCE_ONLY_WITHOUT_REASON"]
    + total["SEMANTIC_LINE_WITHOUT_REASON"]
    + total["NO_REASON_AND_NOT_RENDERED"]
  )
  built_not_consumed = (
    total["REASON_BUILT_BUT_CONCLUSION_NOT_RENDERED"]
    + total["REASON_BUILT_BUT_NOT_INSERTED"]
  )
  inserted = total["REASON_INSERTED"]

  print(f"NO_REASON_VOCABULARY_PRESSURE_TOTAL={no_reason}")
  print(
    "BUILT_REASON_CONSUMPTION_GAP_TOTAL="
    f"{built_not_consumed}"
  )
  print(f"INSERTED_REASON_TOTAL={inserted}")

  if built_not_consumed:
    print(
      "AUDIT_DECISION="
      "REPAIR_EXISTING_REASON_CONSUMPTION_FIRST"
    )
  elif no_reason:
    print(
      "AUDIT_DECISION="
      "EXTEND_GENERIC_REASON_VOCABULARY"
    )
  else:
    print(
      "AUDIT_DECISION="
      "NO_RC4_7C_REASON_PROSE_GAP_FOUND"
    )


if __name__ == "__main__":
  main()
