from typing import (
  get_type_hints,
)

from expression import (
  ScalarSum,
  ScalarSymbol,
  ScalarValue,
)
from proof import (
  ProofRule,
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)


def test_phase46_2_scalar_greater_equal_statement_uses_scalar_value():
  type_hints = get_type_hints(
    ScalarGreaterEqualStatement
  )

  assert type_hints[
    "left"
  ] == ScalarValue

  assert type_hints[
    "right"
  ] == ScalarValue


def test_phase46_2_n_greater_equal_k_plus_2_is_representable():
  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  statement = ScalarGreaterEqualStatement(
    left=n,
    right=ScalarSum(
      left=k,
      right=2,
    ),
  )

  assert statement.left == n

  assert statement.right == ScalarSum(
    left=k,
    right=2,
  )


def test_phase46_2_m_greater_equal_n_is_representable():
  m = ScalarSymbol(
    name="m",
  )

  n = ScalarSymbol(
    name="n",
  )

  statement = ScalarGreaterEqualStatement(
    left=m,
    right=n,
  )

  assert statement.left == m
  assert statement.right == n


def test_phase46_2_greater_equal_statement_has_structural_equality():
  first = ScalarGreaterEqualStatement(
    left=ScalarSymbol(
      name="n",
    ),
    right=ScalarSum(
      left=ScalarSymbol(
        name="k",
      ),
      right=2,
    ),
  )

  second = ScalarGreaterEqualStatement(
    left=ScalarSymbol(
      name="n",
    ),
    right=ScalarSum(
      left=ScalarSymbol(
        name="k",
      ),
      right=2,
    ),
  )

  assert first == second


def test_phase46_2_greater_equal_statement_distinguishes_right_side():
  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  first = ScalarGreaterEqualStatement(
    left=n,
    right=ScalarSum(
      left=k,
      right=2,
    ),
  )

  second = ScalarGreaterEqualStatement(
    left=n,
    right=ScalarSum(
      left=k,
      right=3,
    ),
  )

  assert first != second


def test_phase46_2_greater_equal_statement_distinguishes_direction():
  m = ScalarSymbol(
    name="m",
  )

  n = ScalarSymbol(
    name="n",
  )

  forward = ScalarGreaterEqualStatement(
    left=m,
    right=n,
  )

  reverse = ScalarGreaterEqualStatement(
    left=n,
    right=m,
  )

  assert forward != reverse


def test_phase46_2_greater_equal_statement_accepts_integer_values():
  statement = ScalarGreaterEqualStatement(
    left=5,
    right=3,
  )

  assert statement.left == 5
  assert statement.right == 3


def test_phase46_2_stable_range_premises_are_distinct_statements():
  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  m = ScalarSymbol(
    name="m",
  )

  stable_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=ScalarSum(
        left=k,
        right=2,
      ),
    )
  )

  suspension_range = (
    ScalarGreaterEqualStatement(
      left=m,
      right=n,
    )
  )

  assert (
    stable_range
    != suspension_range
  )


def test_phase46_2_stable_range_statements_can_be_given_proof_steps():
  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  m = ScalarSymbol(
    name="m",
  )

  first_statement = (
    ScalarGreaterEqualStatement(
      left=n,
      right=ScalarSum(
        left=k,
        right=2,
      ),
    )
  )

  second_statement = (
    ScalarGreaterEqualStatement(
      left=m,
      right=n,
    )
  )

  first_step = ProofStep(
    conclusion=first_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=second_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert first_step.conclusion == (
    first_statement
  )

  assert second_step.conclusion == (
    second_statement
  )

  assert first_step.rule == (
    ProofRule.GIVEN
  )

  assert second_step.rule == (
    ProofRule.GIVEN
  )


def test_phase46_2_greater_equal_statement_has_no_solver_semantics():
  statement = ScalarGreaterEqualStatement(
    left=5,
    right=3,
  )

  assert not hasattr(
    statement,
    "evaluate",
  )

  assert not hasattr(
    statement,
    "is_true",
  )

  assert not hasattr(
    statement,
    "solve",
  )


def test_phase46_2_greater_equal_statement_has_no_toda_semantics():
  statement = ScalarGreaterEqualStatement(
    left=ScalarSymbol(
      name="m",
    ),
    right=ScalarSymbol(
      name="n",
    ),
  )

  assert not hasattr(
    statement,
    "toda_4_5",
  )

  assert not hasattr(
    statement,
    "theorem",
  )

  assert not hasattr(
    statement,
    "isomorphism",
  )
