# Phase 165 R6-1 基礎命題の添字修正

変更するのは `phase165_r14_r36_adopted_backward.py` 内の `adopted_leaf_steps()` の基礎命題選択1か所のみです。旧探索が必要とする命題は $E(\\iota_1)=\\iota_2$ であり、前回誤って導入した $E(\\iota_2)=\\iota_3$ を訂正します。

`run.ps1` は対象テストと前回の限定テストを実行します。全体 pytest は実施しません。R6-2 の探索一般化は含みません。
