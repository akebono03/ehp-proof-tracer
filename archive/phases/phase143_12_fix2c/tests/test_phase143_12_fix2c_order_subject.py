from expression import (
  Multiple,
)
from proof import (
  Relation,
  RelationType,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)

from test_phase143_12_purpose_subject import (
  _arguments,
)


def test_phase143_12_fix2c_pi6_3_order_subject_is_scalar_multiple_base():
  argument = next(
    argument
    for argument in _arguments(3, 3)
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    )
  )
  subject = extract_toda_group_proof_narrative_argument_purpose_subject(
    argument
  )
  assert subject is not None
  assert subject.name == "ν′"

  scalar_multiple_bases = []
  for block in argument.supporting_blocks:
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
    ):
      continue
    for step in block.steps:
      statement = step.conclusion
      if not isinstance(statement, Relation):
        continue
      if statement.relation_type is not RelationType.EQUALITY:
        continue
      for expression in (statement.lhs, statement.rhs):
        if isinstance(expression, Multiple):
          scalar_multiple_bases.append(expression.expression)

  assert subject in scalar_multiple_bases


def test_phase143_12_fix2c_pi8_5_order_subjects_remain_resolved():
  order_arguments = tuple(
    argument
    for argument in _arguments(5, 3)
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    )
  )
  subjects = tuple(
    extract_toda_group_proof_narrative_argument_purpose_subject(argument)
    for argument in order_arguments
  )
  assert len(subjects) == 2
  assert all(subject is not None for subject in subjects)
  assert subjects[0] != subjects[1]
