from pathlib import Path
import importlib.util
import sys


COMPARE_PATH = (
  Path(__file__).resolve().parent
  / "compare_r25_11_r6.py"
)


def _load_compare():
  name = "_phase144_6_r25_11_r6_compare"
  if name in sys.modules:
    return sys.modules[name]
  spec = importlib.util.spec_from_file_location(
    name,
    COMPARE_PATH,
  )
  if spec is None or spec.loader is None:
    raise ImportError(
      f"cannot load {COMPARE_PATH}"
    )
  module = importlib.util.module_from_spec(
    spec
  )
  sys.modules[name] = module
  spec.loader.exec_module(module)
  return module


def test_phase144_6_r25_11_r6_retains_historical_190_and_current_192_contract():
  compare = _load_compare()

  assert compare.EXPECTED_HISTORICAL_TOTAL == 190
  assert compare.EXPECTED_CURRENT_TOTAL == 192


def test_phase144_6_r25_11_r6_identity_signature_excludes_insertability():
  compare = _load_compare()

  row = {
    "n": 3,
    "k": 3,
    "argument_role": "establish_order",
    "discourse_role": "middle",
    "statement_type": "Example",
    "rendered": "$x$",
    "provider_anchor": True,
    "placement": "at_provider_anchor",
    "provider_key_count": 2,
    "insertable": False,
  }
  changed = dict(
    row
  )
  changed[
    "insertable"
  ] = True

  assert (
    compare.identity_signature(
      row
    )
    == compare.identity_signature(
      changed
    )
  )
  assert (
    compare.insertion_signature(
      row
    )
    != compare.insertion_signature(
      changed
    )
  )
