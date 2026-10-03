Phase 156-R5 repair7 — Reference boundary filter order

原因
====
repair6 では Reference boundary を、
generic_used_step_ids で早期に絞った boundary_reference_entries から作っていた。

そのため (5.3) が最終 Reference には表示される一方で、
boundary suppression の時点では候補から外れ、
内部 proof:
- nu' bracket membership
- Lemma 5.2 application
- nu' definition purpose
が本文に残った。

修正
====
Reference boundary suppression では root を除外した全 Reference entry を使う。

最終的にどの Reference を表示するかは、
従来どおり body usage / step usage filter に後段で決定させる。

これにより:
- suppression 判定は十分広く行う
- Reference 表示数を不必要に増やさない
- proof graph / semantic sidecar は変更しない

Production change
=================
toda_group_proof_narrative_contribution_renderer.py
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Import changes
==============
None.

Tests
=====
- repair2 の残存旧 header expectation を修正
- repair7 focused test を追加
- repair6 + related regression を再実行

Repository-wide pytest is reserved for Phase 156 closure.
