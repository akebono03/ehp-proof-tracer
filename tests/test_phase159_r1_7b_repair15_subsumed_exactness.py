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


def _render(
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


def test_phase159_r1_7b_repair15_pi6_3_subsumed_windows_are_not_repeated():
  rendered = _render(
    3,
    3,
  )

  h_delta = (
    "\\[\n"
    r"\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} "
    r"\xrightarrow{\Delta} \pi_{5}^{2}."
    "\n\\]"
  )
  delta_e = (
    "\\[\n"
    r"\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} "
    r"\xrightarrow{E} \pi_{6}^{3}."
    "\n\\]"
  )

  assert h_delta not in rendered
  assert delta_e not in rendered

  assert (
    "\\[\n"
    r"\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} "
    r"\xrightarrow{\Delta} \pi_{5}^{2} "
    r"\xrightarrow{E} \pi_{6}^{3}."
    "\n\\]"
    in rendered
  )


def test_phase159_r1_7b_repair15_pi6_3_exactness_uses_canonical_delta():
  rendered = _render(
    3,
    3,
  )

  assert r"\xrightarrow{Δ}" not in rendered


def test_phase159_r1_7b_repair15_pi11_4_keeps_distinct_exactness_windows():
  rendered = _render(
    4,
    7,
  )

  h_delta = (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
  )
  e_h = (
    "\\[\n"
    r"\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}."
    "\n\\]"
  )

  assert rendered.count(
    h_delta
  ) == 1
  assert rendered.count(
    e_h
  ) == 1
