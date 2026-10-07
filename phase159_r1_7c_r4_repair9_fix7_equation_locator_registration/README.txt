Phase 159 R1-7c R4 repair9 fix7

目的
====
Equation 系文献 locator の登録方式を統一する。

従来:
- (5.3)
- (5.5)
- Equation 5.7
- Equation 5.8
- Equation 5.13

修正後:
- (5.3)
- (5.5)
- (5.7)
- (5.8)
- (5.13)

方針
====
表示 renderer で `Equation 5.7 -> (5.7)` と後処理しない。

source provenance / boundary catalog / rule-name inference の段階で
canonical locator を `(N.M)` として登録・推定する。

変更対象
========
Production:
1. toda_literature_statement_boundary.py
2. toda_group_proof_narrative_references.py

Tests:
1. tests/test_phase157_r5_r3_boundary_catalog_expansion.py
2. tests/test_phase157_r4_r2_boundary_catalog.py
3. tests/test_phase156_r5_repair4_bridge_reference_inference.py

Production 詳細
===============

toda_literature_statement_boundary.py
-------------------------------------
- Equation 5.7 catalog key -> (5.7)
- Equation 5.7 component locator -> (5.7)
- rule name `Toda Equation 5.7 nu-prime eta_6 Hopf value`
  -> internal locator `(5.7)`
  これにより既存 PROOF_INTERNAL classification を維持する。
- Equation 5.8 catalog / fixed mapping -> (5.8)
- Equation 5.13 catalog / fixed mapping -> (5.13)

toda_group_proof_narrative_references.py
----------------------------------------
`_infer_toda_group_proof_literature_reference_from_rule_name()` で:

- Proposition N.M -> Proposition N.M
- Lemma N.M -> Lemma N.M
- Theorem N.M -> Theorem N.M
- Equation N.M -> (N.M)

とする。

つまり Equation だけ parenthesized locator にする一般規則。

変更しないもの
==============
- inference rule name 自体
- Proposition / Lemma locator
- Equation (5.7) -> Proposition 2.2 proof dependency
- R3 eta generator canonicalization
- public renderer の title formatting

完了条件
========
- pi_6^3 Reference に `(5.7).` が出る
- `Equation 5.7` が Reference header に出ない
- (5.7) boundary classification は従来どおり PROOF_INTERNAL
- (5.8), (5.13) fixed classification が壊れない
- focused tests PASS

全体 pytest
===========
実行しない。
Phase 159 の最後まで保留。
