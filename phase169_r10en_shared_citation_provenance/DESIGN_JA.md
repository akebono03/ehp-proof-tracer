# Phase 169 R10EN — Citation Provenance 共通化

## 入力監査と対象

GitHub `akebono03/ehp-proof-tracer` の `develop`（R10EM を含む現行ブランチ）で、R10A/R10EC の Projection、R10EL の非表示処理、共通 Renderer、関連する限定テストを確認した。変更するのは次のものに限る。

- 新規 `phase169_r10en_shared_citation_provenance/core.py` の `verified_generator_image_citation_numbers()`。
- 既存 `phase169_r10a_verified_stable_chain_projection/projection.py` の `project_verified_stable_image_chain()`。
- 既存 `phase169_r10ec_direct_sum_narrative_projection/projection.py` の `project_verified_direct_sum_transport()`。
- 新規検証テストと実行・監査スクリプト。

トップレベル import と公開 API は変更しない。各既存関数内の import は変更後の関数全文に記載する。数学的関係、ProofStep、引用台帳の作成・編集は行わない。

## 共通化する責務

`verified_generator_image_citation_numbers(model, order, image_steps, require_each)` は、与えられた検証済み Proof Narrative Model から、入力生成元像の GIVEN 祖先をオブジェクト同一性で探索し、登録済み引用番号を Reference 順で返す。

巡回群の `require_each=False` は「全生成元像の引用の和集合が空でない」という既存条件を維持する。直和群の `require_each=True` は「各生成元像に引用付き GIVEN が存在する」という既存条件を維持する。両方とも未登録引用、未登録祖先、モデル内に存在しない ProofStep、重複した生成元像を拒否する。**文字列や生成元名から引用を推測しない。**

R10EL が確立した非表示ステップの消費先・個別引用・GIVEN 保護の条件は、引き続き同じ共通関数で確認する。R10A と R10EC の群構造別の輸送・同型・生成元検証および数式構成は変更しない。

## 検査対象

| 群 | 生成元像 | 懸垂回数 | 非表示数 |
|---|---:|---:|---:|
| $\pi_{28}^{22}$ | 14 | 14 | 31 |
| $\pi_{32}^{22}$ | 10 | 10 | 40 |
| $\pi_{23}^{15}$ | 10 | 5 | 10 |
| $\pi_{33}^{24}$ | 39 | 13 | 110 |

合計73個の生成元像に対して、R10EM と同じ Trace 結果を比較する。`complete`・Trust PASS、Reference 全件表示、同一の引用番号、数式の重複0件、Proof Tree 不変が完了条件。

## 実行と失敗時処理

`run.ps1` は現在の `develop` と Git blob を検査する。16件の独立した限定 pytest を行い、2ファイルに検証済み全文を適用してから既存の限定テストと4群の実監査を実行する。pytest cache は無効化する。検査失敗時はバックアップから2ファイルをバイト単位で復元する。全体 pytest は Phase 169 終了時のみ行う。

## 次 Phase との境界

今回は Citation Provenance の共有に限定する。R10A と R10EC の数式本文構成や Renderer の一本化、自由巡回群・零群の拡張、11-/14-stem の未完成証明の補完は先取りしない。
