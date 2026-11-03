# Phase 173 R4-R15R7 設計書

## 目的

Phase 173 R4-R15R6 で得た、生成元名を持たない型付き抽象群の推論候補を、出典の検査と既存 ProofStep 推論検証によって実際の証明木にする。

対象は $n=4$ の一般形

$$
\pi_{k+4}^4\cong\pi_{k+3}^3\oplus\pi_{k+4}^7\qquad(k\ge3)
$$

であり、$k=31$ を特別扱いしない。右辺の2群は `ADOPTED_DATABASE_PRIOR`（採用済みデータベース前提）であり、独立の文献定理に読み替えない。

## 既存ソース・テストの事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop`、基準 HEAD `3e3dfecec3c6972a1a2bb19f00372b66314492e2` を検査した。既存の `phase173_r4_r10_general_toda56_core/core.py`、`phase165_r3_recursive_search.py`、`phase173_r4_r11_zero_public_connection/source.py`、`phase169_r10e2_unpositioned_citation/source_first.py`、`phase169_r10e4_ordered_db_prior/db_prior.py` および関連テストで契約を確認した。R4-R15R6 の `abstract_rule.py` は直前の実行用 ZIP の全文ソースを確認した。

## 推論経路

1. `checked_abstract_inputs(proof_target)` で実際の登録済み目標と2つの先行群を照合する。
2. Toda Lemma 5.4 の元の TeX と Source Archive を既存 `_validated_archive` で検証する。
3. 作業用 Bridge のみで `TodaLemma54TypedSource` を出典付き FIXED_STATEMENT として登録し、既存 `screen_independent_sources_for_derived_goal` で引用順・目標の自己引用を排除する。元の Bridge は変更しない。
4. 既存 `reconstruct_registered_goal` で Proposition 4.4 と Lemma 5.4 からの Hopf 関係を解決する。
5. 2つの先行群を `admitted_db_step` で採用し、`verified_db_step` で検証する。これらは新たな文献の GIVEN ではない。
6. 既存 `expand_abstract_toda44`、`find_inference_matches_for_rule`、`derive_inference_proof_step` で4前提から抽象群の結論を再構成する。
7. 戻り値 `AbstractSearchCertificate` は記名群の公開完成状態ではなく、`public_group_complete` は常に False とする。

## 変更対象と追加位置

既存ファイルの import、クラス、関数、メソッドには変更なし。新規パッケージ `phase173_r4_r15r7_source_first_abstract_certificate/` のみを追加する。

- `source.py`：`screened_abstract_context()`
- `search.py`：`AbstractSearchCertificate`、`_screened_given_conclusions()`、`search_source_first_abstract()`
- `audit.py`：`inspect_k()`、`main()`
- `preflight.py`：`git()`、`allowed_committed()`、`normalized_sha256()`、`preflight()`、`main()`
- `tests/test_static.py`、`tests/test_integration.py`：完全なテスト関数を新設する。
- `run.ps1`：DryRun、限定 pytest、監査を起動する。

新規コードの import・クラス・関数全文は `SOURCE_CODE.md` に掲載する。実装に省略コードはない。

## 完了条件

DryRun・Source Guard・限定 pytest が成功し、$k=31$ について次を実測できること。

- `ABSTRACT_CERTIFIED=True`、抽象成分は8個の $\mathbb Z/2$
- 根の証明ステップは4前提（出典付き命題、2つの先行 DB、出典から導出した Hopf 関係）を持ち、推論検証が再実行可能である。
- `NAMED_SHAPE=False`、`PUBLIC_COMPLETE=False` のまま、記名生成元の等式を捏造していない。
- $k=8$ の未証明生成元も不当に完成しない。

## 次工程との境界

R15R7 は「抽象群の独立した証明木」を完成させるための Phase であり、公開 Web の `generic-complete-proof` を変更しない。次工程では公開検索の応答型に、抽象群と記名生成元の証明状態を独立に載せる方法を検討する。推論で得られない個別生成元の等式を付与しない。全体 pytest は Phase 173 終了時のみ。
