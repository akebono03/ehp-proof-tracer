# Phase 159-R1-7b repair5

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase158_normalize_public_narrative_contract`

### Tests
- 新規変更なし。
- repair4 で更新済みの focused tests を再実行する。

## import

production import の変更はありません。

repair5 の apply script は `ast` を使用しますが、
これは ZIP 内適用スクリプトの import です。

## 原因

repair3 の `insert_normalizer_call()` は、source 全体に

`_phase159_r1_7b_normalize_public_exact_sequences`

という文字列が存在すると「call 済み」と判定していました。

しかし helper definition 自体にも同じ名前が含まれるため、
helper を追加した直後に early return し、
`_phase158_normalize_public_narrative_contract()` への call が
追加されませんでした。

## 変更後の対象部分

`_phase158_normalize_public_narrative_contract()` 内で、
既存の equation-number normalization の直後を次の形にします。

```python
  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )
  proof_body = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      presentation,
      proof_body,
    )
  )
```

## 完了条件

- AST verification で R1-7b normalizer call が exactly one。
- focused tests が PASS。
- `pi6_3.md` で short exact sequence が display math。
- `pi11_4.md` で対応 exactness が `完全性より, Δ...は全射.` より前。
- full pytest は Phase 159 最後まで実行しない。

## 次 Phase との境界

R1-7b repair5 では exact-sequence display/order のみを閉じる。

以下はまだ行わない。
- `2ν' = η3η4η5 = η3^3` への統合
- equation numbering policy
- Reference aggregate suppression
- map-property prose の全面統一
