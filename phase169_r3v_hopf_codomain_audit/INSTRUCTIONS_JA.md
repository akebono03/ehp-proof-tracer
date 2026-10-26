# Phase 169 R3V — 実行方法

Git `develop` ブランチのリポジトリ直下に展開してください。

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3v_hopf_codomain_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3v_hopf_codomain_audit\run.ps1"
```

`R3V_*` のログを貼り付けてください。`output/r3v_hopf_codomain_audit.json` に詳細を保存します。

本パッケージは AUDIT_ONLY であり、本番コード、既存テスト、ドキュメントの変更はありません。
検証は限定 pytest 3 件だけです。全体 pytest は Phase 169 の終了時まで行いません。
