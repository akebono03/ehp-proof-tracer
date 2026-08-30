from dataclasses import dataclass

from expression import (
  Expression,
)
from set_rules import (
  Coset,
)


@dataclass(frozen=True)
class CosetMembershipStatement:
  element: Expression
  coset: Coset



