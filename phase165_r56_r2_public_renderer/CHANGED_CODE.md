# Phase 165-R56-R2 変更内容

## 変更対象

- `phase165_r56_presentation_adapter.py`：import 全文および `render_completed_shared_narrative()` 全文を置換。クラスの変更なし。
- 新規 `test_phase165_r56_r2_public_renderer.py`：テスト関数4件と import 全文。
- 新規 `install.py`、`run.ps1`：ルート確認・バックアップ・対象テスト実行。

## 証明生成との境界

`search_shared_group_goal()`、`ProofStep`、`phase165_r52_partial_proof.py`、未完成の証明の Renderer、既存の公開 Renderer 本体は変更しない。特定群専用の文章や新しい推論規則も追加しない。

## import・関数・テスト全文

`phase165_r56_presentation_adapter.py` をそのまま全文置換する。新規ファイル `test_phase165_r56_r2_public_renderer.py` も全文を配置する。省略のない Python コードは同梱の各ファイルに記録している。

## pytest

```powershell
python -m pytest -q .\phase165_r56_r2_public_renderer\test_phase165_r56_r2_public_renderer.py .\test_phase165_r56_common_renderer.py .\test_phase165_r55_nk_only_goal.py
```

全体 pytest は Phase 終了時のみ。公開用 Renderer が新型を表示できずに例外を出した場合、代替表示に戻さず失敗を報告する。
