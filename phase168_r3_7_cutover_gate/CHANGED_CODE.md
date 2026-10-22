# Phase 168 R3-7 変更一覧

- 新規 `phase168_r3_7_cutover_gate.py`: ファイル先頭に import、新規 `NarrativeCutoverReport` クラスと `inspect_narrative_cutover` 関数。
- 新規 `tests/test_phase168_r3_7_cutover_gate.py`: import とテスト関数4件を全て収録。
- 新規 `probe.py`: import と `main` 関数を全て収録。
- 新規 `run.ps1`: Windows PowerShell 実行用。
- 既存の Search / Renderer / Web API は変更なし。

完了条件：限定テスト4件 PASS、4群の引用整合性レポート取得。
次工程の境界：不一致がある群について、モデルの step 対応から長文本文を生成し、従来の表示文章から文献番号を推測しない。
