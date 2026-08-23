from algebra import (
  ExactSequenceStep,
  ExtensionCandidate,
  GroupElement,
  GroupMap,
  InducedMap,
  QuotientGroup,
  Subgroup,
  all_subgroups,
  generated_subgroup_elements,
  group_structure,
  valid_extension_candidates,
  abstract_abelian_group,
  extension_candidates,
  finite_abelian_structures,
  finite_group_order,
  abelian_group_structure,
  relation_matrix,
  structure_from_presentation,
)
from models import AbelianGroup, GroupComponent
import pytest
from math import inf
from sympy import Matrix
from itertools import product

def make_cyclic_group(order, generator):
  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=0,
        order=order,
        generator=generator,
        element=[],
        gen_coe=[],
      )
    ],
  )

def make_subgroup(
  group,
  generators,
):
  generators = tuple(
    GroupElement(group, coefficients)
    for coefficients in generators
  )

  elements = generated_subgroup_elements(
    group,
    generators,
  )

  return Subgroup(
    ambient_group=group,
    elements=elements,
    generators=generators,
  )

def test_apply():
  source = make_cyclic_group(6, "a")
  target = make_cyclic_group(6, "b")

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[[2]],
  )

  x = GroupElement(
    source,
    (2,),
  )

  y = f.apply(x)

  assert y.coefficients == (4,)


def test_kernel():
  source = make_cyclic_group(6, "a")
  target = make_cyclic_group(6, "b")

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[[2]],
  )

  kernel = {
    x.coefficients
    for x in f.kernel()
  }

  assert kernel == {
    (0,),
    (3,),
  }


def test_image():
  source = make_cyclic_group(6, "a")
  target = make_cyclic_group(6, "b")

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[[2]],
  )

  image = {
    x.coefficients
    for x in f.image()
  }

  assert image == {
    (0,),
    (2,),
    (4,),
  }


def test_kernel_subgroup():
  source = make_cyclic_group(6, "a")
  target = make_cyclic_group(6, "b")

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[[2]],
  )

  ker = f.kernel_subgroup()

  assert ker.elements == frozenset(f.kernel())
  assert ker.ambient_group == f.source
  assert ker.order == 2
  assert {
    x.coefficients
    for x in ker.generators
  } == {
    (3,),
  }


def test_image_subgroup():
  source = make_cyclic_group(6, "a")
  target = make_cyclic_group(6, "b")

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[[2]],
  )

  im = f.image_subgroup()

  assert im.elements == frozenset(f.image())
  assert im.ambient_group == f.target
  assert im.order == 3
  assert {
    x.coefficients
    for x in im.generators
  } == {
    (2,),
  }


def test_subgroup_equality():
  a = make_cyclic_group(6, "a")
  b = make_cyclic_group(6, "b")
  c = make_cyclic_group(6, "c")

  f = GroupMap(
    name="f",
    source=a,
    target=b,
    matrix=[[2]],
  )

  g = GroupMap(
    name="g",
    source=b,
    target=c,
    matrix=[[3]],
  )

  assert f.image_subgroup() == g.kernel_subgroup()

def make_product_group(orders, generators):
  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=i,
        order=order,
        generator=generator,
        element=[],
        gen_coe=[],
      )
      for i, (order, generator) in enumerate(
        zip(orders, generators)
      )
    ],
  )


def test_noncyclic_subgroup_generators():
  group = make_product_group(
    [2, 2],
    ["a", "b"],
  )

  f = GroupMap(
    name="id",
    source=group,
    target=group,
    matrix=[
      [1, 0],
      [0, 1],
    ],
  )

  im = f.image_subgroup()

  assert im.order == 4
  assert len(im.generators) == 2

  generated = {
    x.coefficients
    for x in im.generators
  }

  assert generated == {
    (0, 1),
    (1, 0),
  }

def test_subgroup_structure_cyclic_order_4():
  group = make_cyclic_group(4, "a")

  f = GroupMap(
    name="id",
    source=group,
    target=group,
    matrix=[[1]],
  )

  assert f.image_subgroup().structure() == (4,)


def test_subgroup_structure_z2_z2():
  group = make_product_group(
    [2, 2],
    ["a", "b"],
  )

  f = GroupMap(
    name="id",
    source=group,
    target=group,
    matrix=[
      [1, 0],
      [0, 1],
    ],
  )

  assert f.image_subgroup().structure() == (2, 2)

