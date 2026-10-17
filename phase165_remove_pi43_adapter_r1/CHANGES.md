# Phase 165：群別 Adapter の撤去

変更対象：`phase165_r52_r9_shared_math.py` の import と `shared_expansion_provider()`。`phase165_r52_r23_existing_rule_adapter.py` は別のルート直下の利用者がない場合に削除し、内容を `.txt` に退避する。専用 Adapter に依存する古い監査スクリプトは歴史記録として保持する。

共通候補生成は変更しないため、π4³ の探索が完成することを保証しない。テストは対象限定の３件のみ。全体テストは Phase 終了時に実行する。
