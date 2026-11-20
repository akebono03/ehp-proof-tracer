# Phase 176 R3R15R1 監査計画

## 目的
R3R15 実行時に pytest が同名の `test_provider.py` を同一プロセスで収集して発生した import file mismatch を解消する。

## 対象
- 変更ファイル: `phase176_r3r15_shared_extra_provider_probe/run.ps1`
- 変更部分: pytest の呼出しを4つの独立した呼出しに分ける。
- 変更しないもの: `audit.py`、`provider.py`、`tests/`、共有 Proof Search、GIVEN、数学規則。

## テスト
DryRun と監査本体を再実行後、4つの限定テストファイルをそれぞれ独立した pytest プロセスで実行する。いずれかが失敗したらエラーコードで終了。pytest cacheprovider は使用しない。全体 pytest は Phase 終了まで行わない。

## 完了条件
DryRun、本実行、すべての限定 pytest が正常終了すること。`git diff --check` を実施し、既存の証明探索の実装に変更がないことを確認する。

## 次 Phase との境界
R3R15R1 はテスト実行方法だけを修正する。共有 Provider の恒久登録、公開証明の完成判定は行わない。
