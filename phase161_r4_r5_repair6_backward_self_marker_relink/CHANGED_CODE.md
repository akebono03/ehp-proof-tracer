# Phase 161-R4-R5 repair6 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `link_toda_group_proof_narrative_reference_body_consumers()`

変更後関数全文:

- `output/link_toda_group_proof_narrative_reference_body_consumers.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair6_backward_self_marker_relink.py`

必要 import を含むテスト全文:

- `output/test_phase161_r4_r5_repair6_backward_self_marker_relink.py.txt`

## 修正内容

audit により、Proposition 5.1 の self-reference marker は concrete consumer より
後方にあることが確定した。

したがって

```text
pi_4^3 = Z/2{eta_3}

[R3]より, pi_{n+1}^n = Z/2{eta_n}
```

のような順序でも、graph-backed nearest visible consumer が一意なら

```text
[R3]より, pi_4^3 = Z/2{eta_3}
```

へ移す。

後続の Reference filtering / renumbering により final public marker は `[R2]`
となる。

repair4 で追加した marker 0件からの自動 linkage は削除する。
これにより Proposition 4.4 の R2 が `(5.2)` 行へ誤付与される副作用を除去する。

## Phase 境界

今回変更しない:

- 接続語 `これより, 以上より,` の prose normalization
- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ known regression
- Web Provenance header
- documentation
- 全体 pytest