def test_subgroup_structure_z2_z4():
  group = make_product_group(
    [2, 4],
    ["a", "b"],
  )

  f = GroupMap(
    name="id",
    source=group,
    target=group,
    matrix=[
      [1, 0],
      [0, 1],
    ],
  )

  assert f.image_subgroup().structure() == (2, 4)


def test_subgroup_structure_z4_z12():
  group = make_product_group(
    [4, 12],
    ["a", "b"],
  )

  f = GroupMap(
    name="id",
    source=group,
    target=group,
    matrix=[
      [1, 0],
      [0, 1],
    ],
  )

  assert f.image_subgroup().structure() == (4, 12)


def test_subgroup_structure_trivial():
  group = make_cyclic_group(4, "a")
  zero = make_cyclic_group(1, "0")

  f = GroupMap(
    name="0",
    source=group,
    target=zero,
    matrix=[[0]],
  )

  assert f.image_subgroup().structure() == ()

def test_quotient_group_z4_by_2():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [(2,)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  cosets = {
    frozenset(
      x.coefficients
      for x in coset
    )
    for coset in quotient.cosets
  }

  assert cosets == {
    frozenset({
      (0,),
      (2,),
    }),
    frozenset({
      (1,),
      (3,),
    }),
  }

  assert quotient.order == 2

def test_quotient_group_same_coset():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [(2,)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  zero = GroupElement(group, (0,))
  one = GroupElement(group, (1,))
  two = GroupElement(group, (2,))
  three = GroupElement(group, (3,))

  assert quotient.coset(zero) == quotient.coset(two)
  assert quotient.coset(one) == quotient.coset(three)
  assert quotient.coset(zero) != quotient.coset(one)

def test_quotient_group_addition():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [(2,)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  zero_coset = quotient.coset(
    GroupElement(group, (0,))
  )

  one_coset = quotient.coset(
    GroupElement(group, (1,))
  )

  result = quotient.add_cosets(
    one_coset,
    one_coset,
  )

  assert result == zero_coset

def test_quotient_by_trivial_subgroup():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert quotient.order == 4

def test_quotient_by_whole_group():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [(1,)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert quotient.order == 1

def make_group(orders):
  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=i,
        order=order,
        generator=f"a{i}",
        element=[],
        gen_coe=[],
      )
      for i, order in enumerate(orders)
    ],
  )

def test_quotient_group_noncyclic():
  group = make_group(
    (2,4),
  )

  subgroup = make_subgroup(
    group,
    [(0,2)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert subgroup.order == 2
  assert quotient.order == 4

def test_quotient_group_wrong_ambient_group():
  group1 = make_cyclic_group(4, "a")
  group2 = make_cyclic_group(4, "b")

  subgroup = make_subgroup(
    group1,
    [(2,)],
  )

  with pytest.raises(ValueError):
    QuotientGroup(
      ambient_group=group2,
      subgroup=subgroup,
    )

def test_quotient_structure_z4_by_2():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [(2,)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert quotient.structure() == (2,)

def test_quotient_structure_by_trivial():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert quotient.structure() == (4,)

def test_quotient_structure_by_whole_group():
  group = make_cyclic_group(4, "a")

  subgroup = make_subgroup(
    group,
    [(1,)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert quotient.structure() == ()

def test_quotient_structure_z2_z2():
  group = make_group(
    (4,2),
  )

  subgroup = make_subgroup(
    group,
    [(2,0)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert quotient.order == 4
  assert quotient.structure() == (2,2)

def test_quotient_structure_z4():
  group = make_group(
    (4,2),
  )

  subgroup = make_subgroup(
    group,
    [(0,1)],
  )

  quotient = QuotientGroup(
    ambient_group=group,
    subgroup=subgroup,
  )

  assert quotient.order == 4
  assert quotient.structure() == (4,)

def test_induced_map_z4_to_z2():
  source = make_cyclic_group(4, "a")
  target = make_cyclic_group(2, "b")

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  induced = InducedMap(f)

  assert induced.source.structure() == (2,)
  assert induced.target.structure() == (2,)

  assert induced.is_well_defined()
  assert induced.is_injective()
  assert induced.is_surjective()
  assert induced.is_isomorphism()

def test_induced_map_apply():
  source = make_cyclic_group(4, "a")
  target = make_cyclic_group(2, "b")

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  induced = InducedMap(f)

  zero_coset = induced.source.coset(
    GroupElement(source, (0,))
  )

  one_coset = induced.source.coset(
    GroupElement(source, (1,))
  )

  assert induced.apply(
    zero_coset
  ) == GroupElement(
    target,
    (0,),
  )

  assert induced.apply(
    one_coset
  ) == GroupElement(
    target,
    (1,),
  )

def test_induced_map_non_surjective_original_map():
  group = make_cyclic_group(4, "a")

  f = GroupMap(
    name="times2",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  induced = InducedMap(f)

  assert induced.source.structure() == (2,)
  assert induced.target.structure() == (2,)

  assert induced.is_well_defined()
  assert induced.is_injective()
  assert induced.is_surjective()
  assert induced.is_isomorphism()

def test_induced_map_noncyclic_source():
  source = make_group(
    (4,2),
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [1,0],
    ],
  )

  induced = InducedMap(f)

  assert induced.source.structure() == (2,)
  assert induced.target.structure() == (2,)

  assert induced.is_well_defined()
  assert induced.is_injective()
  assert induced.is_surjective()
  assert induced.is_isomorphism()  

def test_group_map_induced_quotient_map():
  source = make_cyclic_group(4, "a")
  target = make_cyclic_group(2, "b")

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  induced = f.induced_quotient_map()

  assert isinstance(
    induced,
    InducedMap,
  )
  assert induced.is_isomorphism()

def test_exact_sequence_step():
  a = make_cyclic_group(2, "a")
  b = make_cyclic_group(4, "b")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="times2",
    source=a,
    target=b,
    matrix=[
      [2],
    ],
  )

  g = GroupMap(
    name="mod2",
    source=b,
    target=c,
    matrix=[
      [1],
    ],
  )

  step = ExactSequenceStep(
    first_map=f,
    second_map=g,
  )

  assert step.is_exact()

  assert step.image_of_first.structure() == (2,)
  assert step.kernel_of_second.structure() == (2,)

  assert step.quotient.structure() == (2,)
  assert step.image.structure() == (2,)

  induced = step.induced_map

  assert induced.is_isomorphism()
  assert step.quotient == induced.source
  assert step.image == induced.target

def test_exact_sequence_quotient_image_isomorphism():
  a = make_cyclic_group(2, "a")
  b = make_cyclic_group(4, "b")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="times2",
    source=a,
    target=b,
    matrix=[
      [2],
    ],
  )

  g = GroupMap(
    name="mod2",
    source=b,
    target=c,
    matrix=[
      [1],
    ],
  )

  step = ExactSequenceStep(
    first_map=f,
    second_map=g,
  )

  assert step.verifies_quotient_image_isomorphism()

def test_nonexact_sequence_step():
  a = make_cyclic_group(2, "a")
  b = make_cyclic_group(4, "b")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="zero",
    source=a,
    target=b,
    matrix=[
      [0],
    ],
  )

  g = GroupMap(
    name="mod2",
    source=b,
    target=c,
    matrix=[
      [1],
    ],
  )

  step = ExactSequenceStep(
    first_map=f,
    second_map=g,
  )

  assert not step.is_exact()
  assert not step.verifies_quotient_image_isomorphism()

  with pytest.raises(ValueError):
    _ = step.induced_map

def test_exact_sequence_step_incompatible_maps():
  a = make_cyclic_group(2, "a")
  b = make_cyclic_group(4, "b")
  d = make_cyclic_group(6, "d")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="f",
    source=a,
    target=b,
    matrix=[
      [2],
    ],
  )

  g = GroupMap(
    name="g",
    source=d,
    target=c,
    matrix=[
      [1],
    ],
  )

  with pytest.raises(ValueError):
    ExactSequenceStep(
      first_map=f,
      second_map=g,
    )

def test_exact_sequence_trivial_quotient():
  a = make_cyclic_group(4, "a")
  b = make_cyclic_group(4, "b")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="id",
    source=a,
    target=b,
    matrix=[
      [1],
    ],
  )

  g = GroupMap(
    name="zero",
    source=b,
    target=c,
    matrix=[
      [0],
    ],
  )

  step = ExactSequenceStep(
    first_map=f,
    second_map=g,
  )

  assert step.is_exact()
  assert step.quotient.structure() == ()
  assert step.image.structure() == ()
  assert step.verifies_quotient_image_isomorphism()

def test_group_structure():
  z4 = make_cyclic_group(
    4,
    "a",
  )

  z2_z2 = make_group(
    (2,2),
  )

  assert group_structure(
    z4
  ) == (4,)

  assert group_structure(
    z2_z2
  ) == (2,2)

def test_all_subgroups_z4():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroups = all_subgroups(
    group
  )

  structures = [
    subgroup.structure()
    for subgroup in subgroups
  ]

  assert len(subgroups) == 3

  assert structures == [
    (),
    (2,),
    (4,),
  ]

def test_extension_candidate_z4():
  a = make_cyclic_group(
    2,
    "a",
  )

  b = make_cyclic_group(
    4,
    "b",
  )

  c = make_cyclic_group(
    2,
    "c",
  )

  candidate = ExtensionCandidate(
    left_group=a,
    middle_group=b,
    right_group=c,
  )

  assert candidate.is_valid()

  assert (
    candidate.left_structure
    == (2,)
  )

  assert (
    candidate.middle_structure
    == (4,)
  )

  assert (
    candidate.right_structure
    == (2,)
  )

  assert len(
    candidate.matching_subgroups
  ) == 1

def test_extension_candidate_z2_z2():
  a = make_cyclic_group(
    2,
    "a",
  )

  b = make_group(
    (2,2),
  )

  c = make_cyclic_group(
    2,
    "c",
  )

  candidate = ExtensionCandidate(
    left_group=a,
    middle_group=b,
    right_group=c,
  )

  assert candidate.is_valid()

  assert (
    candidate.middle_structure
    == (2,2)
  )

  assert len(
    candidate.matching_subgroups
  ) == 3

def test_invalid_extension_candidate():
  a = make_cyclic_group(
    2,
    "a",
  )

  b = make_cyclic_group(
    8,
    "b",
  )

  c = make_cyclic_group(
    2,
    "c",
  )

  candidate = ExtensionCandidate(
    left_group=a,
    middle_group=b,
    right_group=c,
  )

  assert not candidate.is_valid()
  assert candidate.matching_subgroups == ()

def test_extension_multiple_candidates():
  a = make_cyclic_group(
    2,
    "a",
  )

  c = make_cyclic_group(
    2,
    "c",
  )

  z4 = make_cyclic_group(
    4,
    "b",
  )

  z2_z2 = make_group(
    (2,2),
  )

  z8 = make_cyclic_group(
    8,
    "d",
  )

  candidates = valid_extension_candidates(
    a,
    c,
    [
      z4,
      z2_z2,
      z8,
    ],
  )

  structures = {
    candidate.middle_structure
    for candidate in candidates
  }

  assert structures == {
    (4,),
    (2,2),
  }

def test_finite_abelian_structures_order_4():
  assert finite_abelian_structures(
    4
  ) == (
    (4,),
    (2,2),
  )

def test_finite_abelian_structures_order_8():
  assert finite_abelian_structures(
    8
  ) == (
    (8,),
    (2,4),
    (2,2,2),
  )

def test_finite_abelian_structures_order_6():
  assert finite_abelian_structures(
    6
  ) == (
    (6,),
  )

def test_abstract_abelian_group():
  group = abstract_abelian_group(
    (2,4),
  )

  assert group.orders == [
    2,
    4,
  ]

  assert group_structure(
    group
  ) == (2,4)

  assert finite_group_order(
    group
  ) == 8

def test_automatic_extension_candidates_z2_z2():
  a = make_cyclic_group(
    2,
    "a",
  )

  c = make_cyclic_group(
    2,
    "c",
  )

  candidates = extension_candidates(
    a,
    c,
  )

  structures = {
    candidate.middle_structure
    for candidate in candidates
  }

  assert structures == {
    (4,),
    (2,2),
  }

def test_automatic_extension_candidates_z4_z2():
  a = make_cyclic_group(
    4,
    "a",
  )

  c = make_cyclic_group(
    2,
    "c",
  )

  candidates = extension_candidates(
    a,
    c,
  )

  structures = {
    candidate.middle_structure
    for candidate in candidates
  }

  assert structures == {
    (8,),
    (2,4),
  }

def test_finite_group_order_zero_group():
  zero = make_cyclic_group(
    0,
    "0",
  )

  assert finite_group_order(
    zero
  ) == 1

  assert group_structure(
    zero
  ) == ()

def test_exact_sequence_middle_group_candidates():
  a = make_cyclic_group(2, "a")
  b = make_cyclic_group(4, "b")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="times2",
    source=a,
    target=b,
    matrix=[
      [2],
    ],
  )

  g = GroupMap(
    name="mod2",
    source=b,
    target=c,
    matrix=[
      [1],
    ],
  )

  step = ExactSequenceStep(
    first_map=f,
    second_map=g,
  )

  assert (
    step.extension_left_group.orders
    == [2]
  )

  assert (
    step.extension_right_group.orders
    == [2]
  )

  assert set(
    step.middle_group_candidate_structures()
  ) == {
    (4,),
    (2,2),
  }

def test_exact_sequence_actual_middle_is_candidate():
  a = make_cyclic_group(2, "a")
  b = make_cyclic_group(4, "b")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="times2",
    source=a,
    target=b,
    matrix=[
      [2],
    ],
  )

  g = GroupMap(
    name="mod2",
    source=b,
    target=c,
    matrix=[
      [1],
    ],
  )

  step = ExactSequenceStep(
    first_map=f,
    second_map=g,
  )

  actual_structure = group_structure(
    step.middle_group
  )

  candidates = set(
    step.middle_group_candidate_structures()
  )

  assert actual_structure == (4,)
  assert actual_structure in candidates

def test_nonexact_sequence_has_no_middle_candidates():
  a = make_cyclic_group(2, "a")
  b = make_cyclic_group(4, "b")
  c = make_cyclic_group(2, "c")

  f = GroupMap(
    name="zero",
    source=a,
    target=b,
    matrix=[
      [0],
    ],
  )

  g = GroupMap(
    name="mod2",
    source=b,
    target=c,
    matrix=[
      [1],
    ],
  )

  step = ExactSequenceStep(
    first_map=f,
    second_map=g,
  )

  with pytest.raises(ValueError):
    step.middle_group_candidates()

def test_abelian_group_structure_z():
  group = make_cyclic_group(
    inf,
    "ι",
  )

  structure = abelian_group_structure(
    group
  )

  assert structure.free_rank == 1
  assert structure.torsion_orders == ()
  assert structure.is_free
  assert not structure.is_finite
  assert str(structure) == "Z"


def test_abelian_group_structure_z_z2():
  group = make_group(
    (inf,2),
  )

  structure = abelian_group_structure(
    group
  )

  assert structure.free_rank == 1
  assert structure.torsion_orders == (2,)
  assert not structure.is_free
  assert not structure.is_finite
  assert str(structure) == "Z ⊕ Z/2"


def test_abelian_group_structure_z2_z4():
  group = make_group(
    (2,4),
  )

  structure = abelian_group_structure(
    group
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == (2,4)
  assert structure.is_finite
  assert not structure.is_free
  assert str(structure) == "Z/2 ⊕ Z/4"


def test_abelian_group_structure_zero():
  group = make_cyclic_group(
    0,
    "0",
  )

  structure = abelian_group_structure(
    group
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == ()
  assert structure.is_finite
  assert str(structure) == "0"

def test_free_map_times2_rank():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  assert f.free_map_rank() == 1


def test_free_map_times2_smith_normal_form():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  smith = f.smith_normal_form()

  assert smith.shape == (1,1)
  assert abs(int(smith[0,0])) == 2


def test_free_map_times2_kernel_structure():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  structure = f.kernel_structure()

  assert structure.free_rank == 0
  assert structure.torsion_orders == ()
  assert str(structure) == "0"


def test_free_map_times2_image_structure():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  structure = f.image_structure()

  assert structure.free_rank == 1
  assert structure.torsion_orders == ()
  assert str(structure) == "Z"


def test_free_map_times2_cokernel_structure():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  structure = f.cokernel_structure()

  assert structure.free_rank == 0
  assert structure.torsion_orders == (2,)
  assert str(structure) == "Z/2"

def test_free_map_z2_to_z2_structure():
  source = make_group(
    (inf,inf),
  )

  target = make_group(
    (inf,inf),
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [2,0],
      [0,0],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert kernel.free_rank == 1
  assert kernel.torsion_orders == ()
  assert str(kernel) == "Z"

  assert image.free_rank == 1
  assert image.torsion_orders == ()
  assert str(image) == "Z"

  assert cokernel.free_rank == 1
  assert cokernel.torsion_orders == (2,)
  assert str(cokernel) == "Z ⊕ Z/2"

def test_relation_matrix_z():
  group = make_cyclic_group(
    inf,
    "a",
  )

  relations = relation_matrix(
    group
  )

  assert relations.shape == (1,0)


def test_relation_matrix_z2():
  group = make_cyclic_group(
    2,
    "a",
  )

  relations = relation_matrix(
    group
  )

  assert relations.shape == (1,1)
  assert int(relations[0,0]) == 2


def test_relation_matrix_z_z2():
  group = make_group(
    (inf,2),
  )

  relations = relation_matrix(
    group
  )

  assert relations.shape == (2,1)

  assert list(
    relations[:,0]
  ) == [
    0,
    2,
  ]


def test_structure_from_presentation_z_z2():
  group = make_group(
    (inf,2),
  )

  structure = (
    structure_from_presentation(
      relation_matrix(group)
    )
  )

  assert structure.free_rank == 1
  assert structure.torsion_orders == (2,)
  assert str(structure) == "Z ⊕ Z/2"

def test_homomorphism_z_to_z2_is_well_defined():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  assert (
    f.is_well_defined_homomorphism()
  )


def test_homomorphism_z2_to_z_nonzero_is_not_well_defined():
  source = make_cyclic_group(
    2,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="invalid",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  assert not (
    f.is_well_defined_homomorphism()
  )


def test_homomorphism_z2_to_z_zero_is_well_defined():
  source = make_cyclic_group(
    2,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="zero",
    source=source,
    target=target,
    matrix=[
      [0],
    ],
  )

  assert (
    f.is_well_defined_homomorphism()
  )

def test_cokernel_z_to_z2():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  structure = (
    f.cokernel_structure()
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == ()
  assert str(structure) == "0"

def test_cokernel_z_to_z4_times2():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  structure = (
    f.cokernel_structure()
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == (2,)
  assert str(structure) == "Z/2"

def test_cokernel_z2_to_z_zero():
  source = make_cyclic_group(
    2,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="zero",
    source=source,
    target=target,
    matrix=[
      [0],
    ],
  )

  structure = (
    f.cokernel_structure()
  )

  assert structure.free_rank == 1
  assert structure.torsion_orders == ()
  assert str(structure) == "Z"

def test_cokernel_z_to_z_z4():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_group(
    (inf,4),
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [2],
      [2],
    ],
  )

  structure = (
    f.cokernel_structure()
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == (2,4)
  assert str(structure) == "Z/2 ⊕ Z/4"

def test_kernel_z_to_z2():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  structure = (
    f.kernel_structure()
  )

  assert structure.free_rank == 1
  assert structure.torsion_orders == ()
  assert str(structure) == "Z"


def test_image_z_to_z2():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  structure = (
    f.image_structure()
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == (2,)
  assert str(structure) == "Z/2"

def test_kernel_z_to_z4_times2():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  structure = (
    f.kernel_structure()
  )

  assert structure.free_rank == 1
  assert structure.torsion_orders == ()
  assert str(structure) == "Z"


def test_image_z_to_z4_times2():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  structure = (
    f.image_structure()
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == (2,)
  assert str(structure) == "Z/2"

def test_image_z_to_z4_surjective():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="mod4",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  structure = (
    f.image_structure()
  )

  assert structure.free_rank == 0
  assert structure.torsion_orders == (4,)
  assert str(structure) == "Z/4"

def test_image_z_to_z4_zero():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="zero",
    source=source,
    target=target,
    matrix=[
      [0],
    ],
  )

  image = f.image_structure()
  kernel = f.kernel_structure()
  cokernel = f.cokernel_structure()

  assert str(image) == "0"
  assert str(kernel) == "Z"
  assert str(cokernel) == "Z/4"

def test_structure_z2_to_z4_times2():
  source = make_cyclic_group(
    2,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "0"
  assert str(image) == "Z/2"
  assert str(cokernel) == "Z/2"

def test_structure_z2_to_z4_zero():
  source = make_cyclic_group(
    2,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="zero",
    source=source,
    target=target,
    matrix=[
      [0],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z/2"
  assert str(image) == "0"
  assert str(cokernel) == "Z/4"

def test_structure_z4_to_z2_mod2():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z/2"
  assert str(image) == "Z/2"
  assert str(cokernel) == "0"

def test_structure_rejects_invalid_z2_to_z4():
  source = make_cyclic_group(
    2,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="invalid",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  assert not (
    f.is_well_defined_homomorphism()
  )

  with pytest.raises(ValueError):
    f.kernel_structure()

  with pytest.raises(ValueError):
    f.image_structure()

  with pytest.raises(ValueError):
    f.cokernel_structure()

def test_mixed_z_z2_to_z4_surjective():
  source = make_group(
    (inf,2),
  )

  target = make_cyclic_group(
    4,
    "c",
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1,2],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z"
  assert str(image) == "Z/4"
  assert str(cokernel) == "0"

def test_mixed_z_z2_to_z4_free_times2():
  source = make_group(
    (inf,2),
  )

  target = make_cyclic_group(
    4,
    "c",
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [2,0],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z ⊕ Z/2"
  assert str(image) == "Z/2"
  assert str(cokernel) == "Z/2"

def test_mixed_z_z2_to_z4_torsion_times2():
  source = make_group(
    (inf,2),
  )

  target = make_cyclic_group(
    4,
    "c",
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [0,2],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z"
  assert str(image) == "Z/2"
  assert str(cokernel) == "Z/2"

def test_mixed_z_z2_to_z4_zero():
  source = make_group(
    (inf,2),
  )

  target = make_cyclic_group(
    4,
    "c",
  )

  f = GroupMap(
    name="zero",
    source=source,
    target=target,
    matrix=[
      [0,0],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z ⊕ Z/2"
  assert str(image) == "0"
  assert str(cokernel) == "Z/4"

def test_mixed_z_z2_to_z4_invalid():
  source = make_group(
    (inf,2),
  )

  target = make_cyclic_group(
    4,
    "c",
  )

  f = GroupMap(
    name="invalid",
    source=source,
    target=target,
    matrix=[
      [1,1],
    ],
  )

  assert not (
    f.is_well_defined_homomorphism()
  )

  with pytest.raises(ValueError):
    f.kernel_structure()

  with pytest.raises(ValueError):
    f.image_structure()

  with pytest.raises(ValueError):
    f.cokernel_structure()

def test_general_mixed_to_mixed():
  source = make_group(
    (inf,2),
  )

  target = make_group(
    (inf,4),
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [2,0],
      [0,2],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "0"
  assert str(image) == "Z ⊕ Z/2"
  assert str(cokernel) == "Z/2 ⊕ Z/2"

def test_general_mixed_to_mixed_free_kernel():
  source = make_group(
    (inf,2),
  )

  target = make_group(
    (inf,4),
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [0,0],
      [0,2],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z"
  assert str(image) == "Z/2"
  assert str(cokernel) == "Z ⊕ Z/2"

def test_general_mixed_to_mixed_inclusion():
  source = make_group(
    (inf,2),
  )

  target = make_group(
    (inf,4),
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1,0],
      [0,2],
    ],
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "0"
  assert str(image) == "Z ⊕ Z/2"
  assert str(cokernel) == "Z/2"

def test_general_kernel_lattice_basis():
  source = make_group(
    (inf,2),
  )

  target = make_group(
    (inf,4),
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [0,0],
      [0,2],
    ],
  )

  basis = f.kernel_lattice_basis()

  assert basis.shape == (2,2)

  assert basis == Matrix([
    [1,0],
    [0,2],
  ])

def test_general_mixed_to_mixed_invalid():
  source = make_group(
    (inf,2),
  )

  target = make_group(
    (inf,4),
  )

  f = GroupMap(
    name="invalid",
    source=source,
    target=target,
    matrix=[
      [1,1],
      [0,0],
    ],
  )

  assert not (
    f.is_well_defined_homomorphism()
  )

  with pytest.raises(ValueError):
    f.kernel_lattice_basis()

  with pytest.raises(ValueError):
    f.cokernel_structure()

def test_presentation_matches_free_times2():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    inf,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  assert (
    f.presentation_kernel_structure()
    == f.kernel_structure()
  )

  assert (
    f.presentation_image_structure()
    == f.image_structure()
  )

def test_presentation_matches_z_to_z4():
  source = make_cyclic_group(
    inf,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  assert (
    f.presentation_kernel_structure()
    == f.kernel_structure()
  )

  assert (
    f.presentation_image_structure()
    == f.image_structure()
  )

  assert str(
    f.presentation_kernel_structure()
  ) == "Z"

  assert str(
    f.presentation_image_structure()
  ) == "Z/2"

def test_presentation_matches_z2_to_z4():
  source = make_cyclic_group(
    2,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  assert (
    f.presentation_kernel_structure()
    == f.kernel_structure()
  )

  assert (
    f.presentation_image_structure()
    == f.image_structure()
  )

  assert str(
    f.presentation_kernel_structure()
  ) == "0"

  assert str(
    f.presentation_image_structure()
  ) == "Z/2"

def test_presentation_matches_z4_to_z2():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="mod2",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  assert (
    f.presentation_kernel_structure()
    == f.kernel_structure()
  )

  assert (
    f.presentation_image_structure()
    == f.image_structure()
  )

  assert str(
    f.presentation_kernel_structure()
  ) == "Z/2"

  assert str(
    f.presentation_image_structure()
  ) == "Z/2"

def test_presentation_matches_mixed_to_finite():
  source = make_group(
    (inf,2),
  )

  target = make_cyclic_group(
    4,
    "c",
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [2,0],
    ],
  )

  assert (
    f.presentation_kernel_structure()
    == f.kernel_structure()
  )

  assert (
    f.presentation_image_structure()
    == f.image_structure()
  )

  assert str(
    f.presentation_kernel_structure()
  ) == "Z ⊕ Z/2"

  assert str(
    f.presentation_image_structure()
  ) == "Z/2"

def test_zero_source_nonzero_matrix_is_invalid():
  source = make_cyclic_group(
    0,
    "0",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="invalid",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  assert not (
    f.is_well_defined_homomorphism()
  )

  with pytest.raises(ValueError):
    f.kernel_structure()

  with pytest.raises(ValueError):
    f.image_structure()

  with pytest.raises(ValueError):
    f.cokernel_structure()

def test_zero_source_to_z4():
  source = make_cyclic_group(
    0,
    "0",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="zero",
    source=source,
    target=target,
    matrix=[
      [0],
    ],
  )

  assert (
    f.is_well_defined_homomorphism()
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "0"
  assert str(image) == "0"
  assert str(cokernel) == "Z/4"

def test_zero_source_to_z4_relation_multiple():
  source = make_cyclic_group(
    0,
    "0",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="zero",
    source=source,
    target=target,
    matrix=[
      [4],
    ],
  )

  assert (
    f.is_well_defined_homomorphism()
  )

  assert str(
    f.kernel_structure()
  ) == "0"

  assert str(
    f.image_structure()
  ) == "0"

  assert str(
    f.cokernel_structure()
  ) == "Z/4"

def test_general_free_nondiagonal():
  source = make_group(
    (inf,inf),
  )

  target = make_group(
    (inf,inf),
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [2,1],
      [0,2],
    ],
  )

  assert (
    f.is_well_defined_homomorphism()
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "0"
  assert str(image) == "Z^2"
  assert str(cokernel) == "Z/4"

def test_general_mixed_nondiagonal_to_finite():
  source = make_group(
    (inf,4),
  )

  target = make_cyclic_group(
    6,
    "b",
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [2,3],
    ],
  )

  assert (
    f.is_well_defined_homomorphism()
  )

  kernel = f.kernel_structure()
  image = f.image_structure()
  cokernel = f.cokernel_structure()

  assert str(kernel) == "Z ⊕ Z/2"
  assert str(image) == "Z/6"
  assert str(cokernel) == "0"

def test_finite_presentation_crosscheck():
  groups = [
    make_cyclic_group(
      0,
      "0",
    ),
    make_cyclic_group(
      2,
      "a",
    ),
    make_cyclic_group(
      3,
      "a",
    ),
    make_cyclic_group(
      4,
      "a",
    ),
    make_group(
      (2,2),
    ),
    make_group(
      (2,4),
    ),
    make_group(
      (3,3),
    ),
  ]

  checked = 0

  for source in groups:
    for target in groups:
      rows = target.direct_sum
      cols = source.direct_sum

      for entries in product(
        range(4),
        repeat=rows * cols,
      ):
        matrix = [
          list(
            entries[
              i * cols:
              (i + 1) * cols
            ]
          )
          for i in range(rows)
        ]

        f = GroupMap(
          name="crosscheck",
          source=source,
          target=target,
          matrix=matrix,
        )

        if not (
          f.is_well_defined_homomorphism()
        ):
          continue

        enumerated_kernel = (
          f.kernel_subgroup()
          .structure()
        )

        enumerated_image = (
          f.image_subgroup()
          .structure()
        )

        quotient = QuotientGroup(
          ambient_group=target,
          subgroup=f.image_subgroup(),
        )

        enumerated_cokernel = (
          quotient.structure()
        )

        presentation_kernel = (
          f.kernel_structure()
        )

        presentation_image = (
          f.image_structure()
        )

        presentation_cokernel = (
          f.cokernel_structure()
        )

        assert (
          presentation_kernel.free_rank
          == 0
        )

        assert (
          presentation_image.free_rank
          == 0
        )

        assert (
          presentation_cokernel.free_rank
          == 0
        )

        assert (
          presentation_kernel.torsion_orders
          == enumerated_kernel
        )

        assert (
          presentation_image.torsion_orders
          == enumerated_image
        )

        assert (
          presentation_cokernel.torsion_orders
          == enumerated_cokernel
        )

        checked += 1

  assert checked > 500
























