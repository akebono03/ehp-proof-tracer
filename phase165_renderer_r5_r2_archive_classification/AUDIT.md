# Phase 165 Renderer R5-R2 監査

前回 R5-R1 はルート直下と `tests/` へ限定したが、明示的な履歴コピー（例：`toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py`）も本番の import と同じ件数に計上した。

R5-R2 は **ルート直下の `*.phase数字_名称.py`** のみを履歴ファイルとして区別する。検出された旧 import は `archived_root_imports` に残す。その他のルート直下および `tests/` からの旧 import は `old_imports` に残し、ゼロ件でなければ FAIL。

対象となる既存のアプリケーションソースは変更しない。最終判定は実環境の出力と補助 Renderer の経路監査を待つ。
