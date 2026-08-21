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
  