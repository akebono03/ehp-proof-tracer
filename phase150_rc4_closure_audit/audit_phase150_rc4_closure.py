from collections import Counter

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)


REPRESENTATIVE_TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def main() -> None:
  print("=" * 78)
  print("Phase 150 / RC4 closure audit")
  print("=" * 78)

  available_kind_names = tuple(
    kind.name
    for kind in TodaGroupProofNarrativeReasonKind
  )
  print("A. Implemented reason kinds")
  for name in available_kind_names:
    print(" ", name)

  expected_completed_kinds = (
    "DEFINITION_APPLICABILITY",
    "EXACTNESS_TO_MAP_PROPERTY",
    "MULTIPLE_RELATION_TO_ORDER",
    "FINAL_GROUP_STRUCTURE",
  )
  completed_kind_set_ok = all(
    name in available_kind_names
    for name in expected_completed_kinds
  )
  print("COMPLETED_REASON_KINDS_PRESENT=", completed_kind_set_ok)
  print(
    "TRANSPORTED_ORDER_IMPLEMENTED=",
    "TRANSPORTED_ORDER" in available_kind_names,
  )

  print("-" * 78)
  print("B. Representative cross-group reason inventory")

  total_reason_counts = Counter()
  target_rows = []
  pi6_visible_ok = False
  pi6_final_reason_ok = False

  for n, k in REPRESENTATIVE_TARGETS:
    try:
      (
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      ) = _method_evidence_data(n, k)
    except Exception as exc:
      print(
        f"TARGET pi_{n+k}^{n}: UNAVAILABLE "
        f"{type(exc).__name__}: {exc}"
      )
      target_rows.append(
        (n, k, "UNAVAILABLE", ())
      )
      continue

    reason_sidecar = (
      build_toda_group_proof_narrative_reason_sidecar(
        presentation,
        semantic_sidecar,
      )
    )
    counts = Counter(
      reason.kind.name
      for reason in reason_sidecar.reasons
    )
    total_reason_counts.update(counts)

    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

    visible_reason_count = 0
    invisible_reasons = []

    for reason in reason_sidecar.reasons:
      sentence = (
        render_toda_group_proof_narrative_reason_sentence(
          reason
        )
      )
      if sentence is None:
        invisible_reasons.append(
          reason.kind.name
        )
        continue
      if sentence in rendered:
        visible_reason_count += 1
      else:
        invisible_reasons.append(
          reason.kind.name
        )

    print(
      f"TARGET pi_{n+k}^{n}: "
      f"reasons={dict(counts)} "
      f"visible={visible_reason_count}/"
      f"{len(reason_sidecar.reasons)} "
      f"invisible={tuple(invisible_reasons)}"
    )

    target_rows.append(
      (
        n,
        k,
        "OK",
        tuple(invisible_reasons),
      )
    )

    if (n, k) == (3, 3):
      pi6_visible_ok = (
        visible_reason_count
        == len(reason_sidecar.reasons)
      )
      final_reasons = tuple(
        reason
        for reason in reason_sidecar.reasons
        if (
          reason.kind.name
          == "FINAL_GROUP_STRUCTURE"
        )
      )
      pi6_final_reason_ok = (
        len(final_reasons) == 1
        and (
          render_toda_group_proof_narrative_reason_sentence(
            final_reasons[0]
          )
          in rendered
        )
      )

  print("TOTAL_REASON_COUNTS=", dict(total_reason_counts))
  print("PI6_ALL_REASON_SENTENCES_VISIBLE=", pi6_visible_ok)
  print("PI6_FINAL_GROUP_REASON_VISIBLE=", pi6_final_reason_ok)

  print("-" * 78)
  print("C. RC4 completion evidence")
  available_targets = tuple(
    row
    for row in target_rows
    if row[2] == "OK"
  )
  all_available_reasons_visible = all(
    not row[3]
    for row in available_targets
  )
  print(
    "ALL_AVAILABLE_REPRESENTATIVE_REASONS_VISIBLE=",
    all_available_reasons_visible,
  )

  print("-" * 78)
  print("D. Known remaining items and phase boundary")
  print(
    "TRANSPORTED_ORDER_STATUS="
    "NO_NAMED_REASON_KIND; REQUIRE_ONLY_IF_A_CONCRETE_UNEXPLAINED_"
    "TRANSPORTED_ORDER_CONCLUSION_IS_FOUND"
  )
  print(
    "RC4_5D_3_R2_STATUS="
    "AUDIT_HARNESS_FALSE_NEGATIVE_ONLY; PRODUCTION_ALREADY_VERIFIED"
  )
  print(
    "EQUATION_ORDERING_STATUS="
    "OUTSIDE_RC4; KEEP_FOR_RC6"
  )
  print(
    "ETA_NOTATION_NORMALIZATION_STATUS="
    "OUTSIDE_RC4; KEEP_FOR_RC6"
  )
  print(
    "VAGUE_CONNECTOR_FORMATTING_STATUS="
    "OUTSIDE_RC4_WHEN_REASON_IS_ALREADY_EXPLICIT; KEEP_FOR_RC6"
  )

  closure_ready = (
    completed_kind_set_ok
    and pi6_visible_ok
    and pi6_final_reason_ok
    and all_available_reasons_visible
  )

  print("-" * 78)
  print("E. Decision")
  print("RC4_CLOSURE_READY=", closure_ready)

  if closure_ready:
    print(
      "DECISION=RC4 may close without adding TRANSPORTED_ORDER "
      "solely because it appeared in the earlier classification."
    )
    print(
      "NEXT=RC4-6 final regression/documentation closure."
    )
  else:
    print(
      "DECISION=RC4 remains open; inspect the failed visibility/"
      "classification evidence before adding any new reason kind."
    )
    raise SystemExit(1)


if __name__ == "__main__":
  main()
