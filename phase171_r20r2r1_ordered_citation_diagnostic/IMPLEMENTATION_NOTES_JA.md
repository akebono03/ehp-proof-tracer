# Phase 171 R20R2R1：文献順序付き引用の失敗診断

## 確認できた事実

- R20R2 のパッチ適用は `PATCHED`、その後の限定 pytest は24件成功・2件失敗。
- 失敗1は `ordered_typed_reference_steps()` の直接呼び出しで、`reconstruct_registered_goal()` を通らない。
- 失敗2は同じ引用取得が空になることに起因するため、最初の失敗だけでは共通探索器の回帰とは断定できない。
- GitHub `develop` にある引用取得関数・引用判定関数・該当テストの内容を確認した。現行コード上では、fixture のソースID一致・使用可能位置・文献位置・固定主張・リンク付き GIVEN は引用許可の条件を満たすはずである。
- したがって直接引用の資格検査を書き換えず、実際の `CitationAssessment` とロードされたモジュールの所在を出力して原因を確定する。

## 変更対象

既存のファイル・クラス・関数は**変更しない**。

新規ファイルのみ：

- `phase171_r20r2r1_ordered_citation_diagnostic/audit.py`：`git`、`load_existing_fixture`、`blob_comparison`、`describe_fixture`、`run`、`main` を新設。
- `phase171_r20r2r1_ordered_citation_diagnostic/run.ps1`：診断と対象2件だけの pytest 実行。
- 本書、`README.md`、`CHANGED_CODE.md`、ZIP。

新規関数はすべて `audit.py` にのみ追加し、既存製品の import、クラス、関数、API は変更しない。関数全文および import 全文は `CHANGED_CODE.md` に記載する。

## 観測する条件

1. テスト fixture が生成した引用元・引用先の識別子と掲載位置。
2. `AssertionOrigin.FIXED_STATEMENT` の同一性。
3. `assess_citation()` の `decision` と `reason`。
4. `CitationDecision.ALLOWED` との同一性。
5. `ProofStepLink` の個数、`ProofRule.GIVEN`、結論の型と値。
6. `ordered_typed_reference_steps()` の実際の返り値。
7. `reconstruct_registered_goal()` の返り値と例外。
8. 読み込まれたモジュールの実パスと関連ファイルの Git blob 不一致。

## テスト

`python -m pytest -p no:cacheprovider -q phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py::test_ordered_reference_requires_only_prior_order phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py::test_ordered_reference_integrates_with_backward_search`

診断のみのため、全体 pytest は実施しない。既存 pytest の成功を仮定しない。

## 完了条件と次工程の境界

本工程は診断 JSON に引用拒否の理由を明示できれば完了。必要な製品コード修正の判断は診断結果を見て行う。R20R2 の `First Successful Proof Search` による数学的な証明完成を宣言しない。次工程では、引用取得の回帰/環境差異を確定した後、既存仕様を壊さない最小修正を行う。
