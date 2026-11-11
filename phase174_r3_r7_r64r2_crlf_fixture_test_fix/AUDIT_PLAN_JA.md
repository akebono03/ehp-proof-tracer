# Phase 174 R64R2 — CRLF テスト修正

## 実装前の確認

- GitHub `akebono03/ehp-proof-tracer` の `develop` と `e5e392ddd2177fc4db70da48b1c1e6418b33c519` の一致を比較機能で確認。
- 関連テスト `phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py` と既存共通 Renderer を GitHub から確認。
- R64R1 未追跡の既存コードと関連テストは、提供済み R64R1.zip を展開して全文確認。ユーザーの失敗ログと一致。
- 根本原因：`Path.write_text()` の Windows 改行変換後に `replace(b"\n", b"\r\n")` を行い `\r\r\n` を生成。

## 変更ファイル・関数

- **既存** `phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py`: `test_review_accepts_crlf_line_endings()` のみ全文置換（関数内で LF に正規化してから CRLF にする）。import は変更なし。
- **新規** `phase174_r3_r7_r64r2_crlf_fixture_test_fix/install.py`: `git_blob_sha()`, `normalized_contents()`, `patch_test()`, `review()`, `local_git_head()`, `main()`。
- **新規** `phase174_r3_r7_r64r2_crlf_fixture_test_fix/tests/test_install.py`: `fixture_root()` と9テスト（パラメータ化を含む）。
- **新規** `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`、`__init__.py`。
- 5主要文書と既存の本体コード・証明関連ファイルに変更なし。

## 完了条件

1. Git Blob による厳密な Source Guard を通過（監査の本体・R64R1 Installer・既存修正後の R64 テスト）。
2. DryRun では変更なし。本実行で対象テスト関数のみ更新し、再実行しても変更なし。
3. LF / CRLF の両方でテスト fixture を生成し、`\r\r\n` の混入を禁止。
4. R64 監査結果（14段落中3、6段落中2を監査済み）を維持。
5. R64R2・R64R1・R64・R63 の限定 pytest を実行。全体 pytest は行わない。

## 次 Phase との境界

R65 の未監査15段落の数学的・出典的な監査には着手しない。新しい GIVEN、数学規則、既存 API の変更を含まない。
