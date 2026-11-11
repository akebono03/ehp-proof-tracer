# Phase 175 R1 — k=4 全6群の証明探索監査

## 変更対象

変更する既存ファイル／クラス／関数／メソッド：**なし**。

新規追加するファイル：

- `phase175_r1_k4_audit/__init__.py`
- `phase175_r1_k4_audit/audit.py`（CSV 読取り、Git Source Guard、実際の検索 Worker、分類、JSON・Markdown 出力、CLI）
- `phase175_r1_k4_audit/run.ps1`（DryRun、限定 pytest、6群の監査起動）
- `phase175_r1_k4_audit/tests/__init__.py`
- `phase175_r1_k4_audit/tests/test_audit.py`（契約テスト）
- `phase175_r1_k4_audit/README.md`（英語）
- `phase175_r1_k4_audit/AUDIT_PLAN_JA.md`（本書）
- `phase175_r1_k4_audit/CODE_FULL_JA.md`（新規コード全文）

## 実装前に確認した現行ソース

- GitHub `akebono03/ehp-proof-tracer` の `develop` 上の `data/sphere.csv`、登録済み `(n,k)` と生成元・位数。
- `phase165_r55_nk_only_goal.py` の `search_group_from_registered_goal()`。
- `phase165_r52_partial_proof.py` の `PartialProofResult`、`ProofSearchStatus`。
- `phase165_r52_r9_shared_math.py` の共有探索経路。
- `phase169_r10e4_ordered_db_prior/db_prior.py` の `exact_prior_database_result()`。
- `phase168_r3_41p13_trust_boundary/verification.py` の `verify_proof_tree_for_narrative()`。
- `phase168_r3_4_link_bridge.py`、`phase168_r3_3_proof_narrative_model.py`、`phase168_r3_5_model_renderer.py`。
- `web_group_proof.py` の `build_standard_web_group_proof_view()` と `web_group_proof_common.py`。
- `phase173_r1_nge3_audit/audit.py` と関連限定テスト、`phase174_r3_r7_r71_common_narrative_regression/audit.py`、R72 の監査・関連テスト、R74 の終了記録・関連テスト。

## 対象

| `(n,k)` | 群 | DB の登録表示 | 監査の目的 |
|---|---|---|---|
| `(2,4)` | $\pi_6^2$ | $\mathbb{Z}/4\{\eta_2\nu'\}$ | 既存完成経路の確認 |
| `(3,4)` | $\pi_7^3$ | $\mathbb{Z}/2\{\nu'\eta_6\}$ | 未解決 Goal の確認 |
| `(4,4)` | $\pi_8^4$ | $\mathbb{Z}/2\oplus\mathbb{Z}/2$ | 登録の2成分と完成経路の確認 |
| `(5,4)` | $\pi_9^5$ | $\mathbb{Z}/2\{\nu_5\eta_8\}$ | 未解決 Goal の確認 |
| `(6,4)` | $\pi_{10}^6$ | $0$ | 零群証明の確認 |
| `(7,4)` | $\pi_{11}^7$ | $0$ | 零群証明の確認 |

上表は**登録データの構造**であり、各記名生成元の現行証明完成を意味しない。完成／未完成は当該ユーザー環境の監査結果で確定する。

## 判定方法

1. `develop` ブランチ、Phase 174 正式終了時の親コミット継承、追跡済みファイル・index の無変更、監査対象 Git blob の完全一致を検査する。外部ネットワークアクセスや Git 状態変更はしない。
2. 既存 CSV を UTF-8 BOM 対応で読み、`k=4` の明示的な行だけを採用する。`n=4` の2成分は同一群に集約し、6群／7成分行を確認する。
3. 各群を独立した Python Worker で検索し、型付き DB Goal、Status、ProofStep、未解決 Goal、Diagnostics、出典位置・採用された Reference、抽象群証明書の有無を記録する。
4. Complete の場合は既存の `verify_proof_tree_for_narrative()` を実際に通過したことと、共通 `ProofNarrativeModel` の証明 root を確認する。Incomplete の場合は未解決 Goal を保持する。
5. `build_standard_web_group_proof_view(..., mode="narrative", citation_source="model")` を対象ごとに起動し、`generic-complete-proof`／`generic-partial-proof`、Reference、Web の行表現を保存する。
6. Status の不一致、認証不成立、Worker 失敗／Timeout は別分類として報告する。未完成は異常終了と取り違えない。

## テスト・完了条件

- DryRun：Source Guard、登録6群と7成分の確認、限定 pytest を成功させる。証明探索 Worker は起動しない。
- 本実行：6群を実際に検索・Web 表示し、6件の結果を報告する。未完成群は未完成のまま残す。
- 完成認定：証明 root・出典付き trust verification・共通 Renderer・Web status が全て揃う場合のみ。
- 実装の変更は新規監査用ディレクトリのみ。数学規則、GIVEN、既存 production API、公式5文書は変更しない。
- このパッケージ作成環境では実リポジトリの6群を実行できないため、証明結果を捏造しない。**手元の限定契約テスト21件は PASS**、ユーザー Windows 実行による Source Guard と6群の監査は未実施として区別する。
- Phase 175 R1 では全体 pytest を実行しない。Phase 175 最終 Gate のみで実施する。

## 次 Phase／次監査との境界

本 R1 は「何が不足しているかを事実として収集する」段階であり、数学的修正を加えない。R2 では R1 の未解決 Goal と採用済み文献命題を照合し、一般化可能な不足を特定する。R3 以降の新規推論規則と正式 Phase 175 完成判定は、本 R1 の範囲外である。
