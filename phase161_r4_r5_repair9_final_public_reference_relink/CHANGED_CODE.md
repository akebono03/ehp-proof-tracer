# Phase 161-R4-R5 repair9 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

変更内容:

final public Reference filtering / restoration / renumbering がすべて完了した後、
既存の

```python
link_toda_group_proof_narrative_reference_body_consumers()
```

を最終的にもう一度適用する。

これにより内部番号ではなく **最終 public Reference 番号** と **最終 body** を使って
Reference → concrete consumer linkage を確定する。

変更後関数全文:

- `output/render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair9_final_public_reference_relink.py`

必要 import を含む全文:

- `output/test_phase161_r4_r5_repair9_final_public_reference_relink.py.txt`

## 完了条件

Reference:

$$
[R1]\ (5.2),
$$

$$
[R2]\ \text{Proposition 5.1}:
\pi_{n+1}^{n}=\mathbb Z/2\{\eta_n\}.
$$

本文:

$$
[R2]\text{より, }\pi_4^3=\mathbb Z/2\{\eta_3\}.
$$

続いて `(5.2)` の $i=4$ specialization、生成元 transport、最終結論、`□`
を維持する。

## 次 Phase との境界

今回扱わない:

- `これより, 以上より,` の prose normalization
- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ known regression
- Web Provenance header
- documentation
- 全体 pytest
