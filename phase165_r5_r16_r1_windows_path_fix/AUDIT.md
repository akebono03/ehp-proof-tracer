# Phase 165 R5-R16-R1 監査修正

Windows の `Path` の文字列表現が `tests\test_old.py` となり、期待値の POSIX 表記 `tests/test_old.py` と一致しなかった不具合を修正した。

- 変更: `audit.py` の `audit()` 内、direct imports 記録を `.as_posix()` に統一
- テスト: `test_audit.py` に Windows パス変換検査を追加。既存の直接 import 検査も維持
- 変更しない: アプリケーションコード、既存 API、ProofStep、Renderer、Backward Search
- 全体 pytest: Phase 165 終了時まで未実施
- 完了条件: 限定テスト全件成功し監査結果が `PRECONDITION_FAILED` 以外になる
- 次の境界: 旧 Renderer の撤去そのものはこの監査では実施しない
