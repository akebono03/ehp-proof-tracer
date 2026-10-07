# Phase 159-R1-7b repair10

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_exactness_step_latex`

### Tests
新規変更なし。

## import

production import の変更はありません。

`render_toda_proof_statement_latex` と
`TodaProp42ExactnessStatement` は既に import 済みです。

## 変更後関数全文

```python
def _phase159_r1_7b_exactness_step_latex(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion

  if not isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    return None

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  if rendered is None:
    return None

  suffix = (
    r" \text{ is exact}"
  )

  if not rendered.endswith(
    suffix
  ):
    return None

  return rendered[
    :-len(
      suffix
    )
  ]
```

## 修正理由

repair9 smoke check により semantic closure の exactness candidate は

- `\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} \\xrightarrow{Δ} \\pi_{8}^{2}`
- `\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5}`

であることが確認された。

H-Delta candidate の map label が Unicode `Δ` であり、
public Narrative contract の canonical LaTeX `\\Delta` と一致しなかった。

独自に `Δ -> \\Delta` を変換するのではなく、
既存 `render_toda_proof_statement_latex()` が
`TodaProp42ExactnessStatement` を canonical LaTeX で描画するため、
これを再利用し、末尾の `\\text{ is exact}` だけ除去する。

## 実行する pytest

- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase148_rc2_3_exactness_exposure.py`
- `tests/test_phase148_rc2_3_repair_r1.py`

full pytest は Phase 159 最後まで実行しない。

## 完了条件

- canonical H-Delta exactness smoke check PASS
- canonical E-H exactness smoke check PASS
- `$...$.` parser smoke check PASS
- focused tests PASS
- pi6_3 short exact sequence の中央表示維持
- pi11_4 E-H exactness の中央表示
- pi11_4 H-Delta exactness が Delta 全射の前に中央表示

## 次 Phase との境界

R1-7b では exact-sequence display/order のみを扱う。
連続等式統合、equation numbering、Reference aggregate suppression、
map-property prose 全体統一はまだ扱わない。
