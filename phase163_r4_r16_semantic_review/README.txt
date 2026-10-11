Phase 163 R4-R16 — 第1章の数学的意味単位精査（read-only）

前提: Phase 163 R4-R15 パッケージをリポジトリ直下に配置済み。
同じ場所に本フォルダを解凍する。

PowerShell から:
powershell -ExecutionPolicy Bypass -File .\phase163_r4_r16_semantic_review\run.ps1

出力:
phase163_r4_r16_output\semantic_review_queue.csv
phase163_r4_r16_output\named_subclauses.csv
phase163_r4_r16_output\summary.json
phase163_r4_r16_output\report.md

判定は意味的同一性の証明ではない。原典照合・既存67成分の実体照合は未完了。
Statement ID は正式付与しない。既存ソースに変更なし。
