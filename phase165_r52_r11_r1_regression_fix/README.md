# Phase 165 R52-R11-R1 — 回帰テストの期待値修正

変更対象ファイル:
- `test_phase165_r52_r8_show_proof_route.py`
  - `test_r8_unconfigured_proof_calls_partial_search(monkeypatch)` の期待値を更新

変更の理由:
R52-R11 共通 Renderer は従来の内部状態 `search_failed` をユーザー表示からなくし、
`証明未完成` と表示する。古い R8 のテストが内部文字列を探して失敗するため、
確認対象を新しい UI 契約に切り替える。

import の変更: なし (全文はパッケージ内の test ファイルを参照)。
クラス変更: なし。
数学的推論・Renderer・Web 本体の変更: なし。
互換性: `ProofSearchStatus.SEARCH_FAILED` は内部的に維持。
インストーラーは既存テストの該当1行だけを書き換える。差異があれば停止する。

実行手順:
```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r52_r11_r1_regression_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r11_r1_regression_fix\run.ps1"
```

対象 pytest:
- test_phase165_r52_r11_common_renderer.py
- test_phase165_r52_r8_show_proof_route.py
- 存在する場合のみ R52 partial, R9 shared math, R10 readable partial

完了条件: 19件を含む対象テストが全て成功すること。
次の境界: 数学的 Goal を展開して ProofStep を生成する探索側は別 Phase。
全体 pytest: この Phase の末尾まで実施しない。
