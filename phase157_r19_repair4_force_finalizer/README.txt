Phase157-R19 repair4

This repair replaces only:
  _phase157_r19_finalize_pi6_3_public_narrative()

Reason:
Repair3 returned early because Proposition 2.2 is not a native public
reference entry in the current proof graph. The current graph records
the relevant Hopf-value step as Equation 5.7.

Repair4:
- rebuilds reference candidates directly from the presentation;
- keeps Proposition 5.6, (5.3), Proposition 5.3, Proposition 5.1;
- derives the public Proposition 2.2 reference from the Equation 5.7
  provenance entry already used by R19;
- no longer requires all five references to be present in the source
  reference tuple before finalization;
- canonicalizes the pi_6^3 public proof body after the final usage filter.

Files changed:
- toda_group_proof_narrative_contribution_renderer.py

No import changes.
No test-file changes in repair4.
No documentation changes.
No repository-wide pytest.
