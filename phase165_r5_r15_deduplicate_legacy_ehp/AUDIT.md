# Phase 165 R5-R15 実装監査

- 対象: `phase162_web_narrative_integration.py` の `_build_phase162_legacy_validated_isomorphism_markdown()`。
- R5-R11 で共通化済みの `_phase162_ehp_leaves()` に、重複した Prop.5.1・(5.3)・EHP 完全列の入力構築を一本化する。
- 旧公開 API、`render_phase162_r3_narrative`、証明推論、Reference 処理を削除・変更しない。
- ガード: 関数定義、想定する旧処理、共通モジュール・Replay 接続を静的に確認する。既存バックアップがあれば拒否する。
- テスト: 新規3件＋実行 fixture に依存しない旧書式テスト2件の限定実行。旧 Web の実行テストは `prop51_steps` 問題による既知失敗のため対象外とし、成功扱いにしない。実行失敗時はインストーラのバックアップへ復元する。
- **注意**: 既知の `prop51_steps` 空配列により、歴史的実行テストが失敗し得る。その場合、ロールバックし成功扱いにしない。
- 旧 Renderer 本体の撤去は未達。R5-R16 で残る互換 API と未解決回帰の完了判定を行う必要がある。
