# Phase 175 R4R14R1 — 限定 pytest 収集修正

## 発生した問題

R4R14 の監査本体は PASS したが、異なるディレクトリの `test_rule.py` が標準 import モードで衝突し、pytest の収集段階で停止した。数学的な証明の失敗ではない。

## 対象と変更

- 追加ファイル: `phase175_r4r14r1_pytest_collection_fix/run.ps1`
- 追加ファイル: `phase175_r4r14r1_pytest_collection_fix/README.md`
- 追加ファイル: `phase175_r4r14r1_pytest_collection_fix/AUDIT_PLAN_JA.md`
- 追加ファイル: `phase175_r4r14r1_pytest_collection_fix/CODE_FULL_JA.md`

元の R4R14 監査ファイル、本番コード、既存テストは変更しない。

## 修正方法

限定 pytest の起動時だけ `--import-mode=importlib` を明示する。対象テストは4ファイルのままで、全体 pytest は実行しない。

## 完了条件

- DryRun で Source Guard が PASS
- 本実行で Toda (5.9) の登録、添字6特殊化、EHP フロンティア監査が PASS
- 限定 pytest が収集衝突なく PASS
- `git diff --check` が PASS
- `π₁₀⁶ = 0` を未完成のまま正直に記録する

## 次の作業との境界

今回の修正は pytest の収集方法のみ。後続 R4R14R2 で既存の推論の再利用可否を確認し、必要な場合に限り数学的に一般的な推論規則を実装する。
