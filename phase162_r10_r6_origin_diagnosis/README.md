# Phase 162 R10-R6 — 個別行の由来と経路の監査

この ZIP は既存コードを変更しない。`phase162_r10_r5_prose_origin.json` を入力に用い、Web の各表示行と ProofStep の候補、重複行、同じ数式の別ノード、最終結論への経路を読み取り専用で出力する。

## 変更対象

- 新規 `phase162_r10_r6_origin_diagnosis/audit.py`: `normalize`, `risk_tags`, `find_roots`, `parent_path`, `structural_candidate_ids`, `analyze`, `write_reports`, `main`
- 新規 `phase162_r10_r6_origin_diagnosis/test_r10_r6.py`: 独立限定テスト4件
- 新規 `phase162_r10_r6_origin_diagnosis/run.ps1`: テストと監査を実行する
- **変更する既存クラス・関数・import: なし**

## 実行

プロジェクト直下で ZIP を展開し、PowerShell から `powershell -ExecutionPolicy Bypass -File .\phase162_r10_r6_origin_diagnosis\run.ps1` を実行する。既存 R10-R5 JSON がない場合は先に R10-R5 を実行する。

## 出力

- `phase162_r10_r6_origin_diagnosis.md`: 重点対象・完全一致しない項目・全行の照合結果
- `phase162_r10_r6_origin_diagnosis.json`: 行別の候補と依存経路

## 完了条件

重点4項目の表示行と候補ノード・依存経路が列挙され、同じ表示行と同一数式ノードの重複が別々に示される。完全一致しない16項目には「未判定」を残し、捏造した出典を割り当てない。

## 次 Phase との境界

本文行の数学的な必要性判定、証明木・共通 Renderer の修正、全体 pytest は実施しない。実行後の監査結果に基づき、変更対象のルールを決定する。
