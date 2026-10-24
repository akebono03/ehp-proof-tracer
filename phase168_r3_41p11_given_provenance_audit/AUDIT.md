# Phase 168 R3-41P11 — 作業境界（監査のみ）

## 実装前に確認したコード

GitHub `akebono03/ehp-proof-tracer`, `develop` にある以下の現行ファイルと関連テストを確認。

- `phase165_r3_recursive_search.py`: `find_inference_matches_for_rule()` と `derive_inference_proof_step()` を利用する探索経路。
- `phase165_r52_r2_search_adapter.py`: 観測済み Step を `PartialProofResult` に格納。
- `phase165_r52_r16_web_citation_gate.py`: screened bridge を作成する文献前提選別。
- `phase165_r52_r9_shared_math.py`: 同一 screened bridge を使う検索。
- `phase168_r3_4_link_bridge.py`: GIVEN とリンクの一致によって引用を投影。
- `phase168_r3_3_proof_narrative_model.py`: 型付き Step と Citation の関連。
- `phase168_r3_12_body_binding.py`: Citation の相互整合性を確認。
- `unified_statement_registry.py`: 文献前提の `AssertionOrigin.FIXED_STATEMENT` と `ProofStepLink`。
- `phase166_r3c_publication_order.py`: 同一出典を含む文献順判定。
- `phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py` 等の限定テスト。

## 変更対象

アプリ本体・既存テストへの変更なし。新規ディレクトリ `phase168_r3_41p11_given_provenance_audit/` のみ。

新規ファイル・関数の全文は ZIP に含む。

## 監査項目

1. 公開Webで使用された `result`, `screened bridge`, `model`, `markdown` の単一路線を捕捉する。
2. 各 GIVEN について、同一 screened bridge に含まれるリンク・`FIXED_STATEMENT`・同じ結論・Model Citation を調べる。
3. 不登録の人工 GIVEN が Model に格納でき、screened bridge との照合では拒否されることを確かめる。
4. 三群の全文・Reference・Citation・固定主要論証の回帰を確認する。

**注意:** 文献順 `publication_position` の判定条件や推論規則の適用を再認証しない。3群の GIVEN がすべて対応済みであるかも実行結果で判断する。全体 pytest は Phase 終了時まで実行しない。
