# Phase 165 R42 共通 Narrative の型付き命題・文献参照対応

## 変更対象
- `phase165_r14_r38_direct_registry.py`：`build_adopted_typed_reference_registry` 内の `ProofStepLink` 作成で、採用 TeX の文献 locator を元の GIVEN ProofStep に添付する。基本事実の出典は変更しない。
- `toda_group_proof_generic_narrative_renderer.py`：`_render_generic_narrative_statement_prose` に `GeneratorImage` と汎用 `MapInjective` / `MapSurjective` / `MapIsomorphism` の共通文章化を追加する。
- `test_phase165_r14_r42_common_narrative.py`：新規5件の対象テスト（import を含む全文）。
- `install.py`、`run.ps1`：現在のファイルの対象箇所のみ修正しバックアップを残す。

## 適用条件と方針
現行の Phase165 R38・R41 が適用済みであること。出典が独立原本で照合されたとの主張はしない。既存の共通 Presentation、Narrative Renderer、Web 経路をそのまま利用し、専用証明文章を追加しない。Renderer の後処理が参照をさらに除外する可能性は残るため、文献欄については Web 実画面で確認する。

## 完了条件と次工程の境界
対象5テストの成功、文献参照の ProofStep への伝搬、`GeneratorImage` と `MapIsomorphism` の一般文章化、共通 Narrative の実行。全体 pytest は実行しない。文献欄が依然空なら、Reference の body-usage filter を別途調べる。
