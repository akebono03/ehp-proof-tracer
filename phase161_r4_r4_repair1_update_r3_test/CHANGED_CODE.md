# Phase 161-R4-R4 repair1 changed code

## production

変更なし。

## テスト

変更ファイル:

- `tests/test_phase161_r4_r3_fixed_frontier_internal_ancestry.py`

変更理由:

R4-R4 で削除した temporary helper（暫定 helper）を R4-R3 test が import
し続けていたため、pytest collection error になっていた。

更新後は current API（現行 API）:

- `_toda_group_proof_narrative_root_fixed_statement_internal_step_ids()`
- `_toda_group_proof_narrative_reference_internal_step_ids()`
- `_toda_group_proof_narrative_reference_frontier_step_ids()`

を使用する。

テストファイル全文は:

- `output/test_phase161_r4_r3_fixed_frontier_internal_ancestry.py.txt`

に出力する。

## import

production import 変更なし。

test import は更新後テストファイル全文に含む。

## pytest

focused:

- Phase161 R4-R4
- Phase161 R4-R3
- Phase161 R4 repair1
- Phase161 R4
- Phase161 R3

regression:

- Phase156 R12/R13 frontier
- Phase156 R8 owned ancestry（既知 stale 1件を除外）
- Phase59 relevant
- Phase160 k=2

全体 pytest は Phase161 終了時まで実行しない。
