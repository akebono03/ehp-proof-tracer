Phase 163 R4-R11 repair3
========================

目的: Proposition 5.6 の5成分の型付き Statement 登録を証明木の検証から分離。
原典未照合のまま SOURCE_UNVERIFIED として登録し、ProofStepLink を作らない。

Windows PowerShell:
  cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
  Expand-Archive -Path "$HOME\Downloads\phase163_r4_r11_repair3_literature_registration.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r11_repair3_literature_registration\run.ps1"

既存の証明・検索・Renderer・検証器は変更しません。
全体 pytest は Phase 163 最終段階まで実行しません。
