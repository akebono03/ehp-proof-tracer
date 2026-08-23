from pathlib import Path

from ehp import EHPSegment
from repository import SphereRepository


BASE_DIR = Path(__file__).resolve().parent


def main():
  repo = SphereRepository(
    BASE_DIR
    / "data"
    / "sphere.csv"
  )

  segment = EHPSegment(
    repo,
    n=4,
    k=3,
  )

  print(
    "=== E ==="
  )
  print(
    "source orders =",
    segment.E.source.orders,
  )
  print(
    "source generators =",
    segment.E.source.generators,
  )
  print(
    "target orders =",
    segment.E.target.orders,
  )
  print(
    "target generators =",
    segment.E.target.generators,
  )
  print(
    "matrix =",
    segment.E.matrix,
  )

  print()
  print(
    "=== H ==="
  )
  print(
    "source orders =",
    segment.H.source.orders,
  )
  print(
    "source generators =",
    segment.H.source.generators,
  )
  print(
    "target orders =",
    segment.H.target.orders,
  )
  print(
    "target generators =",
    segment.H.target.generators,
  )
  print(
    "matrix =",
    segment.H.matrix,
  )

  print()
  print(
    "=== P ==="
  )
  print(
    "source orders =",
    segment.P.source.orders,
  )
  print(
    "source generators =",
    segment.P.source.generators,
  )
  print(
    "target orders =",
    segment.P.target.orders,
  )
  print(
    "target generators =",
    segment.P.target.generators,
  )
  print(
    "matrix =",
    segment.P.matrix,
  )

  print()
  print(
    "=== exactness at sphere ==="
  )

  sphere = (
    segment
    .exactness_at_sphere()
  )

  print(
    "image =",
    sphere.image_abelian_structure,
  )
  print(
    "kernel =",
    sphere.kernel_abelian_structure,
  )
  print(
    "quotient =",
    sphere.quotient_abelian_structure,
  )
  print(
    "right image =",
    sphere.right_image_abelian_structure,
  )
  print(
    "exact =",
    sphere.is_exact(),
  )
  print(
    "quotient/image =",
    sphere
    .verifies_quotient_image_structure_isomorphism(),
  )

  print()
  print(
    "=== exactness at Hopf target ==="
  )

  hopf = (
    segment
    .exactness_at_hopf_target()
  )

  print(
    "image =",
    hopf.image_abelian_structure,
  )
  print(
    "kernel =",
    hopf.kernel_abelian_structure,
  )
  print(
    "quotient =",
    hopf.quotient_abelian_structure,
  )
  print(
    "right image =",
    hopf.right_image_abelian_structure,
  )
  print(
    "exact =",
    hopf.is_exact(),
  )
  print(
    "quotient/image =",
    hopf
    .verifies_quotient_image_structure_isomorphism(),
  )


if __name__ == "__main__":
  main()
