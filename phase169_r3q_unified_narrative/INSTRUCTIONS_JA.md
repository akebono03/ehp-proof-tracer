# 実行方法

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3q_unified_narrative.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3q_unified_narrative\run.ps1"
```

R3P の補助 Renderer を別途後から適用しないこと。今回の共通処理を再び分岐させないためです。
