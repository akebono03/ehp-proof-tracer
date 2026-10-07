# Phase 159 R1-7c R4 exact-sequence suppression repair2 fix1

## 変更対象

production design の変更はありません。

### 適用スクリプト

`apply_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair2_fix1.py`

- 大きな source block の完全一致を廃止。
- public contribution renderer 内の `generic_used_step_ids = (` を anchor にする。
- その直前へ late exact-sequence suppression call を挿入。
- helper が既に存在する場合は重複追加しない。

### production code

repair2 と同じ変更だけを適用:
- `suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements()`
- public contribution renderer から上記 helper を後段で1回呼ぶ。

import 変更なし。

### テスト

- `tests/test_phase159_r1_7c_r4_exact_sequence_late_prefix_suppression_repair2.py`
- `tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py`
- `tests/test_phase157_r20_repair32_exactness_intro_anchor.py`
- `tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py`

## 完了条件

- helper contract PASS。
- $\pi_3^2$ focused regression PASS。
- $\pi_6^3$ existing exactness regression PASS。
- generator canonicalization regression PASS。
- full pytest は実行しない。
