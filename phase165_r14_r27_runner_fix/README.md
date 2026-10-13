# Phase 165 R14-R27 runner fix

変更対象: `phase165_r14_r27_scope_delta.py` (`audit_r27` 全体と import 部)、`test_phase165_r14_r27_scope_delta.py` (`test_detect_explicit_exclusion_in_context` 全体)、`run.ps1`。その他は前回と同一。

修正: TeX fixture を正常な一重のバックスラッシュにする。R24 の `audit_r24` は `tex_path` 必須なので R27 の適用範囲監査から呼ばない。R24 の再監査状態は `null` として報告し、成功を装わない。

完了条件: 対象6件合格。`n=1` 未認証・実証明0の境界を維持。次工程で Prop 4.2 の適用範囲を原文から検証する。全体 pytest は行わない。
