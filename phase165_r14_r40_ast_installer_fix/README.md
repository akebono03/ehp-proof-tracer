# Phase 165 R40: common renderer integration

変更対象: `web_group_proof.py` の `build_standard_web_group_proof_view` から R39 の専用分岐を削除（それ以外は維持）。`phase164_r5_r2_common_replay.py` の `build_phase164_r5_r2_common_replay` に `(n,k)=(2,1)` の選択分岐のみ追加。新規 `phase165_r14_r40_replay.py` の `build_phase165_r40_pi32_common_replay` は R38 の証明根を既存 `TodaGroupResultProofReplayResult` に載せる。新規テスト5件。全体テストは実施しない。

流れ: 登録済み型付き Reference → 共通 Backward Search → ProofStep → 共通 replay → `build_toda_group_proof_presentation` → `render_toda_group_proof_narrative_markdown` → Web。R39 専用文章は使用しない。

完了条件: 5件の関連テストが PASS、Narrative 画面に表示。共通 Renderer の既存規則が新しいジェネリックな型を描画できない場合は失敗を報告し、専用証明文章への fallback はしない。
