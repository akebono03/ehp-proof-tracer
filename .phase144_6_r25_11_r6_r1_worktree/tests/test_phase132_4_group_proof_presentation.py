import pytest

from toda_calculation import (
  build_known_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
  build_toda_group_proof_presentation,
)
from toda_group_query import TodaGroupQuery
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def build_phase132_4_sigma9_presentation(
  max_depth=1,
):
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return {
    "repository": repository,
    "result": result,
    "group_result": group_result,
    "replay": replay,
    "presentation": presentation,
  }


def test_phase132_4_sigma9_builds_group_proof_presentation():
  data = (
    build_phase132_4_sigma9_presentation()
  )

  assert isinstance(
    data[
      "presentation"
    ],
    TodaGroupProofPresentation,
  )


def test_phase132_4_preserves_source_replay_identity():
  data = (
    build_phase132_4_sigma9_presentation()
  )

  assert (
    data[
      "presentation"
    ].source_replay
    is data[
      "replay"
    ]
  )


def test_phase132_4_preserves_root_and_source_entry_identity():
  data = (
    build_phase132_4_sigma9_presentation()
  )

  presentation = data[
    "presentation"
  ]

  assert (
    presentation.root_step
    is data[
      "group_result"
    ].proof_step
  )
  assert (
    presentation.source_entry
    is data[
      "group_result"
    ].source_entry
  )
  assert (
    presentation.source_entry.theorem
    == "Toda Proposition 5.15"
  )
  assert (
    presentation.source_entry.phase
    == "75"
  )


def test_phase132_4_nodes_are_exact_replay_steps_in_original_order():
  data = (
    build_phase132_4_sigma9_presentation(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  replay = data[
    "replay"
  ]

  assert (
    presentation.nodes
    is replay.steps
  )
  assert tuple(
    id(
      node.proof_step
    )
    for node in presentation.nodes
  ) == tuple(
    id(
      replay_step.proof_step
    )
    for replay_step in replay.steps
  )
  assert tuple(
    node.depth
    for node in presentation.nodes
  ) == tuple(
    replay_step.depth
    for replay_step in replay.steps
  )


def test_phase132_4_depth_zero_contains_root_and_no_edges():
  data = (
    build_phase132_4_sigma9_presentation(
      max_depth=0,
    )
  )

  presentation = data[
    "presentation"
  ]

  assert presentation.max_depth == 0
  assert len(
    presentation.nodes
  ) == 1
  assert (
    presentation.nodes[
      0
    ].proof_step
    is presentation.root_step
  )
  assert presentation.edges == ()


def test_phase132_4_depth_one_preserves_four_direct_root_premise_edges():
  data = (
    build_phase132_4_sigma9_presentation(
      max_depth=1,
    )
  )

  presentation = data[
    "presentation"
  ]
  root_step = presentation.root_step

  root_edges = tuple(
    edge
    for edge in presentation.edges
    if edge.parent_step is root_step
  )

  assert len(
    root_edges
  ) == 4
  assert tuple(
    edge.premise_index
    for edge in root_edges
  ) == (
    0,
    1,
    2,
    3,
  )
  assert tuple(
    edge.premise_step
    for edge in root_edges
  ) == tuple(
    premise
    for premise in root_step.premises
    if hasattr(
      premise,
      "conclusion",
    )
  )


def test_phase132_4_all_edges_connect_selected_nodes_only():
  data = (
    build_phase132_4_sigma9_presentation(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]

  selected_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }

  assert all(
    id(
      edge.parent_step
    )
    in selected_ids
    and id(
      edge.premise_step
    )
    in selected_ids
    for edge in presentation.edges
  )


def test_phase132_4_edges_preserve_original_premise_index_identity():
  data = (
    build_phase132_4_sigma9_presentation(
      max_depth=2,
    )
  )

  for edge in data[
    "presentation"
  ].edges:
    assert (
      edge.parent_step.premises[
        edge.premise_index
      ]
      is edge.premise_step
    )


def test_phase132_4_builder_does_not_mutate_replay_or_repository():
  repository = (
    build_standard_production_proof_repository()
  )

  before_entries = repository.entries()

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )

  before_steps = replay.steps

  first = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  second = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  assert replay.steps is before_steps
  assert repository.entries() == before_entries
  assert tuple(
    (
      id(
        edge.parent_step
      ),
      id(
        edge.premise_step
      ),
      edge.premise_index,
    )
    for edge in first.edges
  ) == tuple(
    (
      id(
        edge.parent_step
      ),
      id(
        edge.premise_step
      ),
      edge.premise_index,
    )
    for edge in second.edges
  )


def test_phase132_4_builder_rejects_non_replay():
  with pytest.raises(
    TypeError,
    match=(
      "replay must be a "
      "TodaGroupResultProofReplayResult"
    ),
  ):
    build_toda_group_proof_presentation(
      "not-a-replay"
    )
