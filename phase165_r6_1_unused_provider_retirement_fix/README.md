# Phase 165 R6-1 — unused provider retirement runner fix

原因: `build_registered_common_replay()` の `if providers is None:` は `else` を持たない。前回の `apply.py` は誤って `else` を必須としたため、書換え前に失敗した。

修正: `if providers is None:` の構造を正しく検証する。従来の変更範囲（旧 Provider 登録と分岐の削除、共通探索の維持）以外には触れない。`apply.py` と本監査パッケージの README を全文置換する。production file は runner が対象を照合して更新する。

実行: リポジトリ直下で `powershell -ExecutionPolicy Bypass -File .\phase165_r6_1_unused_provider_retirement_fix\run.ps1`。

限定 pytest: `phase165_r52_r7_registered_common_proof/test_phase165_r52_r7_registered_common_proof.py` のみ。全体 pytest は実施しない。

完了条件: 旧 Provider の登録・専用分岐がなくなり、通常の共通探索経路の限定テストが通ること。他の歴史的経路や pi4^3 Adapter は今回変更しない。
