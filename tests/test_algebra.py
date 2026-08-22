from algebra import (
  GroupElement,
  GroupMap,
  QuotientGroup,
  Subgroup,
  generated_subgroup_elements,
)
from models import AbelianGroup, GroupComponent

import pytest

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



