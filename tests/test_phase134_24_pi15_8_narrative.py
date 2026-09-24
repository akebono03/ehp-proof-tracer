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


def _pi15_8_presentation(
  max_depth=2,
):
  report = build_standard_toda_report(
    n=8,
    k=7,
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase134_24_pi15_8_narrative_has_mathematical_structure(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  assert "# Group proof narrative" in rendered
  assert "## 証明対象" in rendered
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered
  assert (
    "Toda Proposition 4.4 の分解同型"
    in rendered
  )


def test_phase134_24_pi15_8_narrative_renders_two_boundary_groups(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  assert (
    r"\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}"
    in rendered
  )

  assert (
    r"\pi_{15}^{15} = \mathbb{Z}\{\iota_{15}\}"
    in rendered
  )


def test_phase134_24_pi15_8_narrative_renders_generator_transport(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  assert (
    r"\sigma' \longmapsto E\sigma'"
    in rendered
  )

  assert (
    r"\iota_{15} \longmapsto \sigma_{8}"
    in rendered
  )


def test_phase134_24_pi15_8_narrative_preserves_transport_then_standard_order(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  transported = (
    r"\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}"
  )

  final = (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}"
  )

  assert transported in rendered
  assert final in rendered
  assert (
    rendered.index(
      transported
    )
    < rendered.rindex(
      final
    )
  )
  assert (
    "summand の表示順を標準形に直すと,"
    in rendered
  )


def test_phase134_24_pi15_8_narrative_hides_internal_statement_labels(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  assert "transported decomposition" not in rendered
  assert "decomposition specialization" not in rendered
  assert (
    "Toda515Sigma8TransportedDecompositionStatement"
    not in rendered
  )
  assert "位数を求める" not in rendered


def test_phase134_24_depth_one_keeps_existing_renderer_path(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation(
        max_depth=1,
      )
    )
  )

  assert "## 使用する結果" not in rendered
  assert (
    "summand の表示順を標準形に直すと,"
    not in rendered
  )


def test_phase134_24_pi15_8_narrative_is_deterministic(
):
  presentation = (
    _pi15_8_presentation()
  )

  first = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  second = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert first == second
