from collections import Counter
from tests.test_phase143_19_method_evidence import _method_evidence_data
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

TARGETS = ((3, 3), (5, 3), (4, 6), (5, 7), (8, 7), (9, 7))


def main():
  all_visible = True
  all_safe = True

  for n, k in TARGETS:
    presentation, blocks, semantic_sidecar, arguments = (
      _method_evidence_data(n, k)
    )
    sidecar = build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
    rendered = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
    visible_ids = {
      id(node.proof_step)
      for node in presentation.nodes
    }
    unsafe = tuple(
      reason.kind.name
      for reason in sidecar.reasons
      if (
        id(reason.conclusion_step) not in visible_ids
        or any(
          id(premise) not in visible_ids
          for premise in reason.premise_steps
        )
      )
    )
    invisible = []
    for reason in sidecar.reasons:
      sentence = render_toda_group_proof_narrative_reason_sentence(
        reason
      )
      if sentence is not None and sentence not in rendered:
        invisible.append(reason.kind.name)
    invisible = tuple(invisible)
    counts = Counter(
      reason.kind.name
      for reason in sidecar.reasons
    )
    print(
      f"pi_{n+k}^{n}: reasons={dict(counts)} "
      f"unsafe={unsafe} invisible={invisible}"
    )
    all_safe = all_safe and not unsafe
    all_visible = all_visible and not invisible

  print("ALL_REASON_STEPS_PRESENTATION_VISIBLE=", all_safe)
  print("ALL_RENDERABLE_REASONS_VISIBLE=", all_visible)
  print(
    "TRANSPORTED_ORDER_IMPLEMENTED=",
    "TRANSPORTED_ORDER"
    in tuple(kind.name for kind in TodaGroupProofNarrativeReasonKind),
  )
  print("TRANSPORTED_ORDER_REQUIRED_BY_THIS_AUDIT=", False)
  print("RC4_CLOSURE_READY=", all_safe and all_visible)

  if not (all_safe and all_visible):
    raise SystemExit(1)


if __name__ == "__main__":
  main()
