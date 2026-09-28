Phase 144-6-R5-40
Narrative contribution placement/order audit

Production changes: none.

Added:
- audit_phase144_6_r5_40.py
- tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py

Audit the 190 Phase-39 explanatory contributions for owner-Argument placement
and dependency-order signals. Provider identity remains local to one occurrence
construction, preserving the Phase-39 R3 repair.

Diagnostic placement classes:
- at_provider_anchor
- before_dependent_contribution
- before_argument_conclusion

No production placement API or Narrative output change is made.
The dedicated pi_6^3 renderer remains unchanged.
Run only the focused Phase-39 and Phase-40 tests.
