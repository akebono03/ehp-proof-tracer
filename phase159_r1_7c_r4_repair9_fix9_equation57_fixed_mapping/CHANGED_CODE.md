# 変更対象

## Production

`toda_literature_statement_boundary.py`

変更対象:
`_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME` 内の

```python
"Toda Equation 5.7 nu-prime eta_6 Hopf value": "Equation 5.7"
```

または同等の single-quote 表記。

変更後:

```python
"Toda Equation 5.7 nu-prime eta_6 Hopf value": "(5.7)"
```

## import

変更なし。

## class / function

関数・クラスの実装変更なし。
module-level fixed-rule mapping の locator 値だけを変更。

## Tests

新規 focused test:
`test_phase159_r1_7c_r4_repair9_fix9.py`

確認:
- FIXED_STATEMENT を維持
- component_key を維持
- boundary locator と rule-name inference がともに `(5.7)` になる

## Phase 境界

- renderer は変更しない
- Equation 5.7 の数学的 statement は変更しない
- Proposition 2.2 dependency は変更しない
- generator canonicalization は別課題
- repository-wide pytest は実行しない
