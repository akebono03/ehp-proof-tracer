from homotopy_groups import (
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_map_name_latex,
)
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


def test_phase157_r20_repair39_map_type_name_fallback():
  source = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=2,
  )
  middle = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )
  target = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )

  assert (
    _toda_group_proof_narrative_map_name_latex(
      TodaSuspensionMap(
        source_group=source,
        target_group=middle,
      )
    )
    == "E"
  )
  assert (
    _toda_group_proof_narrative_map_name_latex(
      TodaHopfInvariantMap(
        source_group=middle,
        target_group=target,
      )
    )
    == "H"
  )
  assert (
    _toda_group_proof_narrative_map_name_latex(
      TodaDeltaMap(
        source_group=target,
        target_group=source,
      )
    )
    == r"\Delta"
  )


def test_phase157_r20_repair39_short_exact_follows_surjectivity():
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
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ "
    "は全射である."
  )
  reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  short_exact = (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
  )

  assert body.index(
    surjectivity
  ) < body.index(
    reason
  )
  assert body.index(
    reason
  ) < body.index(
    short_exact
  )
