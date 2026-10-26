# 実行手順

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3x_source_bound_eta_probe.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3x_source_bound_eta_probe\run.ps1"
```

`AUDIT_ONLY` です。本番コード・既存テスト・既存文書は変更せず、監査パッケージ内の `output` に JSON を書き込みます。実行結果をチャットへ貼り付けてください。
