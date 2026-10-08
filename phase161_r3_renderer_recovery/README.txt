Phase 161-R3 renderer recovery

状況
====
local renderer shape audit により、

  toda_group_proof_narrative_contribution_renderer.py
  total lines: 0

が確認された。

最初の Phase 161-R3 apply package は、
production file を書き込む直前に

  backup_before_apply/toda_group_proof_narrative_contribution_renderer.py

を作成していた。

そのため、まずこの original backup から production renderer を復旧する。

安全条件
========
復旧元として使うのは次だけ:

phase161_r3_pi4_2_restored_reference_relink/
  backup_before_apply/
    toda_group_proof_narrative_contribution_renderer.py

この backup が存在しない、空、SyntaxError、または必要 helper を欠く場合は、
production file を変更せず停止する。

復旧後確認
==========
1. py_compile
2. renderer shape audit
3. Phase 161-R1/R2 時点で PASS していた focused regression tests

変更
====
復旧対象:
- toda_group_proof_narrative_contribution_renderer.py

R3 feature repair:
- まだ適用しない

全体 pytest:
- 実行しない
