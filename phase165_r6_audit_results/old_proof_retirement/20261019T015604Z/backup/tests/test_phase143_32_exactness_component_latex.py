import pytest

from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_component_latex,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _primary_component(
  n,
  k,
  role,
  occurrence=0,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  matches = tuple(
    (
      argument_index,
      argument,
    )
    for argument_index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )
  argument_index, argument = matches[
    occurrence
  ]

  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )

  return (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )


def test_phase143_32_pi6_3_order_renders_long_exact_sequence():
  component = _primary_component(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert component is not None
  assert (
    render_toda_group_proof_narrative_exactness_method_component_latex(
      component
    )
    == (
      r"\pi_{7}^{3} \xrightarrow{H} "
      r"\pi_{7}^{5} \xrightarrow{\Delta} "
      r"\pi_{5}^{2} \xrightarrow{E} "
      r"\pi_{6}^{3}"
    )
  )


def test_phase143_32_pi6_3_group_structure_renders_longer_exact_sequence():
  component = _primary_component(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert component is not None
  assert (
    render_toda_group_proof_narrative_exactness_method_component_latex(
      component
    )
    == (
      r"\pi_{7}^{3} \xrightarrow{H} "
      r"\pi_{7}^{5} \xrightarrow{\Delta} "
      r"\pi_{5}^{2} \xrightarrow{E} "
      r"\pi_{6}^{3} \xrightarrow{H} "
      r"\pi_{6}^{5}"
    )
  )


def test_phase143_32_singleton_component_renders_one_window():
  (
    _presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  exactness_block = next(
    block
    for block in blocks
    if any(
      proof_step.conclusion.__class__.__name__
      == "TodaProp42ExactnessStatement"
      for proof_step in block.steps
    )
  )

  window = TodaEHPExactnessWindow(
    source_term=TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    ),
    middle_term=TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=2,
    ),
    target_term=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    ),
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )
  component = (
    TodaGroupProofNarrativeExactnessMethodComponent(
      windows=(
        window,
      ),
      evidence_blocks=(
        exactness_block,
      ),
    )
  )

  assert (
    render_toda_group_proof_narrative_exactness_method_component_latex(
      component
    )
    == (
      r"\pi_{1}^{1} \xrightarrow{E} "
      r"\pi_{2}^{2} \xrightarrow{H} "
      r"\pi_{3}^{3}"
    )
  )


def test_phase143_32_does_not_add_short_exact_sequence_zero_terms():
  component = _primary_component(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert component is not None
  rendered = (
    render_toda_group_proof_narrative_exactness_method_component_latex(
      component
    )
  )

  assert r"0\longrightarrow" not in rendered
  assert r"\longrightarrow 0" not in rendered


def test_phase143_32_returns_latex_body_without_math_delimiters():
  component = _primary_component(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert component is not None
  rendered = (
    render_toda_group_proof_narrative_exactness_method_component_latex(
      component
    )
  )

  assert not rendered.startswith("$")
  assert not rendered.endswith("$")


def test_phase143_32_rejects_non_component():
  with pytest.raises(
    TypeError,
    match=(
      "component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent"
    ),
  ):
    render_toda_group_proof_narrative_exactness_method_component_latex(
      object()
    )
