from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


def render_group(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(
    group_result
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


for label, n, k in (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
):
  print("=" * 88)
  print(label)
  print("=" * 88)
  print(render_group(n, k))
  print()
