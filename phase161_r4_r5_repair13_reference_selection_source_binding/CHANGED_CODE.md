# Phase 161-R4-R5 repair13 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

新規関数:

- `_select_toda_group_proof_narrative_reference_entries_and_statement_lines()`
- 追加位置:
  `_toda_group_proof_narrative_reference_statement_lines_by_number()` の直前

変更関数:

- `_toda_group_proof_narrative_reference_statement_lines_by_number()`
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

各関数全文:

- `output/_select_toda_group_proof_narrative_reference_entries_and_statement_lines.py.txt`
- `output/_toda_group_proof_narrative_reference_statement_lines_by_number.py.txt`
- `output/render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair13_reference_selection_source_binding.py`

必要 import を含む全文:

- `output/test_phase161_r4_r5_repair13_reference_selection_source_binding.py.txt`

## 修正の考え方

Reference は public Narrative pipeline の前半ですでに選択されている。

問題は、その時点で

- Reference locator
- 表示する statement

は確定している一方、

- その statement を代表する source proof step

が Reference entry に反映されていないこと。

repair13 では、Reference statement selection と同じ処理の中で、
表示された fixed component を代表する step が一意なら、
`entry.proof_steps` の aggregate step をその fixed component step に置換する。

以後の root exclusion / filtering / restoration / body linkage は
すべてこの正規化済み Reference entry を使う。

## 完了条件

Reference:

- `[R1] (5.2)`
- `[R2] Proposition 5.1`
- Proposition 5.1 は一般形

本文:

- Proposition 5.1 の一般形を再掲しない
- `[R2]` が具体的 $\pi_4^3$ に付く
- `(5.2)` の $i=4$ specialization
- $\eta_3\mapsto\eta_2\eta_3$
- $\pi_4^2$ の結論
- `□`

を維持する。

## 次 Phase との境界

今回変更しない:

- `これより, 以上より,` の prose normalization
- Web Provenance header
- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ known regression
- documentation
- 全体 pytest
