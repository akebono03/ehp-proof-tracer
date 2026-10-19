import inspect

import main as cli_main
import toda_group_proof_narrative_renderer as narrative_renderer
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _pi6_3_presentation_data():
  return _method_evidence_data(
    3,
    3,
  )


def test_phase144_6_public_pi6_3_equals_contribution_renderer():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _pi6_3_presentation_data()

  expected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  actual = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert actual == expected
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in actual
  )


def test_phase144_6_public_pi6_3_uses_r5_43_contribution_route(
  monkeypatch,
):
  (
    presentation,
    _,
    _,
    _,
  ) = _pi6_3_presentation_data()

  called = {
    "value": False,
  }
  original = (
    narrative_renderer
    .render_toda_group_proof_narrative_multi_argument_with_contributions_markdown
  )

  def recording_renderer(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ):
    called["value"] = True
    return original(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )

  monkeypatch.setattr(
    narrative_renderer,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    recording_renderer,
  )

  rendered = (
    narrative_renderer
    .render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert called["value"]
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in rendered
  )


def test_phase144_6_cli_pi6_3_narrative_uses_public_cutover(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "3",
      "3",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in captured.out
  )


def test_phase144_6_public_branch_calls_contribution_renderer():
  source = inspect.getsource(
    render_toda_group_proof_narrative_markdown
  )

  branch_start = source.index(
    "_is_phase134_3_pi6_3_presentation"
  )
  next_branch = source.index(
    "_is_phase134_9_pi8_5_presentation"
  )
  pi6_branch = source[
    branch_start:
    next_branch
  ]

  assert (
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"
    in pi6_branch
  )
  assert (
    "render_toda_group_proof_narrative_multi_argument_markdown("
    not in pi6_branch
  )
