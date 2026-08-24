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
  EXACTNESS = "exactness"
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


@dataclass(frozen=True)
class ExactnessStatement:
  first_map: Any
  second_map: Any
  is_exact: bool


def exactness_proof_step(
  exact_step,
  image_step,
  kernel_step,
):
  if not isinstance(
    image_step.conclusion,
    ImageStatement,
  ):
    raise TypeError(
      "image_step must conclude "
      "an ImageStatement"
    )

  if not isinstance(
    kernel_step.conclusion,
    KernelStatement,
  ):
    raise TypeError(
      "kernel_step must conclude "
      "a KernelStatement"
    )

  if (
    image_step.conclusion.group_map
    is not exact_step.first_map
  ):
    raise ValueError(
      "image_step must refer to first_map"
    )

  if (
    kernel_step.conclusion.group_map
    is not exact_step.second_map
  ):
    raise ValueError(
      "kernel_step must refer to second_map"
    )

  statement = ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=exact_step.is_exact(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(
      image_step,
      kernel_step,
    ),
    rule=ProofRule.EXACTNESS,
  )


def ehp_exactness_proof_step(
  exact_step,
  image_step,
  kernel_step,
):
  exactness_step = exactness_proof_step(
    exact_step,
    image_step,
    kernel_step,
  )

  return ProofStep(
    conclusion=exactness_step.conclusion,
    premises=exactness_step.premises,
    rule=ProofRule.EHP_EXACTNESS,
  )


def ehp_exactness_proof(exact_step):
  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  exactness_step = (
    ehp_exactness_proof_step(
      exact_step,
      image_step,
      kernel_step,
    )
  )

  return Proof(
    conclusion=exactness_step.conclusion,
    steps=[
      image_step,
      kernel_step,
      exactness_step,
    ],
  )


def ehp_sphere_proof(segment):
  return ehp_exactness_proof(
    segment.exact_step_at_sphere()
  )


def ehp_hopf_target_proof(segment):
  return ehp_exactness_proof(
    segment.exact_step_at_hopf_target()
  )


def relation_inference_proof_step(
  conclusion,
  relation_step,
  note=None,
):
  if not isinstance(
    relation_step,
    ProofStep,
  ):
    raise TypeError(
      "relation_step must be a ProofStep"
    )

  if (
    relation_step.rule
    != ProofRule.RELATION
  ):
    raise ValueError(
      "relation_step must use "
      "ProofRule.RELATION"
    )

  if not isinstance(
    relation_step.conclusion,
    Relation,
  ):
    raise ValueError(
      "relation_step must conclude "
      "a Relation"
    )

  return ProofStep(
    conclusion=conclusion,
    premises=(
      relation_step,
    ),
    rule=ProofRule.RELATION,
    note=note,
  )


def relation_inference_proof(
  relation,
  conclusion,
  note=None,
):
  relation_step = relation_proof_step(
    relation
  )

  inference_step = (
    relation_inference_proof_step(
      conclusion,
      relation_step,
      note=note,
    )
  )

  return Proof(
    conclusion=inference_step.conclusion,
    steps=[
      relation_step,
      inference_step,
    ],
  )















