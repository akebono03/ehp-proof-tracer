import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _argument(
  n,
  k,
  role,
):
  (
    _,
    _,
    _,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  argument = next(
    argument
    for argument in arguments
    if argument.role is role
  )

  return (
    argument,
    arguments,
  )


def test_phase143_61a_pi8_5_order_extracts_double_and_e2_order():
  (
    argument,
    arguments,
  ) = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )

  assert len(
    conclusion_step.premises
  ) == 3
  assert len(
    premises
  ) == 2
  assert premises == (
    conclusion_step.premises[
      0
    ],
    conclusion_step.premises[
      1
    ],
  )


def test_phase143_61a_pi8_5_order_excludes_definition_child_premise():
  (
    argument,
    arguments,
  ) = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )

  assert conclusion_step.premises[
    2
  ] not in premises

  definition_argument = arguments[
    argument.child_argument_indices[
      0
    ]
  ]

  assert (
    definition_argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  )
  assert (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      definition_argument
    )
    is conclusion_step.premises[
      2
    ]
  )


def test_phase143_61a_pi6_3_order_keeps_two_direct_derivation_premises():
  (
    argument,
    arguments,
  ) = _argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )

  assert len(
    conclusion_step.premises
  ) == 2
  assert premises == conclusion_step.premises


def test_phase143_61a_uses_direct_premises_without_expanding_ancestry():
  (
    argument,
    arguments,
  ) = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )

  premise_ids = {
    id(
      premise
    )
    for premise in premises
  }

  assert all(
    ancestor is not premise
    for premise in premises
    for ancestor in premise.premises
  )
  assert all(
    id(
      ancestor
    ) not in premise_ids
    for premise in premises
    for ancestor in premise.premises
  )


def test_phase143_61a_group_structure_extractor_is_safe():
  (
    argument,
    arguments,
  ) = _argument(
    8,
    7,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )

  assert isinstance(
    premises,
    tuple,
  )
  assert all(
    isinstance(
      premise,
      ProofStep,
    )
    for premise in premises
  )


def test_phase143_61a_rejects_non_argument():
  (
    _,
    arguments,
  ) = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  with pytest.raises(
    TypeError,
    match="argument must be a",
  ):
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      object(),
      arguments,
    )


def test_phase143_61a_rejects_non_tuple_arguments():
  (
    argument,
    arguments,
  ) = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  with pytest.raises(
    TypeError,
    match="arguments must be a tuple",
  ):
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      list(
        arguments
      ),
    )


def test_phase143_61a_rejects_invalid_argument_entry():
  (
    argument,
    arguments,
  ) = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  with pytest.raises(
    TypeError,
    match="arguments must contain only",
  ):
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments
      + (
        object(),
      ),
    )
