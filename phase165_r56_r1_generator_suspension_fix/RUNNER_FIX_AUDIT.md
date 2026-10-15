# R56-R1 実行スクリプト修正

## 原因
旧 `run.ps1` は `test_phase165_r56_r1_generator_suspension_fix.py` をプロジェクト直下から相対参照していました。一方、テストファイルはパッケージのサブディレクトリに同梱されています。

## 変更対象
- `phase165_r56_r1_generator_suspension_fix/run.ps1`：スクリプト全文置換。
- 既存クラス・関数・import・証明規則・Renderer は変更なし。
- テストファイルそのものも変更なし。

## 実行対象
- `phase165_r56_r1_generator_suspension_fix/test_phase165_r56_r1_generator_suspension_fix.py`
- `test_phase165_r56_common_renderer.py`
- `test_phase165_r55_nk_only_goal.py`

## 完了条件
対象テストが収集・実行され、全件成功すること。失敗時は失敗をそのまま報告すること。

## 次の作業との境界
この修正では Narrative の表示契約や出典監査を変更しない。全体 pytest は Phase 165 の終わりに実施する。
