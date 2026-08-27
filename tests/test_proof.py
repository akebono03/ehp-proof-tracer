import pytest
from proof import (
  CokernelStatement,
  ExactnessStatement,
  ImageStatement,
  InferenceRule,
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
  order_relation,
  relation_proof_step,
  ehp_exactness_proof,
  ehp_exactness_proof_step,
  ehp_hopf_target_proof,
  ehp_sphere_proof,
  relation_inference_proof,
  relation_inference_proof_step,
  LiteratureReference,
)
from expression import (
  Composition,
  Multiple,
  Zero,
  eta,
  nu,
)
from algebra import (
  ExactSequenceStep,
  GroupMap,
)
from models import AbelianGroup, GroupComponent
from pathlib import Path
from ehp import EHPSegment
from repository import (
  RelationRepository,
  SphereRepository,
)



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


def test_composition_equality_relation_representation():
  composition = Composition(
    left=nu(4),
    right=eta(3),
  )

  relation = Relation(
    lhs=composition,
    rhs=eta(4),
    relation_type=RelationType.EQUALITY,
    source="Toda",
    note="known composition equality",
  )

  assert relation.lhs == Composition(
    left=nu(4),
    right=eta(3),
  )

  assert relation.rhs == eta(4)

  assert (
    relation.relation_type
    == RelationType.EQUALITY
  )

  assert relation.source == "Toda"

  assert (
    relation.note
    == "known composition equality"
  )


def test_order_relation_represents_exact_element_order():
  relation = order_relation(
    eta(3),
    2,
  )

  assert relation == Relation(
    lhs=eta(3),
    rhs=2,
    relation_type=RelationType.ORDER,
  )

  assert relation.lhs == eta(3)
  assert relation.rhs == 2
  assert (
    relation.relation_type
    == RelationType.ORDER
  )


def test_order_relation_preserves_source_and_note():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
  )

  relation = order_relation(
    eta(3),
    2,
    source=reference,
    note="exact order",
  )

  assert relation.source == reference
  assert relation.note == "exact order"


@pytest.mark.parametrize(
  "invalid_order",
  (
    0,
    -1,
  ),
)
def test_order_relation_rejects_nonpositive_order(
  invalid_order,
):
  with pytest.raises(
    ValueError
  ):
    order_relation(
      eta(3),
      invalid_order,
    )


@pytest.mark.parametrize(
  "invalid_order",
  (
    True,
    2.0,
    "2",
  ),
)
def test_order_relation_rejects_noninteger_order(
  invalid_order,
):
  with pytest.raises(
    TypeError
  ):
    order_relation(
      eta(3),
      invalid_order,
    )


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


BASE_DIR = Path(__file__).resolve().parent.parent


def make_sphere_repository():
  return SphereRepository(
    BASE_DIR / "data" / "sphere.csv"
  )


def test_ehp_exactness_proof_step():
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

  step = ehp_exactness_proof_step(
    exact_step,
    image_step,
    kernel_step,
  )

  assert isinstance(
    step.conclusion,
    ExactnessStatement,
  )

  assert step.conclusion.is_exact

  assert step.premises == (
    image_step,
    kernel_step,
  )

  assert (
    step.rule
    == ProofRule.EHP_EXACTNESS
  )


def test_ehp_exactness_proof():
  first_map, second_map = (
    exact_z2_z4_z2_maps()
  )

  exact_step = ExactSequenceStep(
    first_map=first_map,
    second_map=second_map,
  )

  proof = ehp_exactness_proof(
    exact_step
  )

  assert len(proof.steps) == 3

  image_step = proof.steps[0]
  kernel_step = proof.steps[1]
  exactness_step = proof.steps[2]

  assert (
    image_step.rule
    == ProofRule.IMAGE_COMPUTATION
  )

  assert (
    kernel_step.rule
    == ProofRule.KERNEL_COMPUTATION
  )

  assert (
    exactness_step.rule
    == ProofRule.EHP_EXACTNESS
  )

  assert (
    proof.conclusion
    == exactness_step.conclusion
  )


