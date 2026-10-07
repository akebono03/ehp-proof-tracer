# Phase 159 R1-7c R4 exact-sequence subsequence suppression repair1 fix1

## 変更対象

production code の変更はありません。

### `tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py`

import の変更はありません。

変更後のテストファイル全文は ZIP に収録しています。

## 完了条件

- 長い完全列を維持する。
- その部分列である短い完全列を bare / exact のどちらでも再表示しない。
- `H` の単射 `(1)`、全射 `(2)`、同型の流れを維持する。
- $\eta_2$ の現在の文言を変更しない。
- 既存 exactness merge regression を壊さない。
- generator canonicalization regression を壊さない。
- full pytest は実行しない。
