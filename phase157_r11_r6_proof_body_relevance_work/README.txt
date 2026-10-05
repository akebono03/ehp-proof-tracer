Phase157 R11-R6 — Proof body relevance implementation

監査結果
========

R11-R5 で、不要な

    E: pi_4^2 -> pi_5^3 isomorphism

は generic proof body の通常選択ではなく、

    _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism()

によって後から復元されることが確定した。

一方、

    pi_6^5 = Z/2{eta_5}

は base multi-argument renderer の段階から存在する正当な local body statement であり、
最終的な位数計算の consumer より前にある。

今回の変更
==========

Production:
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`
  から pi6_3 専用 suspension-isomorphism restore call を除去。
- helper function 自体は今回削除しない。
  不要な広範囲 refactor を避けるため。

Tests:
- 不要 map が proof body に出ない。
- pi_6^5 group statement は残る。
- pi_6^5 group statement は「短完全列と両端の群の位数」consumer より前にある。

Phase boundary
==============

R11-R6 では proof body relevance の今回確認済み defect だけを修正する。
112-group audit や documentation、full pytest は Phase157 closure まで行わない。
