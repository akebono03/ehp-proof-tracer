# R3Q1 修正の実行

前回 R3Q は失敗時に2ファイルを自動復元したため、新規 R3Q1 を単体で実行する。旧 R3Q ZIP を再実行しないこと。

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3q1_delta_exactness_guard.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3q1_delta_exactness_guard\run.ps1"
```

テスト失敗時は2ファイルを R3Q1 変更前の状態に自動復元する。
