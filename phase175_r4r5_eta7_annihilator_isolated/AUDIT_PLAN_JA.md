# Phase 175 R4R5R2 — 有限巡回直和成分の位数から零関係への一般推論

## 目的と数学的根拠

証明済みの群構造に有限巡回直和成分が含まれる場合、その成分の生成元に位数を掛けると零元になることを、個別の群に依存しない推論規則として扱う。

$$
G=A\oplus\mathbb Z/m\{a\}\oplus B
\quad\Longrightarrow\quad ma=0.
$$

同じ群が有限巡回成分を複数持つ場合は各成分に独立に適用する。無限巡回成分は対象外。群構造を証明する処理と、その群構造から零関係を導く処理を分離する。

## 事前確認

GitHub `akebono03/ehp-proof-tracer`、`develop` の HEAD `2789fb6297efaa35962695b95300063feb6e2ea2` と、関連する型定義、`proof.py` の `find_inference_matches_for_rule`、先行 DB 結果認証 API および R4R5R1 のコード・テストを確認した。

既存データ `sphere.csv` では `(n,k)=(7,1)` に位数2の η₇ があり、`(4,4)` には位数2の2つの成分を持つ π₈⁴ の群構造がある。いずれも `(5,4)` より先行する。

## 変更するファイル・関数

既存本番ファイルは変更しない。置換する単位は `phase175_r4r5_eta7_annihilator_isolated/` の以下の全文。

- `rule.py`：import 全文、`typed_endpoints` 全体、`order_zero_premise` 全体、`finite_cyclic_order_zero_rule` 全体、`expand_finite_cyclic_order_zero` 全体を変更。`typed_endpoints` の直後に `_finite_cyclic_components` を追加。
- `audit.py`：モジュール説明、import 全文、Gate 定数、`run` 全体を変更。`eta7_prior_and_isolated_zero` の直後に `direct_sum_prior_and_isolated_zero` を追加。
- `tests/test_rule.py`：ファイル末尾に一般直和・型安全性のテスト関数を追加。既存テストは保持。
- `tests/test_audit.py`：末尾に認証済み π₈⁴ 先行結果の使用・失敗経路のテスト関数を追加。既存テストは保持。
- `run.ps1`：R4R5R2 の限定 pytest・終了コード表示を追加。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`（日本語）：全文更新。

新規の数学的推論規則は1件（R4R5 から一般化）、新規文献 GIVEN は0件。クラスの変更はない。`CODE_FULL_JA.md` に import と関数・テストを省略せず収録する。

## 証明上の境界

1. `Relation(G, DirectSumGroup(...), EQUALITY)` のような群構造は、実際の `ProofStep` として確立されて初めて利用できる。零関係側の `EQUALITY` / `ZERO` は両方受け付ける。
2. 生成元・位数・群次元が厳密に一致する有限巡回成分だけを採用する。
3. `FreeCyclicGroup`、誤った成分・位数・型不一致の候補を拒否する。
4. 複合生成元の型は、Sphere の始域・終域を検証する。`IteratedSuspension` を含む実際の π₈⁴ の生成元形にも対応する。
5. 先行 DB 結果は `exact_prior_database_result`、`admitted_db_step`、`verified_db_step` の既存認証経路のみで採用する。完成証明を再探索しない。
6. 生成した `ProofStep` は `ProofRule.INFERENCE`。元群構造を新たな文献 GIVEN にしない。
7. 現段階は隔離監査のみ。共有 Backward Search への配線・Web 表示・π₉⁵ の完成扱いは行わない。

## テストと完了条件

限定 pytest：R4R5 パッケージ内テスト、R4R4・R4R3・R4 の関連テストのみ。全体 pytest は Phase 175 終了時のみ。

- DryRun Gate：`PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_DRYRUN`
- 本実行 Gate：`PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_ISOLATED_NOT_PUBLIC`
- `PHASE175_R4R5_2ETA7_ZERO_STEP=True`
- `PHASE175_R4R5R2_DIRECT_SUM_ZERO_STEPS=2`
- `PHASE175_R4R5_PI87_PROOF_SEARCH_EXECUTED=False`
- `PHASE175_R4R5_PI84_PROOF_SEARCH_EXECUTED=False`

## 次の段階との境界

R4R5R3 以降で認証済み先行 DB 結果・文献の検証済み ProofStep を共有探索の source-first context に渡し、一般規則を公開探索へ配線する。Proposition 2.5 と Toda (5.8) の命題登録・導出は別の監査で行う。
