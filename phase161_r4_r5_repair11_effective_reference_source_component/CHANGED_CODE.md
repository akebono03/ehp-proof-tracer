# Phase 161-R4-R5 repair11 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `_phase154_r5_reference_source_steps_by_number()`

変更後関数全文:

- `output/_phase154_r5_reference_source_steps_by_number.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair11_effective_reference_source_component.py`

必要 import を含むテスト全文:

- `output/test_phase161_r4_r5_repair11_effective_reference_source_component.py.txt`

## 根本原因

Reference 表示では aggregate literature statement（集約文献 statement）から
実際に必要な component（成分）だけを表示している。

しかし Reference-body linkage は aggregate `ProofStep` 自身を source としていた。

そのため Proposition 5.1 では、

表示:

$$
\pi_{n+1}^{n}=\mathbb Z/2\{\eta_n\}
$$

であるにもかかわらず、linkage source は

`Toda Proposition 5.1 finite-dimensional integration`

となり、その nearest visible consumer が一般形そのものになっていた。

## 修正規則

selected Reference step に対して既存の

```python
_phase153_r6_reference_aggregate_component()
```

を使う。

component が選択され、その component を conclusion とする premise step が
一意なら、その premise step を effective linkage source（実効的な参照接続元）
として使用する。

一意でなければ既存 step に fallback する。

Proposition 5.1 / pi_4^2 専用条件は追加しない。

## 完了条件

Reference:

- `[R1] (5.2)`
- `[R2] Proposition 5.1`
- Proposition 5.1 は一般形

本文:

- 一般形を再掲しない
- `[R2]` が具体的 $\pi_4^3$ に付く
- `(5.2)` の $i=4$ specialization
- $\eta_3\mapsto\eta_2\eta_3$
- $\pi_4^2$ の結論
- `□`

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
