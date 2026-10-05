# Phase157-R5-R3 changed code

## toda_literature_statement_boundary.py

Import changes: none.

Class changes: none.

New functions: none.

Changed function (complete replacement):

```python
def _proof_step_reference_locator(
  proof_step: ProofStep,
) -> str | None:
  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  reference = inference_rule.literature_reference
  if reference is not None:
    return reference.locator

  rule_name = inference_rule.name

  internal_locator = (
    _PHASE157_R5_R3_INTERNAL_RULE_LOCATORS.get(
      rule_name
    )
  )
  if internal_locator is not None:
    return internal_locator

  for locator in _TRACKED_REFERENCE_LOCATORS:
    if locator.startswith(
      (
        "Proposition ",
        "Lemma ",
        "Equation ",
      )
    ):
      if rule_name.startswith(
        "Toda " + locator
      ):
        return locator

  parenthesized_locators = tuple(
    locator
    for locator in _TRACKED_REFERENCE_LOCATORS
    if (
      locator.startswith("(")
      and locator.endswith(")")
    )
  )

  for locator in parenthesized_locators:
    number = locator[
      1:
      -1
    ]

    if (
      rule_name.startswith(
        "Toda " + locator
      )
      or rule_name.startswith(
        "Toda " + number + " "
      )
    ):
      return locator

  return None
```

Catalog constants are inserted immediately before `_TRACKED_REFERENCE_LOCATORS`.
The exact fixed/internal rule mappings are generated from the user's current
`phase157_r5_r2_catalog_candidates.csv` at apply time. This avoids inventing
rule names that may differ from the local branch.

## tests/test_phase157_r5_r3_boundary_catalog_expansion.py

The complete test file is generated at apply time from the exact R5-R2
candidate pairs. It imports:

```python
from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)
```

The generated test verifies every R5-R2 catalog-candidate locator/rule pair
against its fixed expected classification and component key.
