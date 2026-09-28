from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)

from test_phase143_12_purpose_subject import (
  _arguments,
)


def test_phase143_12_fix2_pi6_3_order_subject_uses_local_calculation():
  argument = next(
    argument
    for argument in _arguments(
      3,
      3,
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    )
  )

  subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )

  assert subject is not None
  assert subject.name == "ν′"


def test_phase143_12_fix2_pi8_5_order_subjects_are_unambiguous():
  order_arguments = tuple(
    argument
    for argument in _arguments(
      5,
      3,
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    )
  )

  subjects = tuple(
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
    for argument in order_arguments
  )

  assert len(
    subjects
  ) == 2
  assert all(
    subject is not None
    for subject in subjects
  )
  assert subjects[
    0
  ] != subjects[
    1
  ]
