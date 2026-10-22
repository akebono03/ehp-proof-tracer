# 変更対象

- `phase165_r52_r4_flask_bridge.py` — `build_group_proof_progress_view()` 全文置換。import の変更なし。
- 新規 `tests/test_phase168_r3_20_flask_actual_cutover.py` — Flask POST を含む限定3テスト。import・関数全文を収録。
- 関数全文: `build_group_proof_progress_view_FULL.py`。

## 完了条件

通常の `group` / `group_proof` POST が model 経路を呼ぶこと、明示的な探索入力が従来動作を保つこと。全体 pytest は実施しない。

## 次工程

証明の型付き文章化、Reference 統一、旧 Renderer の削除は本修正では行わない。
