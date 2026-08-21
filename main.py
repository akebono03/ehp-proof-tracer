from pathlib import Path

from ehp import EHPSegment
from repository import SphereRepository


BASE_DIR = Path(__file__).resolve().parent

repo = SphereRepository(
  BASE_DIR / "data" / "sphere.csv"
)

segment = EHPSegment(
  repo,
  n=11,
  k=18,
)

for result in segment.check():
  print(result.middle_group)
  print(
    f"Im({result.left_map.name}) =",
    result.image()
  )
  print(
    f"Ker({result.right_map.name}) =",
    result.kernel()
  )

  if result.is_exact():
    print(
      f"Im({result.left_map.name}) "
      f"= Ker({result.right_map.name})"
    )
    print("✓ exact")
  else:
    print("✗ not exact")

  print()
  