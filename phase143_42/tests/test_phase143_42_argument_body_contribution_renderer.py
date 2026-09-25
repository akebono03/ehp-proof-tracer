import pytest

from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
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


def _argument_body_data(
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
  primary_component = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )
  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  return (
    presentation,
    blocks,
    argument,
    local_body_blocks,
    primary_component,
  )


def test_phase143_42_pi6_3_group_suppresses_primary_exactness_windows():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is not None

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  assert (
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \text{ is exact}"
    not in rendered
  )
  assert (
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \text{ is exact}"
    not in rendered
  )
  assert (
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5} \text{ is exact}"
    not in rendered
  )


def test_phase143_42_pi6_3_group_keeps_derived_short_exact_sequence():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  assert (
    "この完全性と両端の写像の性質より, "
    "次の短完全列を得る."
    in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


def test_phase143_42_pi6_3_primary_short_exact_has_no_orphan_exactness_lead():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  assert (
    "次の完全列を考える.\n\n"
    "この完全性と両端の写像の性質より"
    not in rendered
  )


def test_phase143_42_pi8_5_group_without_primary_keeps_exactness_window():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is None

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  assert (
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5} \text{ is exact}"
    in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


def test_phase143_42_pi8_5_detached_order_suppresses_window_but_keeps_short_exact():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    occurrence=1,
  )

  assert primary_component is not None

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  assert (
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5} \text{ is exact}"
    not in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_42_four_targets_render_argument_bodies_safely(
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

  for argument_index, argument in enumerate(
    arguments
  ):
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
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    rendered = (
      render_toda_group_proof_narrative_argument_body_markdown(
        presentation,
        blocks,
        local_body_blocks,
        primary_component,
      )
    )

    assert isinstance(
      rendered,
      str,
    )
    assert rendered


def test_phase143_42_rejects_non_tuple_local_body_blocks():
  (
    presentation,
    blocks,
    _argument,
    local_body_blocks,
    primary_component,
  ) = _argument_body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  with pytest.raises(
    TypeError,
    match="local_body_blocks must be a tuple",
  ):
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      list(
        local_body_blocks
      ),
      primary_component,
    )
