# Phase 166 R3-AI π₃² identity repair

変更対象：`phase166_r3af_goal_adapter.py` の `_generator_for_target` 関数全体。生成元の型と名称を既存の `ETA_2` に合わせる。証明規則と表示処理には変更なし。

実行：リポジトリルートに展開して `powershell -ExecutionPolicy Bypass -File .\phase166_r3ai_pi32_identity_repair\run.ps1`

実施テスト：π₃² の型同一性・候補選択・実探索、R3-AF 既存テスト、R3-AI 既存テスト。全体 pytest は実行しない。

完了条件：実探索 `ProofSearchStatus.COMPLETE` と対象の限定テスト PASS。非安定の複合生成元や零群の一般変換はこの修正の対象外。
