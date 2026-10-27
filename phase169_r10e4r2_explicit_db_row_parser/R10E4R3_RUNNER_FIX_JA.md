# R10E4-R3 — PowerShell 実行スクリプトの修正

この配布物は R10E4-R2 に含まれる `run.ps1` の **2行のみ**を置き換えます。

修正対象：
- 25行目：Git の差分一覧のパス区切り正規化
- 44行目：テスト・監査後の同じ処理

`.Replace('', '/')`（空文字列を置換）を `.Replace('\', '/')`（Windows のバックスラッシュを置換）に修正しました。

本番 Python ソース、既存テスト、既存 README.md は変更しません。
R10E4-R2 のすべてのファイルがすでに展開済みであることが前提です。

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r10e4r3_powershell_replace_fix.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r10e4r2_explicit_db_row_parser\run.ps1"
```

終了条件：
- `R10E4R2_INTEGRITY_RESULT=PASS`
- `R10E4R2_LIMITED_TESTS_AND_AUDIT=PASS`

失敗時は元の `run.ps1` 内の `finally` が今回の Python 修正をロールバックします。
**全体 pytest は実行しません。**
