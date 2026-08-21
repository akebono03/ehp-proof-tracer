from pathlib import Path

from ehp import EHPSegment
from repository import SphereRepository


BASE_DIR = Path(__file__).resolve().parent.parent


def make_repository():
  return SphereRepository(
    BASE_DIR / "data" / "sphere.csv"
  )


def test_ehp_exactness_at_sphere():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  result = segment.exactness_at_sphere()

  assert result.image() == {
    (0,),
  }

  assert result.kernel() == {
    (0,),
  }

  assert result.is_exact()


def test_ehp_exactness_at_hopf_target():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  result = segment.exactness_at_hopf_target()

  assert result.image() == {
    (0,),
    (4,),
  }

  assert result.kernel() == {
    (0,),
    (4,),
  }

  assert result.is_exact()

def test_ehp_n3_k5_groups():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  sphere = segment.exactness_at_sphere().middle_group
  hopf_target = segment.exactness_at_hopf_target().middle_group

  assert sphere.n == 3
  assert sphere.k == 5
  assert sphere.orders == [2]
  assert sphere.generators == ["ν'η6^2"]

  assert hopf_target.n == 5
  assert hopf_target.k == 3
  assert hopf_target.orders == [8]
  assert hopf_target.generators == ["ν5"]

def test_ehp_n11_k18_at_sphere():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=11,
    k=18,
  )

  result = segment.exactness_at_sphere()

  expected = {
    (0,0,0),
    (0,0,1),
    (0,2,0),
    (0,2,1),
    (2,0,0),
    (2,0,1),
    (2,2,0),
    (2,2,1),
    (4,0,0),
    (4,0,1),
    (4,2,0),
    (4,2,1),
    (6,0,0),
    (6,0,1),
    (6,2,0),
    (6,2,1),
  }

  assert result.image() == expected
  assert result.kernel() == expected
  assert result.is_exact()


def test_ehp_n11_k18_at_hopf_target():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=11,
    k=18,
  )

  result = segment.exactness_at_hopf_target()

  expected = {
    (0,0),
    (0,1),
    (1,0),
    (1,1),
  }

  assert result.image() == expected
  assert result.kernel() == expected
  assert result.is_exact()

def test_ehp_n11_k18_groups():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=11,
    k=18,
  )

  sphere = segment.exactness_at_sphere().middle_group
  hopf_target = (
    segment.exactness_at_hopf_target().middle_group
  )

  assert sphere.n == 11
  assert sphere.k == 18
  assert sphere.orders == [8,4,2]
  assert sphere.generators == [
    "ξ'",
    "ξ'+λ'",
    r"η11\bar{\mu}12",
  ]

  assert hopf_target.n == 21
  assert hopf_target.k == 8
  assert hopf_target.orders == [2,2]
  assert hopf_target.generators == [
    r"\bar{\nu}10",
    "ε10",
  ]
  
