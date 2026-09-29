import pytest

from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
  render_toda_group_proof_narrative_argument_discourse_marker,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)

from test_phase143_12_purpose_subject import (
  _arguments,
)


def test_phase143_17_pi6_3_discourse_roles():
  roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      _arguments(
        3,
        3,
      )
    )
  )

  assert roles == (
    TodaGroupProofNarrativeArgumentDiscourseRole.FIRST,
    TodaGroupProofNarrativeArgumentDiscourseRole.MIDDLE,
    TodaGroupProofNarrativeArgumentDiscourseRole.FINAL,
  )


def test_phase143_17_pi8_5_detached_order_is_marked_detached():
  roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      _arguments(
        5,
        3,
      )
    )
  )

  assert roles == (
    TodaGroupProofNarrativeArgumentDiscourseRole.FIRST,
    TodaGroupProofNarrativeArgumentDiscourseRole.MIDDLE,
    TodaGroupProofNarrativeArgumentDiscourseRole.FINAL,
    TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED,
  )


def test_phase143_17_pi15_8_single_argument_is_single():
  roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      _arguments(
        8,
        7,
      )
    )
  )

  assert roles == (
    TodaGroupProofNarrativeArgumentDiscourseRole.SINGLE,
  )


def test_phase143_17_pi16_9_discourse_roles():
  roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      _arguments(
        9,
        7,
      )
    )
  )

  assert roles == (
    TodaGroupProofNarrativeArgumentDiscourseRole.FIRST,
    TodaGroupProofNarrativeArgumentDiscourseRole.FINAL,
  )


@pytest.mark.parametrize(
  "role,expected",
  (
    (
      TodaGroupProofNarrativeArgumentDiscourseRole.SINGLE,
      "",
    ),
    (
      TodaGroupProofNarrativeArgumentDiscourseRole.FIRST,
      "まず、",
    ),
    (
      TodaGroupProofNarrativeArgumentDiscourseRole.MIDDLE,
      "次に、",
    ),
    (
      TodaGroupProofNarrativeArgumentDiscourseRole.FINAL,
      "最後に、",
    ),
    (
      TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED,
      "",
    ),
  ),
)
def test_phase143_17_discourse_marker_mapping(
  role,
  expected,
):
  assert (
    render_toda_group_proof_narrative_argument_discourse_marker(
      role
    )
    == expected
  )


def test_phase143_17_empty_arguments_have_no_roles():
  assert (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      ()
    )
    == ()
  )


def test_phase143_17_rejects_non_tuple_arguments():
  with pytest.raises(
    TypeError,
    match="arguments must be a tuple",
  ):
    classify_toda_group_proof_narrative_argument_discourse_roles(
      []
    )


def test_phase143_17_rejects_non_discourse_role():
  with pytest.raises(
    TypeError,
    match=(
      "role must be a "
      "TodaGroupProofNarrativeArgumentDiscourseRole"
    ),
  ):
    render_toda_group_proof_narrative_argument_discourse_marker(
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    )
