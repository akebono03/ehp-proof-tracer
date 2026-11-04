# Phase 173 R4-R15R12R2：限定 pytest 契約の残存固定値修正

## 直前の失敗と根拠

利用者のログでは R15R12 DryRun 5 PASS、通常実行の限定 pytest は `2 failed, 24 passed, 6 errors` となり、`PHASE173_R4_R15R12_RESTORED=PASS` により本番コードは復元された。

失敗の独立した原因は以下の2件である。

1. 新規 `test_prop44_reference_displays_full_isomorphism_not_prelude` が `E:\pi_{i-1}^{n-1}\to\pi_i^n` と厳密比較したが、実際の正しい TeX は `E:\pi_{i-1}^{n-1}\to\pi_i^{n}` だった。数学的内容を変えず、テストの波括弧のみ訂正した。
2. 歴史的な R4G/R4E の `pi64` fixture と Web テストが、ProofStep を18件と固定していた。現行 Source-first / First Successful Proof Search は17件の COMPLETE を返す。実際の結論を導く ProofStep の存在と Web のステップ数が同じことを監査するテストに改める。証明ステップ数を増やさず、18件に合わせるための推論規則は追加しない。

GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `e2996ec2ff496203f94daa9bc22550c5e69a6b11` と対象の既存テストを確認済み。R15R12 の失敗時点の未適用状態を基準とし、HEAD と対象ファイル5件の Git Blob を検査する。

## 変更対象（ファイル／関数）

本番用の変更対象は R15R12 と同じ3ファイルのまま（内容も変更なし）。

- `phase168_r3_37c_reference_projection.py`：`project_reference_bodies`、新規 `_verified_source_sentence`・`project_cited_proof_step_reference_bodies`（先頭 import の直後へ追加）
- `phase168_r3_3_proof_narrative_model.py`：`build_proof_narrative_model`
- `web_group_proof_common.py`：`_build_group_proof_inline_segments`

直接のテスト修正は2ファイル。

- `phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py`：`pi64`、`test_r4g_fibration_is_in_same_source_bound_reference`、`test_r4g_web_and_pi53_existing_route_unchanged`
- `phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py`：`pi64`、`test_r4e_standard_web_path_remains_verified_and_complete`

配布パッケージ側では `patch.py` の既存 `patch_existing_test`・`patch_source`・`changed_units`、新規 `patch_r4e_test`（既存 `patch_existing_test` の直後）、`install.py` の Git Blob ガードと `tests/test_static.py` の新規 `test_first_success_step_count_contract_in_both_historical_tests`（末尾に追加）、`tests/test_integration.py` の1件の期待値を更新した。import の変更は `tests/test_static.py` の R4E_TEST_PATH, TEST_PATH の追加だけである。

## 安全性

- ProofStep、GIVEN、出典本文、出典登録、Root Certification、および既存の public search は変更しない。
- 既存の R4G/R4E の出典、引用番号、完全性、EHP の検査を削除しない。
- 過去の実装で 18 と決め打ちしていた件数は数学的結論の同一性を保証しないため、結論の ProofStep の存在と結果の Web 反映数の一致で検査する。
- パッチの再適用、未承認 Blob、HEAD 変更、混合改行は拒否する。限定テストまたは監査が失敗したら5ファイルを復元する。
- `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` 等の既存主要文書は変更しない。

## 実行確認と完了条件

DryRun ではソース Guard、再適用拒否、5ファイルパッチ構文、強調内 TeX の分割などを限定検査する。通常実行では本番3ファイルと歴史テスト2ファイルを一時的に更新して、R15R12 の限定 pytest と n=4,k=3,4,7,8,31 の Web 監査を行う。全体 pytest は Phase 173 の最後にのみ実行する。

完了条件は `PHASE173_R4_R15R12_FOCUSED_PYTEST=PASS`、`PHASE173_R4_R15R12_AUDIT=PASS`、Proposition 4.4 の同型、Lemma 5.4 の本文、先行 DB の数式、未解決 Goal の状態が保持されることである。今回のパッケージ作成だけでは完了扱いにしない。

## 次工程との境界

R15R12R1 は Reference 表示とテスト契約の訂正まで。抽象群 ProofStep の引用統合、二重見出しの解消、記名生成元の追加証明を先取りしない。

## R15R12R2：追加の失敗と修正

利用者が R15R12R1 を実行したところ、DryRun の静的テストは6件 PASS、本実行は `31 passed, 1 failed` で停止し、`PHASE173_R4_R15R12_RESTORED=PASS` と報告された。未修正だった箇所は、R4G の `test_r4g_web_and_pi53_existing_route_unchanged` 内にある先行群 $\pi_5^3$ の ProofStep 件数固定値28である。現在の完成探索は27件を返しており、`ProofSearchStatus.COMPLETE` を維持する。

修正対象は配布パッケージ `patch.py` の `patch_existing_test` と `tests/test_static.py` のみ。元の `assert len(previous.proven_steps) == 28` を、`assert any(step.conclusion == previous.conclusion for step in previous.proven_steps)` に置換する。テストでは元の固定値の存在、置換結果、`COMPLETE` の検証維持、再適用拒否を確認する。既存の数学的規則・Reference投影・Web表示・本番3ファイルのパッチ内容は一切変更しない。

本 ZIP はあくまで R15R12R2 の再実行用であり、限定 pytest と公開 Web 監査の実測結果を得るまで R15R12 完了とは判定しない。Phase 173 の全体 pytest は実施しない。
