# Phase 165 Renderer R2 監査と境界

R1 のローカル監査では Renderer 名称ファイル 63、旧 Generic import 40、トップレベル重複定義 8 が報告された。今回の R2 では、それらをまだ削除しない。

GitHub の現行 `phase165_r52_partial_proof.py`、`phase165_r56_presentation_adapter.py`、`toda_group_proof_presentation.py`、`toda_group_result_proof_replay.py` と関連テストを確認した。ローカル環境は直前の復旧・一本化パッチが適用され GitHub 本流と異なるため、新規モジュールだけを追加する。

共通の `NarrativeProofModel` は、対象群・探索状態・証明済み `ProofStep`・未解決 Goal・参考文献・診断・結論・根 ProofStep と元データの同一性を保持する。`TodaGroupProofPresentation` は既に完成が確認された Replay から構築されるので、対応モデルは COMPLETE とする。

証明内容を推論・変更しない。Reference や論証を組み立てる Renderer ではない。現行 Renderer は新モデルをまだ消費せず、公開入口切替は R3 の範囲とする。

R2 完了条件は新モデルの追加、完成・未完成入力の保持、型不一致拒否、現行 Narrative 不変、限定 pytest 成功。全体 pytest は Phase 165 終了時のみ。
