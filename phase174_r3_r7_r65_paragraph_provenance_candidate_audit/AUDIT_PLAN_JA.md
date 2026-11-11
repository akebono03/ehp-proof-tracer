# Phase 174 R65 — 未監査文章の証明ステップ候補の監査

## 実装前のコード・関連テスト確認

2026-11-11 の GitHub `akebono03/ehp-proof-tracer` `develop` を確認。監査時の develop は e5e392ddd2177fc4db70da48b1c1e6418b33c519 と同じ系譜上で、対象本体ファイルの Git Blob SHA はソースコード内の PINS を参照。

関連：`phase168_r3_3_proof_narrative_model.py`、`phase168_r3_12_body_binding.py`、`phase168_r3_5_model_renderer.py`、`phase168_r3_27_typed_statement_projection.py`、R63 `audit.py` とテスト、R64 `audit.py` と修正済みテスト。R64 はユーザーが ZIP 適用しており、本体ソースのバイト列を固定する。

## 変更対象

既存 production code、推論規則、証明木、データベース、Reference、既存テスト、主要5文書は変更しない。

新規ディレクトリ `phase174_r3_r7_r65_paragraph_provenance_candidate_audit/` のみ：

- `audit.py`：新規 `git_blob_sha`、`source_guard`、`local_head`、`matching_projection_candidates`、`classify_candidate`、`projected_step_catalog`、`verified_citation_ancestry`、`classify_unreviewed_paragraphs`、`inspect_public`、`markdown_report`、`main`。既存クラス・関数の改変はない。
- `tests/test_audit.py`：新規テスト・fixture 関数。全文は CODE_FULL_JA.md に記載。
- `run.ps1`：DryRun、本監査、限定 pytest。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`。

## 監査対象・完了条件

- R64 の未監査段落全15件を欠落なしに記録（π11^6 11件、π12^7 4件）。
- 数式断片は現行の typed_sentence と `build_narrative_body_lines` の出力でのみ照合する。
- 対応する ProofStep の実際の祖先を追跡し、GIVEN 祖先の引用番号と比較する。
- 一致が複数・不一致・対応なしの場合は曖昧性を消さずに記録する。
- Text match は数学的な「全文の文章単位引用検証」に昇格させない。
- SOURCE_GUARD、限定 pytest PASS。全体 pytest は Phase 最終まで実施しない。

## 次の境界

R66 以後では未解決または候補のみの段落を対象に、実際の数学的帰結をタイプ付き推論規則の前提に照らして確認する。R65 は Renderer を改変せず、結論専用 Narrative を追加しない。
