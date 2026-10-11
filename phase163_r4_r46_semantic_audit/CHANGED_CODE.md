# Phase 163 R4-R46 変更一覧

## 新規ファイル

- `phase163_r4_r46_semantic_audit/phase163_r4_r46_semantic_audit.py`：`RULES`、`compact`、`anchor_in_lines`、`audit`、`write_results`、`main` を追加。既存モジュールの変更なし。
- `phase163_r4_r46_semantic_audit/tests/test_phase163_r4_r46_semantic_audit.py`：限定テスト8件。
- `phase163_r4_r46_semantic_audit/run.ps1`：解凍後の実行用。
- `phase163_r4_r46_semantic_audit/README.md`：英語の説明書。
- 本ファイル：日本語の変更一覧。

## 完了条件

- R4-R45 の優先23 Assertion を全件分類する。
- 参照環境の直接記載・一般式の特殊化・周辺記述・参照内未確認を混同しない。
- TeX 原稿の SHA-256 を検証する。
- Statement ID、Registry、TeX の書き込みを行わない。
- 全体 pytest を実行しない。

## 次工程との境界

R4-R47 以降で、未確認の帰属の解消、証拠の人手監査、正式な順序・登録処理を別に扱う。本 Phase の監査は数学的構造化・証明探索接続をしない。
