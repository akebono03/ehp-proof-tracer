# Phase 169 R3N1 — import 欠落修正

修正対象は `phase169_r3n_prior_result_search/tests/test_r3n_prior_result_alias.py` の import 1 行のみ。

**本番コード・命題台帳・DB・他のテストは変更しません。**

発生していた `NameError: name 'eta' is not defined` に対して、`from expression import ... eta, nu` とする。

## 適用

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3n1_test_import_fix.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3n1_test_import_fix\run.ps1"
```

本 ZIP はテストファイルの全文を収録する。`run.ps1` は既存の R3N インストーラーを再実行するが、R3N の `apply.py` は導入済みパッチに対して冪等である。
R3N の限定テストと 1-stem 回帰テストの後、R3N の既存 Web 監査を実行する。全体 pytest は実行しない。
