# Phase 165 R6-2 R1：import 経路修正

変更範囲：監査 ZIP 内の `run.ps1` の全文のみ。本番 Python コード、推論規則、数学的命題、テスト関数を変更しません。

`PYTHONPATH` にリポジトリ直下と監査フォルダを明示してから監査・限定 pytest を実行し、最後に元の設定に戻します。監査結果は `report.json` に保存されます。`phase165_r8_rule_provider.py` が実際にない場合は明示的に停止します。

完了条件：監査結果と限定 pytest が成功すること。R6-2 R2 の汎用逆向き推論の実装、π₄³ 専用 Adapter の撤去は対象外。全体 pytest は実行しません。
