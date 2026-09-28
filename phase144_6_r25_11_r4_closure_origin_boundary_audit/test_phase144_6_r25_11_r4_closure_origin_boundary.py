from pathlib import Path
import importlib.util
import sys


AUDIT_PATH = (
  Path(__file__).resolve().parent.parent
  / "phase144_6_r25_11_r4_closure_origin_boundary_audit"
  / "audit_r25_11_r4.py"
)


def _load_audit():
  name = "_phase144_6_r25_11_r4_audit"
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


def test_phase144_6_r25_11_r4_closure_preserves_original_step_identity():
  audit = _load_audit()
  _group_result, original, closure = (
    audit.build_depth2_pi6()
  )
  original_ids = audit.presentation_step_ids(
    original
  )
  closure_ids = audit.presentation_step_ids(
    closure
  )

  assert original_ids.issubset(
    closure_ids
  )


def test_phase144_6_r25_11_r4_closure_origin_is_observable_by_identity():
  audit = _load_audit()
  _group_result, original, closure = (
    audit.build_depth2_pi6()
  )
  original_ids = audit.presentation_step_ids(
    original
  )
  closure_ids = audit.presentation_step_ids(
    closure
  )

  assert closure_ids - original_ids
