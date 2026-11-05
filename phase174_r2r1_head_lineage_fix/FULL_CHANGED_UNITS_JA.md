# Phase 174 R2R1 — HEAD 履歴の整合性修正

## 変更対象（先に確定）

1. `phase174_r2_source_math_audit/audit.py`（全文置き換え）
   - 定数 `REVIEWED_HEAD` を GitHub `develop` の新 HEAD に更新。
   - 定数 `R1_BASELINE_HEAD` を新規追加（旧 HEAD を保持）。
   - 関数 `audit_prior_record()` は全文のまま R1 JSON の照合先を `R1_BASELINE_HEAD` に変更。
   - `make_report()` など他の既存関数は変更しない。
   - import の変更なし。
2. `phase174_r2_source_math_audit/run.ps1`（全文置き換え）
   - HEAD 更新、旧 HEAD が祖先にあること、確定済み R1 audit.py の SHA を追加検査。
   - 既存 Source Guard、DryRun、本実行、限定 pytest は維持。
3. 新規 `phase174_r2r1_head_lineage_fix/tests/test_head_lineage.py`
   - 新しいテスト3件を追加。
4. 新規 `phase174_r2r1_head_lineage_fix/run.ps1`, `README.md`, `FULL_CHANGED_UNITS_JA.md`
   - 既存の R2 ファイルが前回の既知 SHA と一致する場合のみ置換。

## GitHub 監査

- 旧 HEAD: `cb85913905b2f7452bda2a2c4428e6fe5a3a793a`
- 新 HEAD: `3558d713fd7939ded656f2458aacc62d71c7e0b3`
- 比較: ahead 1、behind 0、merge base は旧 HEAD。
- 変更12パス: R1 audit パッケージ、R1R1 test correction パッケージ、
  `test_phase165_r55_nk_only_goal.py` の修正だけ。
- Toda 原文と Proof Search 本番ファイルの SHA は不変。

## 証明書と監査上の注意

R1 の `audit.json` は旧 HEAD で生成した正規の記録なので、新 HEAD を偽装しない。
R2 の監査結果における `head` は新 HEAD とする一方、`r1_baseline.verified_head`
は旧 HEAD のまま保持する。新しい `GIVEN`、Inference Rule、ProofStep は生成しない。

## 完了条件

- R2R1 DryRun PASS。
- HEAD Lineage/Source Guard PASS。
- 新規テスト3件 PASS。
- R2 の元の読み取り専用監査 PASS。
- R2 限定 pytest PASS。
- Git index 保持 PASS。

## 次の Phase との境界

R2 の結果が揃うまで R3 の実装に入らない。
全体 pytest は Phase 174 の最後のみ実施する。
