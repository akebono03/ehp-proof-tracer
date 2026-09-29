import pytest

from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)

from test_phase143_12_purpose_subject import (
  _arguments,
)


def _argument(
  n: int,
  k: int,
  role: TodaGroupProofNarrativeArgumentRole,
  occurrence: int = 0,
):
  matches = tuple(
    argument
    for argument in _arguments(
      n,
      k,
    )
    if argument.role is role
  )

  return matches[
    occurrence
  ]


def test_phase143_13_pi6_3_definition_purpose_sentence():
  argument = _argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION,
  )

  assert (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
    == "$\\nu'$ を定める."
  )


def test_phase143_13_pi6_3_order_purpose_sentence():
  argument = _argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER,
  )

  assert (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
    == "$\\nu'$ の位数を決定する."
  )


def test_phase143_13_pi6_3_group_structure_purpose_sentence():
  argument = _argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE,
  )

  assert (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
    == "$\\pi_{6}^{3}$ の群構造を決定する."
  )


def test_phase143_13_pi8_5_order_arguments_have_distinct_purpose_sentences():
  first = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER,
    occurrence=0,
  )
  second = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER,
    occurrence=1,
  )

  first_sentence = (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      first
    )
  )
  second_sentence = (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      second
    )
  )

  assert first_sentence is not None
  assert second_sentence is not None
  assert first_sentence != second_sentence
  assert "位数を決定する." in first_sentence
  assert "位数を決定する." in second_sentence


def test_phase143_13_pi16_9_definition_purpose_sentence():
  argument = _argument(
    9,
    7,
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION,
  )

  sentence = (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
  )

  assert sentence is not None
  assert "\\sigma" in sentence
  assert "を定める." in sentence


def test_phase143_13_rejects_non_argument():
  with pytest.raises(
    TypeError,
    match="argument must be a TodaGroupProofNarrativeArgument",
  ):
    render_toda_group_proof_narrative_argument_purpose_sentence(
      object()
    )
