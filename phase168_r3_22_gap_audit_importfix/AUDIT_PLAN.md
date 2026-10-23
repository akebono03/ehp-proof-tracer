# R3-22 実行時ギャップ監査（import 修正版）

変更対象：`run.ps1` の実行方法のみ。`audit.py` の監査処理および同梱した3群の固定原文は変更しない。

原因：`python <package>/audit.py` 形式で実行したため、リポジトリルートの import 経路が保証されなかった。

対策：ルートから `python -m phase168_r3_22_gap_audit_importfix.audit` を実行し、`PYTHONPATH` にリポジトリルートを明示する。

完了条件：4群の実行時監査が終了し、`output/runtime_gap_report.json` と `output/summary.md` が生成され、エラーが空であること。これは文章品質の合格とは別。

次工程：監査結果を確認して、証明木にあるが表示されない命題・文章構成・引用の問題を分類する。今回はアプリ本体、テスト、全文書の変更および全体 pytest を行わない。
