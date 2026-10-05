import inspect

import pytest

from toda_calculation_facade import (
  build_standard_toda_report,
)
import toda_group_proof_narrative_renderer as narrative_renderer
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)


def _complete_presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  return build_toda_group_proof_presentation(
    replay
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (5, 3),
    (8, 7),
    (4, 3),
  ),
)
def test_phase158_r5_3_depth2_public_narrative_uses_one_generic_route(
  monkeypatch,
  n,
  k,
):
  presentation = _complete_presentation(
    n,
    k,
  )
  calls = []

  def recording_generic_renderer(
    received_presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ):
    calls.append(
      (
        received_presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
    return "PHASE158_R5_3_COMMON_ROUTE_SENTINEL\n"

  def forbidden_route(
    *args,
    **kwargs,
  ):
    raise AssertionError(
      "dedicated or legacy public Narrative route was used"
    )

  monkeypatch.setattr(
    narrative_renderer,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    recording_generic_renderer,
  )
  monkeypatch.setattr(
    narrative_renderer,
    "_phase134_24_render_pi15_8_narrative",
    forbidden_route,
  )
  monkeypatch.setattr(
    narrative_renderer,
    "_render_phase134_9_pi8_5_narrative_markdown",
    forbidden_route,
  )
  monkeypatch.setattr(
    narrative_renderer,
    "_append_narrative_for_step",
    forbidden_route,
  )

  rendered = (
    narrative_renderer.render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert len(calls) == 1
  assert calls[0][0] is not None
  assert isinstance(
    calls[0][1],
    tuple,
  )
  assert isinstance(
    calls[0][3],
    tuple,
  )
  assert (
    "PHASE158_R5_3_COMMON_ROUTE_SENTINEL"
    in rendered
  )


def test_phase158_r5_3_baseline_function_has_no_group_route_dispatch(
):
  source = inspect.getsource(
    narrative_renderer
    ._phase158_baseline_render_toda_group_proof_narrative_markdown
  )

  forbidden_fragments = (
    "_phase134_24_render_pi15_8_narrative",
    "_is_phase134_3_pi6_3_presentation",
    "_is_phase150_rc4_generic_route_target",
    "_is_phase134_9_pi8_5_presentation",
    "_render_phase134_9_pi8_5_narrative_markdown",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source


def test_phase158_r5_3_depth1_direct_api_keeps_existing_fallback(
  monkeypatch,
):
  report = build_standard_toda_report(
    n=4,
    k=6,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=1,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  def forbidden_generic_renderer(
    *args,
    **kwargs,
  ):
    raise AssertionError(
      "depth-1 direct API must keep the existing fallback"
    )

  monkeypatch.setattr(
    narrative_renderer,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    forbidden_generic_renderer,
  )

  rendered = (
    narrative_renderer.render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert rendered.startswith(
    "# Group proof narrative"
  )
