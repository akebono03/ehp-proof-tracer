# R3-4 変更単位

- 新規 `phase168_r3_4_link_bridge.py`（リポジトリ直下）: 全 import、`build_linked_proof_narrative_model` 関数全文を同梱。
- 新規 `tests/test_phase168_r3_4_link_bridge.py`: 全 import、各テスト関数全文を同梱。
- `probe.py` と `run.ps1`: ZIP 内の実行補助。既存 API の変更はありません。

実行対象: `python -m pytest -q tests/test_phase168_r3_4_link_bridge.py tests/test_phase168_r3_3_proof_narrative_model.py`

完了条件: 限定テスト PASS、π₄² の実探索の出典投影レポート取得。二つの出典が未接続なら次工程で欠損箇所を修正。Renderer と全体テストは本工程の範囲外。
