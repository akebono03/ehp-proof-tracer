# Phase 161-R4-R5 repair9a changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

変更後関数全文:

- `output/render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt`

import 変更なし。

### 新規テスト

- `tests/test_phase161_r4_r5_repair9a_final_public_reference_relink.py`

必要 import を含むテスト全文:

- `output/test_phase161_r4_r5_repair9a_final_public_reference_relink.py.txt`

## repair9 package failure の修正

repair9 は production write 前に `ast.parse(TEST_SOURCE)` で失敗したため、
production 変更は適用されていない。

repair9a では test source を apply script 内に文字列埋め込みせず、
package 内の `.template.py` ファイルとして保持し、そのまま `tests/` にコピーする。

## production 修正

final public Reference filtering / restoration / renumbering がすべて完了した後に、

```python
link_toda_group_proof_narrative_reference_body_consumers(
  presentation,
  rendered,
  reference_entries,
)
```

を1回適用する。

これにより final public Reference 番号で

$$
[R2]\text{より, }\pi_4^3=\mathbb Z/2\{\eta_3\}
$$

を接続する。

## 完了条件

Reference:

- `[R1] (5.2)`
- `[R2] Proposition 5.1`
- Proposition 5.1 は一般形

本文:

- Proposition 5.1 一般形を再掲しない
- `[R2]` が具体的 $\pi_4^3$ に付く
- `(5.2)` の $i=4$ specialization を維持
- $\eta_3\mapsto\eta_2\eta_3$ を維持
- $\pi_4^2$ 結論と `□` を維持

## Phase 境界

今回は以下を変更しない。

- `これより, 以上より,` の prose normalization
- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ known regression
- Web Provenance header
- documentation
- 全体 pytest
