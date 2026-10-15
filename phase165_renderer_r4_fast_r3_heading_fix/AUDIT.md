# R4-R3 監査・修正

- 前回: 17限定テストのうち16件成功、1件失敗。R3 への自動復元が実行された。
- 失敗: `test_r11_partial_and_compatibility_are_one_renderer()` が旧見出し `証明（Proof` を期待したが、R3 公開表示の実際は `## 証明`。
- 修正: R4 の変換処理内で、このテストの見出し1箇所を厳密な事前照合付きで `## 証明` に置換。
- 既に更新した Reference 検証、GIVEN を証明として認めない検証は維持。
- R4-R2 の import 変換40対象、数学的推論、Renderer 文章は変更しない。
- バックアップ名を `.phase165_renderer_r4_fast_r3_backup` に変更。
- 限定 pytest と実際の完成・未完成 Narrative のバイト単位一致が完了条件。
- 全体 pytest は Phase 165 完了時のみ。
