from pathlib import Path
import sys

AUDIT_DIR = Path(__file__).resolve().parent
if str(AUDIT_DIR) not in sys.path:
  sys.path.insert(
    0,
    str(AUDIT_DIR),
  )

from audit_phase144_6_r25_21 import (
  _build_generic,
  _build_legacy_pi6_3,
)


def test_phase144_6_r25_21_legacy_specimen_preserves_numbered_dependency_structure():
  legacy = _build_legacy_pi6_3()

  assert r"\tag{1}" in legacy
  assert r"\tag{20}" in legacy
  assert "(1), (2)" in legacy
  assert "(5), (15)" in legacy
  assert "(8), (14), (18)" in legacy
  assert "(7), (17), (19)" in legacy


def test_phase144_6_r25_21_generic_pi6_3_remains_generic_production_text():
  generic = _build_generic(
    3,
    3,
  )

  assert r"$\nu'$ を定める." in generic
  assert r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$" in generic
