# Phase 176 R3R28R1 修正仕様

## 原因

π₈³ の登録済み DB Goal には引用可能な assertion ID がなく、`resolve_specialized_goal_citing_id()` が `None` を返す。これは既存仕様の想定内である。元のテストが `assert citing is not None` と誤って仮定した。

## 変更箇所

- `phase176_r3r28_toda55_quadruple_public/tests/test_public.py`
- `test_shared_provider_proposes_and_proves_nu5_quadruple()` 全体
- import 節の変更なし
- 新規 `phase176_r3r28r1_uncited_root_test_fix/` にインストーラ、テスト関数全文、既存テストファイル全文、実行スクリプトを追加

## 修正方針

群の根 Goal に引用 ID を捏造しない。`screen_independent_sources_for_derived_goal()` によって選択済みの Toda (5.5) 第2関係の GIVEN `ProofStep` が一意であることを確かめ、その `assertion_id` を再構成 API のコンテキストとして渡す。`typed_reference` では出典の候補は既存の審査済み bridge に限定する。

## テスト

R3R28 5件、R3R27R1 6件、Phase174 R3-R6 6件の限定テスト。**全体 pytest は実行しない。**

## 完了条件

DryRun、本実行、限定 pytest が PASS。Toda (5.5) の第2関係は `ProofRule.INFERENCE` で証明され、対象群の直接 GIVEN を追加しない。

## 次の Phase

R3R29 は Hopf 像の型付き代入の経路を検証する。R3R28R1 はテスト修正のみ。
