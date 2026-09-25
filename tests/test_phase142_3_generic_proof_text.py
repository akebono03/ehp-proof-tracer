import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
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


def test_phase142_3_generic_proof_keeps_every_pi6_3_fact():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_generic_proof_markdown(
      presentation,
      blocks,
    )
  )

  assert rendered.startswith(
    "# Generic group proof\n"
  )

  for block in blocks:
    for proof_step in block.steps:
      rendered_step = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      assert rendered_step in rendered

  assert sum(
    len(
      block.steps
    )
    for block in blocks
  ) == len(
    presentation.nodes
  )


def test_phase142_3_generic_proof_uses_dependency_reasons():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_generic_proof_markdown(
      presentation,
      blocks,
    )
  )

  assert "[B" in rendered
  assert " より," in rendered


def test_phase142_3_precondition_precedes_definition():
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

  assert precondition_index < definition_index


def test_phase142_3_generic_proof_contains_core_pi6_3_facts():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_generic_proof_markdown(
      presentation,
      blocks,
    )
  )

  assert r"2\eta_{3} = 0" in rendered
  assert r"\nu'" in rendered
  assert r"H\left(\nu'\right) = \eta_{5}" in rendered
  assert r"2\nu' = \eta_{3}^{3}" in rendered
  assert r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}" in rendered


def test_phase142_3_generic_proof_contains_exactness_and_map_property_blocks():
  presentation = (
    _pi6_3_presentation()
  )
  blocks = (
    _pi6_3_blocks(
      presentation
    )
  )

  roles = tuple(
    block.role
    for block in blocks
  )

  assert (
    TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    in roles
  )
  assert (
    TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
    in roles
  )

  rendered = (
    render_toda_group_proof_generic_proof_markdown(
      presentation,
      blocks,
    )
  )

  assert "完全列" in rendered


def test_phase142_3_generic_proof_has_no_pi6_specific_branch():
  source = inspect.getsource(
    render_toda_group_proof_generic_proof_markdown
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
