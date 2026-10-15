# R5-R4 監査と変更境界

- 変更対象: `tests/test_phase162_r2_validated_proof_presentation.py` 内のローカル import 2箇所のみ。
- 既存の `test_phase165_r52_r11_common_renderer.py` と `test_phase165_r56_common_renderer.py` は実行するが変更しない。
- `tests/test_phase162_r2_validated_proof_presentation.py` の6件は、import 変更箇所に到達する前の `tests/test_phase59_n3_ehp_chain.py:62` で `prop51_steps[0]` が `IndexError` になるため未解決。隠蔽・skip・期待値緩和をしない。
- 正規 Renderer・推論規則・Reference は変更なし。バックアップからの手動復元可能。
- 完了基準: import 対象2箇所が移行され、R5 静的監査が `STATIC_PASS_REVIEW_REQUIRED`、対象の Phase 165 テスト成功。古い Phase 162 の6件は別途解決が必要。
- 次 Phase との境界: 補助 Renderer 候補の分類は引き続き R5。Phase 165 最終全体 pytest は未実施。
