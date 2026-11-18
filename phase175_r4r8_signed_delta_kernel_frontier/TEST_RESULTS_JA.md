# Phase 175 R4R8 — テスト記録

## 作成側で実施する限定試験

`python -B -m pytest -q -p no:cacheprovider --import-mode=importlib phase175_r4r8_signed_delta_kernel_frontier/tests/test_audit.py`

検査内容：成功レポート検証、改ざん拒否、出典文字列と符号、一般的な巡回核の整数計算、未解決 Goal の保存、Git 祖先関係・変更パスの正常系と異常系。

作成環境の限定実行（2026-11-17）：**42 passed**。ただし実リポジトリでの統合試験結果ではありません。

## ユーザー実環境で実施する限定試験

`run.ps1` が R4R8/R4R7/R4R6 の限定 pytest のみ実施する。全体 pytest は実施しない。

## 判定境界

R4R8 の作成・限定試験とユーザー環境の DryRun/本実行は別物として扱う。ユーザー環境の PASS 前に完了を宣言しない。出典に掲載された等式は検証済み ProofStep ではない。
