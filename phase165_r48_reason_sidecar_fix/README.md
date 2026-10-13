# Phase 165 R48 — 共通 ReasonSidecar の型接続

## 変更対象
- `toda_group_proof_narrative_reasons.py`: `_exactness_to_map_property_reason` の命題型の認識を新しい `MapInjective` / `MapSurjective` に拡張する。EHP の写像・群・零性の照合は変更しない。
- `toda_group_proof_generic_narrative_renderer.py`: R48 で追加され、公開経路では使用されない文章挿入処理が存在する場合のみ撤去する。
- `install.py`、`test_r48_reason_sidecar.py`、`run.ps1` は新規。

## 原因と修正
公開 Narrative は `_render_generic_narrative_proof_block()` ではなく、Argument/Contribution/ReasonSidecar を通る。旧 `ReasonSidecar` の理由分類が新しい `MapInjective` / `MapSurjective` を除外していたため、前回のテストでは「完全性より」が出なかった。既存の推論理由機構である `ReasonSidecar` の型接続だけを変更する。

## テスト
対象4件のみ。全体 pytest は行わない。Reference 一般形の復旧、Δ の零写像の理由、他の文章一致処理の完全撤去は別工程で扱う。
