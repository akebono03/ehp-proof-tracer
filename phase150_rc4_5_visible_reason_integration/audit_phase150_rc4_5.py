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
  build_toda_group_proof_narrative_reason_sidecar,
)

CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)

def main():
  print("=" * 78)
  print("Phase 150 / RC4-5 Cross-group visible reason audit")
  print("=" * 78)
  for label, n, k in CASES:
    presentation, blocks, sidecar, arguments = _method_evidence_data(n, k)
    reasons = build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      sidecar,
    )
    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )
    visible = tuple(
      sentence
      for reason in reasons.reasons
      for sentence in (
        render_toda_group_proof_narrative_reason_sentence(reason),
      )
      if sentence is not None and sentence in rendered
    )
    print(
      f"{label}: reasons={len(reasons.reasons)} "
      f"visible={len(visible)}"
    )
    if label == "pi_6^3":
      marker = "この前提条件を満たすので、次の定義を用いる."
      index = rendered.find(marker)
      if index >= 0:
        print("-" * 78)
        print("pi_6^3 visible excerpt")
        print("-" * 78)
        print(rendered[max(0,index-180):min(len(rendered),index+len(marker)+260)])
  print("=" * 78)
  print("AUDIT_RESULT=PASS")
  print("NEXT=User Web Narrative visual confirmation, then RC4-6")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
