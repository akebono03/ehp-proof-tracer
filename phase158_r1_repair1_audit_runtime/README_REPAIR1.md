# Phase 158-R1 repair1

監査スクリプトの実行環境だけを修正する repair です。

変更対象:
- `audit_phase158_r1_repair1.py`
  - repository root を `sys.path` に追加
  - summary を UTF-8 BOM 付きで保存
- `run_phase158_r1_repair1.ps1`
  - repository root を `PYTHONPATH` に追加
  - `Get-Content -Encoding UTF8` で表示
  - 前回の output を削除してから再監査
- `test_phase158_r1_repair1.py`
  - repository module import の focused test を追加

Production code の変更はありません。
全体 pytest は Phase 158 の最後まで実行しません。
