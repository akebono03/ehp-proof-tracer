# Phase 176 R3R27R1R1 修正仕様

## 障害

`find_inference_matches_for_rule` は入力の `ProofStep` を `PremisePattern` に従い照合する。R3R27R1 のテストは、入力順の交換を不正としていたため失敗した。

## 変更対象

- 変更：`phase176_r3r27r1_toda55_quadruple_isolated/tests/test_source.py` の `test_only_independently_inferred_family_member_can_close` 全体。
- 新規：`phase176_r3r27r1r1_premise_order_test_fix/` の `install.py`、`run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`test_source_FULL.py`。
- 既存 `source.py` や数学規則、Source-first、公開 Provider は変更しない。

## 修正内容

入力順序を変えても正しい前提が3つ存在する場合、照合は1件成功することを検査する。さらに `InferenceMatch.premises` が規則で指定した順序に正規化されることを検査する。

## 完了条件

DryRun と本実行後の限定 pytest が PASS。全体 pytest は Phase 末尾まで未実施とする。

## 次 Phase の境界

本修正はテスト期待値のみであり、(5.5) 第2関係の共有探索接続や実際の群構造の証明は次 Phase に留保する。
