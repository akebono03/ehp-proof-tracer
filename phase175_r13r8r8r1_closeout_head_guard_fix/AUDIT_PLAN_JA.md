# Phase 175 R13R8R8R1 — 終了前監査修正

## 原因

R13R8R8 は Git HEAD を固定値に限定しており、監査用コミットの追加だけでも停止した。GitHub develop の現行 HEAD `acd51e9d94f8e67717dbc62b39862d3a6bb8c22b` は基準 HEAD `b5a0b13884f6f0af527034d8c8bcd47b90c7cc97` の直接の子孫であり、本番の監査対象2ファイルは変更されていない。

## 変更対象

- `phase175_r13r8r8r1_closeout_head_guard_fix/audit.py` の `source_guard()` と監査名・報告名
- `phase175_r13r8r8r1_closeout_head_guard_fix/run.ps1` の呼び出し対象・表示名
- 同ディレクトリの `README.md`（英語）、`AUDIT_PLAN_JA.md`（日本語）、`CODE_FULL_JA.py`（完全な監査コード）

本番ファイル、数学規則、GIVEN、ProofStep、Renderer は変更しない。

## 限定監査と完了条件

1. `develop` ブランチであること。
2. 基準 HEAD が現在の HEAD の祖先であること。
3. Reference Projection と Renderer の本番2ファイルが、HEAD / Index / Working Tree の全てで検証済み blob と一致すること。
4. 改行コード LF、`git diff --check` を確認すること。
5. 完成済み3群の公開表示・出典対応監査、および既存の限定 pytest 13件を通すこと。

全体 pytest は Phase 175 の最後にのみ実施する。将来の命題型への一般保証は対象外。
