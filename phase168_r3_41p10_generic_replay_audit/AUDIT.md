# Phase 168 R3-41P10 — 既存の matcher による汎用再検証（監査のみ）

## 監査対象（本体は変更しない）

- `proof.py` — `find_inference_matches_for_rule()`、`apply_inference_match()`
- `phase164_r8_proofstep_factory.py` — `derive_inference_proof_step()`
- `phase165_r3_recursive_search.py` — `reconstruct_registered_goal()`
- `phase165_r52_r2_search_adapter.py` — 探索結果へ渡す `ProofStep`
- `phase165_r52_partial_proof.py` — `PartialProofResult`
- `phase168_r3_3_proof_narrative_model.py` — `ProofNarrativeModel`
- `phase168_r3_27_typed_statement_projection.py` — 表示層の残存再検証

## 監査方法

1. 公開 Web 経路から3群の Proof Tree、Narrative、Citation を取得する。
2. **監査内部だけ**で各推論 Step の前提を `find_inference_matches_for_rule()` に渡す。
3. 同じ前提から型付き結論を再生成し、元の結論と一致するか確認する。
4. R3-41P9 の全文と比較し、Reference と Citation の保存を検査する。
5. 偽の安定 η 表記と偽の EHP 像＝核 Step を Model に渡して、汎用再検証なら拒否できるか確認する。

## 注意

この方法は Renderer から数学的処理を排除する候補にはなるが、**検証の重複**が探索から Model の入口へ移るだけである。

また GIVEN（文献由来の既知命題）の真正性・文献順序をこの試作は保証しない。推論検証で成功しても、ただちに「完全な証明書」とはいえない。

実装方法の最終判断は監査結果を見て行う。全体 pytest は Phase 終了時のみ実行する。
