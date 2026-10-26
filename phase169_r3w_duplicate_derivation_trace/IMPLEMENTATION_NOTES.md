# Phase 169 R3W — 監査設計

## 対象

- 本番コード、既存テスト、既存ドキュメントは変更しない。
- 新規ファイル `audit.py` の `examine()`・`describe_step()`・`main()` を追加する。
- 新規 `tests/test_phase169_r3w_duplicate_derivation_trace.py` は限定テスト3件を含む。

## 手順

既存の型付き出典を適用した $\pi_5^3$ の Proof Context を取得し、Proposition 5.1 の一般 $\eta$ 関係式から $\pi_6^5$ の目標を構成する。`shared_expansion_provider()` が挙げる候補規則と、実際の `reconstruct_registered_goal()` において検証された ProofStep を記録する。`append_unique_verified_derivation` を監査実行中だけラップして元の実装へ委譲するため、探索や重複判定の結果は変えない。

## 判定上の注意

2つの証明のうち一方を暗黙に選択しない。元の重複排除関数 `same_cited_scalar_specialization()` および `same_completed_proof_tree()` の双方の判定も記録し、前提となる文献の引用元まで遡る。今回は原因の可視化のみであり、$\pi_6^5$ の確定や Hopf 全射性の接続は行わない。
