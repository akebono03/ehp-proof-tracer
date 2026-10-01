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


def _render_group(
  n,
  k,
):
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


def _proof_body(
  rendered,
):
  marker = "## 証明\n\n"

  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1]


def test_phase153_r7_pi6_2_suppresses_unconsumed_prop56_aggregate_ancestry():
  rendered = _render_group(
    2,
    4,
  )
  body = _proof_body(
    rendered
  )

  for forbidden in (
    r"\pi_{5}^{2}",
    r"\pi_{7}^{4}",
    r"\pi_{8}^{5}",
    r"\pi_{n + 3}^{n}",
    r"n \ge 6",
    "Toda Proposition 5.6 の有限次元結果",
  ):
    assert forbidden not in body


def test_phase153_r7_pi6_2_keeps_consumed_reference_and_final_conclusion():
  rendered = _render_group(
    2,
    4,
  )
  body = _proof_body(
    rendered
  )

  assert (
    r"\pi_{6}^{3}"
    in rendered
  )
  assert (
    "[R2]"
    in body
  )
  assert (
    r"\pi_{6}^{2}"
    in body
  )


def test_phase153_r7_pi6_2_reference_use_does_not_expand_prop56_siblings():
  rendered = _render_group(
    2,
    4,
  )
  body = _proof_body(
    rendered
  )

  assert body.count(
    "[R2]"
  ) <= 2
