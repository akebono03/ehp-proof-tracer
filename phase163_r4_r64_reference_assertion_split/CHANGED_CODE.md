# Phase 163 R4-R64 変更一覧

既存ファイルは変更しない。新規ファイルを次の位置へ追加する。

- `phase163_r4_r64_reference_assertion_split/phase163_r4_r64_reference_assertion_split.py`：`SUBJECTS`、`MARKERS`、`load_source()`、`make_proposals()`、`write_reports()`、`main()`。import・関数全文は同ファイルに収録。
- `phase163_r4_r64_reference_assertion_split/tests/test_phase163_r4_r64_reference_assertion_split.py`：限定テスト10件。import とテスト関数全文は同ファイルに収録。
- `phase163_r4_r64_reference_assertion_split/run.ps1`：既存 R4-R63 出力を指定して pytest と監査を実行。
- `phase163_r4_r64_reference_assertion_split/README.md`：英語の実行説明。
- 本ファイル：日本語の変更記録。

既存 Registry API やテストの改修、数学的意味の確定、掲載順確定、正式 Statement ID の発行、証明探索の接続は行わない。次の Phase では各提案の文献構造と数学的意味を人手・出典根拠で再確認する。
