from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import toda_group_proof_narrative_renderer as renderer


TEST_FILE = Path(
  "tests/test_phase159_pi3_2_public_definition_premise_locality.py"
)


def load_test_module():
  spec = importlib.util.spec_from_file_location(
    "phase159_pi3_2_public_definition_premise_locality",
    TEST_FILE,
  )

  if spec is None or spec.loader is None:
    raise RuntimeError(
      "could not load repair18 locality test module"
    )

  module = importlib.util.module_from_spec(
    spec
  )
  spec.loader.exec_module(
    module
  )
  return module


def main() -> None:
  helper_name = (
    "_phase159_order_public_unique_preimage_definition_premises"
  )
  helper = getattr(
    renderer,
    helper_name,
    None,
  )

  print(
    "=== repair18 ordering helper ==="
  )

  if helper is None:
    print(
      "MISSING: "
      + helper_name
    )
  else:
    print(
      inspect.getsource(
        helper
      )
    )

  module = load_test_module()

  print()
  print(
    "=== repair18 test constants ==="
  )

  names = (
    "ZERO_GROUP",
    "H_INJECTIVE",
    "E_ISOMORPHISM",
    "E_INJECTIVE",
    "DELTA_ZERO",
    "H_SURJECTIVE",
    "H_ISOMORPHISM",
    "PI3_TARGET",
    "ETA2_DEFINITION",
    "FINAL_GROUP",
  )

  for name in names:
    print(
      name
      + " = "
      + repr(
        getattr(
          module,
          name,
          None,
        )
      )
    )

  print()
  print(
    "=== actual paragraphs after repair22 ==="
  )

  paragraphs = tuple(
    module._phase159_pi3_2_public_paragraphs()
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    print(
      str(
        index
      ).rjust(
        2
      )
      + ": "
      + repr(
        paragraph
      )
    )

  print()
  print(
    "=== missing expected constants ==="
  )

  for name in names:
    value = getattr(
      module,
      name,
      None,
    )

    print(
      name
      + ": "
      + (
        "FOUND"
        if value in paragraphs
        else "MISSING"
      )
    )


if __name__ == "__main__":
  main()
