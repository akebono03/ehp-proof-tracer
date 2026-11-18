# Phase 175 R4R12R10R1R3 — 型の不一致診断

## 背景

R10R1R2 の限定 pytest 9件は PASS。一方、DryRun は `R10R1_ORIENTATION1_TYPED_MISMATCH` で停止した。

Toda (5.11) の等式は採用された TeX の出典事実として扱い、再証明しない。R9 の一般変換で生成元像に渡す前に、商群候補の内部表現と文献事実の内部表現が厳密に一致するか検査する。

## 変更対象

既存ファイル、既存クラス、既存関数、数学規則、文献 Given、README.md など既存の5文書への変更はない。

新規 `phase175_r4r12r10r1r3_orientation_type_diagnostic/audit.py`:

- `git()`、`describe_tree()`、`differences()`、`inspect()`、`main()` を追加する。
- 商群規則の両 Orientation から、`GeneratorImage` の始域と終域、生成元像から作った等式を取得する。
- `canonical_511()` と実際の等式を比較し、左辺と右辺を分離した違いを報告する。
- 構造化表現（`Suspension`、`IteratedSuspension`、`GeneratorSymbol` など）の異同を報告するが、解消処理・無条件の同一視は行わない。

新規 `tests/test_audit.py`:

- `test_equal_objects_have_no_differences()`
- `test_different_class_preserved_as_mismatch()`
- `test_nested_difference_reports_exact_field_path()`
- `test_description_preserves_nested_types_and_values()`

新規 `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`__init__.py`。

## 実行と完了条件

- DryRun と本実行の両方で限定 pytest 4件を実施。
- 現在の Git 履歴を記録し、R9 コミットが祖先であることを確認。
- Toda (5.11) の採用 TeX と文献目録を既存検証関数で確認。
- 二つの Orientation の対応関係を `output` に記録。
- `PASS_R4R12R10R1R3_TYPED_MISMATCH_DIAGNOSED_NOT_COMPLETE` を期待。
- 全体 pytest は実施しない。

## 次 Phase との境界

差分を実行結果で確認してから、既存の証明可能な一般的正規化・定義変換の再利用が可能か検討する。単に見た目が同じであることを理由に構造を上書きしない。対象群の結論を文献 Given として追加しない。
