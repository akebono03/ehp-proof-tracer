# Phase 169 R10EK — 共通 Generator Transport Projection 設計監査

## 方針

**AUDIT_ONLY**。`phase169_r10a_verified_stable_chain_projection/projection.py` と `phase169_r10ec_direct_sum_narrative_projection/projection.py` の現行実装を、同一の検証観点で比較する。今回は新しい推論規則・証明・共通 Renderer を作らない。

対象は以下の4群。

| 対象群 | 類型 | 懸垂回数 | 成分数 |
|---|---|---:|---:|
| $\pi_{28}^{22}$ | 有限巡回群 | 14 | 1 |
| $\pi_{32}^{22}$ | 有限巡回群（合成生成元） | 10 | 1 |
| $\pi_{23}^{15}$ | 直和群 | 5 | 2 |
| $\pi_{33}^{24}$ | 直和群 | 13 | 3 |

## 共通の検査契約

1. Backward Search による `COMPLETE` の Proof Tree が存在する。
2. Trust Boundary の `verify_proof_tree_for_narrative()` が成功する。
3. Root は typed `Relation` の `INFERENCE` であり、実際の prior 群構造と Toda (4.5) の具体的同型を前提にする。
4. 成分ごとの懸垂像はすべて独立に証明された `GeneratorImage` である。
5. Hidden にする ProofStep は個別 Citation を持たず、Root または同じ Hidden 集合以外に consumer を持たない。
6. 合成した表示の Citation 番号は Narrative Model に登録済みのものである。
7. Proof Tree の object identity、premise の identity、Citation 情報を変更しない。
8. 元の Reference と証明終了記号が表示に残る。

## 統合可能な責務と保持する境界

共通化候補は「Root・同型・生成元像の検査」「引用祖先の検証」「hidden 対象の consumer 閉包」「不適合時に圧縮を拒否する処理」。一方、群構造の成分展開と生成元 LaTeX 表示、表示する式の組み立ては型別の adapter として分ける。

今後共通化する場合にも、`VerifiedStableImageChainDisplay`（個別巡回群）と `VerifiedDirectSumTransportDisplay`（直和群）の既存 API を即座に削除しない。既存の R10A・R10EC・R10EJ テストの振る舞いを保つ必要がある。

この監査は自由巡回群、零群、1-stem の専用 eta 正規化経路、未完成の11・14-stemをカバーしない。また「既存の共通契約を満たした」ことは、数学的な定理を追加したことを意味しない。

## Phase 境界

R10EK は設計監査のみ。実装を行う場合は別の小さな Phase 169 サブタスクで安全条件と回帰テストを先に確定する。全体 pytest は Phase 169 終了時に一度だけ実施する。