def test_ehp_sphere_proof_from_segment():
  repo = make_sphere_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  proof = ehp_sphere_proof(
    segment
  )

  assert len(proof.steps) == 3

  image_step = proof.steps[0]
  kernel_step = proof.steps[1]
  exactness_step = proof.steps[2]

  assert (
    image_step.conclusion.group_map
    is segment.E
  )

  assert (
    kernel_step.conclusion.group_map
    is segment.H
  )

  assert (
    exactness_step.conclusion.first_map
    is segment.E
  )

  assert (
    exactness_step.conclusion.second_map
    is segment.H
  )

  assert (
    exactness_step.conclusion.is_exact
  )

  assert (
    exactness_step.rule
    == ProofRule.EHP_EXACTNESS
  )

  assert (
    proof.conclusion
    == exactness_step.conclusion
  )


def test_ehp_hopf_target_proof_from_segment():
  repo = make_sphere_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  proof = ehp_hopf_target_proof(
    segment
  )

  assert len(proof.steps) == 3

  image_step = proof.steps[0]
  kernel_step = proof.steps[1]
  exactness_step = proof.steps[2]

  assert (
    image_step.conclusion.group_map
    is segment.H
  )

  assert (
    kernel_step.conclusion.group_map
    is segment.P
  )

  assert (
    exactness_step.conclusion.first_map
    is segment.H
  )

  assert (
    exactness_step.conclusion.second_map
    is segment.P
  )

  assert (
    exactness_step.conclusion.is_exact
  )

  assert (
    exactness_step.rule
    == ProofRule.EHP_EXACTNESS
  )


def test_relation_inference_proof_step():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  relation_step = relation_proof_step(
    relation
  )

  step = relation_inference_proof_step(
    "η_3 has order dividing 2",
    relation_step,
  )

  assert (
    step.conclusion
    == "η_3 has order dividing 2"
  )

  assert step.premises == (
    relation_step,
  )

  assert (
    step.rule
    == ProofRule.RELATION
  )


def test_relation_inference_proof_step_rejects_non_relation_step():
  step = ProofStep(
    conclusion="something",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(ValueError):
    relation_inference_proof_step(
      "result",
      step,
    )


def test_relation_inference_proof():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  proof = relation_inference_proof(
    relation,
    "η_3 has order dividing 2",
  )

  assert len(proof.steps) == 2

  relation_step = proof.steps[0]
  inference_step = proof.steps[1]

  assert (
    relation_step.conclusion
    == relation
  )

  assert (
    inference_step.premises
    == (
      relation_step,
    )
  )

  assert (
    proof.conclusion
    == "η_3 has order dividing 2"
  )


def test_literature_reference():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Proposition X",
  )

  assert (
    reference.label
    == "Toda"
  )

  assert (
    reference.author
    == "H. Toda"
  )

  assert (
    reference.title
    == (
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    )
  )

  assert (
    reference.year
    == 1962
  )

  assert (
    reference.locator
    == "Proposition X"
  )


def test_relation_with_literature_reference():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
  )

  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source=reference,
  )

  assert (
    relation.source
    == reference
  )


