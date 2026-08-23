import pytest
from proof import (
  CokernelStatement,
  ExactnessStatement,
  ImageStatement,
  KernelStatement,
  Proof,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  cokernel_proof_step,
  exactness_proof_step,
  image_proof_step,
  kernel_proof_step,
  relation_proof_step,
)
from expression import Multiple, Zero, eta
from repository import RelationRepository
from algebra import (
  ExactSequenceStep,
  GroupMap,
)
from models import AbelianGroup, GroupComponent


def test_relation():
  relation = Relation(
    lhs="2η3",
    rhs="0",
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  assert relation.lhs == "2η3"
  assert relation.rhs == "0"
  assert relation.relation_type == RelationType.ZERO
  assert relation.source == "Toda"


def test_proof_step():
  relation = Relation(
    lhs="2η3",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  step = ProofStep(
    conclusion="η3 has order dividing 2",
    premises=(relation,),
    rule=ProofRule.RELATION,
  )

  assert step.conclusion == "η3 has order dividing 2"
  assert step.premises == (relation,)
  assert step.rule == ProofRule.RELATION


def test_proof():
  step1 = ProofStep(
    conclusion="ker(H) = <ν6η9²>",
    premises=(),
    rule=ProofRule.KERNEL_COMPUTATION,
  )

  step2 = ProofStep(
    conclusion="im(E) = ker(H)",
    premises=(step1,),
    rule=ProofRule.EHP_EXACTNESS,
  )

  proof = Proof(
    conclusion="desired result",
    steps=[step1, step2],
  )

  assert proof.conclusion == "desired result"
  assert proof.steps == [step1, step2]


def test_relation_with_expression():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert relation.lhs == Multiple(2, eta(3))
  assert relation.rhs == Zero()


def test_relation_proof_step():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  step = relation_proof_step(
    relation
  )

  assert step.conclusion == relation
  assert step.premises == ()
  assert step.rule == ProofRule.RELATION


def test_relation_proof_step_rejects_non_relation():
  with pytest.raises(TypeError):
    relation_proof_step(
      "2η3 = 0"
    )


def test_relation_repository_to_proof_step():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  repository = RelationRepository([
    relation,
  ])

  relations = repository.find_relations(
    lhs=Multiple(2, eta(3)),
  )

  step = relation_proof_step(
    relations[0]
  )

  assert step.conclusion == relation
  assert step.premises == ()
  assert step.rule == ProofRule.RELATION


def cyclic_group(order, generator):
  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=0,
        order=order,
        generator=generator,
        element=[1],
        gen_coe=[1],
      )
    ],
  )


def z4_to_z2_map():
  source = cyclic_group(
    4,
    "a",
  )

  target = cyclic_group(
    2,
    "b",
  )

  return GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )


def test_kernel_proof_step():
  group_map = z4_to_z2_map()

  step = kernel_proof_step(
    group_map
  )

  assert isinstance(
    step.conclusion,
    KernelStatement,
  )

  assert (
    step.conclusion.group_map
    is group_map
  )

  assert (
    step.conclusion.structure
    == group_map.kernel_structure()
  )

  assert step.premises == ()
  assert (
    step.rule
    == ProofRule.KERNEL_COMPUTATION
  )


def test_image_proof_step():
  group_map = z4_to_z2_map()

  step = image_proof_step(
    group_map
  )

  assert isinstance(
    step.conclusion,
    ImageStatement,
  )

  assert (
    step.conclusion.group_map
    is group_map
  )

  assert (
    step.conclusion.structure
    == group_map.image_structure()
  )

  assert step.premises == ()
  assert (
    step.rule
    == ProofRule.IMAGE_COMPUTATION
  )


def test_cokernel_proof_step():
  group_map = z4_to_z2_map()

  step = cokernel_proof_step(
    group_map
  )

  assert isinstance(
    step.conclusion,
    CokernelStatement,
  )

  assert (
    step.conclusion.group_map
    is group_map
  )

  assert (
    step.conclusion.structure
    == group_map.cokernel_structure()
  )

  assert step.premises == ()
  assert (
    step.rule
    == ProofRule.COKERNEL_COMPUTATION
  )


