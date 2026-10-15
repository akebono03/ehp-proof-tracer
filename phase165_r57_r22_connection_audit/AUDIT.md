# Phase 165-R57-R22 接続監査

対象：GitHub `akebono03/ehp-proof-tracer` の `main`、取得した tree SHA `f0657644ac9699b6cebbe39071de6a1d98f3d958`。GitHub ソース内容を確認した時点での静的評価。ローカル変更がある場合は `audit_results.json` を優先して再評価する。

## 確認事項

- `phase165_r3_recursive_search.py::reconstruct_registered_goal` は Provider が返した `GoalExpansion.subgoals` を再帰的に解き、既存の `find_inference_matches_for_rule` と `derive_inference_proof_step` により順方向検証をする。一方、InferenceRule の結論から汎用的に前提を逆算する機能はこの関数中にない。
- `proof.py::InferenceRule` は `conclusion_pattern`、`conclusion_builder`、`premise_patterns` を持つが、`find_inference_matches_for_rule` は既存の前提 `ProofStep` を照合する側の機能。これだけでは逆向き照合・候補発見・前提生成が完成しているとはいえない。
- `phase165_r52_r9_shared_math.py::shared_expansion_provider` は `expand_existing_pi43_rules` を登録している。
- `phase165_r52_r23_existing_rule_adapter.py::expand_existing_pi43_rules` は固定した π₃²、π₄³、π₅⁵ を使う。名前付き生成元、有限巡回商、懸垂核、懸垂全射の4形を逆向きに展開する。
- R18 は証明済み生成元等式からの有限巡回群表示置換で、推論規則自体は汎用。ただし π₄³ の逆向き前提を構成する箇所は Adapter にある。
- R19 は登録された符号付き Δ 命題から Δ の像の候補を作る。任意の推論規則の逆向き適用ではない。
- R20 は出典付き型付き ScalarSymbol テンプレートの具体化。全種類の結論と型変数に対する Unification ではない。
- `phase165_r14_r14_diagonal_and_prop42.py` の Proposition 4.2 については、source review の時点で applicability を未認証と明記した経路がある。このモジュールのみを根拠に π₄³ の任意の exactness 前提を流用できるとは判定しない。現在の登録済み ProofStep を別途確認する必要がある。

## 暫定的な差分フロンティア

専用 Adapter が直接出している候補の形：

| Goal | Adapter 候補 | 共通機能との重複 |
|---|---:|---|
| π₄³ = Z/2{η₃} | 1 | R18 の forward 規則と重複するが逆向き前提は専用 |
| π₄³ = Z/2{Eη₂} | 1 | 有限巡回商の汎用逆向き規則は未確認 |
| ker(E) = Z{2η₂} | 1 | 完全性に基づく専用逆向き前提 |
| E surjective | 1 | 右端の零群と完全性の専用逆向き前提 |
| im(Δ) = Z{2η₂} | 0 | R19 が登録済み witness の存在時だけ提案 |

これは **Adapter 自体の観測対象** であり、共通 Provider から除去した後の実行時未解決 Goal の確定結果ではない。削除の安全性は未認証。

## R23〜R26 の評価

- R23: 既存の `_bind` は scalar 特化。規則の conclusion を使った型付き一般照合は別途必要。
- R24: R19・R20 のような限定された Source-driven discovery は再利用できる。規則横断的な候補発見は不足。
- R25: Adapter に埋め込まれた 4 系列の前提生成を、規則メタデータに移す必要がある。群別分岐の新設は禁止。
- R26: 探索器と forward verification は再利用する。Provider 側の一般化のみを最小変更とする。

## 変更境界とテスト

本体変更：なし。監査パッケージのみ新規追加。pytest は監査用 `test_audit.py` に限定。Phase 165 終了前に全体 pytest は行わない。R23 以降の実装は今回行わない。
