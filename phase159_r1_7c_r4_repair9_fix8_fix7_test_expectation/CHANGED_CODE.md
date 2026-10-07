# fix8 変更一覧

## Production

変更なし。

fix7 で適用済みの以下を維持する。

- `toda_literature_statement_boundary.py`
  - Equation locator を `(5.7)`, `(5.8)`, `(5.13)` に統一
- `toda_group_proof_narrative_references.py`
  - named Equation rule の locator 推定を `(N.M)` に統一

## 今回訂正したテスト契約

誤:
```python
assert boundary.classification == (
  TodaLiteratureStatementClassification.PROOF_INTERNAL
)
```

正:
```python
assert boundary.classification == (
  TodaLiteratureStatementClassification.FIXED_STATEMENT
)
assert boundary.reference_locator == "(5.7)"
assert boundary.component_key == "nu_prime_eta6_hopf_relation"
```

## 理由

既存 Phase157-R5-R3 contract では Equation 5.7 は
`fixed_statement / nu_prime_eta6_hopf_relation` として登録済み。

fix7 の補助テストだけが過去契約を誤読していた。

## Phase 境界

- production は追加変更しない
- generator canonicalization は別課題
- pi_4^3 はまだ見ない
- repository-wide pytest は実行しない
