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


def build_phase132_6_sigma9_narrative(
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


def test_phase132_6_sigma9_narrative_has_source_and_conclusion():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=1,
    )
  )

  rendered = data[
    "rendered"
  ]

  assert "# Group proof narrative" in rendered
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


def test_phase132_6_sigma9_narrative_preserves_direct_premise_indexes_and_facts():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=1,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  root_edges = tuple(
    sorted(
      (
        edge
        for edge in presentation.edges
        if edge.parent_step
        is presentation.root_step
      ),
      key=lambda edge: edge.premise_index,
    )
  )

  assert tuple(
    edge.premise_index
    for edge in root_edges
  ) == (
    0,
    1,
    2,
    3,
  )

  direct_facts = tuple(
    _render_group_proof_narrative_fact(
      edge.premise_step
    )
    for edge in root_edges
  )

  assert all(
    fact in rendered
    for fact in direct_facts
  )


def test_phase132_6_sigma9_narrative_renders_pi12_5_as_math():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=1,
    )
  )

  assert (
    r"$\pi_{12}^{5} = "
    r"\mathbb{Z}/2\{\sigma'''\}$"
    in data[
      "rendered"
    ]
  )


def test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=1,
    )
  )

  rendered = data[
    "rendered"
  ]

  assert "まず、" in rendered
  assert "また、" in rendered
  assert "さらに、" in rendered
  assert "このことから、" in rendered
  assert "したがって、" in rendered
  assert "まず、既出の" not in rendered
  assert "まず、すでに得た" not in rendered


def test_phase132_6_depth_zero_does_not_invent_premises():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=0,
    )
  )

  rendered = data[
    "rendered"
  ]

  assert (
    "Toda Proposition 5.15を用いる。"
    in rendered
  )
  assert "まず、" not in rendered
  assert "また、" not in rendered
  assert "さらに、" not in rendered
  assert (
    "したがって、"
    r"$\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}$"
    "である。"
    in rendered
  )


def test_phase132_6_depth_two_uses_nested_edges_before_parent_fact():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=2,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  nested_edge = next(
    edge
    for edge in presentation.edges
    if edge.parent_step
    is not presentation.root_step
  )

  parent_fact = (
    _render_group_proof_narrative_fact(
      nested_edge.parent_step
    )
  )

  child_fact = (
    _render_group_proof_narrative_fact(
      nested_edge.premise_step
    )
  )

  parent_edges = tuple(
    edge
    for edge in presentation.edges
    if edge.parent_step
    is nested_edge.parent_step
  )

  derivation_lead = (
    "このことから、"
    if len(
      parent_edges
    ) == 1
    else "これらから、"
  )

  parent_sentence = (
    derivation_lead
    + parent_fact
    + "を得る。"
  )

  assert child_fact in rendered
  assert parent_sentence in rendered
  assert (
    rendered.index(
      child_fact
    )
    < rendered.index(
      parent_sentence
    )
  )


def test_phase132_6_sigma_family_statements_use_readable_labels():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=1,
    )
  )

  presentation = data[
    "presentation"
  ]
  rendered = data[
    "rendered"
  ]

  root_edges = tuple(
    edge
    for edge in presentation.edges
    if edge.parent_step is presentation.root_step
  )

  expected_labels = {
    (
      "Toda48Pi16_9OrderAndE4InjectiveStatement"
    ): (
      "π₁₆⁹ の位数 16 と E⁴ の単射性"
    ),
    (
      "TodaLemma514Sigma8Statement"
    ): (
      "Toda Lemma 5.14 の σ₈ に関する結果"
    ),
    (
      "TodaSigmaFamilyDefinitionStatement"
    ): (
      "σ-family の定義"
    ),
  }

  labelled_steps = tuple(
    edge.premise_step
    for edge in root_edges
    if (
      type(
        edge.premise_step.conclusion
      ).__name__
      in expected_labels
    )
  )

  assert {
    type(
      step.conclusion
    ).__name__
    for step in labelled_steps
  } == set(
    expected_labels
  )

  for step in labelled_steps:
    type_name = type(
      step.conclusion
    ).__name__

    assert (
      expected_labels[
        type_name
      ]
      in rendered
    )

    assert (
      type_name
      not in rendered
    )

    if step.inference_rule is not None:
      assert (
        step.inference_rule.name
        not in rendered
      )


def test_phase132_6_narrative_is_deterministic_and_non_mutating():
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


def test_phase132_6_narrative_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "TodaGroupProofPresentation"
    ),
  ):
    render_toda_group_proof_narrative_markdown(
      "not-a-presentation"
    )


def test_phase138_4_sigma9_narrative_states_proof_purpose():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=2,
    )
  )

  rendered = data[
    "rendered"
  ]

  purpose = (
    "$\\sigma_{9}$ の位数を確認し、"
    "これが $\\pi_{16}^{9}$ を生成することを示す。"
  )

  assert purpose in rendered
  assert "まず、" in rendered
  assert (
    rendered.index(
      purpose
    )
    < rendered.index(
      "まず、"
    )
  )
