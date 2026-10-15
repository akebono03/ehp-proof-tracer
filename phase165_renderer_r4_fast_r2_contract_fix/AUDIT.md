# Phase 165 R4 再実施の原因分析

- 前回の40ファイル・43 import 移行は完了したが、限定テスト16件中2件が失敗。復元処理は成功と報告された。
- `test_r11_partial_and_compatibility_are_one_renderer`: 出典情報を持たない `references` 文字列を文献参照として表示することを要求。現行 Renderer は出典付き ProofStep のみ使用するため、期待値が旧仕様。
- `test_r11_same_renderer_handles_completed_proof`: `ProofRule.GIVEN` を完成証明に利用。現行 `phase165_r56_presentation_adapter.py` は推論規則による derived root を要求。
- 数学的検証を緩めないため、2件の旧テスト期待値のみ訂正。完成証明・未完成証明の本文は snapshot 前後で完全一致させる。
- 前回のバックアップは保存し、新しい専用バックアップで実行する。
- この修正は実環境では未検証。Phase 165 全体 pytest は実施しない。
