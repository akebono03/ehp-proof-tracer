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


@dataclass(frozen=True)
class KernelStatement:
  group_map: Any
  structure: Any


@dataclass(frozen=True)
class ImageStatement:
  group_map: Any
  structure: Any


@dataclass(frozen=True)
class CokernelStatement:
  group_map: Any
  structure: Any


def kernel_proof_step(group_map):
  statement = KernelStatement(
    group_map=group_map,
    structure=group_map.kernel_structure(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.KERNEL_COMPUTATION,
  )


def image_proof_step(group_map):
  statement = ImageStatement(
    group_map=group_map,
    structure=group_map.image_structure(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.IMAGE_COMPUTATION,
  )


def cokernel_proof_step(group_map):
  statement = CokernelStatement(
    group_map=group_map,
    structure=group_map.cokernel_structure(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.COKERNEL_COMPUTATION,
  )










