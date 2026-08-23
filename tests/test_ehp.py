from pathlib import Path

from ehp import EHPSegment
from repository import SphereRepository
from algebra import group_structure


BASE_DIR = Path(__file__).resolve().parent.parent


def make_repository():
  return SphereRepository(
    BASE_DIR / "data" / "sphere.csv"
  )


def coefficients(subgroup):
  return {
    x.coefficients
    for x in subgroup.elements
  }


def test_ehp_exactness_at_sphere():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  result = segment.exactness_at_sphere()

  assert coefficients(result.image()) == {
    (0,),
  }

  assert coefficients(result.kernel()) == {
    (0,),
  }

  assert result.image_structure == ()
  assert result.kernel_structure == ()

  assert result.is_exact()


def test_ehp_exactness_at_hopf_target():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  result = segment.exactness_at_hopf_target()

  assert coefficients(result.image()) == {
    (0,),
    (4,),
  }

  assert coefficients(result.kernel()) == {
    (0,),
    (4,),
  }

  assert result.image_structure == (2,)
  assert result.kernel_structure == (2,)

  assert result.is_exact()


def test_ehp_n3_k5_groups():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  sphere = segment.exactness_at_sphere().middle_group
  hopf_target = (
    segment.exactness_at_hopf_target().middle_group
  )

  assert sphere.n == 3
  assert sphere.k == 5
  assert sphere.orders == [2]
  assert sphere.generators == [
    "ν'η6^2",
  ]

  assert hopf_target.n == 5
  assert hopf_target.k == 3
  assert hopf_target.orders == [8]
  assert hopf_target.generators == [
    "ν5",
  ]


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

  assert coefficients(result.image()) == expected
  assert coefficients(result.kernel()) == expected

  assert result.image_structure == (2,2,4)
  assert result.kernel_structure == (2,2,4)

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

  assert coefficients(result.image()) == expected
  assert coefficients(result.kernel()) == expected

  assert result.image_structure == (2,2)
  assert result.kernel_structure == (2,2)

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
  assert sphere.orders == [
    8,
    4,
    2,
  ]

  assert sphere.generators == [
    "ξ'",
    "ξ'+λ'",
    r"η11\bar{\mu}12",
  ]

  assert hopf_target.n == 21
  assert hopf_target.k == 8
  assert hopf_target.orders == [
    2,
    2,
  ]

  assert hopf_target.generators == [
    r"\bar{\nu}10",
    "ε10",
  ]

def test_ehp_n3_k5_exact_step_at_sphere():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  step = segment.exact_step_at_sphere()

  assert step.first_map == segment.E
  assert step.second_map == segment.H

  assert step.is_exact()
  assert step.verifies_quotient_image_isomorphism()

  assert step.quotient.structure() == (2,)
  assert step.image.structure() == (2,)

def test_ehp_n3_k5_exact_step_at_hopf_target():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  step = segment.exact_step_at_hopf_target()

  assert step.first_map == segment.H
  assert step.second_map == segment.P

  assert step.is_exact()
  assert step.verifies_quotient_image_isomorphism()

  assert step.quotient.structure() == (4,)
  assert step.image.structure() == (4,)

def test_ehp_n11_k18_exact_step_at_sphere():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=11,
    k=18,
  )

  step = segment.exact_step_at_sphere()

  assert step.is_exact()
  assert step.verifies_quotient_image_isomorphism()

  assert step.quotient.order == 4
  assert step.quotient.structure() == (2,2)

  assert step.image.order == 4
  assert step.image.structure() == (2,2)

def test_ehp_n11_k18_exact_step_at_hopf_target():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=11,
    k=18,
  )

  step = segment.exact_step_at_hopf_target()

  assert step.is_exact()
  assert step.verifies_quotient_image_isomorphism()

  assert step.quotient.structure() == ()
  assert step.image.structure() == ()

def test_ehp_n3_k5_sphere_group_candidates():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  candidates = (
    segment.sphere_group_candidate_structures()
  )

  assert candidates == (
    (2,),
  )

  actual = (
    segment
    .exact_step_at_sphere()
    .middle_group
    .orders
  )

  assert actual == [2]

def test_ehp_n3_k5_hopf_target_group_candidates():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  candidates = set(
    segment.hopf_target_group_candidate_structures()
  )

  assert candidates == {
    (8,),
    (2,4),
  }

  actual = (
    segment
    .exact_step_at_hopf_target()
    .middle_group
  )

  assert group_structure(
    actual
  ) == (8,)

  assert (
    group_structure(actual)
    in candidates
  )

def test_ehp_general_structure_api_at_sphere():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  result = (
    segment.exactness_at_sphere()
  )

  assert result.is_exact()

  assert str(
    result.image_abelian_structure
  ) == "0"

  assert str(
    result.kernel_abelian_structure
  ) == "0"

  assert str(
    result.quotient_abelian_structure
  ) == "Z/2"

  assert str(
    result.right_image_abelian_structure
  ) == "Z/2"

  assert (
    result.verifies_quotient_image_structure_isomorphism()
  )

def test_ehp_general_structure_api_at_hopf_target():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  result = (
    segment.exactness_at_hopf_target()
  )

  assert result.is_exact()

  assert str(
    result.image_abelian_structure
  ) == "Z/2"

  assert str(
    result.kernel_abelian_structure
  ) == "Z/2"

  assert str(
    result.quotient_abelian_structure
  ) == "Z/4"

  assert str(
    result.right_image_abelian_structure
  ) == "Z/4"

  assert (
    result.verifies_quotient_image_structure_isomorphism()
  )

def test_ehp_general_structure_api_noncyclic():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=11,
    k=18,
  )

  result = (
    segment.exactness_at_sphere()
  )

  assert result.is_exact()

  assert str(
    result.image_abelian_structure
  ) == "Z/2 ⊕ Z/2 ⊕ Z/4"

  assert str(
    result.kernel_abelian_structure
  ) == "Z/2 ⊕ Z/2 ⊕ Z/4"

  assert str(
    result.quotient_abelian_structure
  ) == "Z/2 ⊕ Z/2"

  assert str(
    result.right_image_abelian_structure
  ) == "Z/2 ⊕ Z/2"

  assert (
    result.verifies_quotient_image_structure_isomorphism()
  )

def test_ehp_old_new_structure_api_agree():
  repo = make_repository()

  segments = [
    EHPSegment(
      repo,
      n=3,
      k=5,
    ),
    EHPSegment(
      repo,
      n=11,
      k=18,
    ),
  ]

  for segment in segments:
    results = [
      segment.exactness_at_sphere(),
      segment.exactness_at_hopf_target(),
    ]

    for result in results:
      assert (
        result.image_abelian_structure
        .free_rank
        == 0
      )

      assert (
        result.kernel_abelian_structure
        .free_rank
        == 0
      )

      assert (
        result.image_abelian_structure
        .torsion_orders
        == result.image_structure
      )

      assert (
        result.kernel_abelian_structure
        .torsion_orders
        == result.kernel_structure
      )

def test_ehp_exactness_result_delegates_to_exact_step():
  repo = make_repository()

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  result = (
    segment.exactness_at_sphere()
  )

  step = (
    segment.exact_step_at_sphere()
  )

  assert (
    result.is_exact()
    == step.is_exact()
  )

  assert (
    result.image_abelian_structure
    == step.image_of_first_structure
  )

  assert (
    result.kernel_abelian_structure
    == step.kernel_of_second_structure
  )

  assert (
    result.quotient_abelian_structure
    == step.quotient_structure
  )

  assert (
    result.right_image_abelian_structure
    == step.image_structure
  )









