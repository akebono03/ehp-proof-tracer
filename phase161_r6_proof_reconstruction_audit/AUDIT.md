# Phase 161 R6 — Proof Reconstruction Audit

## 対象
- R5 `reconstruct_phase161_r5_goal`
- R4 `match_phase161_r4_existing_premises`
- R3 `expand_phase161_r3_goal`
- Phase 59 既存テスト fixture

## ソースから確認した事実
1. R5 は最終目標と相違する入力を拒否し、R3 の目標展開で前提を逆向きに決定する。
2. 7規則で `find_inference_matches_for_rule` と `apply_inference_match` を呼び、最終結論を照合する。
3. 4つの完全性は `ProofRule.GIVEN` の既存入力であり、R5 はそれらを証明しない。
4. 文献前提は `ProofRule.INFERENCE` と構造的内容で選別するが、祖先の `ProofStep` の完全性・出所の検証はしない。
5. R5 の文献前提は Phase 59 テストの `build_phase59_3_data()` から取り出しており、この fixture 自体は Phase 59 の forward 推論処理を実行する。完成済み結果は R5 に渡さない。
6. 目標は `E:π₄²→π₅³` に限定。一般の `n,k` に対する backward search は未実装。
7. `len(created) == 7` は具体的成功経路の検査であって、一般 Proof Search の健全性保証ではない。

## 判定
- **CONCRETE_RECONSTRUCTION_CONFIRMED_BY_PRIOR_17_FOCUSED_TESTS**（ユーザー提供の 17 passed ログに基づく）。
- **END_TO_END_SOURCE_INDEPENDENCE_NOT_ESTABLISHED**（文献入力の ancestry と完全性は既存資料に依存）。
- **GENERAL_BACKWARD_SEARCH_NOT_ESTABLISHED**（対象固定）。
- R6 の追加 focused audit はローカル実行前で未判定。

## 追加監査テスト
- 7つの新しい `INFERENCE` が最終結果から到達可能であること
- 4つの完全性を個別に取り除くと必ず失敗すること
- 2つの文献前提を個別に取り除くと必ず失敗すること
- 文献前提の根拠となる ancestry を欠いても現行 R5 は採用すること（既知の境界を検出する回帰監査）

既存 production の修正を伴わない R6 監査。全体 pytest は Phase 161 の終了時のみ。
