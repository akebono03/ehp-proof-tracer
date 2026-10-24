# Phase 168 R3-41D — 実探索の Reference・Narrative 監査

読み取り専用。使用された ProofStep と screened bridge、Model、Web 表示を同時に確認する。

| 対象 | 状態 | 証明 Step | Reference | 本文あり | Goal | 表示・引用の問題 |
|---|---|---:|---:|---:|---:|---|
| pi6_4 | 実行エラー | - | - | - | - | ValueError: common Narrative lacks the proof boundary |
| pi6_3 | 実行エラー | - | - | - | - | ValueError: common Narrative lacks the proof boundary |
| pi7_5 | 実行エラー | - | - | - | - | ValueError: common Narrative lacks the proof boundary |
| pi7_4 | 実行エラー | - | - | - | - | ValueError: common Narrative lacks the proof boundary |
| pi8_5 | 実行エラー | - | - | - | - | ValueError: common Narrative lacks the proof boundary |
| pi4_3_control | complete | 25 | 4 | 4 | 0 | 0件 |

## 実探索の観測範囲

- 未完成の検索結果: 0件
- うち ProofStep あり: 0件
- うち Reference あり: 0件
- うち登録出典あり: 0件
- うち Reference 本文あり: 0件

## 判定上の注意

- Reference 番号や見出しがあっても、本文がなければ本文完成とは判定しない。
- 非完成の探索結果に引用が存在しなければ、実際の部分証明の引用表示は未検証と記録する。
- GIVEN で出典がない場合は未接続として報告し、引用は補わない。
- 各群の `*_reference.md` と `*_narrative.md` に実表示の内容を保存する。
- 実行エラーや表示不足があっても調査結果として報告し、実装ファイルは変更しない。
- 全体 pytest は実行しない。

## 見つかった問題

- 観測できた範囲では整合性違反なし（未観測範囲は未検証）。
