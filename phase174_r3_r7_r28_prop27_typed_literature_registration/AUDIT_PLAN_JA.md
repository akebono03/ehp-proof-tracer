# Phase 174 R3-R7-R28 監査計画

## 実装前確認

- GitHub `akebono03/ehp-proof-tracer` の `develop` と R27 HEAD `7203ed2ced9a4bb05274e2a4380241b328943c33` を基準にする。
- `unified_statement_registry.py`、`phase163_r4_registry_bridge.py`、`phase165_r52_r27_r5_literature.py`、`proof.py`、R25/R26/R27 のコードと関連限定テストを確認。
- 採用原文 `sources/toda/Toda_02_2.tex` の Proposition 2.7 の内容と SHA256 を照合する。

## 変更対象（すべて新規）

- `registration.py`: `Prop27UniversalLiteratureStatement`、`verified_universal_statement`、`register_universal_prop27`、`prop27_literature_to_premise_rule`、`derive_registered_general_premise`。
- `audit.py`: `git`、`allowed_paths`、`source_guard`、`check_registration`、`main`。
- `tests/test_registration.py`: 独立登録・一般から個別への推論・誤登録拒否のテスト。
- `run.ps1`: DryRun と限定 pytest（`--import-mode=importlib`）の実行。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

## 数学的契約

一般命題のみ `ProofRule.GIVEN` として文献由来の固定定理を登録する。これは個別次元の結論を直接 GIVEN とすることではない。R25 の一般前提と n=6 の型付き関係は、引用情報を持つ INFERENCE とする。符号は `±` のまま維持する。出典 SHA が一致しなければ登録しない。

## 完了条件

Source Guard PASS、一般命題の厳密な出典照合 PASS、単一 `ProofStepLink` を持つ孤立 Registry から二段の INFERENCE 生成 PASS、限定 pytest PASS。全体 pytest は Phase 最終時まで実行しない。

## R29 との境界

公開検索への登録と root complete の確認は R28 の範囲外。R29 で公開 Provider と出典順序・資格条件を監査し、出典認証された一般命題から導出できるか確認する。
