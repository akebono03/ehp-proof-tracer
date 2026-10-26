# Phase 169 R3N 実装内容

## 変更対象の一覧

1. `phase165_r3_recursive_search.py` — `reconstruct_registered_goal` 全体（既存の直接固定文献葉で照合できなかった場合に限る補助分岐を追加、関数全文をインストール時出力）。import 節は変更しない。
2. 新規 `phase169_r3n_prior_result_alias.py` — `prior_result_presentation_rule`、`resolve_prior_result_alias_step` をファイル先頭に追加（全文同梱）。
3. 新規 `phase169_r3n_prior_result_search/tests/test_r3n_prior_result_alias.py` — テスト関数を7件追加（全文同梱）。

## 不変条件

- DB の行自体を文献 `GIVEN` として追加しない。
- 出典の `FIXED_STATEMENT` が先行していることを R3M が検証し、さらに実際の検索で citation-screened された唯一の `ProofStepLink` が存在することを要求する。
- 生成元表記の同一性は `same_registered_group_presentation`（HyoujiGen ID）で厳密に照合する。
- 既存の直接 `GIVEN` で解ける場合は新しい推論を適用しない。
- `CompletedInternalProof` および以前の証明・完了状態を参照しない。

## 実行する限定 pytest

`python -B -m pytest -q phase169_r3n_prior_result_search/tests/test_r3n_prior_result_alias.py phase169_r3m_prior_result_catalog/tests/test_prior_results.py`

`python -B -m pytest -q phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py`

## 完了条件・次工程

限定テスト成功、実際の Web 検索で既存完成群を維持、全ての新規推論が元の固定文献葉を前提とすることを確認。$π_8^6$ の安定輸送に必要な `Toda (4.5)` と合成生成元の一致の証明は次工程とし、この Phase で完了と偽らない。全体 pytest は Phase 末のみ。