def test_group_map_calculation_proof_steps():
  group_map = z4_to_z2_map()

  kernel_step = kernel_proof_step(
    group_map
  )

  image_step = image_proof_step(
    group_map
  )

  cokernel_step = cokernel_proof_step(
    group_map
  )

  assert (
    kernel_step.conclusion.structure
    == group_map.kernel_structure()
  )

  assert (
    image_step.conclusion.structure
    == group_map.image_structure()
  )

  assert (
    cokernel_step.conclusion.structure
    == group_map.cokernel_structure()
  )


def exact_z2_z4_z2_maps():
  left = cyclic_group(
    2,
    "a",
  )

  middle = cyclic_group(
    4,
    "b",
  )

  right = cyclic_group(
    2,
    "c",
  )

  first_map = GroupMap(
    name="f",
    source=left,
    target=middle,
    matrix=[
      [2],
    ],
  )

  second_map = GroupMap(
    name="g",
    source=middle,
    target=right,
    matrix=[
      [1],
    ],
  )

  return first_map, second_map


def test_exactness_proof_step():
  first_map, second_map = (
    exact_z2_z4_z2_maps()
  )

  exact_step = ExactSequenceStep(
    first_map=first_map,
    second_map=second_map,
  )

  image_step = image_proof_step(
    first_map
  )

  kernel_step = kernel_proof_step(
    second_map
  )

  step = exactness_proof_step(
    exact_step,
    image_step,
    kernel_step,
  )

  assert isinstance(
    step.conclusion,
    ExactnessStatement,
  )

  assert (
    step.conclusion.first_map
    is first_map
  )

  assert (
    step.conclusion.second_map
    is second_map
  )

  assert step.conclusion.is_exact

  assert step.premises == (
    image_step,
    kernel_step,
  )

  assert (
    step.rule
    == ProofRule.EXACTNESS
  )


def test_nonexactness_proof_step():
  left = cyclic_group(
    2,
    "a",
  )

  middle = cyclic_group(
    4,
    "b",
  )

  right = cyclic_group(
    2,
    "c",
  )

  first_map = GroupMap(
    name="f",
    source=left,
    target=middle,
    matrix=[
      [0],
    ],
  )

  second_map = GroupMap(
    name="g",
    source=middle,
    target=right,
    matrix=[
      [1],
    ],
  )

  exact_step = ExactSequenceStep(
    first_map=first_map,
    second_map=second_map,
  )

  image_step = image_proof_step(
    first_map
  )

  kernel_step = kernel_proof_step(
    second_map
  )

  step = exactness_proof_step(
    exact_step,
    image_step,
    kernel_step,
  )

  assert not step.conclusion.is_exact


def test_exactness_proof_step_rejects_wrong_image():
  first_map, second_map = (
    exact_z2_z4_z2_maps()
  )

  other_map = z4_to_z2_map()

  exact_step = ExactSequenceStep(
    first_map=first_map,
    second_map=second_map,
  )

  image_step = image_proof_step(
    other_map
  )

  kernel_step = kernel_proof_step(
    second_map
  )

  with pytest.raises(ValueError):
    exactness_proof_step(
      exact_step,
      image_step,
      kernel_step,
    )


def test_exactness_proof():
  first_map, second_map = (
    exact_z2_z4_z2_maps()
  )

  exact_step = ExactSequenceStep(
    first_map=first_map,
    second_map=second_map,
  )

  image_step = image_proof_step(
    first_map
  )

  kernel_step = kernel_proof_step(
    second_map
  )

  exactness_step = exactness_proof_step(
    exact_step,
    image_step,
    kernel_step,
  )

  proof = Proof(
    conclusion=exactness_step.conclusion,
    steps=[
      image_step,
      kernel_step,
      exactness_step,
    ],
  )

  assert proof.conclusion.is_exact

  assert proof.steps == [
    image_step,
    kernel_step,
    exactness_step,
  ]












