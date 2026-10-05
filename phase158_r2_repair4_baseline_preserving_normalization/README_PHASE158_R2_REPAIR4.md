# Phase 158-R2 repair4

## 方針

Phase 158 は pre-R2 baseline の数学的内容を変更しない。

R2 実行直前の
`phase158_r2_backup_before_apply/toda_group_proof_narrative_renderer.py`
を毎回復元し、その public renderer を baseline renderer として保持する。

Phase 158 wrapper が変更してよいのは次だけ。

- `## 証明対象`
- `## 使用する結果`
- `---`
- `## 証明`
- terminal QED を `□` に正規化

## Production code

対象:
- `toda_group_proof_narrative_renderer.py`

import 変更:
- なし

新規:
- `_phase158_public_narrative_target_lines()`
- `_phase158_strip_terminal_qed_lines()`
- `_phase158_normalize_public_narrative_contract()`
- public wrapper `render_toda_group_proof_narrative_markdown()`

既存 renderer:
- 本体を変更せず
  `_phase158_baseline_render_toda_group_proof_narrative_markdown()`
  へ名前変更。

## 監査

112群すべてについて baseline と normalized を比較する。

必須:
- public contract valid = 112
- Reference payload preserved = 112
- Proof payload preserved = 112
- fully valid = 112
- exceptions = 0

古い個別文字列 expectation を Phase 158 の完了条件にはしない。
Phase 158 前の baseline と比較して content preservation を判定する。

全体 pytest は Phase 158 の最後のみ。
