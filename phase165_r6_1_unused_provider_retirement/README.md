# Phase 165 R6-1: 未使用の群専用 Provider 経路の撤去

対象は `phase165_r52_r7_registered_common_proof.py` の `RegisteredProofProvider`、`registered_proof_providers()`、`build_registered_common_replay()` と、対応する旧専用 Provider テストです。

公開画面の通常経路で利用される `search_shared_group_goal()` は維持し、`phase165_r14_r38_direct_registry.py` の `build_adopted_typed_reference_registry()` は絶対に削除しません。

`run.ps1` はバックアップを作って、対象テストだけを実行します。全体 pytest は実施しません。過去の監査・開発用ファイルの削除、`pi32_goal()` など他経路に依存する関数の削除、および `pi4^3` Adapter の撤去はこの変更に含めません。後者は共通逆向き適用の同等性を確認してから行います。
