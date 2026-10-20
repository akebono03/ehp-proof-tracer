# Phase 166 R3 回復措置

- 対象: `phase165_r3_recursive_search.py` と `phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py` の2ファイル。
- 変更した関数: R3が差し替えた `_typed_reference_steps`、`reconstruct_registered_goal` と既存の限定テスト関数。両ファイルは元のバックアップの**全文**に戻す。
- 原因候補: R3の順序判定は `source_id`、`component_position`、`available_after_position`、`publication_position` が未設定だと固定命題を除外する。実Web上の順序情報の整備状況を確認せずに切り替えた。
- 回復に使用するバックアップは実行ログが報告した時刻 `20261019T233533Z` のものに固定し、存在しなければ停止する。
- テスト: `python -m pytest -q tests/test_phase165_r3_recursive_search.py phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py`。
- 完了条件: ファイル復元SHA-256一致、限定テストPASS、Webの `π₃²` の完全証明を人手で確認。
- R3との境界: 復元はR3の完了を意味しない。新しい資格制度を作らず、既存の順序情報を実探索で利用できるように整備する必要がある。
- 全体pytestは実行しない。
