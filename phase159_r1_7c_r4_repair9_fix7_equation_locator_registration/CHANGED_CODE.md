# 変更対象

## Production

### 1. `toda_literature_statement_boundary.py`

変更対象:
- `_EQUATION_513_COMPONENTS`
- `_FIXED_COMPONENTS_BY_REFERENCE`
- `_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME`
- `_PHASE157_R5_R3_ADDITIONAL_COMPONENTS`
- `_PHASE157_R5_R3_INTERNAL_RULE_LOCATORS`
- Phase157-R5-R3 `_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.update(...)`

import 変更なし。

変更内容:
- `"Equation 5.7"` -> `"(5.7)"`
- `"Equation 5.8"` -> `"(5.8)"`
- `"Equation 5.13"` -> `"(5.13)"`
- `Toda Equation 5.7 ...` rule name には internal locator `(5.7)` を明示して、
  既存の PROOF_INTERNAL classification を保持する。

### 2. `toda_group_proof_narrative_references.py`

変更関数:
`_infer_toda_group_proof_literature_reference_from_rule_name()`

import 変更なし。

変更後関数全体:

```python
def _infer_toda_group_proof_literature_reference_from_rule_name(
  rule_name: str,
) -> LiteratureReference | None:
  if not isinstance(rule_name, str):
    raise TypeError("rule_name must be a str")

  normalized_rule_name = rule_name.lower()

  if "bridge" in normalized_rule_name:
    return None

  named_match = re.match(
    r"^Toda (Proposition|Lemma|Theorem|Equation) ([0-9]+(?:\.[0-9]+)*)\b",
    rule_name,
  )
  if named_match is not None:
    kind, number = named_match.groups()

    if kind == "Equation":
      locator = f"({number})"
    else:
      locator = f"{kind} {number}"

    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  parenthesized_match = re.match(
    r"^Toda \(([0-9]+(?:\.[0-9]+)*)\)\b",
    rule_name,
  )
  if parenthesized_match is not None:
    number = parenthesized_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  bare_equation_match = re.match(
    r"^Toda ([0-9]+\.[0-9]+)\b",
    rule_name,
  )
  if bare_equation_match is not None:
    number = bare_equation_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  return None
```

## Tests

変更:
- `tests/test_phase157_r5_r3_boundary_catalog_expansion.py`
  - Equation 5.7 -> (5.7)
  - Equation 5.8 -> (5.8)

- `tests/test_phase157_r4_r2_boundary_catalog.py`
  - Equation 5.13 -> (5.13)

- `tests/test_phase156_r5_repair4_bridge_reference_inference.py`
  - named Equation が `(5.7)` を推定する focused test を追加

新規:
- `phase159_r1_7c_r4_repair9_fix7_equation_locator_registration/test_phase159_r1_7c_r4_repair9_fix7.py`

## Phase 境界

- renderer の title normalizer は追加しない
- generator canonicalization は別課題
- pi_4^3 はまだ見ない
- repository-wide pytest は実行しない
