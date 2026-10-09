# Phase 163 R1B 登録候補の分類

本報告は静的解析結果であり、実在する文献命題の確定件数ではありません。

## 件数

- 本体候補: 1034
- テスト候補: 2520
- 登録・出典関連の優先候補: 115
- 構文解析エラー: 0

## 本体分類（各候補は重複する命題を含み得る）

- api_or_container_definition: 156
- explicit_entry_constructor: 21
- literature_reference_candidate: 50
- named_container_assignment: 106
- registration_call_candidate: 39
- repository_constructor: 5
- rule_function_candidate: 495
- statement_class_candidate: 162

## R1 完了前に必要な確認

- 登録先ごとに実行時の登録件数を確認する
- Statement 型と固定された文献主張を分ける
- 文献位置が不明なら未確認と記録する
- ProofStep と固定文献主張の重複を照合する
- R2 のデータ構造はここでは追加しない
