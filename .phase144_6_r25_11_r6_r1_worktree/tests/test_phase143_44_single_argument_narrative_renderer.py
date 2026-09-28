import pytest

from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
)
from toda_group_proof_narrative_argument_single_renderer import (
  render_toda_group_proof_narrative_single_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
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


def _single_argument_data(
  n,
  k,
  role,
  discourse_role,
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
    argument_index
    for argument_index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )
  argument_index = matches[
    occurrence
  ]
  argument = arguments[
    argument_index
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
  primary_component = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )

  rendered = (
    render_toda_group_proof_narrative_single_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
      discourse_role,
      primary_component,
    )
  )

  return (
    argument,
    primary_component,
    rendered,
  )


def test_phase143_44_pi6_3_order_combines_header_method_and_body():
  (
    _argument,
    primary_component,
    rendered,
  ) = _single_argument_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .MIDDLE,
  )

  assert primary_component is not None
  assert rendered.startswith(
    "次に、$\\nu'$ の位数を決定する. "
    "そのために、次の完全列を考える."
  )
  assert (
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}"
    in rendered
  )
  assert (
    r"\operatorname{ord}\left(\nu'\right) = 4"
    in rendered
  )


def test_phase143_44_pi6_3_group_has_one_primary_formula_and_keeps_short_exact():
  (
    _argument,
    primary_component,
    rendered,
  ) = _single_argument_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .FINAL,
  )

  assert primary_component is not None
  primary_formula = (
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}"
  )

  assert rendered.count(
    primary_formula
  ) == 1
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


def test_phase143_44_pi6_3_definition_without_primary_has_no_method_transition():
  (
    _argument,
    primary_component,
    rendered,
  ) = _single_argument_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .FIRST,
  )

  assert primary_component is None
  assert rendered.startswith(
    "まず、$\\nu'$ を定める."
  )
  assert "そのために、次の完全列を考える." not in rendered


def test_phase143_44_pi8_5_detached_order_has_no_discourse_marker():
  (
    _argument,
    primary_component,
    rendered,
  ) = _single_argument_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    TodaGroupProofNarrativeArgumentDiscourseRole
    .DETACHED,
    occurrence=1,
  )

  assert primary_component is not None
  assert rendered.startswith(
    "$\\nu'$ の位数を決定する."
  )
  assert not rendered.startswith(
    "まず、"
  )
  assert not rendered.startswith(
    "次に、"
  )
  assert not rendered.startswith(
    "最後に、"
  )


@pytest.mark.parametrize(
  "n,k,role,discourse_role",
  (
    (
      3,
      3,
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE,
      TodaGroupProofNarrativeArgumentDiscourseRole
      .FINAL,
    ),
    (
      5,
      3,
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE,
      TodaGroupProofNarrativeArgumentDiscourseRole
      .FINAL,
    ),
    (
      8,
      7,
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE,
      TodaGroupProofNarrativeArgumentDiscourseRole
      .SINGLE,
    ),
    (
      9,
      7,
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE,
      TodaGroupProofNarrativeArgumentDiscourseRole
      .FINAL,
    ),
  ),
)
def test_phase143_44_four_targets_render_single_argument_safely(
  n,
  k,
  role,
  discourse_role,
):
  (
    _argument,
    _primary_component,
    rendered,
  ) = _single_argument_data(
    n,
    k,
    role,
    discourse_role,
  )

  assert isinstance(
    rendered,
    str,
  )
  assert rendered


def test_phase143_44_rejects_non_discourse_role():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  with pytest.raises(
    TypeError,
    match=(
      "discourse_role must be a "
      "TodaGroupProofNarrativeArgumentDiscourseRole"
    ),
  ):
    render_toda_group_proof_narrative_single_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
      0,
      "final",
      None,
    )
