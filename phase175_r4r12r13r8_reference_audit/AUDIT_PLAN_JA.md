# Phase 175 R13R8 監査計画

## 対象

1. `phase168_r3_3_proof_narrative_model.py` の `build_proof_narrative_model`
2. `phase168_r3_37c_reference_projection.py` の `project_reference_bodies` および `project_cited_proof_step_reference_bodies`
3. `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown`
4. 共通 Reference Renderer と関連実行ログ

## 現状

GitHub の `develop` で、`NarrativeCitation.statement_bodies` が assertion-ID の登録内容を優先し、補助的に引用済み GIVEN から取得することを確認した。一部の参照では番号があっても本体が空になる可能性があり、R3/R7 の実際の ProofStep と照合する必要がある。

## 今回の成果物の境界

この ZIP は診断専用。既存の本番コードや数学規則を変更せず、R13R8 完了を宣言しない。ローカル `develop` の実データを監査し、後続の最小修正のための証拠を保存する。

## 完了条件（未達）

- [ ] (5.11) の式が R3 Reference に表示される
- [ ] (5.8) の式が R7 Reference に表示される
- [ ] 本文がそれぞれの出典番号を明示する
- [ ] 符号・生成元・次数を保持する
- [ ] Web の generic-complete-proof を維持する
- [ ] 関連する限定 pytest が PASS

Phase 全体の pytest は Phase 175 終了まで実施しない。

## R13R8R1 実行修正

変更対象は `run.ps1` の本実行限定 pytest 呼び出しのみ。Windows PowerShell 5.1 で `Join-Path` を2引数ずつネストする。`audit.py`、既存テスト、数学的証明や Web 表示は無変更。DryRun は旧版で PASS、本実行は旧版で pytest 起動前に停止したため、修正版のユーザー環境での確認が必要。
