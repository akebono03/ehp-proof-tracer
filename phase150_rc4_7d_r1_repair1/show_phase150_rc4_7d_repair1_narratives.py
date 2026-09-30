from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)

for label, n, k in (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
):
  presentation, blocks, sidecar, arguments = _method_evidence_data(n, k)
  reasons = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    sidecar,
  )
  markdown = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )
  print("=" * 90)
  print(label)
  print("reason_kinds=", tuple(r.kind.value for r in reasons.reasons))
  print(markdown)
  print()
