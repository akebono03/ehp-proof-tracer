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


def _phase159_public_narrative(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_pi4_3_public_exactness_surjectivity_is_emitted_once():
  rendered = _phase159_public_narrative(
    3,
    1,
  )

  map_statement = (
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  )
  reason_statement = (
    "完全性より, "
    + map_statement
  )

  assert rendered.count(
    map_statement
  ) == 1
  assert rendered.count(
    reason_statement
  ) == 1


def test_phase159_pi6_3_public_exactness_injectivity_is_emitted_once():
  rendered = _phase159_public_narrative(
    3,
    3,
  )

  map_statement = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  )
  reason_statement = (
    "完全性より, "
    + map_statement
  )

  assert rendered.count(
    map_statement
  ) == 1
  assert rendered.count(
    reason_statement
  ) == 1
