from dataclasses import dataclass

from algebra import Subgroup
from expression import Expression


@dataclass(frozen=True)
class MembershipStatement:
  element: Expression
  subgroup: Subgroup



