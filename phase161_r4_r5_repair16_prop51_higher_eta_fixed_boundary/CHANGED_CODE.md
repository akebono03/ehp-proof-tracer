# Phase 161-R4-R5 repair16 changed code

## 変更対象

### `toda_literature_statement_boundary.py`

変更定数:

- `_FIXED_RULE_COMPONENT_KEYS`
- `_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME`

import 変更なし。
class 変更なし。
function / method 変更なし。

変更後の各辞書全文は package 内の以下に出力される。

- `output/_FIXED_RULE_COMPONENT_KEYS.py.txt`
- `output/_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.py.txt`

## 追加する boundary

```python
_FIXED_RULE_COMPONENT_KEYS[
  "Toda Proposition 5.1 higher eta group relation"
] = "higher_eta_group_relation"
```

```python
_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME[
  "Toda Proposition 5.1 higher eta group relation"
] = "Proposition 5.1"
```

これにより

```text
Toda Proposition 5.1 higher eta group relation
```

は

- classification: `FIXED_STATEMENT`
- locator: `Proposition 5.1`
- component_key: `higher_eta_group_relation`

となる。

## 新規テスト

- `tests/test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.py`

必要 import を含む全文は:

- `output/test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.py.txt`

## 完了条件

Reference:

- `[R1] (5.2)`
- `[R2] Proposition 5.1`
- R2 は一般形
  `$\\pi_{n+1}^{n}=\\mathbb Z/2\\{\\eta_n\\}$`
- concrete `$\\pi_4^3$` は Reference に置かない

本文:

- Proposition 5.1 一般形を再掲しない
- `[R2]` が concrete `$\\pi_4^3$` に付く
- `(5.2)` の `$i=4$` specialization を維持
- generator transport を維持
- target conclusion と `□` を維持

## 次 Phase との境界

今回変更しない:

- `これより, 以上より,` の prose normalization
- Web Provenance header
- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ の別 regression
- documentation
- 全体 pytest
