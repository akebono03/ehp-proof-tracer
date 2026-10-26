# Phase 169 R3R 実行手順

リポジトリのルートから PowerShell で実行します。

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3r_source_dependency_audit.zip" `
  -DestinationPath "." `
  -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3r_source_dependency_audit\run.ps1"
```

出力は `phase169_r3r_source_dependency_audit/output/r3r_audit.json` に保存します。監査専用で、本番・既存テスト・文書を変更しません。全体 pytest は実行しません。
