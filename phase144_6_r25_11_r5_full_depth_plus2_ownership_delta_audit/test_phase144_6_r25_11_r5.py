from pathlib import Path
import importlib.util
import sys


AUDIT_PATH = (
  Path(__file__).resolve().parent
  / "audit_r25_11_r5.py"
)


def _load_audit():
  name = "_phase144_6_r25_11_r5_audit"
  if name in sys.modules:
    return sys.modules[name]
  spec = importlib.util.spec_from_file_location(
    name,
    AUDIT_PATH,
  )
  if spec is None or spec.loader is None:
    raise ImportError(
      f"cannot load {AUDIT_PATH}"
    )
  module = importlib.util.module_from_spec(
    spec
  )
  sys.modules[name] = module
  spec.loader.exec_module(module)
  return module


def test_phase144_6_r25_11_r5_expected_baseline_is_not_rebased():
  audit = _load_audit()

  assert audit.EXPECTED_TOTAL == 190
  assert audit.EXPECTED_PI6 == 5
  assert audit.EXPECTED_PARTICIPATING == 33
  assert audit.EXPECTED_DETACHED == 157
  assert audit.EXPECTED_DETACHED_INSERTABLE == 0


def test_phase144_6_r25_11_r5_targets_match_six_group_audit_boundary():
  audit = _load_audit()

  assert audit.TARGETS == (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
  )
