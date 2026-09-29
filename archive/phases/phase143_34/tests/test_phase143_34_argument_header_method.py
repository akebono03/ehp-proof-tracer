import pytest

from toda_group_proof_narrative_argument_discourse import (
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_header_method_section,
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


def _ordered_sections(
  n,
  k,
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
  ordered = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )
  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }

  sections = []

  for argument, discourse_role in zip(
    ordered,
    discourse_roles,
  ):
    argument_index = source_index_by_identity[
      id(
        argument
      )
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

    sections.append(
      (
        argument,
        render_toda_group_proof_narrative_argument_header_method_section(
          argument,
          discourse_role,
          primary_component,
        ),
      )
    )

  return tuple(
    sections
  )


def test_phase143_34_pi6_3_definition_header_has_first_marker_without_method():
  sections = _ordered_sections(
    3,
    3,
  )

  argument, rendered = sections[
    0
  ]

  assert (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  )
  assert rendered == (
    "まず、$\\nu'$ を定める."
  )


def test_phase143_34_pi6_3_order_header_and_method_section():
  sections = _ordered_sections(
    3,
    3,
  )

  argument, rendered = sections[
    1
  ]

  assert (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER
  )
  assert rendered == (
    "次に、$\\nu'$ の位数を決定する."
    "そのために、次の完全列を考える."
    "\n\n"
    "$\\pi_{7}^{3} \\xrightarrow{H} "
    "\\pi_{7}^{5} \\xrightarrow{\\Delta} "
    "\\pi_{5}^{2} \\xrightarrow{E} "
    "\\pi_{6}^{3}$"
  )


def test_phase143_34_pi6_3_group_structure_header_and_method_section():
  sections = _ordered_sections(
    3,
    3,
  )

  argument, rendered = sections[
    2
  ]

  assert (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE
  )
  assert rendered == (
    "最後に、$\\pi_{6}^{3}$ の群構造を決定する."
    "そのために、次の完全列を考える."
    "\n\n"
    "$\\pi_{7}^{3} \\xrightarrow{H} "
    "\\pi_{7}^{5} \\xrightarrow{\\Delta} "
    "\\pi_{5}^{2} \\xrightarrow{E} "
    "\\pi_{6}^{3} \\xrightarrow{H} "
    "\\pi_{6}^{5}$"
  )


def test_phase143_34_pi8_5_detached_order_has_no_discourse_marker():
  sections = _ordered_sections(
    5,
    3,
  )

  argument, rendered = sections[
    3
  ]

  assert (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER
  )
  assert rendered.startswith(
    "$\\nu'$ の位数を決定する."
  )
  assert "まず、" not in rendered
  assert "次に、" not in rendered
  assert "最後に、" not in rendered
  assert (
    "そのために、次の完全列を考える."
    in rendered
  )


def test_phase143_34_pi15_8_single_has_no_discourse_marker_or_method():
  sections = _ordered_sections(
    8,
    7,
  )

  assert len(
    sections
  ) == 1

  _argument, rendered = sections[
    0
  ]

  assert rendered == (
    "$\\pi_{15}^{8}$ の群構造を決定する."
  )


def test_phase143_34_pi16_9_definition_has_first_marker_without_method():
  sections = _ordered_sections(
    9,
    7,
  )

  _argument, rendered = sections[
    0
  ]

  assert rendered.startswith(
    "まず、$\\sigma"
  )
  assert "を定める." in rendered
  assert "完全列を考える" not in rendered


def test_phase143_34_rejects_non_argument():
  sections = _ordered_sections(
    8,
    7,
  )
  argument, _rendered = sections[
    0
  ]

  from toda_group_proof_narrative_argument_discourse import (
    TodaGroupProofNarrativeArgumentDiscourseRole,
  )

  with pytest.raises(
    TypeError,
    match=(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    ),
  ):
    render_toda_group_proof_narrative_argument_header_method_section(
      object(),
      TodaGroupProofNarrativeArgumentDiscourseRole.SINGLE,
      None,
    )

  assert argument is not None
