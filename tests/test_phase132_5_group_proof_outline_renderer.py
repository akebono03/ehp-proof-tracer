import pytest

from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_calculation import (
  build_known_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_proof_outline_renderer import (
  render_toda_group_proof_outline_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_query import TodaGroupQuery
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def build_phase132_5_sigma9_outline(
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

  rendered = (
    render_toda_group_proof_outline_markdown(
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


def test_phase132_5_sigma9_outline_has_source_and_conclusion():
  data = (
    build_phase132_5_sigma9_outline()
  )

  rendered = data[
    "rendered"
  ]

  assert "# Group proof outline" in rendered
  assert "## Source" in rendered
  assert "Toda Proposition 5.15" in rendered
  assert "- Phase: 75" in rendered
  assert "## Conclusion" in rendered
  assert (
    r"$\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}$"
    in rendered
  )


def test_phase132_5_sigma9_outline_uses_four_direct_premises():
  data = (
    build_phase132_5_sigma9_outline(
      max_depth=1,
    )
  )

  rendered = data[
    "rendered"
  ]

  direct_premise_lines = tuple(
    line
    for line in rendered.splitlines()
    if (
      line.startswith(
        "  - Premise "
      )
      and not line.startswith(
        "    - Premise "
      )
    )
  )

  assert len(
    direct_premise_lines
  ) == 4

  assert tuple(
    line.split(
      ":",
      1,
    )[
      0
    ]
    for line in direct_premise_lines
  ) == (
    "  - Premise 1",
    "  - Premise 2",
    "  - Premise 3",
    "  - Premise 4",
  )


def test_phase132_5_renderable_group_premise_uses_latex():
  data = (
    build_phase132_5_sigma9_outline(
      max_depth=1,
    )
  )

  assert (
    r"\pi_{12}^{5} = "
    r"\mathbb{Z}/2\{\sigma'''\}"
    in data[
      "rendered"
    ]
  )


def test_phase132_5_unrenderable_premises_use_rule_name_before_type_name():
  data = (
    build_phase132_5_sigma9_outline(
      max_depth=1,
    )
  )

  rendered = data[
    "rendered"
  ]

  root_step = data[
    "presentation"
  ].root_step

  root_edges = tuple(
    edge
    for edge in data[
      "presentation"
    ].edges
    if edge.parent_step is root_step
  )

  unrenderable_rule_names = tuple(
    edge.premise_step.inference_rule.name
    for edge in root_edges
    if (
      edge.premise_step.inference_rule
      is not None
      and type(
        edge.premise_step.conclusion
      ).__name__
      in (
        "Toda48Pi16_9OrderAndE4InjectiveStatement",
        "TodaLemma514Sigma8Statement",
        "TodaSigmaFamilyDefinitionStatement",
      )
    )
  )

  assert unrenderable_rule_names

  assert all(
    rule_name in rendered
    for rule_name in unrenderable_rule_names
  )


def test_phase132_5_depth_zero_has_no_premise_lines():
  data = (
    build_phase132_5_sigma9_outline(
      max_depth=0,
    )
  )

  rendered = data[
    "rendered"
  ]

  assert "## Outline" in rendered
  assert "- Conclusion:" in rendered
  assert "Premise " not in rendered


def test_phase132_5_depth_two_uses_edges_for_nested_outline():
  data = (
    build_phase132_5_sigma9_outline(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  nested_edges = tuple(
    edge
    for edge in presentation.edges
    if edge.parent_step is not presentation.root_step
  )

  assert nested_edges
  assert "    - Premise " in rendered


def test_phase132_5_outline_is_deterministic_and_non_mutating():
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

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  before_nodes = presentation.nodes
  before_edges = presentation.edges

  first = (
    render_toda_group_proof_outline_markdown(
      presentation
    )
  )
  second = (
    render_toda_group_proof_outline_markdown(
      presentation
    )
  )

  assert first == second
  assert presentation.nodes is before_nodes
  assert presentation.edges is before_edges
  assert repository.entries() == before_entries


def test_phase132_5_outline_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "TodaGroupProofPresentation"
    ),
  ):
    render_toda_group_proof_outline_markdown(
      "not-a-presentation"
    )
