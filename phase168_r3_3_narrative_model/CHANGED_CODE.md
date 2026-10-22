# Phase 168 R3-3 変更一覧

- 新規 `phase168_r3_3_proof_narrative_model.py`：モジュール全文を同梱。追加位置はリポジトリ直下。`NarrativeCitation`、`ProofNarrativeModel`、`build_proof_narrative_model()` を新規追加。
- 新規 `tests/test_phase168_r3_3_proof_narrative_model.py`：テスト4件と全 import を同梱。
- `run.ps1`：コピーと限定 pytest の実行。
- 既存の production 関数・クラス・import・テスト・ドキュメントは変更しない。

完了条件：4件の限定テスト PASS、Root 推論出典保持、同一文献の重複排除、未使用リンクの不採用。

次工程との境界：Web Renderer の切替、文献順 Search gate、ProofStepLink の探索結果への受け渡しはこの R3-3 の対象外。
