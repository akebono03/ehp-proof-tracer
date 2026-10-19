# Phase 165 R6-8 — 共通 import 依存経路の確定

このパッケージは R6-8 の原因確定を行う。既存の `phase165_r6_dependency_audit/audit.py` を再利用する。旧規則や旧 Renderer を復活させず、テストを削除しない。

## 変更対象

新規ファイルのみ：`phase165_r6_8_dependency_chain/run.ps1`、`summarize.py`、`README.md`。既存コードのクラス・関数・import・テストは変更しない。

## 実行

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r6_8_dependency_chain.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_8_dependency_chain\run.ps1"
```

## 必要な既存ファイル

- `phase165_r6_audit_results/collection_close/triage_130.json`
- `phase165_r6_dependency_audit/audit.py`

## 出力

- `phase165_r6_audit_results/collection_close/r6_8_dependency_chains.json`
- `phase165_r6_audit_results/collection_close/r6_8_summary.json`

## R6-8 完了条件と境界

105件のうち、旧 probe に至る静的依存経路が証明できた件数と未解決件数を確定する。解析結果に応じて必要最小の修正箇所を決める。静的依存解析だけで105件の収集エラーが修正されたとは判定しない。収集の再実行や本体コードの変更はこのパッケージでは行わない。全体 pytest は Phase 165 の最後にだけ行う。R6-9（他25件の原因対応）は扱わない。
