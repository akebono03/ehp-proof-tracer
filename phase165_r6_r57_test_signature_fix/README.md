# Phase 165 R6 — R57 テストの現行 API 対応

対象：`phase165_r57_r1_single_entry/test_phase165_r57_r1_single_entry.py` 内の `test_standard_route_uses_r55_for_arbitrary_nk` のみ。

変更：テスト内 `search` の `goal=None` 受け取り、呼出し記録と期待値の `None` 照合。実装コードと他のテストを変更しない。未知のローカル版は変更せず停止する。既存 import への変更なし。

実行：`powershell -ExecutionPolicy Bypass -File .\phase165_r6_r57_test_signature_fix\run.ps1`

このパッケージはテストファイルの関数を変更するため、実行前に Git の状態を保存しておくこと。限定 pytest のみ実行し、全体 pytest は Phase 165 の最終段階まで実行しない。

完了条件：3件の R57-R1 テストが PASS すること。`generic-partial-proof` に対する追加失敗がある場合は実際の探索状態を確認し、成功に偽装しない。

次 Phase との境界：実装・Renderer・証明探索や新機能には一切手を加えない。
