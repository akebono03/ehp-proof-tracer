# Phase 158-R2 repair3

## 原因

repair2 の apply script が生成ファイル末尾へ literal `\n` を書き込み、
`toda_group_proof_narrative_renderer.py` を SyntaxError にした。

target 補完用 TeX delimiter も single backslash の `\[` / `\]` に修正する。

## Production code

対象:
- `toda_group_proof_narrative_renderer.py`

import 変更:
- なし

R2 実行直前の
`phase158_r2_backup_before_apply/toda_group_proof_narrative_renderer.py`
から毎回復元する。

既存 public renderer 本体は変更せず、
`_phase158_baseline_render_toda_group_proof_narrative_markdown()`
へ名前変更する。

追加:
- `_phase158_public_narrative_target_lines()`
- `_phase158_normalize_public_narrative_contract()`
- wrapper `render_toda_group_proof_narrative_markdown()`

## 実行順

1. baseline 復元 + wrapper 適用
2. `py_compile`
3. focused test
4. 112群 audit
5. summary

全体 pytest は Phase 158 最後のみ。
