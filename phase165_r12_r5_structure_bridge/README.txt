Phase 165 R12-R5 — 共通型付き橋渡し

変更対象:
- phase165_r8_rule_provider.py: DEFAULT_RULE_MODULES のみ
- phase165_r12_r5_structure_bridge.py: 新規、一般規則1件
- phase165_r12_r5_structure_bridge_audit.py: 新規、ルートでの逆向き提案を観測
- tests/test_phase165_r12_r5_structure_bridge.py: 新規、テスト6件

PowerShell（リポジトリ直下から）:
Expand-Archive -Path "$HOME\Downloads\phase165_r12_r5_structure_bridge.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r12_r5_structure_bridge\run.ps1"

この段階は pi4^3 の完全証明ではありません。商群規則とルート目標の型を結ぶ一般規則のみ追加します。
