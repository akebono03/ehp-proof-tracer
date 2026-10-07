from __future__ import annotations

import importlib.util
from pathlib import Path


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
      "could not load test module"
    )

  module = importlib.util.module_from_spec(
    spec
  )
  spec.loader.exec_module(
    module
  )
  return module


def main() -> None:
  if not TEST_FILE.exists():
    raise FileNotFoundError(
      "missing local repair18 test file: "
      + str(
        TEST_FILE
      )
    )

  module = load_test_module()

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

  print(
    "=== repair18 expected paragraph constants ==="
  )

  for name in names:
    value = getattr(
      module,
      name,
      None,
    )
    print(
      name
      + " = "
      + repr(
        value
      )
    )

  paragraphs_fn = getattr(
    module,
    "_phase159_pi3_2_public_paragraphs",
    None,
  )

  if paragraphs_fn is None:
    raise RuntimeError(
      "_phase159_pi3_2_public_paragraphs not found"
    )

  paragraphs = tuple(
    paragraphs_fn()
  )

  print()
  print(
    "=== actual public paragraphs ==="
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
    "=== expected constants found? ==="
  )

  for name in names:
    value = getattr(
      module,
      name,
      None,
    )
    found = (
      value in paragraphs
      if value is not None
      else False
    )
    print(
      name
      + ": "
      + (
        "FOUND"
        if found
        else "MISSING"
      )
    )

  print()
  print(
    "=== nearest containment candidates for missing constants ==="
  )

  for name in names:
    value = getattr(
      module,
      name,
      None,
    )

    if (
      value is None
      or value in paragraphs
      or not isinstance(
        value,
        str,
      )
    ):
      continue

    tokens = tuple(
      token
      for token in (
        r"\pi_{2}^{1}",
        r"\pi_{3}^{3}",
        r"E: \pi_{1}^{1}",
        r"H: \pi_{3}^{2}",
        r"\Delta: \pi_{3}^{3}",
        r"H(\eta_{2})",
        r"\pi_{3}^{2} = ",
      )
      if token in value
    )

    candidates = tuple(
      paragraph
      for paragraph in paragraphs
      if any(
        token in paragraph
        for token in tokens
      )
    )

    print(
      name
      + ":"
    )

    for paragraph in candidates:
      print(
        "  actual = "
        + repr(
          paragraph
        )
      )


if __name__ == "__main__":
  main()
