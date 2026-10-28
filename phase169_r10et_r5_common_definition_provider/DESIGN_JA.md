# Phase 169 R10ET-R5 — 共通 Definition の本番探索優先

## 直前の根拠

R10ET-R2 は、共通 Definition を探索時に優先して16ケースの完成証明と Trust Boundary を維持した。ただし、巡回群の圧縮表示は欠けた。R10ET-R3B は、型付き検証済み Definition に限定すれば巡回群2ケースの表示を回復可能と確認した。R10ET-R4 は当該 Projection と Renderer を実装し、限定 pytest 68 PASS・10ケース Trust PASS を確認した。

## 変更対象

1. `phase165_r52_r9_shared_math.py` の **`shared_expansion_provider` 全体**（その内部の `expand` を冒頭で共通 Definition 優先にする）。
2. `phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py` の `test_r10a_4fold_eta_square_is_single_certified_display` 全体。
3. `phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py` の `test_r10ec_complete_pi39_compresses_all_verified_image_prose` 全体。
4. `phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py` の CASES 定数（旧 Proof Tree 固有の suppression 件数を共通 Definition に合わせる）。
5. `phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py` の `test_r10er_mixed_direct_sum_has_two_compressed_images` 全体、`test_r10er_common_definition_replaces_cited_prefix` 全体（旧テストを改名して置換）。
6. 新規 `patch.py`、`audit.py`、`run.py`、`tests/test_r5_patch.py`、`tests/test_r5_live.py` は本フォルダに追加。変更後の import 部分はファイル全文とともに出力する。

## 厳密な境界

`GeneratorImage` が厳密な安定範囲で共通 Definition に該当する場合だけ、ゼロ前提の replayable `GoalExpansion` を優先する。該当しない `Goal` では既存探索を維持する。定義は新しい群同型や DB 事実、異なる元の同一性を証明しない。

DB prior と Toda (4.5) は独立した引用付き祖先として保持する。旧個別 Definition の登録・台帳は今回は削除しない。Reference の個別 Definition が消えるのは Proof Tree がそれを利用しなくなるためであり、Renderer が意図的に隠すためではない。

## 検証と完了条件

限定 pytest：新規2ファイル、変更した4既存テストファイル、R4、R10EQ、R10EN、R10ES。実際の本番探索16ケースで complete・Trust PASS、R2 shadow 基準との Definition 件数と引用の一致、巡回群2ケース・直和群7ケースの圧縮表示、引用祖先を確認する。

失敗時は R5 で変更した5ファイルだけ元に戻し、R4 の作業差分は維持する。全体 pytest は実行しない。

## 次 Phase との境界

R5 は探索上の Definition 優先を固定する。個別 Definition 登録の除去、一般 Definition の数学的意味の拡張、Renderer の大規模再設計、全体テスト・文書の主要ファイル更新は行わない。
