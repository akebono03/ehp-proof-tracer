import pytest

from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
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
  occurrence=0,
):
  (
    _presentation,
    _blocks,
    _sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  matches = tuple(
    argument
    for argument in arguments
    if argument.role is role
  )

  return matches[
    occurrence
  ]


def test_phase143_55a_pi6_3_identifies_nu_prime_order_step():
  argument = _argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  assert isinstance(
    step,
    ProofStep,
  )
  assert isinstance(
    step.conclusion,
    Relation,
  )
  assert (
    step.conclusion.relation_type
    is RelationType.ORDER
  )
  assert (
    step
    in argument.conclusion_block.steps
  )

  other_order_steps = tuple(
    proof_step
    for proof_step in argument.conclusion_block.steps
    if (
      isinstance(
        proof_step.conclusion,
        Relation,
      )
      and proof_step.conclusion.relation_type
      is RelationType.ORDER
      and proof_step is not step
    )
  )

  assert other_order_steps
  assert all(
    proof_step.conclusion.lhs
    != step.conclusion.lhs
    for proof_step in other_order_steps
  )


def test_phase143_55a_pi8_5_identifies_nu5_order_step():
  argument = _argument(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  assert isinstance(
    step,
    ProofStep,
  )
  assert isinstance(
    step.conclusion,
    Relation,
  )
  assert (
    step.conclusion.relation_type
    is RelationType.ORDER
  )
  assert (
    step
    in argument.conclusion_block.steps
  )

  other_order_steps = tuple(
    proof_step
    for proof_step in argument.conclusion_block.steps
    if (
      isinstance(
        proof_step.conclusion,
        Relation,
      )
      and proof_step.conclusion.relation_type
      is RelationType.ORDER
      and proof_step is not step
    )
  )

  assert other_order_steps
  assert all(
    proof_step.conclusion.lhs
    != step.conclusion.lhs
    for proof_step in other_order_steps
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_55a_group_structure_identifies_target_equality(
  n,
  k,
):
  argument = _argument(
    n,
    k,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  assert isinstance(
    step,
    ProofStep,
  )
  assert isinstance(
    step.conclusion,
    Relation,
  )
  assert (
    step.conclusion.relation_type
    is RelationType.EQUALITY
  )
  assert (
    step
    in argument.conclusion_block.steps
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (9, 7),
  ),
)
def test_phase143_55a_definition_identifies_definition_step(
  n,
  k,
):
  argument = _argument(
    n,
    k,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  assert isinstance(
    step,
    ProofStep,
  )
  assert hasattr(
    step.conclusion,
    "element",
  )
  assert (
    step
    in argument.conclusion_block.steps
  )


def test_phase143_55a_returns_none_when_order_purpose_is_ambiguous():
  source = _argument(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  ambiguous = (
    TodaGroupProofNarrativeArgument(
      role=source.role,
      supporting_blocks=(),
      conclusion_block=source.conclusion_block,
      child_argument_indices=(),
    )
  )

  assert (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      ambiguous
    )
    is None
  )


def test_phase143_55a_rejects_non_argument():
  with pytest.raises(
    TypeError,
    match=(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    ),
  ):
    extract_toda_group_proof_narrative_argument_conclusion_step(
      "argument"
    )
