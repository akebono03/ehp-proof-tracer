# Phase 165 R57-R3 旧 Renderer の段階的廃止

## 変更対象

- `toda_group_proof_generic_narrative_renderer.py`: 未使用の `render_toda_group_proof_generic_proof_markdown()` 関数を全文削除。数式・文章化の共通ヘルパーは維持する。
- `phase165_r14_r39_web_connection.py`: モジュール全文を互換ラッパーに置換。既存関数名 `build_phase165_pi32_web_view()` を維持し、固定 Narrative の文字列を撤去する。変更後の import は `from web_group_proof import build_standard_web_group_proof_view` のみ。
- 新規テスト `test_phase165_r57_r3_legacy_renderer_retirement.py`: 4件。既存 R57-R2 / R56-R2 / R57-R1 / R55 を対象テストに含める。

## 監査範囲

GitHub 現行ブランチの該当ソースと関連テストを確認済み。R57-R1 の AST 監査では旧 generic proof 関数の本番直下呼び出し 0、R39 関数の本番直下呼び出し 0。R39 関数は以前の歴史的テストで import されるため、直接削除せず互換ラッパーとした。インストーラーが導入先の直下 Python を再スキャンし、旧 generic 関数への直接参照を見つけた場合は変更を中止する。

## 完了条件

公開 Renderer、完成・部分証明、現行 Web 経路の対象テストが成功すること。群固有の R39 固定文章はなくなること。既存の共通数学ヘルパーは残ること。

## 次段階との境界

既存の旧部分証明 API `render_toda_partial_proof_narrative_markdown()` は歴史的テストから直接呼ばれているため、この Phase では削除しない。公開 Renderer 内の群別特例は今回変更しない。全方式の廃止完了とは扱わない。全体 pytest は Phase 終了時のみ。
