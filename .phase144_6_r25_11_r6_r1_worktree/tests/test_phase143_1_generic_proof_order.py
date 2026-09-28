import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
import toda_group_proof_generic_narrative_renderer as generic_renderer
from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_indices,
  _generic_narrative_proof_order_indices,
  _render_generic_narrative_step,
  render_toda_group_proof_generic_proof_markdown,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
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


def test_phase143_1_proof_order_places_dependencies_before_parent_blocks():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  proof_order = (
    _generic_narrative_proof_order_indices(
      presentation,
      blocks,
    )
  )
  position_by_block_index = {
    block_index: position
    for position, block_index in enumerate(
      proof_order
    )
  }

  assert len(
    proof_order
  ) == len(
    blocks
  )
  assert len(
    set(
      proof_order
    )
  ) == len(
    blocks
  )

  for block_index in range(
    len(
      blocks
    )
  ):
    for dependency_index in (
      _generic_narrative_dependency_indices(
        presentation,
        blocks,
        block_index,
      )
    ):
      assert (
        position_by_block_index[
          dependency_index
        ]
        <
        position_by_block_index[
          block_index
        ]
      )


def test_phase143_1_pi6_3_target_block_is_rendered_last():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  target_index = next(
    index
    for index, block in enumerate(
      blocks
    )
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )
  )

  proof_order = (
    _generic_narrative_proof_order_indices(
      presentation,
      blocks,
    )
  )

  assert proof_order[
    -1
  ] == target_index

  rendered = (
    render_toda_group_proof_generic_proof_markdown(
      presentation,
      blocks,
    )
  )
  target_step = blocks[
    target_index
  ].steps[
    0
  ]
  target_fact = (
    _render_generic_narrative_step(
      target_step
    )
  )

  assert rendered.rstrip().endswith(
    target_fact
  )


def test_phase143_1_pi6_3_precondition_is_rendered_before_definition():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  precondition_index = next(
    index
    for index, block in enumerate(
      blocks
    )
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION
    )
  )
  definition_index = next(
    index
    for index, block in enumerate(
      blocks
    )
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
    )
  )

  proof_order = (
    _generic_narrative_proof_order_indices(
      presentation,
      blocks,
    )
  )

  assert proof_order.index(
    precondition_index
  ) < proof_order.index(
    definition_index
  )


def test_phase143_1_proof_order_preserves_every_block_once():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  proof_order = (
    _generic_narrative_proof_order_indices(
      presentation,
      blocks,
    )
  )

  assert sorted(
    proof_order
  ) == list(
    range(
      len(
        blocks
      )
    )
  )


def test_phase143_1_generic_order_has_no_pi6_specific_hardcoding():
  source = inspect.getsource(
    generic_renderer
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
