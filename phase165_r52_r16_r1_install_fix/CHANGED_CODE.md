# R16-R1 変更対象

- 新規配置（リポジトリ直下）: `phase165_r52_r15_ordered_citation.py` — 元の R15 ファイルを変更せずコピー。既存の `ordered_typed_reference_steps()` を利用。
- 新規配置: `phase165_r52_r16_web_citation_gate.py` — 元の R16 ファイルを変更せずコピー。`screen_shared_proof_context()` を利用。
- 既存変更: `phase165_r52_r9_shared_math.py` — `build_shared_typed_bridge()` 内の `records.extend(...)` を ID 対応に修正し、`search_shared_group_goal()` を全文置換。
- インストーラー: `install.py` を全文更新。`run.ps1` を全文更新。
- テスト: R16 元の `test_phase165_r52_r16_web_citation_gate.py` 全文を同梱（変更なし）。
- import の変更なし。`README.md` は英語、監査メモは日本語。
- 全体 pytest なし。
