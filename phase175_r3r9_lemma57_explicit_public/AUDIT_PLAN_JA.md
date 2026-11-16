# Phase 175 R3R9 — Lemma 5.7 特別結論の直接引用と公開証明監査

## 目的

現行の $\pi_7^3$ の公開 Proof Tree は Lemma 5.4 を経由して $E(\eta_2\circ\nu')=0$ を導く。しかしプロジェクト採用 Toda Chapter V 転記の Lemma 5.7 自体に「特に、$E(\eta_2\circ\nu')=0$」と明記されている。したがって、後続の証明でこの結論を引用するために Lemma 5.4 の証明を再実行する必要はない。

一般の $\alpha$ に対する Lemma 5.7 の仮定 $E^2\alpha\in2\iota_5\circ\pi_{i+2}^5$ を不要にするわけではない。今回採用するのは明記された特別な結論そのものである。

## 監査した既存コード・テスト

- `phase165_r52_r9_shared_math.py`：現行 `search_shared_group_goal()` および公開接続
- `phase175_r3r8r1_verified_prior_public/route.py`・`rule.py`・`install.py`
- `phase175_r3r8r1_verified_prior_public/tests/test_public_search.py`・`tests/test_verified_prior.py`
- `phase175_r3r6_lemma57_general/source.py`・`rule.py`・`tests/test_source.py`
- `phase175_r3r7_lemma54_membership/rule.py`
- `phase169_r10e4_ordered_db_prior/db_prior.py`：実際の先行 DB 検証
- `phase175_r1_k4_audit/audit.py`：通常 Group query・Trust・共通 Renderer・Web の実監査
- `phase168_r3_5_model_renderer.py`：共通 Narrative
- `phase163_r4_r94_output/manifest.json` の Lemma 5.7：出典 ID `toda:tex:ch5:0015`、SHA256 `01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c`、出版順 9100。Proposition 5.8 は順 9200。

**出典上の留保**：検証対象はプロジェクト採用の日本語転記とその署名済みマニフェストであり、原著の印刷版との独立照合は未実施。

## 変更対象一覧

1. **既存ファイル** `phase165_r52_r9_shared_math.py`
   - **関数** `search_shared_group_goal()` の全体：$(n,k)=(3,4)$ の import 接続先のみ `phase175_r3r9_lemma57_explicit_public.route` に変更。既存の import 部と他の関数は変更しない。
2. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/source.py`
   - **クラス** `TodaLemma57ExplicitNuPrimeZero`、**関数** `verify_explicit_lemma57_source()`、`build_explicit_lemma57_source()` を新規追加。
3. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/rule.py`
   - **関数** `exact_lemma57_zero_image_goal()`、`lemma57_explicit_zero_rule()`、`expand_cited_lemma57_explicit_zero()` を新規追加。
4. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/route.py`
   - **関数** `public_cited_ehp_extensions()`、`prepare_pi73_public_connection()` を新規追加。
5. **新規ファイル** `phase175_r3r9_lemma57_explicit_public/install.py`・`audit.py`・`run.ps1`・`tests/`・`README.md`・本監査文書・全文コード・テスト記録。

新規関数／クラスはいずれも記載した新規ファイル内に配置する。既存のクラス・数学的規則・公開 Renderer・他のテストを修正しない。

## 数学的推論の境界

1. Lemma 5.7 の出典を厳格に検証し、明記された特別結論の引用自体を一つの `GIVEN` ソース型で表す。
2. その型から $E(\eta_2\circ\nu')=0$ に対応する `GeneratorImage` を **INFERENCE** として抽出する。この段階で登録済み HyoujiGen ID による同一生成元検証を要求する。
3. $\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}$ の先行 DB `ProofStep` を `verified_db_step()` で再検証して零写像性を導く。
4. EHP 完全性から $H$ の単射性を導く。
5. 出典付き Hopf 像と先行 $\pi_7^5$ の検証済み群構造から $\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}$ を導く。

**禁止事項**：最終群構造の直接 GIVEN、条件付き一般命題からの無条件特殊化、未登録の名前同一視、専用証明・専用 Narrative、証明の保存済み再生。

## DryRun／本実行・テスト

- DryRun：Git HEAD と既存コード・出典 SHA・先行正常報告・差分の検査だけを実施し、追跡済みファイルを変更しない。
- 本実行：既存の `search_shared_group_goal()` 関数全体のみに限定した変更を適用し、限定 pytest と通常 Group query の公開検証を実施。
- 成功条件：`complete`、未解決 Goal 0、Trust `True`、Web `generic-complete-proof`、Lemma 5.7 の引用出典、該当抽出推論1件、Lemma 5.4 の使用0件。
- 失敗時：検証開始前の `phase165_r52_r9_shared_math.py` を**バイト単位で復元**。
- **全体 pytest は Phase 175 終了時にのみ行う。**

## 次 Phase との境界

R3R9 は $\pi_7^3$ の出典依存関係を短くすることだけに集中し、$\pi_9^5$ や $\pi_{10}^6$ の新しい証明規則・文献登録や一般 Narrative の追加変更を先取りしない。共通 Renderer の表示簡略化は証明の出典が安定した後に独立した監査として行う。
