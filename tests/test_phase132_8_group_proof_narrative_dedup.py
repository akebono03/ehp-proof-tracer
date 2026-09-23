from collections import Counter

import main as cli_main

from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_calculation import (
  build_known_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_query import TodaGroupQuery
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def build_phase132_8_sigma9_narrative(
  max_depth=2,
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

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  return {
    "repository": repository,
    "result": result,
    "group_result": group_result,
    "replay": replay,
    "presentation": presentation,
    "rendered": rendered,
  }


def _incoming_use_count_by_step_id(
  presentation,
):
  return Counter(
    id(
      edge.premise_step
    )
    for edge in presentation.edges
  )


def test_phase132_8_sigma9_has_shared_dependencies_at_depth_two():
  data = (
    build_phase132_8_sigma9_narrative(
      max_depth=2,
    )
  )

  counts = (
    _incoming_use_count_by_step_id(
      data[
        "presentation"
      ]
    )
  )

  assert any(
    count > 1
    for count in counts.values()
  )


def test_phase132_8_shared_dependency_subtree_is_expanded_once():
  data = (
    build_phase132_8_sigma9_narrative(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  counts = (
    _incoming_use_count_by_step_id(
      presentation
    )
  )

  shared_parent = next(
    node.proof_step
    for node in presentation.nodes
    if (
      counts[
        id(
          node.proof_step
        )
      ]
      > 1
      and any(
        edge.parent_step
        is node.proof_step
        for edge in presentation.edges
      )
      and node.proof_step
      is not presentation.root_step
    )
  )

  parent_fact = (
    _render_group_proof_narrative_fact(
      shared_parent
    )
  )

  parent_edges = tuple(
    edge
    for edge in presentation.edges
    if edge.parent_step is shared_parent
  )

  derivation_lead = (
    "このことから、"
    if len(
      parent_edges
    ) == 1
    else "これらから、"
  )

  assert (
    rendered.count(
      derivation_lead
      + parent_fact
      + "を得る。"
    )
    == 1
  )


def test_phase132_8_repeated_shared_dependency_uses_existing_reference():
  data = (
    build_phase132_8_sigma9_narrative(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  counts = (
    _incoming_use_count_by_step_id(
      presentation
    )
  )

  shared_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if counts[
      id(
        node.proof_step
      )
    ] > 1
  )

  assert shared_steps
  assert "すでに得た" in rendered

  assert any(
    (
      "すでに得た"
      + _render_group_proof_narrative_fact(
        step
      )
      + "を用いる。"
    )
    in rendered
    for step in shared_steps
  )


def test_phase132_8_same_proof_step_is_not_reexpanded_from_each_parent():
  data = (
    build_phase132_8_sigma9_narrative(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  counts = (
    _incoming_use_count_by_step_id(
      presentation
    )
  )

  candidates = tuple(
    node.proof_step
    for node in presentation.nodes
    if (
      counts[
        id(
          node.proof_step
        )
      ]
      > 1
      and any(
        edge.parent_step
        is node.proof_step
        for edge in presentation.edges
      )
    )
  )

  assert candidates

  for step in candidates:
    fact = (
      _render_group_proof_narrative_fact(
        step
      )
    )

    premise_count = sum(
      1
      for edge in presentation.edges
      if edge.parent_step is step
    )

    derivation_lead = (
      "このことから、"
      if premise_count == 1
      else "これらから、"
    )

    assert (
      rendered.count(
        derivation_lead
        + fact
        + "を得る。"
      )
      <= 1
    )


def test_phase132_8_root_conclusion_and_source_remain_unchanged():
  data = (
    build_phase132_8_sigma9_narrative(
      max_depth=2,
    )
  )

  rendered = data[
    "rendered"
  ]

  assert (
    "Toda Proposition 5.15を用いる。"
    in rendered
  )
  assert (
    "したがって、"
    r"$\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}$"
    "を得る。"
    in rendered
  )


def test_phase132_8_depth_one_also_references_shared_direct_dependency():
  data = (
    build_phase132_8_sigma9_narrative(
      max_depth=1,
    )
  )

  rendered = data[
    "rendered"
  ]

  assert "すでに得た" in rendered
  assert (
    r"$\pi_{12}^{5} = "
    r"\mathbb{Z}/2\{\sigma'''\}$"
    in rendered
  )


def test_phase132_8_cli_narrative_uses_deduplicated_renderer(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group proof narrative" in captured.out
  assert "すでに得た" in captured.out
  assert (
    captured.out.count(
      "このことから、"
      "Toda Lemma 5.13 sigma triple-prime definition"
      "を得る。"
    )
    <= 1
  )


def test_phase132_8_narrative_remains_deterministic_and_non_mutating():
  data = (
    build_phase132_8_sigma9_narrative(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  repository = data[
    "repository"
  ]

  before_entries = repository.entries()
  before_nodes = presentation.nodes
  before_edges = presentation.edges

  first = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  second = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert first == second
  assert presentation.nodes is before_nodes
  assert presentation.edges is before_edges
  assert repository.entries() == before_entries
