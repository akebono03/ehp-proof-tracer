from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _data(
  depth: int = 2,
):
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
    max_depth=depth,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  return (
    raw,
    presentation,
    blocks,
  )


def test_phase156_r6_repair2_order_relation_normalizes_expression_lhs_with_scalar_rhs():
  (
    raw,
    presentation,
    blocks,
  ) = _data()

  order_steps = tuple(
    proof_step
    for block in blocks
    if block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.ORDER
    for proof_step in block.steps
  )
  eta_order_step = next(
    proof_step
    for proof_step in order_steps
    if proof_step.conclusion.rhs == 2
  )

  assert (
    _render_generic_narrative_step(
      eta_order_step
    )
    == (
      r"$\operatorname{ord}\left("
      r"\eta_{3}^{3}"
      r"\right) = 2$"
    )
  )


def test_phase156_r6_repair2_equality_relation_still_keeps_distinct_canonical_sides():
  (
    raw,
    presentation,
    blocks,
  ) = _data()

  rendered_steps = tuple(
    _render_generic_narrative_step(
      node.proof_step
    )
    for node in presentation.nodes
  )

  assert (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}$"
    in rendered_steps
  )
  assert (
    r"$\eta_{3}^{3} = \eta_{3}^{3}$"
    not in rendered_steps
  )


def test_phase156_r6_repair2_public_chain_and_order_are_canonical():
  (
    raw,
    presentation,
    blocks,
  ) = _data()
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  equation_one = (
    r"$2\nu' = "
    r"\eta_{3}\eta_{4}\eta_{5}\tag{1}$"
  )
  equation_two = (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
  )
  connector = "(1) と (2) より,"
  equation_three = (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
  )
  order_statement = (
    r"$\operatorname{ord}\left("
    r"\eta_{3}^{3}"
    r"\right) = 2$"
  )

  assert (
    rendered.index(
      equation_one
    )
    < rendered.index(
      equation_two
    )
    < rendered.index(
      connector
    )
    < rendered.index(
      equation_three
    )
    < rendered.index(
      order_statement
    )
  )


def test_phase156_r6_repair2_public_order_is_not_left_in_expanded_eta_form():
  (
    raw,
    presentation,
    blocks,
  ) = _data()
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  assert (
    r"$\operatorname{ord}\left("
    r"\eta_{3}\eta_{4}\eta_{5}"
    r"\right) = 2$"
    not in rendered
  )
