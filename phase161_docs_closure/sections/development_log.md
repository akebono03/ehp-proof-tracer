## Phase 161 — Concrete Backward Chaining と証明再構築（2026-10-08）

Phase 161 は $E:\pi_4^2\to\pi_5^3$ の同型性を Concrete Goal（具体的証明目標）に設定して実施した。初期監査では既存 Production Catalog が目標から前提を直接生成する metadata（逆向き情報）を十分持たず、既存 proof ancestry を探索しただけでは新しい証明探索にならないことが確認された。

R1：対象となる7つの `toda_53_n3_*_inference_rule` を棚卸しし、`toda_rules.py` の実体を監査した。ローカル監査ツール報告は `rule_count=7`、`error_count=0`。

R2：`phase161_backward_goal_schema.py` を追加し、同型目標を単射・全射の2部分目標に分解。focused pytest は `3 passed in 1.95s`。

R3：`phase161_r3_backward_goal_schema.py` を追加し、4つの EHP 完全性窓を独立した前提として保持しつつ、単射・全射の枝を逆向き展開。R2+R3 focused pytest は `7 passed in 2.49s`。

R4：`phase161_r4_literature_premise_matching.py` を追加。$\Delta_5$ 単射に Proposition 5.1、$H_6$ 全射に $H(\nu')=\eta_5$ と Proposition 5.1 に由来する推論済み前提を照合。R2–R4 focused pytest は `11 passed in 3.55s`。

R5：`phase161_r5_backward_proof_reconstruction.py` を追加。完成済みの最終同型 `ProofStep` を入力せず、用意された前提から7つの Production Rule を適用して結論を再構築。R2–R5 focused pytest は `17 passed in 5.00s`。

R6：推論依存と4つの完全性、文献前提を個別に除去した場合の失敗を監査。従来の R5 では推論済み文献前提の祖先検証が不十分という限界を記録。R6 focused pytest は `4 passed in 2.10s`。

R7：`phase161_r7_premise_provenance_validation.py` に検証付き入口を新設。再帰的な `INFERENCE` 再計算、未承認 `GIVEN` の拒否、欠落前提・改変結論・循環の拒否を確認。R7+R6 回帰 focused pytest は `10 passed in 3.49s`。

Phase 161 の成果は「特定の非安定 EHP 同型性に対する goal-driven な依存生成・前提照合・推論再構築・限定的 provenance 検証」である。一般的な非安定証明探索、文献の完全自律発見、public Narrative 接続はまだ実装しない。次 Phase 162 で既存 Renderer への接続を監査する。

**利用者の明示指示により、Phase 161 の終了時も repository-wide full pytest は実行しない。** 完了判定は局所検証と限定事項の記録に基づき、全体テスト成功は主張しない。

