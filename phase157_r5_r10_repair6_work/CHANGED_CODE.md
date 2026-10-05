# Phase157 R5-R10 repair6

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更する関数:

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`

Reference/Proof の正式な section structure を組み立てる直前で、
proof body が次の legacy intro で始まる場合のみ除去する。

```text
使用する結果を先にまとめる.
```

これは旧表示上の導入文であり、`## 使用する結果` が導入された後は重複となる。

### `tests/test_phase157_r5_r10_reference_proof_boundary_qed.py`

proof body 内に legacy intro が残らないことを追加確認。

## Phase 境界

proof body relevance の本体修正
（不要 map 除外、必要 group statement の配置）は次の R11 で扱う。
