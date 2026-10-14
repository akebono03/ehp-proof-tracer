# Phase 165 R27-R53-R2

この修正版は、R53-R1 の関数外にインデント付き import を挿入してしまう不具合を修正します。

- 対象: `toda_calculation_facade.py` の `build_toda_report()` と `build_standard_toda_report()`。
- 変更: 既存の関数本体を維持したまま、旧 Repository 関連 import を該当関数内へ移動します。
- AST により構文を検証し、既存の関数形が想定外の場合は書き込み前に停止します。
- R52 の型付き API は維持します。
- 既存の Repository モジュールの削除は行いません。
- pytest は修正版の対象テストだけを実行し、全体 pytest は実行しません。

Windows PowerShell:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r53_r2.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r53_r2\run.ps1"
```

R53-R1 が `IndentationError` で停止した場合は、通常、元のソースには変更が書き込まれていません。R2 は構文検証に合格した場合だけ変更を書き込みます。
