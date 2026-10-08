# Phase 161-R4-R5 repair3 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `link_toda_group_proof_narrative_reference_body_consumers()`

変更後関数全文:

- `output/link_toda_group_proof_narrative_reference_body_consumers.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair3_reference_self_marker_relink.py`

テスト全文と必要 import:

- `output/test_phase161_r4_r5_repair3_reference_self_marker_relink.py.txt`

## 修正規則

既存の graph-backed nearest visible consumer（グラフに基づく最寄りの可視利用先）
探索を再利用する。

本文に

```text
[Rn]より, <Reference statement 自身>
```

があり、その Reference から到達する最寄りの visible non-root consumer が一意なら、
その marker を consumer へ移す。

これにより

```text
[R2]より, pi_{n+1}^n = Z/2{eta_n}.
pi_4^3 = Z/2{eta_3}.
```

を

```text
[R2]より, pi_4^3 = Z/2{eta_3}.
```

へ正規化する。

pi_4^2 専用条件は追加しない。

## Phase 境界

今回変更しない:

- Proposition 5.1 の数学的内容
- Toda (5.2)
- pi_5^3
- pi_6^4
- Phase157 pi_6^3 known regression
- Web Provenance header
- documentation
- 全体 pytest
