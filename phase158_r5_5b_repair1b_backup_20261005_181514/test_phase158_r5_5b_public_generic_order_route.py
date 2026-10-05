import toda_group_proof_narrative_renderer as narrative_renderer
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase158_r5_5b_has_ordered_root_argument,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _presentation(
  n: int,
  k: int,
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

  return build_toda_group_proof_presentation(
    replay
  )


def _web_text(
  n: int,
  k: int,
) -> str:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )
  parts = []
  in_proof = False

  for line in view.rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )

  return "
".join(
    parts
  )

def test_phase158_r5_5b_pi7_4_root_argument_uses_generic_order():
  presentation = _presentation(
    4,
    3,
  )

  assert (
    _phase158_r5_5b_has_ordered_root_argument(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  premise = (
    r"$\nu_{4}$ の分解を用いる."
  )
  target = (
    r"$\pi_{7}^{4} = "
    r"\mathbb{Z}\{\nu_{4}\} "
    r"\oplus \mathbb{Z}/4\{E\nu'\}$"
  )

  assert premise in rendered
  assert target in rendered
  assert rendered.index(
    premise
  ) < rendered.index(
    target
  )


def test_phase158_r5_5b_pi15_8_root_argument_uses_generic_order():
  presentation = _presentation(
    8,
    7,
  )

  assert (
    _phase158_r5_5b_has_ordered_root_argument(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  transported = (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
  )
  target = (
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
  )

  assert transported in rendered
  assert target in rendered
  assert rendered.index(
    transported
  ) < rendered.index(
    target
  )


def test_phase158_r5_5b_pi15_8_does_not_use_legacy_dedicated_renderer(
  monkeypatch,
):
  presentation = _presentation(
    8,
    7,
  )

  def fail_if_called(
    _presentation,
  ):
    raise AssertionError(
      "legacy pi15_8 renderer was called"
    )

  monkeypatch.setattr(
    narrative_renderer,
    "_phase134_24_render_pi15_8_narrative",
    fail_if_called,
  )

  rendered = (
    narrative_renderer
    .render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"\pi_{15}^{8}"
    in rendered
  )


def test_phase158_r5_5b_web_depth2_pi7_4_preserves_premise_before_target():
  rendered = _web_text(
    4,
    3,
  )

  premise = (
    r"\nu_{4} の分解を用いる."
  )
  target = (
    r"\pi_{7}^{4} = "
    r"\mathbb{Z}\{\nu_{4}\} "
    r"\oplus \mathbb{Z}/4\{E\nu'\}"
  )

  assert premise in rendered
  assert target in rendered
  assert rendered.index(
    premise
  ) < rendered.index(
    target
  )


def test_phase158_r5_5b_web_depth2_pi15_8_preserves_transport_before_target():
  rendered = _web_text(
    8,
    7,
  )

  transported = (
    r"\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}"
  )
  target = (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}"
  )

  assert transported in rendered
  assert target in rendered
  assert rendered.index(
    transported
  ) < rendered.index(
    target
  )
