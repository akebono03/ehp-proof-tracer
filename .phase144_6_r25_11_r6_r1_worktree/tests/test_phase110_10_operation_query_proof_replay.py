import pytest

from repository_operation_query_facade import (
  query_standard_repository_operation_input,
)
from repository_operation_query_presentation import (
  build_repository_operation_query_presentation,
)
from repository_operation_query_proof_replay import (
  build_repository_operation_query_proof_replay,
)
from repository_operation_query_proof_replay_presentation import (
  build_repository_operation_query_proof_replay_presentation,
)
from repository_operation_query_proof_replay_renderer import (
  render_repository_operation_query_proof_replay_markdown,
)


def _presentation(
  query_input,
):
  result = (
    query_standard_repository_operation_input(
      query_input
    )
  )

  return (
    build_repository_operation_query_presentation(
      result
    )
  )


def test_phase110_10_single_fact_replays_without_fact_number():
  presentation = (
    _presentation(
      "E(eta_2 o nu_prime)"
    )
  )

  replay = (
    build_repository_operation_query_proof_replay(
      presentation
    )
  )

  assert (
    replay.source_item
    is presentation.items[
      0
    ]
  )

  assert (
    replay.source_match
    is presentation.items[
      0
    ].primary_match
  )

  assert (
    replay.root_step
    is replay.source_match.scope_node.proof_step
  )

  assert (
    replay.root_step.conclusion
    is replay.source_match.statement
  )

  assert replay.steps[
    0
  ].depth == 0

  assert (
    replay.steps[
      0
    ].proof_step
    is replay.root_step
  )


def test_phase110_10_multiple_facts_require_fact_number():
  presentation = (
    _presentation(
      "H(nu_prime)"
    )
  )

  with pytest.raises(
    ValueError,
    match="fact_number is required",
  ):
    build_repository_operation_query_proof_replay(
      presentation
    )


def test_phase110_10_fact_number_selects_presented_fact():
  presentation = (
    _presentation(
      "H(nu_prime)"
    )
  )

  replay = (
    build_repository_operation_query_proof_replay(
      presentation,
      fact_number=2,
    )
  )

  assert (
    replay.source_item
    is presentation.items[
      1
    ]
  )

  assert (
    replay.source_item.statement_latex
    == r"H\left(\nu'\right) = E^{2}\eta_{3}"
  )


def test_phase110_10_fact_number_out_of_range_is_rejected():
  presentation = (
    _presentation(
      "H(nu_prime)"
    )
  )

  with pytest.raises(
    ValueError,
    match="fact_number exceeds repository fact count",
  ):
    build_repository_operation_query_proof_replay(
      presentation,
      fact_number=3,
    )


def test_phase110_10_replay_is_bounded_to_depth_one_by_default():
  presentation = (
    _presentation(
      "Delta(iota_9)"
    )
  )

  replay = (
    build_repository_operation_query_proof_replay(
      presentation,
      fact_number=1,
    )
  )

  assert replay.max_depth == 1

  assert all(
    step.depth <= 1
    for step in replay.steps
  )


def test_phase110_10_replay_does_not_repeat_proof_step_identity():
  presentation = (
    _presentation(
      "eta_2 o nu_prime"
    )
  )

  replay = (
    build_repository_operation_query_proof_replay(
      presentation,
      fact_number=4,
    )
  )

  proof_step_ids = tuple(
    id(
      step.proof_step
    )
    for step in replay.steps
  )

  assert len(
    proof_step_ids
  ) == len(
    set(
      proof_step_ids
    )
  )


def test_phase110_10_presentation_preserves_query_fact_conclusion():
  query_presentation = (
    _presentation(
      "H(nu_prime)"
    )
  )

  replay = (
    build_repository_operation_query_proof_replay(
      query_presentation,
      fact_number=1,
    )
  )

  presentation = (
    build_repository_operation_query_proof_replay_presentation(
      replay
    )
  )

  assert (
    presentation.conclusion
    is replay.root_step.conclusion
  )

  assert (
    presentation.conclusion_latex
    == query_presentation.items[
      0
    ].statement_latex
  )


def test_phase110_10_renderer_starts_from_query_fact_not_repository_root():
  query_presentation = (
    _presentation(
      "H(nu_prime)"
    )
  )

  replay = (
    build_repository_operation_query_proof_replay(
      query_presentation,
      fact_number=1,
    )
  )

  presentation = (
    build_repository_operation_query_proof_replay_presentation(
      replay
    )
  )

  markdown = (
    render_repository_operation_query_proof_replay_markdown(
      presentation
    )
  )

  assert (
    "# Query fact"
    in markdown
  )

  assert (
    r"$H\left(\nu'\right) = \eta_{5}$"
    in markdown
  )

  assert (
    "First provenance: Toda Proposition 5.6, "
    "Phase 65, depth 3"
    in markdown
  )

  assert (
    "## Proof"
    in markdown
  )

  assert (
    "1. Depth 0:"
    in markdown
  )
