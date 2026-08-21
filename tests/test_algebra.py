from algebra import GroupElement, GroupMap
from models import AbelianGroup, GroupComponent


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
  