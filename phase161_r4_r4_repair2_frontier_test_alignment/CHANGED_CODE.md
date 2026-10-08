# Phase 161-R4-R4 repair2 changed code

## production

変更なし。

## テスト

変更:

- `tests/test_phase161_r4_r4_restore_global_frontier.py`

変更内容:

Phase156-R12/R13 の global frontier（全体参照境界）契約を確認するテストでは、
既存テストと同じ

1. `build_toda_group_proof_narrative_reference_entries()`
2. `exclude_toda_group_proof_narrative_root_reference()`
3. `_toda_group_proof_narrative_reference_frontier_step_ids()`

の経路を使用する。

`pi_4^2` public rendering の確認では従来どおり fixed-statement boundary filter
を使用する。

これにより「public Reference 選択」と「lower-level frontier helper 契約」を
混同しない。

更新後テスト全文:

- `output/test_phase161_r4_r4_restore_global_frontier.py.txt`

## import

production import 変更なし。

test import は更新後ファイル全文に含む。

## pytest

全体 pytest は実行しない。
