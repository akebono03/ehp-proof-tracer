# Phase 175 R4R4 — $\pi_9^5$ の6前提 Source-first 監査計画

## 1. 確認済みの基点

- ユーザーの R4R3R2 DryRun・本実行：限定 pytest **85 passed**、Source PIN 18件、両 Gate PASS。
- 本実行の Gate：`PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC`。一般商群規則は隔離されたまま。$\pi_9^5$ は未完成。
- R4R3 実行時 HEAD：`20622a303b8c4558fe297eed070b43ca2f322831`。GitHub `develop` 上でも確認。
- R4 本実行の実測：対象 $\pi_9^5$ に Open Goals 3件、検索による検証済み導出は0。先行群 $\pi_8^4$ は完成・trust 検証済み。

今回の対象は **R4R3 の一般規則が要求する6個の ProofStep 前提の証拠状況**だけ。一般規則の公開登録や、目標結論の直接 GIVEN 登録はしない。

## 2. 監査対象となる6前提

| 番号 | 数学的前提 | 現時点で確認すべき証拠 |
|---|---|---|
| 1 | $\pi_8^4=\mathbb Z/2\{\nu_4\eta_7\}\oplus\mathbb Z/2\{E\nu'\eta_7\}$ | 先行完成群の検証済み結果と、商群規則が期待する型付きの直和表示が一致すること |
| 2 | $\pi_{10}^9=\mathbb Z/2\{\eta_9\}$ | $\eta$-family 等の出典を経由した登録済み導出を確認すること |
| 3 | $\Delta(\eta_9)=E\nu'\eta_7$ | Toda Proposition 2.5 と (5.8)、$2\eta_7=0$、位数2による符号処理から INFERENCE すること |
| 4 | $\operatorname{im}\Delta=\ker E$ | Proposition 4.2 の具体的な $\Delta\to E$ window の出典付き特殊化を証明すること |
| 5 | $E:\pi_8^4\to\pi_9^5$ の全射性 | 右端の $\Delta:\pi_9^9\to\pi_7^4$ の単射性と EHP exactness から証明すること |
| 6 | $E(\nu_4\eta_7)=\nu_5\eta_8$ | $E\nu_4=\nu_5$、$E\eta_7=\eta_8$、合成と懸垂の両立を ProofStep として証明すること |

**文献上の文字列・適切な型・証明済み ProofStep を区別する。** R4R4 自身は検証済み親 ProofStep を再生しないので、6前提を「証明完了」とは記録しない。先行群については完成事実を保持するが、特定の直和表示の親ステップが R4R4 で再生されたとはしない。

## 3. 出典と意味論の注意

1. `sources/toda/Toda_02_2.tex` Proposition 2.5：一般式は $\Delta\alpha\circ\beta\subset\Delta(\alpha\circ E^2\beta)$。$2$-primary 等の等号条件を無視しない。
2. `sources/toda/Toda_05_2.tex` (5.8)：$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$。Proposition 5.8 の証明が $\Delta(\eta_9)$ と $E$ の全射性を記載する。
3. 符号 $\pm$ を落とすときは、$E\nu'\eta_7$ の位数2が証明済みであることを前提とする。
4. Proposition 5.8 の EHP 列にある `\pi^{9}_{8}` は次元の転記・誤植の疑いがある。元資料を書き換えず、正しい型の EHP window を別途構成して検査する。
5. $\nu_n\eta_{n+3}=0$ は $n\ge6$。今回の $n=5$ に誤用しない。
6. `phase165_r12_r11_prop42_unified.py` の EHP window 検査、`phase169_r10e5_composite_generator_image/rule.py` の合成懸垂規則等が存在することと、具体的な前提を証明したことは同一ではない。

## 4. 今回の変更対象（最初に列挙）

既存本番コード・既存テスト・既存 API・Root の5文書は**変更なし**。新規 `phase175_r4r4_pi95_premise_frontier/` のみ追加する。

- `audit.py`：新規関数 `latest_prior_report`、`validate_prior_report`、`validate_prior_lineage`、`verify_code_and_source_pins`、`read_printed_source_evidence`、`verify_ehp_shape`、`premise_frontier`、`report_folder`、`run`、`main`。いずれも新規ファイル内で定義する。クラス新規・変更なし。
- `tests/test_audit.py`：新規の全テスト関数と `prior_fixture`、`printed_fixture`、`fake_git`。既存テストの変更なし。
- `run.ps1`：新規。限定 pytest は `-p no:cacheprovider --import-mode=importlib` を用いる。
- `__init__.py`、`README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md`：すべて新規ファイル全文。

全 import、変更対象の関数・テスト全文は `CODE_FULL_JA.md` に収録。実行コードやテスト内で `...` による省略はない。

## 5. Git／Source Guard

- R4R2 の `preflight()` を再利用し、18 Source PIN と `develop` ブランチを検査。
- 追加で Toda Chapter II/V と、関連規則ソースの計7 Git blob SHA を固定照合。原文のテキストも必要な節の順序・式・条件を実際に読む。
- R4R3 `rule.py` の SHA256 を R4R3R2 配布 ZIP の実体と一致させる。公開コード変更は不許可。
- R4R3 の成功レポートに記載された HEAD と現行 HEAD の祖先関係を検査。途中の追跡差分は R4R3 監査パッケージ内・既知 pytest `nodeids` に限定し、数学的ソースや `rule.py` の変化を拒否。
- Git のコミット、追跡済みファイル復元、Source 書換え、全体 pytest はしない。

## 6. Gate と次段階

DryRun の期待 Gate：`PASS_R4R4_PREMISE_FRONTIER_DRYRUN`。
本実行の期待 Gate：`PASS_R4R4_PREMISE_FRONTIER_RECORDED_NOT_PUBLIC`。

成功時にも `public_proof_complete=false`、`verified_parent_steps_replayed_here=0` と記録する。次段階 R4R5 では出典付き $\Delta(\eta_9)$ と位数2の符号処理を最小単位として検討する。既存の一般推論規則があればそれを優先し、R4R3 の規則を将来の準備としてだけ扱う。全体 pytest は Phase 175 終了時に実施。
