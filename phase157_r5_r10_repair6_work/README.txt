Phase157 R5-R10 repair6

repair5 では Reference/Proof 境界・Web separator・QED は成立し、
focused test は 37 passed / 1 failed まで進んだ。

残り1件:
- pi_6^3 の proof body 先頭に旧 intro
  `使用する結果を先にまとめる.`
  が残っていた。

repair6:
- generic contribution renderer の public output 直前で、
  先頭に残った legacy intro だけを除去する。
- proof graph、Reference selection、statement relevance、
  argument ordering は変更しない。

変更対象:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r5_r10_reference_proof_boundary_qed.py

全体 pytest は Phase157 closure の最後だけ実行する。
