# Phase 158-R2 repair2

## 方針変更

R2 / repair1 の変更を積み重ねず、R2 実行直前に自動保存された

`phase158_r2_backup_before_apply/toda_group_proof_narrative_renderer.py`

を exact baseline として復元する。

## Production code 変更

対象:
- `toda_group_proof_narrative_renderer.py`

import 変更:
- なし

### 既存関数

元の `render_toda_group_proof_narrative_markdown()` は本体を変更せず、
`_phase158_baseline_render_toda_group_proof_narrative_markdown()` へ名前変更する。

### 新規関数

ファイル末尾に追加:

- `_phase158_public_narrative_target_lines()`
- `_phase158_normalize_public_narrative_contract()`
- 新しい public `render_toda_group_proof_narrative_markdown()`

新しい public renderer は baseline renderer の出力を受け取り、
depth 2 以上にだけ public shell normalization を適用する。

## 保存する既存仕様

- pi15_8 Proposition 4.4 canonical formula
- pi15_8 generator transport
- 既存 Reference attribution
- 既存 proof body
- depth 1 legacy route

focused test が失敗した場合は audit に進まない。
全体 pytest は Phase 158 の最後まで実行しない。
