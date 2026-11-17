# Phase 175 R3R12R3 — 型付き単射表示と結論重複の修正

## 変更対象（事前列挙）

1. 既存 `phase175_r3r11_cited_hopf_narrative/projection.py` の `project_verified_source_and_hopf_summary()` 全体を、R3R12 で監査済みの接続関数に置換。**import とそれ以外の関数は変更なし**。
2. 新規パッケージ `phase175_r3r12_hopf_conclusion/projection.py` の import に既存の `typed_sentence` を追加し、`project_verified_hopf_lift_conclusion()` **関数全体**を置換。
3. `phase175_r3r12_hopf_conclusion/tests/test_projection.py` に `test_injectivity_line_matches_the_real_typed_renderer()` と `test_missing_injectivity_line_preserves_original()` を、既存 `test_missing_rendered_summary_does_not_infer_surjectivity()` の直前へ追加。既存テスト・import は維持。
4. `audit.py` の Gate・ログ ID、`run.ps1` のログ ID を R3R12R3 に更新。
5. `README.md`・`AUDIT_PLAN_JA.md`・`CODE_FULL_JA.md`・`TEST_RESULTS_JA.md` を**全文更新**。基幹5文書、数学的コード、GIVEN、推論規則は変更しない。

## 現行コード・関連テストの事前監査

GitHub `akebono03/ehp-proof-tracer` `develop` の R3R11R4 表示本体（Blob `258d22589f92fbebdb9c4516dbe72c1f94a98afd`）、`phase171_r20r13_eta_sentence_layout/projection.py`、`phase168_r3_27_typed_statement_projection.py`、`phase168_r3_5_model_renderer.py`、Phase 172 と R3R11R4 の既存テスト、R3R12R2 の配布コードと実行失敗ログを確認した。

R3R12R2 の Windows 限定 pytest は **47 passed, 2 failed**。失敗は `test_pi73_single_final_conclusion_and_hopf_isomorphism()` と `test_internal_cyclic_latex_is_not_a_second_proof_requirement()` で、検証済み結論の二重表示が残ることによる。`ROLLBACK=RESTORED` で既存コードに戻った。

## 原因と修正

旧表示の一意性検査は、証明木で単射が立証されていても、表示済み行を `"H:" + source_group` で探索した。既存 `map_property_sentence()` は `rf"${symbol}: {source}\\to {target}$ は{label}."` を返すため、実際は **`H: ` と空白が入る**。一致する行を発見できず、後続の全射・同型文章と重複削除に到達できなかった。

R3R12R3 では、3前提を持つ既存 Hopf lift の証明書を確認したうえで、`typed_sentence(injective_step.conclusion, injective_step)` から得た実際の表示文章と行を**完全一致**させる。数学的な単射の主張を Renderer が推論するわけではない。候補が一意でなければ表示変更を拒否する。

## 完了条件

- $\pi_7^3$（`n=3,k=4`）は `complete`、`generic-complete-proof`、Trust `True`、Reference 7件を維持。
- [R5] [R6] [R7] の Hopf 1式、[R4] の生成元、実際の単射性行が存在する場合のみ、全射と同型を説明。
- 重複する途中の群結論のみ除去し、`以上より,` の最終結論は1回残す。
- $\pi_6^3$ の Phase 172 表示と、引用・計算・Proof Tree は維持。
- 数学的 GIVEN 追加0、推論規則追加0、フル pytest 実施なし。

## 限定テストと次 Phase の境界

`audit.py` の `TEST_PATHS` で R3R12・R3R11R4・R3R10・R3R9・Phase 172・171 と R70 の有効な機能テストを実行する。**全体 pytest は Phase 175 の最後**。次の R4（$\pi_9^5$）の機能は先取りしない。

Gate: `PASS_R3R12R3_VERIFIED_HOPF_ISOMORPHISM_SINGLE_CONCLUSION`。
