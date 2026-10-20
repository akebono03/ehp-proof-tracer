# Phase 166 R3-H 変更記録

変更: `phase165_r52_r16_web_citation_gate.py` の `screen_shared_proof_context()` 全体。既存の `ProofStepLink` の有無に依存する条件分岐を掲載順モードから削除。

新規テスト: `test_phase166_r3h_uniform_assertion_source.py` の5テスト。既存リンクの有無による不変性、後続命題の不採用、先行命題の利用、旧経路との境界を確認。

完了条件: 限定テスト PASS と、リンク有無による選択結果の一致。通常 Web 経路の証明対象 ID 指定と Toda (4.5) の逆向き移送接続は今後の作業。全体 pytest は Phase の最後のみ。
