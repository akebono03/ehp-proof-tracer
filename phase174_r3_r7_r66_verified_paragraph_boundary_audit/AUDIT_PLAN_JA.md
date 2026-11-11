# Phase 174 R66 — 監査計画

## 実装前に確認した現行 GitHub と関連テスト

- リポジトリ `akebono03/ehp-proof-tracer` の `develop` は、監査時点で `2c22e4bdeee035776b202e8d50fd4aaf85f53b5c` の後継コミットに進んでいる。固定 HEAD ではなく、関連コードの Git Blob SHA を検証する。
- `phase174_r3_r7_r65_paragraph_provenance_candidate_audit/audit.py`、`tests/test_audit.py` を確認。R65 の候補分類は文字列と祖先候補の照合であり、数学的な文章全体の妥当性ではない。
- `phase174_r3_r7_r63_sentence_witness_audit/audit.py` と `phase174_r3_r7_r64_sentence_coverage_frontier_audit/audit.py` を確認。R63 は対象5行の引用根拠を監査済み。R64 は未監査15段落を列挙。
- `phase168_r3_3_proof_narrative_model.py`、`phase168_r3_12_body_binding.py`、`phase168_r3_5_model_renderer.py`、`phase168_r3_26_exactness_projection.py`、`phase168_r3_27_typed_statement_projection.py` を確認。完全列は型付き窓を連結した表示であり、単一の typed_sentence と一致しない場合がある。

## 今回の変更対象

**新規追加のみ**：`phase174_r3_r7_r66_verified_paragraph_boundary_audit/`

- `audit.py`：`git_blob_sha`、`source_guard`、`local_head`、`certified_exactness_line_index`、`actual_step_detail`、`validate_frontier_record`、`inspect_public`、`markdown_report`、`main` を追加。
- `tests/test_audit.py`：新規20テストケースを追加。使用する補助関数は `fake_record`、`fake_step_details`、`candidate`。テストの import と関数全文は `CODE_FULL_JA.md` を参照。
- `run.ps1`：DryRun、監査実行、限定 pytest を順番に実行。
- `__init__.py`、`README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md`。

既存 import・既存クラス・既存関数は一切変更しない。

## 数学的・出典上の保証境界

1. R65 の候補を証明木の root ancestor（根の祖先）へ照合する。引用付きの6段落は引用番号が実際の GIVEN 祖先にあることを再検証する。
2. 引用のない7段落は Verified ProofStep 候補との構造的対応を確認するが、引用を自動追加しない。
3. 直接の型付き文字列と一致しない2段落は、既存の `project_exactness_chains` が生成する完全列と文字列が**完全一致**する場合のみ「既存の完全列の表示に由来」と記録する。一致しない場合は未解決のまま維持。
4. 上記のいずれも日本語の証明文章全体について独立した数学的証明を与えるわけではない。R63 の既存5行以外に文章全体の妥当性証明を増やさない。
5. R65 の既知の15段落の分類件数に変化があれば安全側に停止する。全体 pytest は Phase 174 終了時まで行わない。

## 完了条件

- 9ファイルの Source Guard PASS。
- 既存 Group query 2件の complete 証明を再実行し、Reference 件数7・3件を保持。
- 未監査15段落のすべてに構造的な境界判定を保存。
- R66 と関連 R65/R63 限定 pytest PASS。
- 新規 GIVEN 0・数学的規則0・Production 変更0。

## 次の Phase 境界

R67 では R66 の `report.json` で曖昧と残った文章だけについて、証明ステップとの正確な意味上の対応や出典表示修正の必要性を検討する。R66 は Renderer 統合や証明規則の改変を先取りしない。
