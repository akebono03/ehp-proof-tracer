from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)

from test_phase143_12_purpose_subject import (
  _arguments,
)


def test_phase143_12_fix2b_pi6_3_order_subject_uses_local_calculation():
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


