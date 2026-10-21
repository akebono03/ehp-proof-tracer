# R3-AG 変更対象

既存ファイル・クラス・関数・メソッドは変更しない。

新規 `phase166_r3ag_actual_search_audit/audit.py`：`analyze_case`、`audit`、`main` を新規作成。DB の目標と命題台帳の Reference を区別して監査する。

新規 `phase166_r3ag_actual_search_audit/test_r3ag.py`：限定テスト2件（import 全文含む）。

`run.ps1`：監査および限定 pytest のみ実行。`report.json`：実行時に出力。

完了条件：9群の目標取得・掲載境界・実探索の状態を報告すること。すべて COMPLETE であることは要求しない。次 Phase は監査結果で確定する。本体コードおよびプロジェクト既存ドキュメントは変更しない。
