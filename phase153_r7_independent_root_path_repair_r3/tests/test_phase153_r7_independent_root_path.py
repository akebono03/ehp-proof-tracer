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


def _pi6_2_body():
  report = build_standard_toda_report(
    n=2,
    k=4,
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
  marker = "## 証明\n\n"

  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1]


def test_phase153_r7_repair_suppresses_prop56_siblings_without_independent_root_path():
  body = _pi6_2_body()

  for forbidden in (
    r"\pi_{5}^{2}",
    r"\pi_{7}^{4}",
    r"\pi_{8}^{5}",
    r"\pi_{n + 3}^{n}",
    r"n \ge 6",
    "Toda Proposition 5.6 の有限次元結果",
  ):
    assert forbidden not in body


def test_phase153_r7_repair_keeps_reference_use_and_final_group():
  body = _pi6_2_body()

  assert "[R2]" in body
  assert r"\pi_{6}^{2}" in body
