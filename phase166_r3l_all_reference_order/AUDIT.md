# Phase 166 R3-L 変更監査

- Phase 163 の順序 manifest を唯一の番号の正本として使用。
- `publication_position` は維持し、既存の出典 ID と明示的に確認された異名 ID から接続。
- `(5.1)` のような locator の文字列だけを根拠に接続しない。
- `component_position`、`AssertionEntry`、`ProofStepLink`、既存推論規則は変更しない。
- 全登録文献項目を走査し、出典 ID が対応不能な項目は JSON に列挙する。
- `build_shared_typed_bridge()` に接続。`screen_shared_proof_context()` の利用資格・Web 経路は今回変更しない。
- 全体 pytest は Phase 166 終了時のみ。
