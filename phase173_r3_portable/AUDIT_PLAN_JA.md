# Phase 173 R3 — プロファイル・コミット変動への対応

## 対象

- 新規 `phase173_r3_portable/__init__.py`
- 新規 `phase173_r3_portable/audit.py`：`git`, `verify_committed_changes`, `preflight`, `r1_baseline_status`, `inspect_roots`, `format_report`, `main` の全関数
- 新規 `phase173_r3_portable/run.ps1`
- 新規 `phase173_r3_portable/tests/test_audit.py`
- 新規 `phase173_r3_portable/README.md`, `CODE_FULL_JA.md`, この文書

既存の本番コード、既存テスト、五つの正式ドキュメントは変更しない。

## 検査方法

- `develop` かつローカル `origin/develop` と HEAD が一致し、追跡済みファイルがクリーンである。
- `11ea331f` が HEAD の祖先で、基準以後のコミット差分は `phase173_*` 内の**新規追加**だけである。既存ファイルの変更・削除は禁止する。
- 重要な六つの source blob が GitHub でレビューした SHA と一致する。
- Toda Proposition 5.6 の原文が確認できる。
- R1 レポートが現在の Windows プロファイルにない場合、`NOT_AVAILABLE_IN_THIS_PROFILE` として報告し、過去の成功結果を捏造しない。
- 公開の検索器と同一の screened context を用い、根の候補・直下 Subgoal の候補だけを調査する。型付き候補を ProofStep とみなさない。

## 完了条件

- `run.ps1 -DryRun` と限定 pytest が PASS。
- 本実行が二群の候補、既存 GIVEN、先行結果を出力。
- `%LOCALAPPDATA%/EHPProofTracerRecovery/phase173_r3_portable/audit.json` と `audit.md` を出力。
- tracked files 不変、全体 pytest 未実行。

Phase 173 R4 は本レポートの診断後に検討する。新しい数学的規則・GIVEN の追加は本パッケージで実施しない。
