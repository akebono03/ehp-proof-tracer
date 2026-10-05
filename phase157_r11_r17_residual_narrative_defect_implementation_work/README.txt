Phase157 R11-R17 — Residual Narrative defect implementation

R11-R15:
- 112 groups scanned
- 0 exceptions
- 15 findings / 6 affected groups
- visible dependency order findings = 0

R11-R16 classification:
- zero-map visibility gap: 1 confirmed
- redundant left EHP term: 1 confirmed presentation candidate
- standalone connector: 7
- repeated numeric equality: 1 confirmed
- public Reference without body marker:
  - needed_but_marker_missing: 2
  - needed_for_root_but_marker_missing: 1
  - ancestry_only_candidate: 2

Scope
=====

Production:
- toda_group_proof_narrative_contribution_renderer.py only

Tests:
- new tests/test_phase157_r11_r17_residual_narrative_defects.py

No change:
- toda_group_proof_narrative_references.py
- dependency ordering implemented in R11-R14
- documents

Implementation
==============

1. Hidden zero-map premise visibility
2. Redundant left EHP term trimming after established E injectivity
3. Standalone connector normalization
4. Repeated numeric equality normalization
5. Final Reference attribution followed by existing body-usage filtering

No hard-code:
- pi_6^3 等の群名
- Lemma 5.4 / 5.13 / 5.14
- Proposition 名
- specific numeric equality 4=4

Testing
=======

Focused tests only.
Full repository pytest remains deferred until Phase157 closure.
