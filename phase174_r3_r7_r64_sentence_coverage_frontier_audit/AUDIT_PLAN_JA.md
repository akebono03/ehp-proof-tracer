# Phase 174 R64 — 文章単位の出典監査範囲の棚卸し

## 既存コード・関連テストの確認

- GitHub `akebono03/ehp-proof-tracer`, `develop`, 監査時 `13300ea3e2d4e51d020772e7089a5f60246f8cf5`。HEAD は固定しない。
- `phase168_r3_3_proof_narrative_model.py`：引用番号と各 ProofStep の所有関係。
- `phase168_r3_5_model_renderer.py`：Reference セクション後に `証明` を出す共通 Renderer。
- `phase168_r3_12_body_binding.py`：各 ProofStep の出典番号を相互検査。
- `phase174_r3_r7_r60_reference_ownership_audit/audit.py`：双方向の引用対応。
- `phase174_r3_r7_r61_reference_attribution_route_audit/audit.py`：3経路を監査。
- `phase174_r3_r7_r63_sentence_witness_audit/audit.py` と `tests/test_audit.py`：出典祖先と5個の対象文章の引用照合。

## 目的

2群の全証明段落を棚卸しし、R63 が引用根拠を検査した3段落および2段落と、それ以外を明確に分ける。数学的な内容の正否や各文章の出典の十分性を機械的に推認しない。

## 変更対象

新規ディレクトリ `phase174_r3_r7_r64_sentence_coverage_frontier_audit/` のみ。
- `audit.py`：新規関数 `git_blob_sha`, `source_guard`, `local_head`, `proof_body_lines`, `priority_of_untested_line`, `audited_line_inventory`, `inspect_public`, `main`（この順で追加）。
- `tests/test_audit.py`：新規テスト関数をファイル全体として追加。
- `run.ps1`、`README.md`（英語）、日本語の監査・コード・テスト文書を新規追加。

既存の import・クラス・関数・テスト・主要5文書は変更しない。新規 GIVEN・数学規則・ProofStep は追加しない。

## 完了条件

- Source Guard が Git Blob SHA 8件と照合して PASS。Git HEAD はログに記録するのみ。
- `π_11^6` と `π_12^7` が完成したままで Reference は 7件と3件。
- R63 の対象3段落と2段落が一意に実際の証明本文と一致する。
- すべての非空段落を棚卸しし、未監査段落を `UNREVIEWED_SENTENCE_RELEVANCE` と表示する。
- 限定 pytest PASS。全体 pytest を実行しない。

## R65 との境界

R64 は監査対象の一覧を作るだけ。R65 が未監査段落の出典根拠を確認するときも、表示の引用と数学的証明の正しさを混同しない。Renderer の無条件共通化を先取りしない。
