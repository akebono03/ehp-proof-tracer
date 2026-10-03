Phase 156-R5 repair13 — root Reference frontier

診断結果
========
Proposition 5.1 と Toda (5.2) の違い:

Proposition 5.1:
- Proposition 5.1 -> (5.3) -> root
- Proposition 5.1 -> Proposition 5.3 -> root
- Proposition 5.1 -> Lemma 5.4 -> root

Toda (5.2):
- (5.2) -> Proposition 5.6 -> ... -> root

Proposition 5.6 は今回の root proof 自身の LiteratureReference である。

一般規則
========
Reference frontier の探索中:

- same Reference への遷移: 許可
- unreferenced step への遷移: 許可
- root Reference への遷移: 許可
- それ以外の別 Reference への遷移: 打ち切り

これにより:
- Proposition 5.1 は parent-level Reference から除外
- Toda (5.2) は parent proof が直接利用する Reference として保持

Production changes
==================
toda_group_proof_narrative_contribution_renderer.py

変更関数:
- _toda_group_proof_narrative_reference_frontier_step_ids()

Import changes
==============
None.

Test changes
============
tests/test_phase156_r5_repair3_eta3_zero_attribution.py

変更:
- test_phase156_r5_repair3_two_eta3_zero_is_not_under_53_header()

新規:
- tests/test_phase156_r5_repair13_root_reference_frontier.py

Expected pi_6^3 public References
=================================
- (5.3)
- Proposition 5.3
- Lemma 5.4
- (5.2)

Proposition 5.1 remains in the raw proof graph but is not shown as a
parent-level sibling Reference.

Repository-wide pytest is reserved for Phase 156 closure.
