# Phase 165 R6-1 R3 — Final candidate triage

既存の `phase165_r6_1_r2_classification/classification.json` を再利用する読み取り専用監査。389 Python ファイルを再走査しない。

## 対象ファイル

新規: `phase165_r6_1_r3_final_triage/audit.py` の `classify_candidate()`、`run()`、`test_audit.py` の3テスト、`run.ps1`。既存 production code と既存テストは変更しない。

## 実行

リポジトリのルートで ZIP を展開後:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_1_r3_final_triage\run.ps1"
```

出力は `triage.json` と `triage.md`。116件を行番号・条件・静的import経路付きで列挙する。分類は撤去の確定ではなく、群専用処理と数学的型条件の混同を防ぐための一次判定。全体pytestは実行しない。

## 完了条件

既存分類JSONを読み込み、116件の詳細一覧と既知の1 Adapterを提示できること。実行結果に基づき、7件と109件の意味を確認してからR6-1を閉じる。R6-2の逆向き規則生成、Adapter削除は行わない。
