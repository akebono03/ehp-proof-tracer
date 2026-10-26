# Phase 169 R3S1 実行手順

リポジトリルートで ZIP を展開し、次を実行してください。

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3s1_composite_scope_fix.zip" `
  -DestinationPath "." `
  -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3s1_composite_scope_fix\run.ps1"
```

R3S が失敗して元ファイルへ復元された状態から実行できます。
変更対象は `phase168_r3_37c_reference_projection.py` の
`project_reference_bodies()` 関数だけです。import 部分は変更しません。
全関数は `full_functions/project_reference_bodies_FULL.py` に、
適用後のファイル全文は `output/phase168_r3_37c_reference_projection.py` に保存します。
異常があれば R3S1 のバックアップから復元します。

限定 pytest は新規4件、R3S既存4件、既存 Reference 3件、
1-stem 回帰10件。全体テストは実行しません。
