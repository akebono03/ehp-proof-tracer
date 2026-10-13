# Phase 165 R52-R11 runner 修正

今回の修正はテスト実行スクリプト `run.ps1` のみです。既にインストールした `toda_group_proof_generic_narrative_renderer.py`、`phase165_r52_partial_proof.py`、`test_phase165_r52_r11_common_renderer.py` は変更しません。

必須テスト `test_phase165_r52_r11_common_renderer.py` は必ず実行します。R52-R10 などの過去の関連テストは、プロジェクト直下に存在するものだけを追加実行します。存在しない場合は警告を表示してスキップします。pytest が失敗した場合は終了コードを伝播します。全体 pytest は実行しません。

## 実行方法

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase165_r52_r11_runner_fix.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase165_r52_r11_runner_fix\run.ps1"
```

## 完了条件

- R52-R11 の必須テストが実行されること。
- 導入済みの関連テストが成功すること。
- 群の証明表示を変更しないこと。

次の作業との境界: 証明探索・数学的推論規則の改修は含みません。
