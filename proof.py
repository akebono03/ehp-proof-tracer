from dataclasses import dataclass
from enum import Enum
from typing import Any


class RelationType(Enum):
  EQUALITY = "equality"
  ZERO = "zero"
  ORDER = "order"


@dataclass(frozen=True)
class LiteratureReference:
  label: str
  author: str | None = None
  title: str | None = None
  year: int | None = None
  locator: str | None = None


@dataclass(frozen=True)
class Relation:
  lhs: Any
  rhs: Any
  relation_type: RelationType = RelationType.EQUALITY
  source: LiteratureReference | str | None = None
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
class InferenceRule:
  name: str
  description: str | None = None


@dataclass(frozen=True)
class ProofStep:
  conclusion: Any
  premises: tuple[Any, ...]
  rule: ProofRule
  note: str | None = None
  inference_rule: InferenceRule | None = None

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


def _normalize_proof_steps(
  steps,
  name,
):
  if isinstance(
    steps,
    ProofStep,
  ):
    return (
      steps,
    )

  if not isinstance(
    steps,
    (tuple, list),
  ):
    raise TypeError(
      f"{name} must be a ProofStep "
      "or a tuple/list of ProofStep"
    )

  normalized = tuple(
    steps
  )

  for step in normalized:
    if not isinstance(
      step,
      ProofStep,
    ):
      raise TypeError(
        f"{name} must contain "
        "only ProofStep objects"
      )

  return normalized


def _normalize_relations(
  relations,
):
  if isinstance(
    relations,
    Relation,
  ):
    return (
      relations,
    )

  if not isinstance(
    relations,
    (tuple, list),
  ):
    raise TypeError(
      "relations must be a Relation "
      "or a tuple/list of Relation"
    )

  normalized = tuple(
    relations
  )

  for relation in normalized:
    if not isinstance(
      relation,
      Relation,
    ):
      raise TypeError(
        "relations must contain "
        "only Relation objects"
      )

  return normalized


def _validate_inference_rule(
  inference_rule,
):
  if (
    inference_rule is not None
    and not isinstance(
      inference_rule,
      InferenceRule,
    )
  ):
    raise TypeError(
      "inference_rule must be "
      "an InferenceRule or None"
    )


def relation_inference_proof_step(
  conclusion,
  relation_steps,
  premises=(),
  note=None,
  inference_rule=None,
):
  normalized_relation_steps = (
    _normalize_proof_steps(
      relation_steps,
      "relation_steps",
    )
  )

  if not normalized_relation_steps:
    raise ValueError(
      "relation_steps must not be empty"
    )

  for relation_step in (
    normalized_relation_steps
  ):
    if (
      relation_step.rule
      != ProofRule.RELATION
    ):
      raise ValueError(
        "relation_steps must use "
        "ProofRule.RELATION"
      )

    if not isinstance(
      relation_step.conclusion,
      Relation,
    ):
      raise ValueError(
        "relation_steps must conclude "
        "Relation objects"
      )

  normalized_premises = (
    _normalize_proof_steps(
      premises,
      "premises",
    )
  )

  _validate_inference_rule(
    inference_rule
  )

  return ProofStep(
    conclusion=conclusion,
    premises=(
      normalized_relation_steps
      + normalized_premises
    ),
    rule=ProofRule.RELATION,
    note=note,
    inference_rule=inference_rule,
  )


def relation_inference_proof(
  relations,
  conclusion,
  premises=(),
  note=None,
  inference_rule=None,
):
  normalized_relations = (
    _normalize_relations(
      relations
    )
  )

  if not normalized_relations:
    raise ValueError(
      "relations must not be empty"
    )

  relation_steps = tuple(
    relation_proof_step(
      relation
    )
    for relation
    in normalized_relations
  )

  normalized_premises = (
    _normalize_proof_steps(
      premises,
      "premises",
    )
  )

  _validate_inference_rule(
    inference_rule
  )

  inference_step = (
    relation_inference_proof_step(
      conclusion,
      relation_steps,
      premises=normalized_premises,
      note=note,
      inference_rule=inference_rule,
    )
  )

  return Proof(
    conclusion=inference_step.conclusion,
    steps=[
      *relation_steps,
      *normalized_premises,
      inference_step,
    ],
  )













