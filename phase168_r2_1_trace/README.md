# Phase 168 R2-1 — Toda (5.2) 引用審査と展開の切り分け

現行コードと DB を変更しない診断。`build_shared_typed_bridge()`、`screen_shared_proof_context()`、および既存 R2 の `expand_toda52_finite_cyclic_goal()` を使用する。

実行: リポジトリ直下に展開し、`powershell -ExecutionPolicy Bypass -File .\phase168_r2_1_trace\run.ps1`

出力: `phase168_r2_1_trace/results.json`

- `full_toda52`: 統合命題台帳における型付き (5.2) と ProofStepLink
- `screened_toda52`: 公開引用審査後の型付き (5.2)
- `raw_transport_count`: 引用審査前の (5.2) を用いた候補数（証明ではない）
- `screened_transport_count`: 審査後の利用可能な候補数（証明ではない）
- `screened_root_rules`: 根の展開候補と規則名

本診断は pytest も実装変更も行わない。全体テストは Phase 末尾のみ。
