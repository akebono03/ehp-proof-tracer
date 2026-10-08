# Phase 161-R4-R5 repair12 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `_phase154_r5_reference_source_steps_by_number()`

変更後関数全文:

- `output/_phase154_r5_reference_source_steps_by_number.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair12_fixed_component_source_resolution.py`

必要 import を含むテスト全文:

- `output/test_phase161_r4_r5_repair12_fixed_component_source_resolution.py.txt`

## 根本原因

repair11 は aggregate statement（集約 statement）の component を得た後、
aggregate の内部 premise を linkage source にした。

しかし proof graph の向きは、

```text
aggregate Proposition 5.1
  -> fixed higher-eta component
  -> pi_4^3 specialization
```

である。

したがって aggregate の premise から探索すると、一般形 component が依然として
nearest visible consumer になる。

また repair11 では effective source を追加した後も `entry.proof_steps` から
aggregate step 自身を再追加していた。

## 修正規則

表示対象となった component と同じ conclusion を持つ presentation step のうち、

- `FIXED_STATEMENT`
- Reference locator が entry と一致
- `component_key is not None`

を満たす step が一意なら、その **fixed component step 自身**を linkage source とする。

置換された aggregate step は fallback source として再追加しない。

一意に解決できない場合だけ従来 step に fallback する。

## 完了条件

Reference:

$$
[R1]\ (5.2),
$$

$$
[R2]\ \mathrm{Proposition\ 5.1}:
\pi_{n+1}^{n}=\mathbb Z/2\{\eta_n\}.
$$

本文:

$$
[R2]\text{より, }\pi_4^3=\mathbb Z/2\{\eta_3\}.
$$

さらに `(5.2)` の $i=4$ specialization、generator transport、最終結論、`□`
を維持する。

## 次 Phase との境界

今回変更しない:

- `これより, 以上より,` の prose normalization
- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ known regression
- Web Provenance header
- documentation
- 全体 pytest
