# Phase 175 R3R7 — 実装・数学・証拠監査

## 現行コードの事前確認

GitHub `akebono03/ehp-proof-tracer`、`develop`、HEAD `40bd19c0a91d09e7aaf15b216eae985fda65e347` の内容を確認した。対象は次の既存ファイルとその関連テスト。

- `sources/toda/Toda_05_2.tex`：Git blob `579661138928499ba04a51327f686d9b971b5314`。
- `phase163_r4_r94_output/manifest.json`：Lemma 5.4 / Lemma 5.7 / Proposition 5.8 の文献順、記述および SHA-256。
- `phase173_r4_r1_lemma54_source_bridge/source.py`：`TodaLemma54TypedSource`、`validate_lemma54_text`、`canonical_hopf_relation`、`add_verified_lemma54_source` と関連 `tests/test_source.py`。
- `phase174_r3_r6_r2_prop44_lemma54/source.py`：`attach_earlier_verified_lemma54` と `tests/test_source.py`。
- `phase175_r3r6_lemma57_general/source.py`、`rule.py`、`audit.py`、`run.ps1` と `tests/test_source.py`、`tests/test_rule.py`、`tests/test_lineage.py`。
- `phase175_r3r5_pi73_lemma57_frontier/frontier.py`、`source.py` と関連テスト。
- `phase175_r3_pi73_hopf_lift/frontier.py`、`rule.py`、`audit.py` と関連テスト。
- `phase174_r3_r7_r5_zero_image_hopf_injective/rule.py`、`phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py`、`phase165_r3_recursive_search.py`、`phase168_r2_8_3_generator_identity/identity.py`、`phase169_r10eq_r1_universal_stable_definition/definition.py`、`expression.py`、`homotopy_groups.py`。

## 数学的検証

Toda Lemma 5.4 の source clause は `2E\nu_4=E^2\nu'` である。`\nu_4\in\pi_7^4` から `E\nu_4\in\pi_8^5` が型付きで従い、恒等写像 `\iota_5` による左合成の一般的な定義から

$$
E^2\nu'=2E\nu_4=2\iota_5\circ E\nu_4\in2\iota_5\circ\pi_8^5.
$$

R3R6 が保持する一般形 `E^2\alpha\in2\iota_5\circ\pi_{i+2}^5 \Rightarrow E(\eta_2\circ\alpha)=0` を、その適用条件の **INFERENCE** が完成した場合にだけ使用する。

出典の固定命題は Lemma 5.4 全体および Lemma 5.7 の一般条件のみ。2倍の懸垂等式は引用出典からの抽出であって新たな GIVEN ではない。位相次元と構成元 ID の異同を検査し、未登録の別元素や似た名前を同一視しない。任意の型が合う `alpha` と `beta` に使える2倍因数分解規則を採用する。

## 対象ファイル・変更単位

既存追跡ファイルは **変更なし**。新規ディレクトリ `phase175_r3r7_lemma54_membership/` のみ。

- `source.py`：`verify_lemma54_before_lemma57` 新規関数。
- `rule.py`：`canonical_nu_prime`、`cited_lemma54_double_relation`、`_same_typed_alpha_identity`、`lemma54_double_rule`、`expand_cited_lemma54_double`、`even_factorization_inputs`、`even_factor_membership_rule`、`expand_even_factor_membership` 新規関数。
- `audit.py`：`verify_lineage`、`scoped_preflight`、`latest_successful_r3r6`、`inspect_actual_search`、`worker`、`launch_worker`、`write_report`、`run`、`main` 新規関数。
- `run.ps1`：限定 pytest と DryRun／本監査を実行する新規スクリプト。
- `tests/test_rule.py`、`tests/test_source.py`、`tests/test_audit.py`：新規テスト関数。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`（日本語）。

新規ファイルはすべて ZIP 解凍によりリポジトリのルート直下へ追加する。変更 import／クラス／関数およびテスト関数の全文を `CODE_FULL_JA.md` に収録する。既存の classes・functions・imports は変更しない。

## 検証と Gate

1. `run.ps1 -DryRun`：限定 pytest、Git Source Guard、R2→HEAD の監査専用履歴、R3R6 正常終了報告、Toda の原文・manifest 検査。実際の数学探索はしない。
2. `run.ps1`：同じ事前検査の後、別プロセス内で既存の標準 backward search に新しい候補だけを加え、6個の証明義務を順に探索する。各目標を同じ共有 Renderer に統合したと主張しない。
3. 既存追跡ファイル変更があれば拒否。報告はリポジトリ外へ書く。
4. 限定 pytest のみ。Phase 175 全体 pytest は Closeout の最後だけで実行する。

**完了条件**：`double_suspension_membership` が `INFERRED` であり、後続の `lemma57_zero_generator_image` なども、実際の ProofStep の status として記録されること。根の `pi73_cyclic_lift` が `INFERRED` でも、公開 Provider に接続する次の作業まで Web 結果を `complete` と断定しない。
