# Phase 159-R1-6b repair3

## 変更対象

- `toda_literature_statement_boundary.py`
  - `_FIXED_RULE_COMPONENT_KEYS`
  - `_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME`

import:
- 変更なし

class:
- 変更なし

function / method:
- 変更なし

test:
- 変更なし

## `_FIXED_RULE_COMPONENT_KEYS` への追加

dictionary の先頭に以下を追加する。

```python
  "Toda Equation 5.7 nu-prime eta_6 Hopf value": (
    "nu_prime_eta6_hopf_relation"
  ),
```

## `_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME` への追加

dictionary の先頭に以下を追加する。

```python
  "Toda Equation 5.7 nu-prime eta_6 Hopf value": "Equation 5.7",
```

## 修正理由

diagnostic の結果、不一致は 36 CASES 中1件のみ。

```text
CASE 14
locator: Equation 5.7
rule_name: Toda Equation 5.7 nu-prime eta_6 Hopf value
expected:
  fixed_statement
  Equation 5.7
  nu_prime_eta6_hopf_relation
actual:
  proof_internal
  Equation 5.7
  None
```

`nu_prime_eta6_hopf_relation` component 自体は既存 catalog にあるため、
新しい component を追加する必要はない。

不足している rule-name → fixed component / locator mapping だけを補う。

## 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase49_low_dimensional_facts.py" `
  ".\tests\test_phase49_generator_transport.py"
```

## 完了条件

- Phase157-R5-R3 catalog test PASS。
- R1-6 focused tests PASS。
- Phase159 focused tests PASS。
- related regressions PASS。
- `git diff --check` PASS。
- pi_3^2 の `[R1] (5.1)` と map-property numbering を維持。

## 次 Phase との境界

- 今回は Equation 5.7 の既存 catalog mapping 修復のみ。
- `(5.1)` body linkage の追加は行わない。
- full pytest は Phase 159 最後のみ。
