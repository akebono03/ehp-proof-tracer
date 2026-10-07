from tests.test_phase157_r5_r3_boundary_catalog_expansion import (
  CASES,
  _step,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


def main():
  mismatches = []

  for index, (
    locator,
    rule_name,
    expected_classification,
    expected_component,
  ) in enumerate(
    CASES,
    start=1,
  ):
    boundary = classify_toda_literature_statement_step(
      _step(
        locator,
        rule_name,
      )
    )

    actual = (
      None
      if boundary is None
      else (
        boundary.classification.value,
        boundary.reference_locator,
        boundary.component_key,
      )
    )
    expected = (
      expected_classification,
      locator,
      expected_component,
    )

    if actual != expected:
      mismatches.append(
        (
          index,
          locator,
          rule_name,
          expected,
          actual,
        )
      )

  print(
    "Phase 159-R1-6b repair3 diagnosis"
  )
  print(
    "CASES:",
    len(
      CASES
    ),
  )
  print(
    "mismatches:",
    len(
      mismatches
    ),
  )
  print()

  for (
    index,
    locator,
    rule_name,
    expected,
    actual,
  ) in mismatches:
    print(
      "CASE",
      index,
    )
    print(
      " locator:",
      locator,
    )
    print(
      " rule_name:",
      rule_name,
    )
    print(
      " expected:",
      expected,
    )
    print(
      " actual:",
      actual,
    )
    print()

  if not mismatches:
    print(
      "No mismatch found."
    )


if __name__ == "__main__":
  main()
