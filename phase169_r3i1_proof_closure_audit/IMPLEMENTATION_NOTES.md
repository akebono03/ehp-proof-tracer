# Phase 169 R3I1 — 修正一覧と完了条件

## 監査結果に基づく原因

R3I は 36 件中 33 PASS / 3 FAIL で停止した。別々の歴史的規則ファクトリの戻り値に含まれる関数は別オブジェクトだが、内部の Python コードオブジェクトは同じであるため、`match_guard is ...` と `conclusion_builder is ...` のテストは不正確だった。R3I 適用後、π₅³ は実探索で COMPLETE となり、R3H の二つのテストに固定された旧 partial 期待値と矛盾した。

## 変更対象

- `phase165_r52_r9_shared_math.py` — `shared_expansion_provider()` の全文。**前回 R3I からコード変更なし**。
- `phase165_r14_r5_ehp_connection.py` — `audit_ehp_connection()` 直前に `expand_cited_ehp_terminal_goal()` を新規追加。**前回 R3I からコード変更なし**。
- `phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py` — `test_r3h_actual_publication_position_is_prior()` および `test_r3h_historical_terminal_requires_inference_even_after_citation()` を関数全体として置換。「部分証明である」を削除し、文献順・歴史的規則が不変であることだけを検証する。他の 4 件は変更しない。変更後のテストファイル全文は `full_tests/` にある。既存 import に残った不要な `ProofSearchStatus` は削除する（import 全文は同ファイルに掲載）。
- `tests/test_phase169_r3i_cited_ehp_inference.py` — `test_r3i_historical_inference_only_rules_remain_intact()` を関数全体として修正。関数本体のオブジェクト同一性ではなく `__code__` の同一性を検証する。import 全文・テスト8件全文を同梱。
- `audit.py` — `validate_completed_proof_tree()` を新規追加（`audit()` の直前）。`audit()` 全文を変更し、数学的規則のコードオブジェクト、完成したルート ProofStep、すべての推論の再実行、すべての GIVEN の先行文献リンク、EHP の２つの終端導出を検証する。必要な import 全文を同ファイルに掲載。
- `tests/test_phase169_r3i1_proof_closure_audit.py` — 新規テスト2件を追加。import とテスト関数全文を同梱。
- `patch_r3h_tests.py` — リポジトリ上で確認したテスト Git blob `0d6b2a4ca34534425fae125ce29f0523d0cdd71e` を確認してから置換。失敗時に元のテストへ復元。
- `apply.py` — 前回 R3I と同一。2本の本番関数を正確に適用し、自動復元する。
- `run.ps1` — 限定テストと実証監査を実行し、失敗時にはテストと本番コードを元に戻す。

## 限定 pytest

`python -B -m pytest -q -p no:cacheprovider` を使用して `run.ps1` に記載した Phase R3F3、R3H、R3I、R3I1 と既存 EHP テストに限定して実行する。

## 完了条件

`R3I1_FOCUSED_PYTEST_EXIT_CODE=0`、`R3I1_AUDIT_EXIT_CODE=0`、`R3I1_CLOSED_PROOF_TREE_VERIFIED=True`、`R3I1_COMPLETE`。

これらが確認されるまでは、π₅³ の完成宣言を行わない。全体 pytest は Phase 169 最終時にのみ実施する。

## 次段階

完了後に Renderer と Reference の品質、凍結文章との差分、生成元の表記、π₆⁴ の輸送を別 Phase 手順で扱う。本段階で先取りしない。
