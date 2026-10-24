# Phase 168 R3-41P3 — 範囲と完了条件

R3-41P2 実測：32件 PASS、ProofStep 18/25/10、Reference 4/4/3、引用の不整合なし。

再検証7回の内訳：π₃²で4、π₄³で1、π₅⁴で2。

変更するのは次の関数だけ。

- `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` 内にある `validated_specialization_citation_numbers()`（新名称：`direct_given_premise_citation_numbers()`）と呼び出し1箇所。
- `phase168_r3_27_typed_statement_projection.py` の `toda45_specialization_evidence()`。

変更後の引用元は ProofStep にある `GIVEN` 前提と `model.step_citation_numbers` から取得し、数学的 Rule を再実行しない。

Toda (4.5) の $(n,m,k)$ は証明済みの `TodaIteratedSuspensionMap` の source/target の次数から表示値として算出する。適用条件の数式不等式は再判定しない。

全文比較の基準は添付 R3-41P2 監査 ZIP の公開 Web 3群の出力。本文と Reference の完全一致をテストする。

完了条件：3群全文一致、Citation 一致、Renderer/Projection からの `specialize_typed_statement()` 呼び出しがない、限定 pytest PASS。

境界：`_stable_eta_renaming_shape()`、`prop42_exactness_indices()`、推論規則名依存は今回変更しない。全体 pytest は Phase 168 終了時のみ。

安全策：変更前の SHA-256 はユーザーの R3-41P2 `audit.json` に記録された値と照合し、不一致の場合は変更しない。
