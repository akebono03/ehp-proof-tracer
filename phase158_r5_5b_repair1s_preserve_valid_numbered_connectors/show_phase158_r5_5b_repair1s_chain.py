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
  build_toda_group_result_proof_replay,
)


report = build_standard_toda_report(
  n=3,
  k=3,
)
group_result = (
  report
  .candidates[0]
  .source_candidate
  .group_result
)
replay = build_toda_group_result_proof_replay(
  group_result,
  max_depth=2,
)
presentation = build_toda_group_proof_presentation(
  replay
)
rendered = render_toda_group_proof_narrative_markdown(
  presentation
)

patterns = (
  r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$",
  r"$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$",
  "(1) と (2) より,",
  r"$2\nu' = \eta_{3}^{3}\tag{3}$",
  r"$2\nu' = \eta_{3}^{3}$",
)

for pattern in patterns:
  print(
    "present="
    + str(
      pattern in rendered
    )
    + " :: "
    + pattern
  )

print(
  ""
)
print(
  rendered.split(
    "## 証明",
    1,
  )[
    1
  ]
)