def test_relation_inference_proof_step_multiple_relations():
  relation1 = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  relation2 = Relation(
    lhs=Multiple(
      2,
      eta(4),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  step1 = relation_proof_step(
    relation1
  )

  step2 = relation_proof_step(
    relation2
  )

  step = relation_inference_proof_step(
    "combined result",
    (
      step1,
      step2,
    ),
  )

  assert (
    step.conclusion
    == "combined result"
  )

  assert step.premises == (
    step1,
    step2,
  )

  assert (
    step.rule
    == ProofRule.RELATION
  )


def test_relation_inference_proof_step_with_additional_premise():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  relation_step = (
    relation_proof_step(
      relation
    )
  )

  additional_step = ProofStep(
    conclusion="additional fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  step = relation_inference_proof_step(
    "combined result",
    relation_step,
    premises=(
      additional_step,
    ),
  )

  assert step.premises == (
    relation_step,
    additional_step,
  )


def test_relation_inference_proof_multiple_relations():
  relation1 = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  relation2 = Relation(
    lhs=Multiple(
      2,
      eta(4),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  proof = relation_inference_proof(
    (
      relation1,
      relation2,
    ),
    "combined result",
  )

  assert len(
    proof.steps
  ) == 3

  relation_step1 = (
    proof.steps[0]
  )

  relation_step2 = (
    proof.steps[1]
  )

  inference_step = (
    proof.steps[2]
  )

  assert (
    relation_step1.conclusion
    == relation1
  )

  assert (
    relation_step2.conclusion
    == relation2
  )

  assert (
    inference_step.premises
    == (
      relation_step1,
      relation_step2,
    )
  )

  assert (
    proof.conclusion
    == "combined result"
  )


def test_relation_inference_proof_with_additional_premise():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  additional_step = ProofStep(
    conclusion="additional fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  proof = relation_inference_proof(
    relation,
    "combined result",
    premises=(
      additional_step,
    ),
  )

  assert len(
    proof.steps
  ) == 3

  relation_step = (
    proof.steps[0]
  )

  assert (
    proof.steps[1]
    == additional_step
  )

  inference_step = (
    proof.steps[2]
  )

  assert (
    inference_step.premises
    == (
      relation_step,
      additional_step,
    )
  )


def test_relation_inference_proof_step_rejects_empty_relations():
  with pytest.raises(
    ValueError
  ):
    relation_inference_proof_step(
      "result",
      (),
    )


def test_relation_inference_proof_rejects_empty_relations():
  with pytest.raises(
    ValueError
  ):
    relation_inference_proof(
      (),
      "result",
    )


def test_relation_inference_proof_step_rejects_invalid_additional_premise():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  relation_step = (
    relation_proof_step(
      relation
    )
  )

  with pytest.raises(
    TypeError
  ):
    relation_inference_proof_step(
      "result",
      relation_step,
      premises=(
        "not a ProofStep",
      ),
    )


def test_inference_rule():
  rule = InferenceRule(
    name=(
      "zero relation implies "
      "order bound"
    ),
    description=(
      "If m alpha = 0, "
      "the order of alpha divides m."
    ),
  )

  assert (
    rule.name
    == (
      "zero relation implies "
      "order bound"
    )
  )

  assert (
    rule.description
    == (
      "If m alpha = 0, "
      "the order of alpha divides m."
    )
  )


def test_relation_inference_proof_step_with_inference_rule():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  relation_step = (
    relation_proof_step(
      relation
    )
  )

  rule = InferenceRule(
    name=(
      "zero relation implies "
      "order bound"
    ),
  )

  step = relation_inference_proof_step(
    "η_3 has order dividing 2",
    relation_step,
    inference_rule=rule,
  )

  assert (
    step.inference_rule
    == rule
  )

  assert (
    step.premises
    == (
      relation_step,
    )
  )


def test_relation_inference_proof_with_inference_rule():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  rule = InferenceRule(
    name=(
      "zero relation implies "
      "order bound"
    ),
  )

  proof = relation_inference_proof(
    relation,
    "η_3 has order dividing 2",
    inference_rule=rule,
  )

  inference_step = (
    proof.steps[-1]
  )

  assert (
    inference_step.inference_rule
    == rule
  )

  assert (
    proof.conclusion
    == "η_3 has order dividing 2"
  )


def test_relation_inference_without_inference_rule_is_backward_compatible():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  proof = relation_inference_proof(
    relation,
    "η_3 has order dividing 2",
  )

  inference_step = (
    proof.steps[-1]
  )

  assert (
    inference_step.inference_rule
    is None
  )


def test_relation_inference_rejects_invalid_inference_rule():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  with pytest.raises(
    TypeError
  ):
    relation_inference_proof(
      relation,
      "η_3 has order dividing 2",
      inference_rule=(
        "not an InferenceRule"
      ),
    )


def test_multiple_relation_inference_with_inference_rule():
  relation1 = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  relation2 = Relation(
    lhs=Multiple(
      2,
      eta(4),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  rule = InferenceRule(
    name="combined relation rule",
  )

  proof = relation_inference_proof(
    (
      relation1,
      relation2,
    ),
    "combined result",
    inference_rule=rule,
  )

  inference_step = (
    proof.steps[-1]
  )

  assert (
    inference_step.inference_rule
    == rule
  )

  assert (
    inference_step.premises
    == (
      proof.steps[0],
      proof.steps[1],
    )
  )


















