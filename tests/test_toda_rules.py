from expression import (
  TodaBracket,
  eta,
  nu,
  sigma,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def test_toda_bracket_membership_statement():
  x = eta(3)

  bracket = TodaBracket(
    first=nu(4),
    second=sigma(8),
    third=eta(9),
  )

  statement = TodaBracketMembershipStatement(
    element=x,
    bracket=bracket,
  )

  assert statement.element == x
  assert statement.bracket == bracket


def test_toda_bracket_membership_statement_has_structural_equality():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  first = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  second = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  assert first == second


def test_toda_bracket_membership_statement_distinguishes_element():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  first = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  second = TodaBracketMembershipStatement(
    element=nu(9),
    bracket=bracket,
  )

  assert first != second


def test_toda_bracket_membership_statement_distinguishes_bracket():
  element = eta(9)

  first = TodaBracketMembershipStatement(
    element=element,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  second = TodaBracketMembershipStatement(
    element=element,
    bracket=TodaBracket(
      first=eta(3),
      second=sigma(8),
      third=nu(4),
    ),
  )

  assert first != second





