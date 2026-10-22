# Phase 168 R2-1 診断の属性参照修正版

本体コードは変更せず、診断スクリプトの `snapshot()` だけを修正します。`publication_position` は `LiteratureEntry` から取得し、`component_position` は `AssertionEntry` から取得します。

リポジトリ直下へ展開し、PowerShell から次を実行してください。

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_1_trace_fix\run.ps1"
```

出力先は `phase168_r2_1_trace_fix/results.json` です。実装コード、DB、既存テストは変更しません。全体 pytest は実行しません。
