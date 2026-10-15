# Phase 165 R5-R5 監査計画

## 前提

R5-R4 のログでは限定テスト11件成功、稼働中の旧 Generic import 0件、共通 Dispatcher と公開定義各1件を確認した。補助 Renderer の候補26件は未分類。過去の Phase 162 テスト6件は `prop51_steps` が空で失敗しており、依然未解決である。

## 今回の対象

新規ファイル `phase165_renderer_r5_r5_callgraph_audit/audit.py` の `load_base`, `reference_sites`, `definition_call_sites`, `analyze`, `main`、および `test_audit.py` の5つのテスト関数。既存の本番関数・クラス・import は変更しない。

## 判定方法

R5-R2 が抽出した26件の各ファイルについて、モジュール名による静的 import と、明示的な関数呼出を AST で収集する。独立公開入口になりうる関数を含むものは `POTENTIAL_INDEPENDENT_ENTRY`、呼出元がある部品は `CALLED_HELPER_REVIEW`、直接呼出が検出されないものは `NO_DIRECT_CALL_FOUND_REVIEW` として記録する。すべてレビュー対象であり、自動的に「一本化済み」とは認定しない。

## 完了条件と次作業

R5-R5 の完了条件は26候補の証拠一覧が生成できること。R5 全体の完了条件は、候補に含まれる独立 Narrative 入口の実際の実行経路を確認し、必要なものだけ移行した上で、旧 Phase 162 の既知失敗を解決または別扱いの根拠を確立すること。全体 pytest は Phase 165 終了時のみ。
