from pathlib import Path

from ehp import EHPSegment
from formatter import format_proof
from proof import (
  ehp_hopf_target_proof,
  ehp_sphere_proof,
)
from repository import SphereRepository


BASE_DIR = Path(__file__).resolve().parent


repo = SphereRepository(
  BASE_DIR
  / "data"
  / "sphere.csv"
)

segment = EHPSegment(
  repo,
  n=3,
  k=5,
)

print("=== Sphere ===")

sphere_proof = ehp_sphere_proof(
  segment
)

print(
  format_proof(
    sphere_proof
  )
)

print()

print("=== Hopf target ===")

hopf_proof = ehp_hopf_target_proof(
  segment
)

print(
  format_proof(
    hopf_proof
  )
)

