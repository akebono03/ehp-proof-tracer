# Phase 161-R4-R5 repair4 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `link_toda_group_proof_narrative_reference_body_consumers()`

変更後関数全文:

- `output/link_toda_group_proof_narrative_reference_body_consumers.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair4_zero_marker_consumer_linkage.py`

必要 import を含むテスト全文:

- `output/test_phase161_r4_r5_repair4_zero_marker_consumer_linkage.py.txt`

## 修正内容

Reference marker が本文に 0 件の場合でも、

1. existing graph-backed consumer search を使う
2. nearest visible non-root consumer が一意であることを要求する
3. その consumer に `[Rn]より, ` を付与する

という一般規則を追加する。

既存の

- marker-only relocation
- self-reference marker relocation

は維持する。

## 今回の完了条件

Reference:

$$
\pi_{n+1}^{n}=\mathbb Z/2\{\eta_n\}
$$

を Proposition 5.1 として表示。

本文:

$$
[R2]\text{より, }\pi_4^3=\mathbb Z/2\{\eta_3\}.
$$

を表示。

さらに `(5.2)` の $i=4$ specialization、生成元 transport、最終結論、`□`
を維持する。

## Phase 境界

変更しない:

- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ known regression
- Web Provenance header
- documentation
- 全体 pytest
