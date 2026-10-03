from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _depth2_presentations():
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
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  return (
    presentation,
    closure,
  )


def test_phase156_r6_repair1_equation2_preserves_distinct_lhs_and_rhs():
  (
    presentation,
    closure,
  ) = _depth2_presentations()

  rendered_steps = tuple(
    _render_generic_narrative_step(
      node.proof_step
    )
    for node in closure.nodes
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


def test_phase156_r6_repair1_public_numbered_chain_has_canonical_equation2():
  (
    presentation,
    closure,
  ) = _depth2_presentations()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    r"$2\nu' = "
    r"\eta_{3}\eta_{4}\eta_{5}\tag{1}$"
    in rendered
  )
  assert (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
    in rendered
  )
  assert (
    "(1) と (2) より,"
    in rendered
  )
  assert (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
    in rendered
  )


def test_phase156_r6_repair1_equation3_is_immediately_after_equation2_derivation():
  (
    presentation,
    closure,
  ) = _depth2_presentations()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
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
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
  )

  assert (
    rendered.index(
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
