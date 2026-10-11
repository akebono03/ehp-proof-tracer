# Phase 163 R4-R44 変更対象

既存実装・既存テストは変更しない。

- 新規 `phase163_r4_r44_assertion_audit/phase163_r4_r44_assertion_audit.py`
  - `audit`：既存 Reference / Assertion と TeX 全文との読み取り専用照合表を構築。
  - `validate_tex_sources`：5原稿の SHA-256 を照合。
  - `write_report`：JSON、CSV、報告書を出力。
  - `main`：限定実行のエントリポイント。
  - `_require`：不整合時に実行を停止。
- 新規 `phase163_r4_r44_assertion_audit/tests/test_phase163_r4_r44_assertion_audit.py`：限定9テスト。
- 新規 `phase163_r4_r44_assertion_audit/run.ps1`：解凍後実行用。
- 新規 `phase163_r4_r44_assertion_audit/README.md`（英語）、`CHANGED_CODE.md`（日本語）。

新設コードは import と関数全体をファイルに完全収録し、省略なし。

完了条件：限定9テストの成功、現行23 Reference と67 Assertion の欠落なし、108 TeX環境の保持、既存ID不変、事前ステータス維持、原本不変。

次工程との境界：命題内部分領域との数学的照合、記号ラベルの識別子確定、Definitionの環境外抽出、永続的登録・ID発行、証明探索接続は実施しない。
