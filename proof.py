from dataclasses import dataclass
from enum import Enum
from typing import Any


class RelationType(Enum):
  EQUALITY = "equality"
  ZERO = "zero"
  ORDER = "order"


@dataclass(frozen=True)
class Relation:
  lhs: Any
  rhs: Any
  relation_type: RelationType = RelationType.EQUALITY
  source: str | None = None
  note: str | None = None


class ProofRule(Enum):
  GIVEN = "given"
  RELATION = "relation"
  EHP_EXACTNESS = "ehp_exactness"
  KERNEL_COMPUTATION = "kernel_computation"
  IMAGE_COMPUTATION = "image_computation"
  COKERNEL_COMPUTATION = "cokernel_computation"


@dataclass(frozen=True)
class ProofStep:
  conclusion: Any
  premises: tuple[Any, ...]
  rule: ProofRule
  note: str | None = None


@dataclass
class Proof:
  conclusion: Any
  steps: list[ProofStep]


def relation_proof_step(relation):
  if not isinstance(relation, Relation):
    raise TypeError(
      "relation must be a Relation"
    )

  return ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )





