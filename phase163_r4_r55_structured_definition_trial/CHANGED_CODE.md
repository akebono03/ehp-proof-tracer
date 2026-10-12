# Phase 163 R4-R55 変更内容

## 変更対象

既存のファイル・クラス・関数・import は変更しない。

追加ファイル（新規であるため全文を ZIP に収録）:

1. `phase163_r4_r55_structured_definition_trial.py`：新規クラス `SourceGroundedDefinition`、新規関数 `sha256`, `build_trial`, `write_report`, `main`。すべて新規モジュール内に追加する。
2. `tests/test_phase163_r4_r55_structured_definition_trial.py`：新規テスト関数9件と必要な import。
3. `run.ps1`：入力・限定テスト・監査レポート出力。
4. `README.md`：英語の操作説明。
5. `CHANGED_CODE.md`：日本語の変更記録。

## 完了条件

- (2.9)、(2.10)、(4.3) の TeX 本文と SHA-256 を検証し、仮 Registry に3つの `AssertionKind.DEFINITION` を生成する。
- `ReferenceKind.EQUATION` と `AssertionKind.DEFINITION` を分離する。
- 原文 TeX・前後文脈・出典・掲載順を保持する。
- 形式的数学 AST・原本照合・既存主張との同値性を「未検証」と明記する。
- 既存 ID・本番 Registry・証明探索を変更しない。
- 限定 pytest 9 件を実行する。全体 pytest は Phase 163 終了時のみ。

## 次の R4-R56 との境界

意味的な範囲条件の型付け、正式 ID 発行、残り16定義候補と237未判定候補への拡張は行わない。
