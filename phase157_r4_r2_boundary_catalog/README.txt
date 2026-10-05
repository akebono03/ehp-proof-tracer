Phase157-R4-R2 representative fixed-statement catalog

変更対象:
- toda_literature_statement_boundary.py
- tests/test_phase157_r4_r2_boundary_catalog.py

追加する fixed statement boundary:
- Proposition 5.11 finite-dimensional part
- Proposition 5.15 finite-dimensional part
- Lemma 5.13 sigma''' statement
- Lemma 5.14 sigma'', sigma', sigma_8 branches
- Equation 5.13 three Delta relations
- Toda (5.5) nu-family relations

重要:
- Proposition 5.11 / 5.15 の map property, exactness,
  transport, decomposition semantics は PROOF_INTERNAL のまま。
- Reference selection への接続は R4-R3 で行う。
- 全体 pytest は Phase157 closure まで行わない。
