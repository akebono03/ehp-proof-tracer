# Phase 165 R6-8 — 生成元の表記差を修正

変更対象: `toda_rules.py` の既存 `toda_53_eta3_twice_zero_inference_rule` 全体、および `probes/probe_phase58_capabilities.py` の import 全体・`build_phase58_representative_result` 全体。新規テスト `test_phase165_r6_8_eta_name_fix.py` の2関数。変更箇所の元コードを AST と文字列照合してから、その関数全体を置換する。新規規則・新規 Renderer は追加しない。

変更内容: π₄³ が位数2で、生成元が HomotopyElement、次数・始域・終域・GeneratorSymbol が同一で、名前が `η₃` または `η_3` である場合のみ規則を許す。既存の数学的条件を維持。Phase 58 の旧 Phase 50 呼出しを現行の共通探索に切り替える。

実行: `powershell -ExecutionPolicy Bypass -File .\phase165_r6_8_eta_name_fix\run.ps1`

限定 pytest 2件が PASS した場合のみ適用を確定する。不一致・テスト失敗の場合は両ファイルをロールバック。既存の `.r6_8_eta_name_fix.bak` を上書きしない。全体 pytest は行わない。

終了条件: Phase 58 の接続テスト PASS。これだけで R6-8 全体（105件）は完了としない。Phase 53/55 は次の接続対象。
