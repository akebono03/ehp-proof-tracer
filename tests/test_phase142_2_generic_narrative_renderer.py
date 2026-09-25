import inspect

import pytest

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  render_toda_group_proof_generic_narrative_markdown,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _pi6_3_presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=3,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _pi6_3_blocks(
  presentation,
):
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  return (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )


def test_phase142_2_generic_renderer_renders_every_block_once():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_generic_narrative_markdown(
      presentation,
      blocks,
    )
  )

  assert rendered.startswith(
    "# Generic group proof narrative\n"
  )

  for block_index in range(
    len(
      blocks
    )
  ):
    label = (
      "[B"
      + f"{block_index + 1:02d}"
      + "]"
    )

    assert rendered.count(
      "## "
      + label
    ) == 1


def test_phase142_2_generic_renderer_exposes_existing_dependencies():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_generic_narrative_markdown(
      presentation,
      blocks,
    )
  )

  assert "依存: [B" in rendered


def test_phase142_2_generic_renderer_uses_mathematical_role_labels():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_generic_narrative_markdown(
      presentation,
      blocks,
    )
  )

  assert "証明対象" in rendered
  assert "適用条件" in rendered
  assert "定義" in rendered
  assert "所属" in rendered
  assert "計算" in rendered
  assert "完全性" in rendered
  assert "写像の性質" in rendered
  assert "位数" in rendered
  assert "群構造" in rendered


def test_phase142_2_generic_renderer_rejects_incomplete_blocks():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "blocks must cover presentation nodes "
      "exactly once"
    ),
  ):
    render_toda_group_proof_generic_narrative_markdown(
      presentation,
      blocks[
        1:
      ],
    )


def test_phase142_2_generic_renderer_has_no_pi6_target_hardcoding():
  source = inspect.getsource(
    render_toda_group_proof_generic_narrative_markdown
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
