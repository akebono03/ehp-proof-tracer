Phase 161-R3
pi_4^2 restored Reference relink

R2 diagnosis
============
Reference pipeline:

build entries
  -> (5.2), (5.2), Proposition 4.4

fixed-statement filter
  -> (5.2), Proposition 4.4

root-reference exclusion
  -> Proposition 4.4

body-usage filter
  -> Proposition 4.4

fixed-reference restore
  -> (5.2), Proposition 4.4

final body-usage filter
  -> Proposition 4.4

Repair
======
既存の general helper

link_toda_group_proof_narrative_unmarked_reference_consumers()

を restore 直後に再適用する。

final body-usage filter は削除しない。
したがって ancestry-only orphan Reference を無条件に復活させる変更ではない。

Production変更
==============
toda_group_proof_narrative_contribution_renderer.py
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Test追加
========
tests/test_phase161_pi4_2_restored_reference_relink.py

全体テスト
==========
実行しない。
Phase 161 最後にのみ実行する。
